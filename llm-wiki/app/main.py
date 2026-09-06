from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import markdown as md
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile as StarletteUploadFile

load_dotenv()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# access.py liest MPB_SECRET beim Modulimport (siehe access._load_secret) -
# load_dotenv() muss deshalb VOR diesem Import laufen, sonst gilt .env nie.
from . import (  # noqa: E402
    access, basic_auth, evaluation, evaluation_cache, extractors, kompass, llm,
    llm_metadata, proposals, stats, urlfetch, wiki,
)
from .access import PageMeta  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="MediaparkBrain LLM-Wiki")
# Passwortschutz vor allem anderen, sobald MPB_BASIC_AUTH_USER/-PASS gesetzt sind.
app.add_middleware(basic_auth.BasicAuthMiddleware)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def render_markdown(text: str) -> str:
    return md.markdown(text, extensions=["fenced_code", "tables"])


def format_ts(value: str) -> str:
    """ISO-Zeitstempel lesbar: TT.MM.JJJJ HH:MM. Unlesbares wird durchgereicht."""
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value).strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return value


templates.env.filters["ts"] = format_ts
templates.env.filters["user_name"] = access.user_name
templates.env.filters["risk_class"] = evaluation.risk_class


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# Seed / Demo-Seiten
# ---------------------------------------------------------------------------

SEED_PAGES = [
    (
        "start",
        "Start",
        "Willkommen im **LLM-Wiki** von MediaparkBrain.\n\n"
        "Dies ist die minimale Wissensbasis fuer das agentische "
        "KI-Wissensmanagement aus PLAN.md. Lege eigene Seiten an, "
        "verlinke sie und stelle unten Fragen - das Wiki sucht die "
        "passenden Stellen und lässt (bei konfiguriertem API-Key) "
        "ein LLM eine begruendete Antwort daraus formulieren.",
    ),
    (
        "vier-experten-agenten",
        "Vier Experten-Agenten",
        "Das System nutzt vier Stakeholder-Agenten: Betriebsrat, "
        "CFO/Controlling, IT/Architektur/Cybersecurity und CEO/Strategie. "
        "Jeder Agent bewertet einen Projektvorschlag aus seiner Perspektive "
        "mit Value Score, Risk Score und Strategy Score.\n\n"
        "Der Orchestrator-Agent koordiniert den Prozess, ist selbst aber "
        "kein fachlicher Gutachter.",
    ),
    (
        "wissensmanagement",
        "Wissensmanagement",
        "Die Wissensbasis basiert auf einem RAG-System und enthaelt sowohl "
        "internes Wissen (Richtlinien, Architektur, Budgets) als auch extern "
        "recherchierte Informationen (Hersteller, Zertifizierungen, "
        "Regulatorik).\n\n"
        "Dokumente koennen widerspruechlich oder veraltet sein - Agenten "
        "muessen Aktualitaet und Herkunft beruecksichtigen.",
    ),
]

# Demo-Seiten fuer die Rechte-Demo: Finance sieht der Einreicher nicht,
# die BR-Ablage liest selbst die Leitung nicht. Keine echten Personennamen.
DEMO_PAGES = [
    (
        "budgetfreigabe-q4",
        "Budgetfreigabe Q4",
        "Budgetantrag fuer den KI-Wissensassistenten, Freigabe Q4 (fiktive Zahlen).\n\n"
        "| Position | Betrag |\n|---|---|\n"
        "| Lizenzen Sprachmodell (12 Monate) | 48.000 EUR |\n"
        "| Externe Entwicklung Demonstrator | 95.000 EUR |\n"
        "| Interner Aufwand (0,8 FTE) | 62.000 EUR |\n"
        "| Schulung und Rollout | 15.000 EUR |\n"
        "| **Gesamt** | **220.000 EUR** |\n\n"
        "Kostenstelle 4711, Projektnummer P-2026-031. Freigabe durch Controlling "
        "unter Vorbehalt eines Zwischenberichts nach Phase 1. Erwartete Einsparung "
        "durch kuerzere Recherchezeiten: rund 140.000 EUR pro Jahr ab 2027.",
        PageMeta(erstellt_von="cfo", vertraulichkeit="intern", domaene="finance"),
    ),
    (
        "betriebsratsprotokoll-juli",
        "Betriebsratsprotokoll Juli",
        "Protokoll der Betriebsratssitzung im Juli (fiktiv).\n\n"
        "**TOP 3: KI-Wissensassistent und Leistungskontrolle**\n\n"
        "Der Betriebsrat sieht in der Protokollierung von Suchanfragen die Gefahr "
        "einer Verhaltens- und Leistungskontrolle nach BetrVG. Gefordert wird: "
        "keine personenbezogene Auswertung von Anfragen, Loeschfrist von 30 Tagen "
        "fuer Zugriffsprotokolle und eine Betriebsvereinbarung vor dem Rollout.\n\n"
        "Beschluss: Die Zustimmung zur Einfuehrung wird bis zur Vorlage eines "
        "Datenschutzkonzepts zurueckgestellt. Naechste Sitzung im August.",
        PageMeta(erstellt_von="betriebsrat", vertraulichkeit="intern", domaene="br"),
    ),
]


def seed_if_empty() -> None:
    if wiki.list_pages():
        return
    for slug, title, content in SEED_PAGES:
        wiki.save_page(
            slug,
            title,
            content,
            PageMeta(
                erstellt_von="system",
                erstellt_am=now_iso(),
                vertraulichkeit="oeffentlich",
                domaene="allgemein",
            ),
        )


def ensure_demo_pages() -> None:
    """Ergaenzt fehlende Demo-Seiten, auch wenn pages/ schon Seiten enthaelt."""
    for slug, title, content, meta in DEMO_PAGES:
        if wiki.get_page(slug) is None:
            meta.erstellt_am = meta.erstellt_am or now_iso()
            wiki.save_page(slug, title, content, meta)


# Stufe 2 (US-19): flache Altdateien zuerst in Domaenenordner einsortieren,
# dann erst pruefen, ob Seed/Demo-Seiten fehlen.
wiki.migrate_flat_pages()
seed_if_empty()
ensure_demo_pages()


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------


def ctx(request: Request, **extra) -> dict:
    """Gemeinsamer Template-Kontext: gefilterte Seitenliste + Nutzerauswahl."""
    user = access.current_user(request)
    base = {
        "pages": wiki.list_pages(user),
        "user": user,
        "user_name": access.user_name(user),
        "users": access.list_users(),
        # Formulare zeigen nur Domaenen, in die der Nutzer schreiben darf
        # (Write ⊆ Read); der POST prueft trotzdem noch einmal (require_writable).
        "domains": access.readable_domains(user),
        "is_admin": access.is_admin(user),
        "confidentiality_levels": access.list_confidentiality_levels(),
        "default_confidentiality": access.default_confidentiality_for_user(user),
        "current_path": request.url.path,
    }
    base.update(extra)
    return base



# ---------------------------------------------------------------------------
# Kompass-Shell (templates/kompass/). Eigener Kontext neben `ctx`, damit die
# alten Seiten unveraendert weiterlaufen: sie brauchen `pages`/`users`, die
# Kompass-Shell braucht `current_user`/`visible_domains`/`active`/`collapsed`.
# Rechte kommen in beiden Faellen aus denselben Funktionen in access.py.
# ---------------------------------------------------------------------------


def kctx(request: Request, active: str, **extra) -> dict:
    user = access.current_user(request)
    base = {
        "current_user": kompass.current_user_vm(user),
        "visible_domains": access.readable_domains(user),
        "active": active,
        # Sidebar-Zustand kommt aus dem Cookie, das kpToggleSidebar() setzt.
        "collapsed": request.cookies.get("kp_collapsed") == "1",
        "q": request.query_params.get("q", ""),
        # Demo-Modus: kein Cookie, aber MPB_DEFAULT_USER greift -> kleiner Hinweis unten links.
        "default_user_hint": access.is_default_user(request),
    }
    base.update(extra)
    return base


def _form_value(form, key: str) -> str:
    """Erster nicht-leerer Wert eines Feldes.

    Das Drop-In und die Vollstaendigkeits-Sektion schicken teils denselben
    Feldnamen zweimal (einmal befuellt, einmal leer). Der befuellte gewinnt.
    """
    for value in form.getlist(key):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _form_uploads(form, key: str) -> list[StarletteUploadFile]:
    """Alle Datei-Teile eines Feldes mit Dateinamen.

    request.form() liefert starlette.datastructures.UploadFile, NICHT
    fastapi.UploadFile - ein isinstance gegen die FastAPI-Klasse ist immer
    False und laesst die Datei unbemerkt unter den Tisch fallen.
    """
    return [
        f for f in form.getlist(key)
        if isinstance(f, StarletteUploadFile) and f.filename
    ]


