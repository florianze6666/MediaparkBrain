from __future__ import annotations

import logging
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import markdown as md
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()
logging.basicConfig(level=logging.INFO)

# access.py liest MPB_SECRET beim Modulimport (siehe access._load_secret) -
# load_dotenv() muss deshalb VOR diesem Import laufen, sonst gilt .env nie.
from . import access, evaluation, extractors, llm, llm_metadata, proposals, stats, wiki  # noqa: E402
from .access import PageMeta  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="MediaparkBrain LLM-Wiki")
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
    # secure=False bleibt bewusst (localhost/http); httponly + lax wie bisher.
    resp.set_cookie(
        access.COOKIE_NAME, access.sign_user(uid),
        httponly=True, samesite="lax", secure=False,
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
def index(request: Request):
    user = access.current_user(request)
    start = wiki.get_page_for("start", user)
    html = render_markdown(start.content) if start else ""
    return templates.TemplateResponse(
        request, "index.html", ctx(request, content_html=html, page=start)
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


@app.get("/upload")
def upload_form(request: Request):
    user = access.current_user(request)
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


@app.post("/upload")
async def upload_submit(
    request: Request,
    file: UploadFile = File(...),
    vertraulichkeit: str = Form("intern"),
    domaene: str = Form("projekt"),
):
    user = require_author(request)
    if not file.filename:
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
    require_writable(user, PageMeta(domaene=domaene, vertraulichkeit=vertraulichkeit))

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

    # 4. Pruefen ob der Nutzer in dieser Domaene mit dieser Einstufung schreiben darf (Write ⊆ Read)
    require_writable(user, meta)

    # 5. Slug & Inhalt zusammensetzen
    slug = wiki.slugify(extracted_title)
    full_content = f"{extracted_text.strip()}\n"

    # Speichern unter pages/
    wiki.save_page(slug, extracted_title, full_content, meta=meta)

    # 6. One-Click Redirect mit Erfolgs-Feedback (Sound & Badge)
    return RedirectResponse(f"/wiki/{slug}?uploaded=1", status_code=303)


# ---------------------------------------------------------------------------
# Projektvorschläge
# ---------------------------------------------------------------------------



@app.get("/proposals")
def proposal_list(request: Request):
    user = access.current_user(request)
    # US-12: Liste gefiltert ueber decide, wie die Seitenliste.
    return templates.TemplateResponse(
        request,
        "proposal_list.html",
        ctx(request, proposals=proposals.list_proposals(user)),
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


@app.get("/proposals/new")
def proposal_new_form(request: Request):
    require_author(request)  # Gast darf nicht einreichen (403, US-12)
    return _proposal_form(request)


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
    results = [
        {"proposal": p, "data": evaluation.evaluate_proposal(p)} for p in recent
    ]
    return templates.TemplateResponse(
        request,
        "proposal_evaluation.html",
        ctx(request, results=results, roles=evaluation.ROLE_CRITERIA),
    )


@app.get("/proposals/{slug}")
def proposal_view(request: Request, slug: str):
    user = access.current_user(request)
    proposal = require_proposal(slug, user)
    description_html = render_markdown(proposal.description)
    return templates.TemplateResponse(
        request,
        "proposal_view.html",
        ctx(request, proposal=proposal, description_html=description_html),
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