def _upload_page_content(text: str, filename: str, title: str, slug: str, original_name: str) -> str:
    """Seiteninhalt einer hochgeladenen Datei: oben die Zeile "Original: <name>"
    (Link auf /knowledge/<slug>/original), bei Bildern zusaetzlich das Bild
    selbst, dann der extrahierte Text (bei Bildern die Modellbeschreibung oder
    der Fallback mit den Bildmassen)."""
    parts = [f"Original: [{original_name}](/knowledge/{slug}/original)"]
    if extractors.is_image(filename):
        parts.append(f"![{title}](/knowledge/{slug}/original)")
    if text.strip():
        parts.append(text.strip())
    return "\n\n".join(parts)


def _free_slug(title: str) -> str:
    """Slug aus dem Titel; ist er belegt, wird -2, -3, ... angehaengt statt
    die vorhandene Seite zu ueberschreiben oder zu verschieben."""
    base = wiki.slugify(title)
    slug, n = base, 2
    while wiki.slug_exists(slug):
        slug = f"{base}-{n}"
        n += 1
    return slug


def _title_from_text(text: str) -> str:
    """Notnagel-Titel aus der ersten brauchbaren Zeile eines eingefuegten Textes."""
    for zeile in (text or "").splitlines():
        zeile = zeile.strip().lstrip("#").strip()
        if len(zeile) > 3:
            return zeile[:80]
    return "Notiz"


def _title_from_filename(filename: str) -> str:
    stem = Path(filename).stem.replace("_", " ").replace("-", " ").strip()
    return " ".join(stem.split()) or "Hochgeladenes Dokument"


def _felder_from_form(form) -> dict[str, str]:
    return {
        key: _form_value(form, key)
        for key, _ in kompass.PFLICHTFELDER
        if _form_value(form, key)
    }


def require_page(slug: str, user: str) -> wiki.Page:
    """Seite aus Nutzersicht; fehlend und verboten sind nicht unterscheidbar (404)."""
    page = wiki.get_page_for(slug, user)
    if page is None:
        raise HTTPException(status_code=404, detail="Seite nicht gefunden")
    return page


GUEST_403 = "Bitte erst Nutzer wählen"
WRITE_403 = "Du darfst in dieser Domäne nichts anlegen"


def require_author(request: Request) -> str:
    """Gast darf nichts anlegen, bearbeiten oder loeschen (403)."""
    user = access.current_user(request)
    if user == access.GUEST:
        raise HTTPException(status_code=403, detail=GUEST_403)
    return user


def require_writable(user: str, meta: PageMeta) -> None:
    """Schreiben nur, wo man lesen darf (Write ⊆ Read): Zieldomaene muss lesbar
    sein und decide muss die Seite mit diesen Metadaten erlauben, sonst 403."""
    if not access.can_write(user, meta):
        raise HTTPException(status_code=403, detail=WRITE_403)


def require_admin(request: Request) -> str:
    """Admin-Dashboard existiert fuer Nicht-Admins nicht (404, US-16)."""
    user = access.current_user(request)
    if not access.is_admin(user):
        raise HTTPException(status_code=404, detail="Seite nicht gefunden")
    return user


def parse_recipients(raw: str) -> list[str]:
    return [r.strip() for r in raw.split(",") if r.strip()]


def _simple_page(title: str, text: str, status: int) -> HTMLResponse:
    html = (
        "<!doctype html><html lang='de'><head><meta charset='utf-8'>"
        f"<title>{title}</title>"
        "<link rel='stylesheet' href='/static/style.css?v=3'></head>"
        f"<body><main class='content'><h1>{title}</h1><p>{text}</p>"
        "<p><a href='/'>Zurück zur Startseite</a></p></main></body></html>"
    )
    return HTMLResponse(html, status_code=status)


@app.exception_handler(403)
def forbidden_handler(request: Request, exc: HTTPException):
    detail = getattr(exc, "detail", None) or GUEST_403
    if detail == GUEST_403:
        return _simple_page(
            GUEST_403,
            "Als Gast kannst du Seiten nur lesen. Wähle in der Seitenleiste, "
            "als wer du arbeitest, und versuche es erneut.",
            403,
        )
    # Dieselbe 403-Seite, anderer Text (z. B. Schreiben in fremder Domaene).
    return _simple_page("Nicht erlaubt", detail, 403)


@app.exception_handler(404)
def not_found_handler(request: Request, exc: HTTPException):
    # Bewusst gleiche Antwort fuer "gibt es nicht" und "darfst du nicht sehen" (US-8).
    return _simple_page(
        "Seite nicht gefunden",
        "Unter dieser Adresse gibt es keine Seite, die du sehen kannst.",
        404,
    )


# ---------------------------------------------------------------------------
# Login-Simulation (signierter Cookie), bis ein echtes Login existiert.
# Der Cookie traegt `<uid>.<hmac>`; ein roher oder manipulierter Wert ist Gast.
# ---------------------------------------------------------------------------


def _safe_next(next_url: str | None) -> str:
    # Nur lokale Pfade erlauben (kein Open Redirect)
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return "/"


@app.post("/login")
def login(user: str = Form(...), next: str = Form("/")):
    uid = access.get_user(user)["id"]
    resp = RedirectResponse(_safe_next(next), status_code=303)
    # secure kommt aus MPB_COOKIE_SECURE: hinter TLS an, lokal ueber http aus.
    resp.set_cookie(
        access.COOKIE_NAME, access.sign_user(uid),
        httponly=True, samesite="lax", secure=access.cookie_secure(),
    )
    return resp


@app.post("/logout")
def logout(next: str = Form("/")):
    resp = RedirectResponse(_safe_next(next), status_code=303)
    resp.delete_cookie(access.COOKIE_NAME)
    return resp


# ---------------------------------------------------------------------------
# Seiten
# ---------------------------------------------------------------------------


@app.get("/")
def index(request: Request, sort: str = ""):
    """Startseite ist jetzt das Kompass-Dashboard.

    Die alte Startseite (Wiki-Seite "start" in der alten Shell) bleibt ueber
    /wiki/start erreichbar - dieselbe Route wie jede andere Wiki-Seite.
    """
    user = access.current_user(request)
    rows = kompass.dashboard_rows(user, sort or "submitted")
    return templates.TemplateResponse(
        request,
        "kompass/dashboard.html",
        kctx(
            request,
            "dashboard",
            proposals=rows,
            kpi=kompass.kpi(user, rows),
            knowledge_count=len(wiki.list_pages(user)),
            show_kpis=True,
        ),
    )


@app.get("/wiki/{slug}")
def view_page(request: Request, slug: str, gespeichert: int = 0, uploaded: int = 0):
    user = access.current_user(request)
    page = require_page(slug, user)
    html = render_markdown(page.content)
    return templates.TemplateResponse(
        request,
        "index.html",
        ctx(
            request,
            content_html=html,
            page=page,
            just_saved=bool(gespeichert or uploaded),
        ),
    )



@app.get("/wiki/{slug}/edit")
def edit_page_form(request: Request, slug: str):
    user = access.current_user(request)
    page = require_page(slug, user)
    require_author(request)
    return templates.TemplateResponse(
        request, "edit.html", ctx(request, page=page, slug=slug)
    )


@app.post("/wiki/{slug}/edit")
def edit_page_save(
    request: Request,
    slug: str,
    title: str = Form(...),
    content: str = Form(...),
    vertraulichkeit: str = Form("intern"),
    domaene: str = Form("allgemein"),
    empfaenger: str = Form(""),
):
    user = access.current_user(request)
    page = require_page(slug, user)
    require_author(request)
    meta = page.meta
    # US-3: Ersteller und Anlagedatum bleiben erhalten, nicht editierbar.
    meta.geaendert_von = user
    meta.geaendert_am = now_iso()
    meta.vertraulichkeit = vertraulichkeit
    meta.domaene = domaene
    meta.empfaenger = parse_recipients(empfaenger)
    # Write ⊆ Read: gilt fuer die NEUE Domaene - Verschieben in eine fremde
    # Domaene ist verboten (403), die Datei bleibt, wo sie ist.
    require_writable(user, meta)
    new_slug = wiki.slugify(title)
    if new_slug != slug:
        if wiki.slug_exists(new_slug):
            return templates.TemplateResponse(
                request, "edit.html",
                ctx(request, page=page, slug=slug,
                    error=f'Der Titel "{title}" ist bereits vergeben (Adresse /wiki/{new_slug}).'),
                status_code=409,
            )
        wiki.delete_page(slug)
    # US-17: save_page legt die Datei im Ordner ihrer Domaene ab und verschiebt bei Wechsel.
    wiki.save_page(new_slug, title, content, meta)
    return RedirectResponse(f"/wiki/{new_slug}?gespeichert=1", status_code=303)


@app.post("/wiki/{slug}/delete")
def delete_page_route(request: Request, slug: str):
    user = access.current_user(request)
    require_page(slug, user)
    require_author(request)
    wiki.delete_page(slug)
    return RedirectResponse("/", status_code=303)


@app.get("/new")
def new_page_form(request: Request):
    require_author(request)
    return templates.TemplateResponse(
        request, "edit.html", ctx(request, page=None, slug=None)
    )


@app.post("/new")
def new_page_save(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    vertraulichkeit: str = Form("intern"),
    domaene: str = Form("allgemein"),
    empfaenger: str = Form(""),
):
    user = require_author(request)
    slug = wiki.slugify(title)
    meta = PageMeta(
        erstellt_von=user,
        erstellt_am=now_iso(),
        vertraulichkeit=vertraulichkeit,
        domaene=domaene,
        empfaenger=parse_recipients(empfaenger),
    )
    require_writable(user, meta)  # Write ⊆ Read (403 in fremder Domaene)
    # US-17: Slugs sind global eindeutig - egal in welchem Ordner der Slug liegt.
    # (Fehlt/verboten wird hier bewusst nicht unterschieden: Anlegen wird abgelehnt.)
    if wiki.slug_exists(slug):
        draft = wiki.Page(slug=slug, title=title, content=content, meta=meta)
        return templates.TemplateResponse(
            request, "edit.html",
            ctx(request, page=None, slug=None, draft=draft,
                error=f'Der Titel "{title}" ist bereits vergeben (Adresse /wiki/{slug}). Bitte anderen Titel wählen.'),
            status_code=409,
        )
    wiki.save_page(slug, title, content, meta)
    return RedirectResponse(f"/wiki/{slug}?gespeichert=1", status_code=303)


# ---------------------------------------------------------------------------
# Datei-Upload & Wissensdatenbank-Überführung (Arbeitspaket 2)
# ---------------------------------------------------------------------------


@app.post("/api/extract-document")
async def extract_document_api(
    request: Request,
    file: UploadFile = File(...),
):
    user = require_author(request)
    if not file.filename:
        raise HTTPException(status_code=400, detail="Keine Datei ausgewählt.")

    content_bytes = await file.read()
    if not content_bytes:
        raise HTTPException(status_code=400, detail="Die Datei ist leer.")

    # 1. Originaldatei im Upload-Ordner sichern
    saved_path = wiki.save_uploaded_file(file.filename, content_bytes)

    # 2. Text extrahieren
    try:
        extracted_text = extractors.extract_text_from_file(saved_path, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Extraktion fehlgeschlagen: {e}")

    # 3. LLM-Header generieren
    header_block, meta, extracted_title = llm_metadata.generate_header(
        extracted_text,
        file.filename,
        user,
    )

    return {
        "title": extracted_title,
        "content": extracted_text.strip(),
        "vertraulichkeit": meta.vertraulichkeit,
        "domaene": meta.domaene or "allgemein",
        "empfaenger": ", ".join(meta.empfaenger) if meta.empfaenger else "",
    }


KNOWLEDGE_FILL_FIELDS = [
    {"key": key, "label": label} for key, label in kompass.KNOWLEDGE_FIELDS
]


def _kompass_upload(
    request: Request,
    user: str,
    saved: bool = False,
    error: str | None = None,
    saved_pages: list[dict] | None = None,
    status: int = 200,
):
    """Kompass-Upload-Maske. `error` wird als roter Hinweis ueber dem Formular
    gerendert (Formular bleibt), `saved_pages` als Links auf die neuen Seiten."""
    default_domain = (access.readable_domains(user) or [wiki.DEFAULT_DOMAIN])[0]
    return templates.TemplateResponse(
        request,
        "kompass/upload.html",
        kctx(
            request,
            "upload",
            target="knowledge",
            fill_fields=KNOWLEDGE_FILL_FIELDS,
            fill_endpoint="/api/prefill?target=knowledge",
            readers=kompass._readers_text(default_domain),
            saved=saved,
            saved_pages=saved_pages or [],
            error=error,
        ),
        status_code=status,
    )


@app.get("/upload")
def upload_form(request: Request, target: str = "", classic: int = 0):
    """Kompass-Upload. Die alte Maske bleibt unter /upload?classic=1 erreichbar."""
    user = access.current_user(request)
    if classic:
        conf_levels = access.list_confidentiality_levels()
        default_conf = access.default_confidentiality_for_user(user)
        domains = access.readable_domains(user)
        return templates.TemplateResponse(
            request,
            "upload.html",
            ctx(
                request,
                confidentiality_levels=conf_levels,
                default_confidentiality=default_conf,
                domains=domains,
                error=None,
            ),
        )
    return _kompass_upload(request, user)


@app.post("/upload")
async def upload_submit(
    request: Request,
    file: UploadFile | None = File(None),
    files: list[UploadFile] = File(default=[]),
    target: str = Form(""),
    vertraulichkeit: str = Form("intern"),
    domaene: str = Form("projekt"),
    titel: str = Form(""),
    dokumenttyp: str = Form(""),
    datum: str = Form(""),
    verfasser: str = Form(""),
    empfaenger: str = Form(""),
    text: str = Form(""),
):
    user = require_author(request)
    if target:
        # Kompass-Weg: mehrere Dateien oder ein eingefuegter Text/Link.
        return await _upload_kompass(
            request, user, files, titel, domaene, vertraulichkeit,
            dokumenttyp, datum, verfasser, parse_recipients(empfaenger), text,
        )
    if file is None or not file.filename:
        return templates.TemplateResponse(
            request,
            "upload.html",
            ctx(
                request,
                error="Bitte wähle eine Datei aus.",
            ),
        )

    content_bytes = await file.read()
    if not content_bytes:
        return templates.TemplateResponse(
            request,
            "upload.html",
            ctx(
                request,
                error="Die hochgeladene Datei ist leer.",
            ),
        )

    # 0. Vorab-Pruefung (Write <= Read), damit die Originaldatei gar nicht erst in einem
    #    fremden Domaenenordner landet. Die endgueltige Pruefung folgt auf das fertige meta.
    #    Mit Ersteller und Empfaengern, sonst scheitert `vertraulich` (Regel 4) am
    #    eigenen Nutzer.
    empfaenger_liste = parse_recipients(empfaenger)
    require_writable(user, PageMeta(
        erstellt_von=user, domaene=domaene, vertraulichkeit=vertraulichkeit,
        empfaenger=empfaenger_liste,
    ))

    # 1. Originaldatei im Uploads-Ordner sichern (nach Domaene)
    saved_path = wiki.save_uploaded_file(file.filename, content_bytes, domaene=domaene)

    # 2. Text extrahieren
    try:
        extracted_text = extractors.extract_text_from_file(saved_path, file.filename)
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "upload.html",
            ctx(
                request,
                error=f"Fehler bei der Textextraktion: {e}",
            ),
        )

    # 3. LLM-Header generieren
    header_block, meta, extracted_title = llm_metadata.generate_header(
        extracted_text,
        file.filename,
        user,
        custom_domain=domaene,
        custom_confidentiality=vertraulichkeit,
    )
    # Original bleibt: der abgelegte (bereinigte) Dateiname, den /knowledge/<slug>/original findet.
    meta.original_datei = saved_path.name
    for e in empfaenger_liste:
        if e not in meta.empfaenger:
            meta.empfaenger.append(e)

    # 4. Pruefen ob der Nutzer in dieser Domaene mit dieser Einstufung schreiben darf (Write ⊆ Read)
    require_writable(user, meta)

    # 5. Slug & Inhalt zusammensetzen
    slug = _free_slug(extracted_title)  # Kollision: -2, -3, ... statt Ueberschreiben
    full_content = _upload_page_content(
        extracted_text, file.filename, extracted_title, slug, saved_path.name
    ) + "\n"

    # Speichern unter pages/
    wiki.save_page(slug, extracted_title, full_content, meta=meta)

    # 6. One-Click Redirect mit Erfolgs-Feedback (Sound & Badge)
    return RedirectResponse(f"/wiki/{slug}?uploaded=1", status_code=303)


# ---------------------------------------------------------------------------
# Projektvorschläge
# ---------------------------------------------------------------------------



@app.get("/proposals")
def proposal_list(request: Request, sort: str = ""):
    user = access.current_user(request)
    # US-12: Liste gefiltert ueber decide, wie die Seitenliste.
    rows = kompass.dashboard_rows(user, sort or "submitted")
    return templates.TemplateResponse(
        request,
        "kompass/dashboard.html",
        kctx(
            request,
            "proposals",
            proposals=rows,
            kpi=kompass.kpi(user, rows),
            knowledge_count=len(wiki.list_pages(user)),
            show_kpis=False,
        ),
    )


def _proposal_form(request: Request, status: int = 200, **fields):
    defaults = {
        "error": None,
        "project_name": "",
        "description": "",
        "vertraulichkeit": "intern",
        "domaene": proposals.DEFAULT_DOMAIN,
        "empfaenger": "",
    }
    defaults.update(fields)
    return templates.TemplateResponse(
        request, "proposal_new.html", ctx(request, **defaults), status_code=status
    )


PROPOSAL_FILL_FIELDS = [
    {"key": key, "label": label}
    for key, label in (list(kompass.BASE_FIELDS) + list(kompass.PFLICHTFELDER))
]


@app.get("/proposals/new")
def proposal_new_form(request: Request):
    user = require_author(request)  # Gast darf nicht einreichen (403, US-12)
    return templates.TemplateResponse(
        request,
        "kompass/proposal_detail.html",
        kctx(
            request,
            "proposals",
            mode="new",
            p=kompass.proposal_vm(None, user, "new"),
            can_edit=True,
            domains=access.readable_domains(user),
            default_domain=proposals.DEFAULT_DOMAIN,
            confidentiality_levels=access.list_confidentiality_levels(),
            default_confidentiality=access.default_confidentiality_for_user(user),
            fill_fields=PROPOSAL_FILL_FIELDS,
            fill_endpoint="/api/prefill?target=proposal",
        ),
    )


@app.post("/proposals/new")
async def proposal_new_save(
    request: Request,
    project_name: str = Form(...),
    description: str = Form(...),
    vertraulichkeit: str = Form("intern"),
    domaene: str = Form(proposals.DEFAULT_DOMAIN),
    empfaenger: str = Form(""),
    files: list[UploadFile] = File(default=[]),
):
    user = require_author(request)
    # US-11: Einreicher und Rolle (Anzeigename jetzt) kommen aus dem aktuellen Nutzer.
    meta = PageMeta(
        erstellt_von=user,
        erstellt_am=now_iso(),
        vertraulichkeit=vertraulichkeit,
        domaene=domaene,
        empfaenger=parse_recipients(empfaenger),
        quelle=proposals.SOURCE,
    )
    require_writable(user, meta)  # Write ⊆ Read (403 in fremder Domaene)
    if proposals.already_submitted(project_name):
        return _proposal_form(
            request, 409,
            error=(
                f'Ein Projektvorschlag mit dem Namen "{project_name}" wurde '
                "bereits eingereicht. Einreichung abgelehnt."
            ),
            project_name=project_name, description=description,
            vertraulichkeit=vertraulichkeit, domaene=domaene, empfaenger=empfaenger,
        )

    uploaded_files = []
    for f in files:
        if not f.filename:
            continue
        if not f.filename.lower().endswith(".md"):
            return templates.TemplateResponse(
                request,
                "proposal_new.html",
                ctx(
                    request,
                    error=(
                        f'Datei "{f.filename}" ist keine Markdown-Datei (.md). '
                        "Nur .md-Dateien sind als Projektdatei zulaessig."
                    ),
                    project_name=project_name,
                    description=description,
                ),
                status_code=415,
            )
        uploaded_files.append((f.filename, await f.read()))

    duplicate = proposals.find_duplicate_file(uploaded_files)
    if duplicate is not None:
        return _proposal_form(
            request, 409,
            error=(
                "Diese Projektdatei wurde bereits eingereicht - als Vorschlag "
                f'"{duplicate.project_name}" (Hash identisch). Einreichung abgelehnt.'
            ),
            project_name=project_name, description=description,
            vertraulichkeit=vertraulichkeit, domaene=domaene, empfaenger=empfaenger,
        )

    proposal = proposals.save_proposal(
        project_name, description, uploaded_files, meta, rolle=access.user_name(user)
    )
    return RedirectResponse(f"/proposals/{proposal.slug}", status_code=303)


def require_proposal(slug: str, user: str) -> proposals.Proposal:
    """Vorschlag aus Nutzersicht; fehlend und verboten sind nicht unterscheidbar (404)."""
    proposal = proposals.get_proposal_for(slug, user)
    if proposal is None:
        raise HTTPException(status_code=404, detail="Seite nicht gefunden")
    return proposal


# Hinweis: muss VOR "/proposals/{slug}" registriert werden, sonst faengt die
# Slug-Route "evaluate" faelschlich als Slug ab (Starlette matcht Routen in
# Registrierungsreihenfolge).
@app.get("/proposals/evaluate")
def proposal_evaluate(request: Request):
    """Bewertet die zuletzt eingereichten Projektvorschlaege in allen vier
    Experten-Dimensionen gemaess Bewertungslogik_Experten-Agent_MVP.md."""
    recent = proposals.list_proposals()[:3]  # bereits nach submitted_at absteigend sortiert
    results = []
    for p in recent:
        data = evaluation.evaluate_proposal(p)
        # Ergebnis merken, damit Dashboard und Antragsdetail Scores zeigen
        # koennen, ohne bei jeder Seitenansicht das LLM zu rufen.
        evaluation_cache.store(p.slug, data)
        results.append({"proposal": p, "data": data})
    return templates.TemplateResponse(
        request,
        "proposal_evaluation.html",
        ctx(request, results=results, roles=evaluation.ROLE_CRITERIA),
    )


@app.get("/proposals/{slug}")
def proposal_view(request: Request, slug: str):
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    return templates.TemplateResponse(
        request,
        "kompass/proposal_detail.html",
        kctx(
            request,
            "proposals",
            mode="view",
            p=kompass.proposal_vm(proposal, user),
            # Felder speichern darf nur, wer in dieser Domaene schreiben darf.
            can_edit=access.can_write(user, proposal.meta),
            fill_fields=PROPOSAL_FILL_FIELDS,
            fill_endpoint="/api/prefill?target=proposal",
        ),
    )


@app.post("/proposals/{slug}/delete")
def proposal_delete(request: Request, slug: str):
    user = access.current_user(request)
    require_proposal(slug, user)
    require_author(request)
    proposals.delete_proposal(slug)
    return RedirectResponse("/proposals", status_code=303)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


@app.get("/dashboard")
def dashboard(request: Request):
    user = access.current_user(request)
    dashboard_stats = stats.get_dashboard_stats(user)
    return templates.TemplateResponse(
        request, "dashboard.html", ctx(request, stats=dashboard_stats)
    )


@app.get("/dashboard/projektantraege")
def dashboard_proposals(request: Request):
    user = access.current_user(request)
    proposal_stats = stats.get_proposal_stats(user)
    return templates.TemplateResponse(
        request,
        "dashboard_proposals.html",
        ctx(request, proposal_stats=proposal_stats),
    )


# ---------------------------------------------------------------------------
# Frag das Wiki
# ---------------------------------------------------------------------------


@app.get("/ask")
def ask_form(request: Request):
    return templates.TemplateResponse(
        request,
        "ask.html",
        ctx(
            request,
            question="",
            antwort=None,
            snippets=[],
            llm_configured=llm.is_configured(),
        ),
    )


@app.post("/ask")
def ask_submit(request: Request, question: str = Form(...)):
    user = access.current_user(request)
    # US-7: Rechte-Filter VOR der Trefferauswahl, das LLM sieht nur Erlaubtes.
    snippets = wiki.search_snippets(question, user)
    # Paket 10: Fakten mit woertlichem Beleg, belegt nur gegen diese Snippets.
    antwort = llm.ask_llm(question, snippets)
    return templates.TemplateResponse(
        request,
        "ask.html",
        ctx(
            request,
            question=question,
            antwort=antwort,
            snippets=snippets,
            llm_configured=llm.is_configured(),
        ),
    )


# ---------------------------------------------------------------------------
# Admin-Dashboard (Stufe 2, US-13 bis US-16). Nur Gruppe admin, sonst 404.
# Jede Aenderung geht ueber access.save_permissions -> permissions.yaml + Changelog.
# ---------------------------------------------------------------------------

ADMIN_MESSAGES = {
    "ungueltige-id": "Ungültige Kennung: erlaubt sind 2–40 Zeichen aus a–z, 0–9 und Bindestrich.",
    "nutzer-existiert": "Diesen Nutzer gibt es bereits.",
    "nutzer-fehlt": "Diesen Nutzer gibt es nicht.",
    "gast-nicht-loeschbar": "Der Gast kann nicht entfernt werden.",
    "selbst-nicht-loeschbar": "Du kannst dich nicht selbst entfernen.",
    "admin-selbst": "Du kannst dir die Gruppe admin nicht selbst entziehen (sonst sperrst du dich aus).",
    "domaene-existiert": "Diese Domäne gibt es bereits.",
    "domaene-fehlt": "Diese Domäne gibt es nicht.",
    "domaene-nicht-leer": "Die Domäne hat noch Seiten in ihrem Ordner und kann nicht entfernt werden.",
    "gruppe-existiert": "Diese Gruppe gibt es bereits.",
    "gruppe-unbekannt": "Mindestens eine gewählte Gruppe existiert nicht.",
    "gespeichert": "Änderung gespeichert und protokolliert.",
    "unveraendert": "Keine Änderung – nichts gespeichert.",
}


def _admin_redirect(code: str) -> RedirectResponse:
    return RedirectResponse(f"/admin?meldung={quote(code)}", status_code=303)


def _valid_id(value: str) -> bool:
    return bool(access.ID_RE.match(value or ""))


def _fmt_list(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def _ordered_groups(selected: list[str], all_groups: list[str]) -> list[str]:
    """Gewaehlte Gruppen in der Reihenfolge der Gruppenliste (stabile Protokollzeilen)."""
    chosen = set(selected)
    return [g for g in all_groups if g in chosen]


def _copy_permissions() -> dict:
    data = access.load_permissions()
    return {
        "gruppen": list(data["gruppen"]),
        "nutzer": {uid: {"name": u.get("name", uid), "gruppen": list(u.get("gruppen") or [])}
                   for uid, u in data["nutzer"].items()},
        "domaenen": {dom: {"lesen": list((spec or {}).get("lesen") or [])}
                     for dom, spec in data["domaenen"].items()},
    }


@app.get("/admin")
def admin_dashboard(request: Request, meldung: str = ""):
    admin = require_admin(request)
    data = access.load_permissions()
    domain_folders = {
        dom: sum(1 for _ in (wiki.pages_dir() / dom).rglob("*.md"))
        if (wiki.pages_dir() / dom).is_dir() else 0
        for dom in data["domaenen"]
    }
    return templates.TemplateResponse(
        request,
        "admin.html",
        ctx(
            request,
            admin=admin,
            gruppen=list(data["gruppen"]),
            nutzer=access.list_users(),
            domaenen={dom: list((spec or {}).get("lesen") or []) for dom, spec in data["domaenen"].items()},
            domain_counts=domain_folders,
            changelog=access.read_changelog(20),
            meldung=ADMIN_MESSAGES.get(meldung, ""),
            meldung_ist_fehler=bool(meldung) and meldung not in ("gespeichert", "unveraendert"),
        ),
    )


@app.post("/admin/users/save")
def admin_user_save(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(""),
    gruppen: list[str] = Form(default=[]),
):
    admin = require_admin(request)
    data = _copy_permissions()
    if user_id not in data["nutzer"]:
        return _admin_redirect("nutzer-fehlt")
    if not set(gruppen) <= set(data["gruppen"]):
        return _admin_redirect("gruppe-unbekannt")
    new_groups = _ordered_groups(gruppen, data["gruppen"])
    if user_id == access.GUEST:
        new_groups = []  # Gast bleibt ohne Gruppen (Regel 2)
    if user_id == admin and access.ADMIN_GROUP not in new_groups:
        return _admin_redirect("admin-selbst")  # Aussperrung verhindern
    entry = data["nutzer"][user_id]
    old_name, old_groups = entry["name"], entry["gruppen"]
    new_name = (name or "").strip() or old_name
    notes = []
    if new_name != old_name:
        notes.append(f"Name {old_name} → {new_name}")
    if new_groups != old_groups:
        notes.append(f"Gruppen {_fmt_list(old_groups)} → {_fmt_list(new_groups)}")
    if not notes:
        return _admin_redirect("unveraendert")
    entry["name"], entry["gruppen"] = new_name, new_groups
    access.save_permissions(data, admin, f"Nutzer {user_id}: " + "; ".join(notes))
    return _admin_redirect("gespeichert")


@app.post("/admin/users/new")
def admin_user_new(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(""),
    gruppen: list[str] = Form(default=[]),
):
    admin = require_admin(request)
    user_id = (user_id or "").strip().lower()
    if not _valid_id(user_id):
        return _admin_redirect("ungueltige-id")
    data = _copy_permissions()
    if user_id in data["nutzer"]:
        return _admin_redirect("nutzer-existiert")
    if not set(gruppen) <= set(data["gruppen"]):
        return _admin_redirect("gruppe-unbekannt")
    new_groups = _ordered_groups(gruppen, data["gruppen"])
    new_name = (name or "").strip() or user_id
    data["nutzer"][user_id] = {"name": new_name, "gruppen": new_groups}
    access.save_permissions(
        data, admin, f"Nutzer {user_id} angelegt: Name {new_name}, Gruppen {_fmt_list(new_groups)}"
    )
    return _admin_redirect("gespeichert")


@app.post("/admin/users/delete")
def admin_user_delete(request: Request, user_id: str = Form(...)):
    admin = require_admin(request)
    if user_id == access.GUEST:
        return _admin_redirect("gast-nicht-loeschbar")
    if user_id == admin:
        return _admin_redirect("selbst-nicht-loeschbar")
    data = _copy_permissions()
    entry = data["nutzer"].pop(user_id, None)
    if entry is None:
        return _admin_redirect("nutzer-fehlt")
    access.save_permissions(
        data, admin,
        f"Nutzer {user_id} entfernt (Name {entry['name']}, Gruppen {_fmt_list(entry['gruppen'])})",
    )
    return _admin_redirect("gespeichert")


@app.post("/admin/domains/save")
def admin_domain_save(
    request: Request,
    domaene: str = Form(...),
    lesen: list[str] = Form(default=[]),
):
    admin = require_admin(request)
    data = _copy_permissions()
    if domaene not in data["domaenen"]:
        return _admin_redirect("domaene-fehlt")
    if not set(lesen) <= set(data["gruppen"]):
        return _admin_redirect("gruppe-unbekannt")
    new_readers = _ordered_groups(lesen, data["gruppen"])
    old_readers = data["domaenen"][domaene]["lesen"]
    if new_readers == old_readers:
        return _admin_redirect("unveraendert")
    data["domaenen"][domaene]["lesen"] = new_readers
    access.save_permissions(
        data, admin,
        f"Domäne {domaene}: Lesegruppen {_fmt_list(old_readers)} → {_fmt_list(new_readers)}",
    )
    return _admin_redirect("gespeichert")


@app.post("/admin/domains/new")
def admin_domain_new(
    request: Request,
    domaene: str = Form(...),
    lesen: list[str] = Form(default=[]),
):
    admin = require_admin(request)
    domaene = (domaene or "").strip().lower()
    if not _valid_id(domaene):
        return _admin_redirect("ungueltige-id")
    data = _copy_permissions()
    if domaene in data["domaenen"]:
        return _admin_redirect("domaene-existiert")
    if not set(lesen) <= set(data["gruppen"]):
        return _admin_redirect("gruppe-unbekannt")
    new_readers = _ordered_groups(lesen, data["gruppen"])
    data["domaenen"][domaene] = {"lesen": new_readers}
    access.save_permissions(
        data, admin, f"Domäne {domaene} angelegt: Lesegruppen {_fmt_list(new_readers)}"
    )
    # US-14: neue Domaene bekommt sofort ihren Ordner unter pages/
    (wiki.pages_dir() / domaene).mkdir(parents=True, exist_ok=True)
    return _admin_redirect("gespeichert")


@app.post("/admin/domains/delete")
def admin_domain_delete(request: Request, domaene: str = Form(...)):
    admin = require_admin(request)
    data = _copy_permissions()
    if domaene not in data["domaenen"]:
        return _admin_redirect("domaene-fehlt")
    folder = wiki.pages_dir() / domaene
    if folder.is_dir() and any(folder.rglob("*.md")):
        return _admin_redirect("domaene-nicht-leer")
    old_readers = data["domaenen"].pop(domaene)["lesen"]
    access.save_permissions(
        data, admin, f"Domäne {domaene} entfernt (Lesegruppen {_fmt_list(old_readers)})"
    )
    if folder.is_dir():
        shutil.rmtree(folder)  # nur leere Ordner (ggf. mit leerem vertraulich/)
    return _admin_redirect("gespeichert")


@app.post("/admin/groups/new")
def admin_group_new(request: Request, gruppe: str = Form(...)):
    admin = require_admin(request)
    gruppe = (gruppe or "").strip().lower()
    if not _valid_id(gruppe):
        return _admin_redirect("ungueltige-id")
    data = _copy_permissions()
    if gruppe in data["gruppen"]:
        return _admin_redirect("gruppe-existiert")
    data["gruppen"].append(gruppe)
    access.save_permissions(data, admin, f"Gruppe {gruppe} angelegt")
    return _admin_redirect("gespeichert")


# ---------------------------------------------------------------------------
# Kompass (Design-Handoff v8). Alle Routen hier rendern templates/kompass/*.
#
# Rechte: jede Route holt den Nutzer ueber access.current_user und liest
# ausschliesslich ueber wiki.list_pages(user), proposals.list_proposals(user),
# wiki.search_snippets(q, user) bzw. require_page/require_proposal/
# require_author/require_writable/require_admin. Keine Sonderlogik.
# ---------------------------------------------------------------------------


async def _upload_kompass(
    request: Request,
    user: str,
    files: list[UploadFile],
    titel: str,
    domaene: str,
    vertraulichkeit: str,
    dokumenttyp: str,
    datum: str,
    verfasser: str,
    empfaenger: list[str] | None = None,
    text: str = "",
):
    """Wissens-Upload aus der Kompass-Maske: je Datei eine Wiki-Seite.

    Jeder Fehler (keine Datei, leere Datei, Extraktion, Schreibrecht) landet als
    lesbare Meldung in der Maske - nie als nackte 403/500-Seite. Nur der Gast
    bekommt vorher in `require_author` die 403-Seite (mit Standardnutzer kommt
    das nicht mehr vor).
    """
    real_files = [f for f in files if f and f.filename]
    # Eingefuegter Text oder eine abgelegte Adresse sind gleichwertig zur Datei:
    # der Prefill liest sie bereits aus, nur das Speichern verlangte bisher
    # zwingend eine Datei und antwortete "Bitte zuerst eine Datei ablegen".
    eingabe = (text or "").strip()
    if not real_files and not eingabe:
        return _kompass_upload(
            request, user,
            error="Bitte zuerst eine Datei ablegen oder einen Link bzw. Text einfügen.",
            status=400,
        )

    domaene = (domaene or "").strip() or wiki.DEFAULT_DOMAIN
    vertraulichkeit = vertraulichkeit or access.default_confidentiality_for_user(user)
    empfaenger = list(empfaenger or [])
    # Write ⊆ Read schon vor dem Schreiben der Originaldatei pruefen - mit Ersteller
    # und Empfaengern, sonst scheitert `vertraulich` (Regel 4) am eigenen Nutzer.
    try:
        require_writable(user, PageMeta(
            erstellt_von=user, domaene=domaene, vertraulichkeit=vertraulichkeit,
            empfaenger=empfaenger,
        ))
    except HTTPException as exc:
        return _kompass_upload(
            request, user,
            error=f"{exc.detail} (Domäne „{domaene}“). Bitte eine Domäne wählen, die du lesen darfst.",
            status=exc.status_code,
        )

    saved_pages: list[dict] = []

    if not real_files:
        # Nur Text oder Adresse. Besteht die Eingabe ausschliesslich aus einer
        # Adresse, wird die Seite dahinter geladen - dieselbe Regel und derselbe
        # SSRF-Schutz wie im Prefill, damit Vorschau und Ergebnis uebereinstimmen.
        quelltext, bezeichnung = eingabe, ""
        url = urlfetch.find_url(eingabe)
        if url:
            try:
                quelltext, bezeichnung = await run_in_threadpool(urlfetch.fetch_text, url)
            except ValueError as exc:
                return _kompass_upload(request, user, error=str(exc), status=400)
        title = (titel or "").strip() or bezeichnung.strip() or _title_from_text(quelltext)
        slug = _free_slug(title)
        meta = PageMeta(
            erstellt_von=user,
            erstellt_am=now_iso(),
            vertraulichkeit=vertraulichkeit,
            domaene=domaene,
            empfaenger=list(empfaenger),
            dokumenttyp=dokumenttyp,
            datum=datum,
            verfasser=verfasser or user,
            titel=title,
            quelle="link" if url else "text",
        )
        try:
            require_writable(user, meta)
        except HTTPException as exc:
            return _kompass_upload(request, user, error=str(exc.detail), status=exc.status_code)
        inhalt = quelltext.strip()
        if url:
            # Die Adresse gehoert in die Seite: sonst ist spaeter nicht mehr
            # nachvollziehbar, woher der Text stammt.
            inhalt = f"Quelle: <{url}>\n\n{inhalt}"
        wiki.save_page(slug, title, inhalt, meta)
        saved_pages.append({"slug": slug, "title": title})
        return _kompass_upload(request, user, saved=True, saved_pages=saved_pages)

    for f in real_files:
        content_bytes = await f.read()
        if not content_bytes:
            return _kompass_upload(
                request, user, error=f"Die Datei „{f.filename}“ ist leer.",
                status=400, saved_pages=saved_pages,
            )
        # Original bleibt: unter uploads/<domaene>/, der abgelegte Name steht in meta.
        saved_path = wiki.save_uploaded_file(f.filename, content_bytes, domaene=domaene)
        try:
            text = extractors.extract_text_from_file(saved_path, f.filename)
        except Exception as exc:  # unlesbare Datei: Meldung statt Traceback
            log.warning("Extraktion fehlgeschlagen fuer %s: %s", f.filename, exc)
            return _kompass_upload(
                request, user,
                error=f"„{f.filename}“ konnte nicht gelesen werden: {exc}",
                status=400, saved_pages=saved_pages,
            )
        # Titel leer (Prefill fehlgeschlagen oder uebersprungen): aus dem Dateinamen.
        title = (titel or "").strip() or _title_from_filename(f.filename)
        slug = _free_slug(title)  # Kollision: -2, -3, ... statt Abbruch
        meta = PageMeta(
            erstellt_von=user,
            erstellt_am=now_iso(),
            vertraulichkeit=vertraulichkeit,
            domaene=domaene,
            empfaenger=list(empfaenger),
            dokumenttyp=dokumenttyp,
            datum=datum,
            verfasser=verfasser or user,
            titel=title,
            quelle="upload",
            original_datei=saved_path.name,
        )
        try:
            require_writable(user, meta)  # nach Normalisierung erneut pruefen
        except HTTPException as exc:
            return _kompass_upload(
                request, user, error=str(exc.detail), status=exc.status_code,
                saved_pages=saved_pages,
            )
        wiki.save_page(
            slug, title,
            _upload_page_content(text, f.filename, title, slug, saved_path.name),
            meta,
        )
        saved_pages.append({"slug": slug, "title": title})
        # Nur die erste Datei liefert den Titel; weitere behalten ihren Dateinamen.
        titel = ""

    return _kompass_upload(request, user, saved=True, saved_pages=saved_pages)


# --- Antraege ---------------------------------------------------------------


@app.post("/proposals")
async def proposal_create(request: Request):
    """Neuer Antrag aus der Kompass-Maske. Der alte POST /proposals/new bleibt."""
    user = require_author(request)
    form = await request.form()
    name = _form_value(form, "name") or _form_value(form, "projektname")
    description = _form_value(form, "description") or _form_value(form, "beschreibung")
    if not name:
        raise HTTPException(status_code=400, detail="Ohne Projektnamen kein Antrag.")

    felder = _felder_from_form(form)
    felder.setdefault("projektname", name)
    if description:
        felder.setdefault("beschreibung", description)
    for form_key, field_key in (("cost", "kosten"), ("benefit", "nutzen"),
                                ("duration", "laufzeit")):
        value = _form_value(form, form_key)
        if value:
            felder[field_key] = value

    meta = PageMeta(
        erstellt_von=user,
        erstellt_am=now_iso(),
        vertraulichkeit=(_form_value(form, "vertraulichkeit")
                         or access.default_confidentiality_for_user(user)),
        domaene=_form_value(form, "domaene") or proposals.DEFAULT_DOMAIN,
        empfaenger=parse_recipients(_form_value(form, "empfaenger")),
        quelle=proposals.SOURCE,
    )
    require_writable(user, meta)  # Write ⊆ Read (403 in fremder Domaene)

    if proposals.already_submitted(name):
        raise HTTPException(
            status_code=409,
            detail=f'Ein Projektvorschlag mit dem Namen "{name}" wurde bereits eingereicht.',
        )

    uploaded: list[tuple[str, bytes]] = []
    for f in _form_uploads(form, "files"):
        uploaded.append((f.filename, await f.read()))
    duplicate = proposals.find_duplicate_file(uploaded)
    if duplicate is not None:
        raise HTTPException(
            status_code=409,
            detail=("Diese Projektdatei wurde bereits eingereicht - als Vorschlag "
                    f'"{duplicate.project_name}" (Hash identisch).'),
        )

    proposal = proposals.save_proposal(
        name, description, uploaded, meta,
        rolle=access.user_name(user), felder=felder,
    )
    return RedirectResponse(f"/proposals/{proposal.slug}", status_code=303)


@app.post("/proposals/{slug}")
async def proposal_save_fields(request: Request, slug: str):
    """Pflichtfelder eines Antrags speichern."""
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    require_author(request)
    require_writable(user, proposal.meta)  # nur wer hier schreiben darf
    form = await request.form()
    proposal.felder.update(_felder_from_form(form))
    proposals.write_proposal(proposal)
    return RedirectResponse(f"/proposals/{slug}#vollstaendigkeit", status_code=303)


@app.post("/proposals/{slug}/evaluate")
def proposal_evaluate_run(request: Request, slug: str):
    """Bewertung anstossen und das Ergebnis im Cache ablegen.

    Ohne LLM-Key liefert evaluation.evaluate_proposal ein {"error": ...} -
    das wird ebenfalls gespeichert, damit die Oberflaeche zeigen kann, dass
    ein Lauf stattgefunden hat, aber kein Score entstanden ist.
    """
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    evaluation_cache.store(slug, evaluation.evaluate_proposal(proposal))
    return RedirectResponse(f"/proposals/{slug}#bewertung", status_code=303)


def _append_dialog(proposal: proposals.Proposal, user: str, kind: str, text: str) -> None:
    proposal.dialog.append({
        "author": user,
        "kind": kind,
        "text": text,
        "zeit": now_iso(),
    })
    proposals.write_proposal(proposal)


@app.post("/proposals/{slug}/message")
async def proposal_message(request: Request, slug: str):
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    require_author(request)
    form = await request.form()
    kind = _form_value(form, "kind") or "message"
    if kind not in ("message", "escalation", "internal"):
        kind = "message"
    text = _form_value(form, "text") or _form_value(form, "message")
    if text:
        _append_dialog(proposal, user, kind, text)
    return RedirectResponse(f"/proposals/{slug}#dialog", status_code=303)


@app.post("/proposals/{slug}/remind")
def proposal_remind(request: Request, slug: str):
    """Erinnerung: es wird nichts verschickt (kein Mailversand angebunden),
    sondern ein sichtbarer Vermerk im Dialog hinterlegt."""
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    require_author(request)
    _append_dialog(
        proposal, user, "internal",
        f"Erinnerung vermerkt für {kompass.owner_name(proposal)}",
    )
    return RedirectResponse(f"/proposals/{slug}#dialog", status_code=303)


@app.post("/proposals/{slug}/share")
def proposal_share(request: Request, slug: str):
    """Statuslink: die Adresse des Antrags, als Vermerk festgehalten. Wer den
    Link oeffnet, sieht den Antrag nur, wenn er ihn ohnehin sehen darf."""
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    require_author(request)
    _append_dialog(proposal, user, "internal", f"Statuslink: /proposals/{slug}")
    return RedirectResponse(f"/proposals/{slug}#dialog", status_code=303)


DECISIONS = {"approve": "freigegeben", "defer": "zurueckgestellt", "reject": "abgelehnt"}


@app.post("/proposals/{slug}/decide")
async def proposal_decide(request: Request, slug: str):
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    require_author(request)
    require_writable(user, proposal.meta)
    form = await request.form()
    decision = _form_value(form, "decision")
    if decision not in DECISIONS:
        raise HTTPException(status_code=400, detail="Unbekannte Entscheidung.")
    view = kompass.proposal_vm(proposal, user)
    if not view["decision_enabled"]:
        raise HTTPException(
            status_code=409,
            detail="Entscheidung erst, wenn alle vier Rollen bewertet haben.",
        )
    proposal.status = DECISIONS[decision]
    name = access.user_name(user)
    proposal.dialog.append({
        "author": user,
        "kind": "internal",
        "text": f"Entscheidung: {proposal.status} durch {name}",
        "zeit": now_iso(),
    })
    proposals.write_proposal(proposal)
    return RedirectResponse(f"/proposals/{slug}#entscheidung", status_code=303)


@app.post("/proposals/{slug}/escalations/{escalation_id}/approve")
def proposal_escalation_approve(request: Request, slug: str, escalation_id: str):
    """Es gibt noch keine Eskalationen (Agenten fragen heute nicht nach) -
    deshalb gibt es auch keine, die man freigeben koennte: 404."""
    user = access.current_user(request)
    require_proposal(slug, user)
    raise HTTPException(status_code=404, detail="Seite nicht gefunden")


@app.get("/proposals/{slug}/files/{name}")
def proposal_file(request: Request, slug: str, name: str):
    user = access.current_user(request)
    proposal = require_proposal(slug, user)  # gleiche Schranke wie der Antrag
    safe_name = Path(name).name  # keine Traversal ueber den Dateinamen
    target = proposal.upload_dir / safe_name
    if safe_name != name or not target.is_file():
        raise HTTPException(status_code=404, detail="Seite nicht gefunden")
    return FileResponse(target, filename=safe_name)


# --- Wissen -----------------------------------------------------------------


@app.get("/knowledge")
def knowledge(request: Request, sort: str = "title", dir: str = "asc", dept: str = ""):
    user = access.current_user(request)
    view = kompass.knowledge_vm(user, sort, dir, dept)
    return templates.TemplateResponse(
        request, "kompass/knowledge.html", kctx(request, "knowledge", **view)
    )


@app.get("/knowledge/share")
def knowledge_share():
    # Teilen heisst bei uns: Rechte aendern. Das macht der Admin, nicht diese Seite.
    return RedirectResponse("/knowledge", status_code=303)


@app.get("/knowledge/edit")
def knowledge_edit():
    return RedirectResponse("/new", status_code=303)


@app.get("/knowledge/{slug}")
def knowledge_page(request: Request, slug: str):
    user = access.current_user(request)
    page = require_page(slug, user)
    meta = page.meta
    herkunft = [
        {"label": "Eingebracht von", "value": access.user_name(meta.erstellt_von)},
        {"label": "Domäne", "value": meta.domaene},
        {"label": "Vertraulichkeit", "value": meta.vertraulichkeit.replace("oeffentlich", "öffentlich")},
        {"label": "Zuletzt geändert",
         "value": format_ts(meta.geaendert_am or meta.erstellt_am) or kompass.MISSING},
    ]
    return templates.TemplateResponse(
        request,
        "kompass/page.html",
        kctx(request, "knowledge", page=page,
             content_html=render_markdown(page.content), herkunft=herkunft),
    )


@app.get("/knowledge/{slug}/original")
def knowledge_original(request: Request, slug: str):
    """Originaldatei einer Wissensseite (uploads/<domaene>/). Gleiche Schranke
    wie die Seite selbst; fehlend und verboten sind nicht unterscheidbar (404)."""
    user = access.current_user(request)
    page = require_page(slug, user)
    name = page.meta.original_datei
    target = wiki.uploaded_file_path(name, page.meta.domaene)
    if target is None:
        raise HTTPException(status_code=404, detail="Seite nicht gefunden")
    return FileResponse(target, filename=Path(name).name)


# --- Vorbefuellung ----------------------------------------------------------


PREFILL_PROPOSAL_PROMPT = (
    "Du fuellst ein Antragsformular aus einem Dokument. Antworte AUSSCHLIESSLICH "
    "mit JSON, ohne Markdown-Codeblock. Fuelle nur Felder, die im Text belegt "
    "sind; alles andere ist null. Erfinde nichts.\n"
    'Struktur: {"name": ..., "description": ..., "cost": ..., "benefit": ..., '
    '"duration": ..., ' + ", ".join(f'"{k}": ...' for k, _ in kompass.PFLICHTFELDER) + "}"
)


def _parse_json_object(raw: str) -> dict:
    """JSON-Objekt aus einer Modellantwort: Code-Zaeune weg, erstes {...} nehmen."""
    cleaned = llm_metadata.strip_code_fences(raw)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("kein JSON-Objekt in der Antwort")
    parsed = json.loads(cleaned[start:end + 1])
    if not isinstance(parsed, dict):
        raise ValueError(f"JSON ist kein Objekt ({type(parsed).__name__})")
    return parsed


def _prefill_proposal_fallback(text: str, filename: str) -> dict:
    """Ohne LLM-Key: Name aus Dateiname bzw. erster Zeile, Beschreibung aus den
    ersten 500 Zeichen, alles andere null. Keine geratenen Felder."""
    first_line = next((line.strip(" #") for line in text.splitlines() if line.strip()), "")
    name = Path(filename).stem.replace("_", " ").strip() if filename else first_line[:80]
    fields: dict[str, str | None] = {key: None for key, _ in kompass.PFLICHTFELDER}
    fields.update({key: None for key, _ in kompass.BASE_FIELDS})
    fields["name"] = name or first_line[:80] or None
    fields["description"] = text[:500].strip() or None
    return fields


@app.post("/api/prefill")
async def api_prefill(request: Request, target: str = "knowledge"):
    """Felder aus einer Datei oder einem Text vorschlagen.

    Antwort: {"status": "ok", "fields": {...}, "readers": "..."}. Der Nutzer
    sieht die Vorschlaege und kann jedes Feld korrigieren, bevor gespeichert
    wird - vorbefuellen ist kein Speichern.

    Besteht die Eingabe nur aus einer Adresse, wird die Seite dahinter geladen
    und ihr Text wie eine Datei behandelt (Grenzen: siehe urlfetch). Geht das
    schief, kommt {"status": "error", "message": "..."} zurueck - der Satz
    landet unveraendert in der Statuszeile des Drop-Ins.
    """
    user = require_author(request)
    text, filename = "", ""
    if request.headers.get("content-type", "").startswith("application/json"):
        payload = await request.json()
        text = str(payload.get("text") or "")
        url = urlfetch.find_url(text)
        if url:
            try:
                text, filename = await run_in_threadpool(urlfetch.fetch_text, url)
            except ValueError as exc:
                return {"status": "error", "fields": None, "message": str(exc)}
    else:
        form = await request.form()
        uploads = _form_uploads(form, "files")
        if uploads:
            first = uploads[0]
            filename = first.filename
            content = await first.read()
            saved = wiki.save_uploaded_file(filename, content)
            try:
                text = extractors.extract_text_from_file(saved, filename)
            except Exception as exc:
                raise HTTPException(status_code=400, detail=f"Extraktion fehlgeschlagen: {exc}")
        else:
            text = _form_value(form, "text")

    if target == "proposal":
        fields = _prefill_proposal_fallback(text, filename)
        if llm.is_configured() and text.strip():
            raw = ""
            try:
                # 4000 statt 1500: denkende Modelle brauchen das Budget zuerst im
                # Thinking-Block (siehe llm_metadata.HEADER_MAX_TOKENS).
                raw = llm.chat(PREFILL_PROPOSAL_PROMPT, text[:8000], max_tokens=4000).strip()
                parsed = _parse_json_object(raw)
                if isinstance(parsed, dict):
                    for key in list(fields):
                        value = parsed.get(key)
                        fields[key] = str(value).strip() if value not in (None, "") else fields[key]
            except Exception as exc:
                # Kein Ergebnis vom Modell: die Fallback-Felder bleiben stehen.
                log.warning("Prefill (Antrag) ohne LLM-Ergebnis (%s: %s). Antwort: %.200r",
                            type(exc).__name__, exc, raw)
        return {"status": "ok", "fields": fields, "readers": ""}

    # target == knowledge: derselbe Weg wie beim Upload (llm_metadata mit
    # Fallback). Bilder kommen hier bereits als Beschreibung an (extract_image,
    # je Datei-Hash gecacht - der Upload danach ruft das Modell nicht erneut).
    _, meta, title = llm_metadata.generate_header(text, filename or "eingabe.txt", user)
    if filename and extractors.is_image(filename) and meta.dokumenttyp in ("", "Dokument"):
        meta.dokumenttyp = "Bild"  # ohne Modell weiss der Fallback-Kopf nicht, dass es ein Bild ist
    fields = {
        "titel": title,
        # Bilder sind immer vom Typ "Bild" (der Fallback-Kopf wuesste es nicht).
        "dokumenttyp": "Bild" if extractors.is_image(filename) else (meta.dokumenttyp or None),
        "datum": meta.datum or None,
        "verfasser": meta.verfasser or user,
        "domaene": meta.domaene or wiki.DEFAULT_DOMAIN,
        "vertraulichkeit": meta.vertraulichkeit,
        # Korpus-Stufen (z.B. C-Level) bringen ihre Empfaenger mit; nur bei vertraulich relevant.
        "empfaenger": ", ".join(meta.empfaenger),
    }
    return {
        "status": "ok",
        "fields": fields,
        "readers": kompass._readers_text(fields["domaene"]),
    }


# --- Suche ------------------------------------------------------------------


@app.get("/search")
def search(request: Request, q: str = ""):
    """Die Suchleiste ist zugleich "Frag das Wiki": aus den Treffern wird eine
    belegte Antwort (Paket 10), darunter stehen die Fundstellen und die
    Projekte. Der Rechte-Filter steckt in search_snippets bzw.
    list_proposals(user) - hier wird nichts zusaetzlich gefiltert, und weil
    `ask_llm` ausschliesslich gegen diese Snippets belegt, kann auch kein
    Zitat aus einer gesperrten Seite stammen."""
    user = access.current_user(request)
    snippets = wiki.search_snippets(q, user) if q.strip() else []
    antwort = llm.ask_llm(q, snippets) if q.strip() else None
    needle = q.strip().lower()
    hits = []
    if needle:
        for p in proposals.list_proposals(user):
            haystack = f"{p.project_name}\n{p.description}".lower()
            if needle in haystack:
                hits.append({
                    "slug": p.slug,
                    "name": p.project_name,
                    "owner": kompass.owner_name(p),
                    "excerpt": (p.description or "").strip()[:220],
                })
    return templates.TemplateResponse(
        request, "kompass/search.html",
        kctx(request, "", q=q, antwort=antwort, snippets=snippets, hits=hits,
             llm_configured=llm.is_configured()),
    )


# --- Grundsaetze, Protokoll, Einstellungen ----------------------------------


@app.get("/principles")
def principles(request: Request):
    user = access.current_user(request)
    return templates.TemplateResponse(
        request, "kompass/principles.html",
        kctx(request, "principles", stats=kompass.principles_stats(user)),
    )


@app.get("/admin/log")
def admin_log(request: Request):
    require_admin(request)  # Nicht-Admins: 404, wie das uebrige Admin-Backend
    return templates.TemplateResponse(
        request, "kompass/log.html",
        kctx(request, "principles", changelog=kompass._changelog_vm(50)),
    )


@app.get("/settings")
def settings(request: Request):
    return templates.TemplateResponse(
        request, "kompass/settings.html",
        kctx(
            request, "settings",
            users=[{"key": u["id"], "display_name": u["name"]} for u in access.list_users()],
            mail_reminders=request.cookies.get("kp_mail") == "1",
        ),
    )


@app.post("/switch-user")
def switch_user(user: str = Form(...)):
    """Rollenwechsel wie POST /login - derselbe signierte Cookie, kein Sonderweg."""
    uid = access.get_user(user)["id"]
    resp = RedirectResponse("/settings", status_code=303)
    resp.set_cookie(
        access.COOKIE_NAME, access.sign_user(uid),
        httponly=True, samesite="lax", secure=access.cookie_secure(),
    )
    return resp


@app.post("/settings/mail")
def settings_mail(request: Request):
    """Schalter fuer Mail-Erinnerungen. Es wird nichts verschickt (kein
    Mailversand angebunden); der Zustand steht im Cookie."""
    on = request.cookies.get("kp_mail") == "1"
    resp = Response(status_code=204)
    resp.set_cookie(
        "kp_mail", "0" if on else "1", samesite="lax", secure=access.cookie_secure()
    )
    return resp


# --- Berechtigungen (Kompass-Oberflaeche auf dasselbe Backend) --------------


@app.get("/admin/permissions")
def admin_permissions(request: Request):
    require_admin(request)
    return templates.TemplateResponse(
        request, "kompass/admin_permissions.html",
        kctx(request, "settings", **kompass.permissions_matrix()),
    )


@app.post("/admin/permissions")
async def admin_permissions_save(request: Request, changes: str = Form("[]")):
    """changes = JSON {"gruppe/domaene": ""|"r"|"rw"}.

    Unser Modell kennt nur Lesegruppen je Domaene (Schreiben ist daran
    gebunden, Write ⊆ Read), deshalb wird 'r' wie 'rw' behandelt: die Gruppe
    steht in `lesen` oder nicht. Geschrieben wird ueber access.save_permissions,
    also mit Protokollzeile je Aenderung.
    """
    admin = require_admin(request)
    try:
        payload = json.loads(changes or "{}")
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    data = _copy_permissions()
    notes = []
    for key, value in payload.items():
        if "/" not in str(key):
            continue
        group, domain = str(key).split("/", 1)
        if group not in data["gruppen"] or domain not in data["domaenen"]:
            continue
        readers = data["domaenen"][domain]["lesen"]
        wanted = str(value) in ("r", "rw")
        if wanted and group not in readers:
            data["domaenen"][domain]["lesen"] = _ordered_groups(
                readers + [group], data["gruppen"]
            )
            notes.append(f"Domäne {domain}: Gruppe {group} darf jetzt lesen")
        elif not wanted and group in readers:
            data["domaenen"][domain]["lesen"] = [g for g in readers if g != group]
            notes.append(f"Domäne {domain}: Gruppe {group} liest nicht mehr")

    for note in notes:
        access.save_permissions(data, admin, note)
    return RedirectResponse("/admin/permissions", status_code=303)


@app.get("/admin/roles/new")
def admin_roles_new():
    # Nutzerverwaltung bleibt das alte Admin-Dashboard (dort steht die Wahrheit).
    return RedirectResponse("/admin", status_code=303)


@app.get("/admin/roles/{key}")
def admin_roles_edit(key: str):
    return RedirectResponse("/admin", status_code=303)
