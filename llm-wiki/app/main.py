from __future__ import annotations

from datetime import datetime
from pathlib import Path

import markdown as md
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import access, extractors, llm, llm_metadata, proposals, stats, wiki
from .access import PageMeta

load_dotenv()

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
        "domains": access.list_domains(),
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


def require_author(request: Request) -> str:
    """Gast darf nichts anlegen, bearbeiten oder loeschen (403)."""
    user = access.current_user(request)
    if user == access.GUEST:
        raise HTTPException(status_code=403, detail="Bitte erst Nutzer wählen")
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
    return _simple_page(
        "Bitte erst Nutzer wählen",
        "Als Gast kannst du Seiten nur lesen. Wähle in der Seitenleiste, "
        "als wer du arbeitest, und versuche es erneut.",
        403,
    )


@app.exception_handler(404)
def not_found_handler(request: Request, exc: HTTPException):
    # Bewusst gleiche Antwort fuer "gibt es nicht" und "darfst du nicht sehen" (US-8).
    return _simple_page(
        "Seite nicht gefunden",
        "Unter dieser Adresse gibt es keine Seite, die du sehen kannst.",
        404,
    )


# ---------------------------------------------------------------------------
# Login-Simulation (Cookie), bis ein echtes Login existiert
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
    resp.set_cookie(access.COOKIE_NAME, uid, httponly=True, samesite="lax")
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
    new_slug = wiki.slugify(title)
    if new_slug != slug:
        wiki.delete_page(slug)
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
    wiki.save_page(slug, title, content, meta)
    return RedirectResponse(f"/wiki/{slug}?gespeichert=1", status_code=303)


# ---------------------------------------------------------------------------
# Datei-Upload & Wissensdatenbank-Überführung (Arbeitspaket 2)
# ---------------------------------------------------------------------------


@app.get("/upload")
def upload_form(request: Request):
    user = access.current_user(request)
    conf_levels = access.list_confidentiality_levels()
    default_conf = access.default_confidentiality_for_user(user)
    domains = access.list_domains()
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
    user = access.current_user(request)
    if not file.filename:
        return templates.TemplateResponse(
            request,
            "upload.html",
            ctx(
                request,
                confidentiality_levels=access.list_confidentiality_levels(),
                default_confidentiality=access.default_confidentiality_for_user(user),
                domains=access.list_domains(),
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
                confidentiality_levels=access.list_confidentiality_levels(),
                default_confidentiality=access.default_confidentiality_for_user(user),
                domains=access.list_domains(),
                error="Die hochgeladene Datei ist leer.",
            ),
        )

    # 1. Originaldatei im Uploads-Ordner sichern
    saved_path = wiki.save_uploaded_file(file.filename, content_bytes)

    # 2. Text extrahieren
    try:
        extracted_text = extractors.extract_text_from_file(saved_path, file.filename)
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "upload.html",
            ctx(
                request,
                confidentiality_levels=access.list_confidentiality_levels(),
                default_confidentiality=access.default_confidentiality_for_user(user),
                domains=access.list_domains(),
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

    # 4. Slug & Inhalt zusammensetzen
    slug = wiki.slugify(extracted_title)
    full_content = f"{extracted_text.strip()}\n"

    # Speichern unter pages/
    wiki.save_page(slug, extracted_title, full_content, meta=meta)

    # 5. One-Click Redirect mit Erfolgs-Feedback (Sound & Badge)
    return RedirectResponse(f"/wiki/{slug}?uploaded=1", status_code=303)


# ---------------------------------------------------------------------------
# Projektvorschläge
# ---------------------------------------------------------------------------



@app.get("/proposals")
def proposal_list(request: Request):
    return templates.TemplateResponse(
        request,
        "proposal_list.html",
        ctx(request, proposals=proposals.list_proposals()),
    )


@app.get("/proposals/new")
def proposal_new_form(request: Request):
    return templates.TemplateResponse(
        request,
        "proposal_new.html",
        ctx(request, error=None, project_name="", description=""),
    )


@app.post("/proposals/new")
async def proposal_new_save(
    request: Request,
    project_name: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(default=[]),
):
    if proposals.already_submitted(project_name):
        return templates.TemplateResponse(
            request,
            "proposal_new.html",
            ctx(
                request,
                error=(
                    f'Ein Projektvorschlag mit dem Namen "{project_name}" wurde '
                    "bereits eingereicht. Einreichung abgelehnt."
                ),
                project_name=project_name,
                description=description,
            ),
            status_code=409,
        )

    uploaded_files = []
    for f in files:
        if not f.filename:
            continue
        uploaded_files.append((f.filename, await f.read()))

    proposal = proposals.save_proposal(project_name, description, uploaded_files)
    return RedirectResponse(f"/proposals/{proposal.slug}", status_code=303)


@app.get("/proposals/{slug}")
def proposal_view(request: Request, slug: str):
    proposal = proposals.get_proposal(slug)
    if proposal is None:
        return RedirectResponse("/proposals")
    description_html = render_markdown(proposal.description)
    return templates.TemplateResponse(
        request,
        "proposal_view.html",
        ctx(request, proposal=proposal, description_html=description_html),
    )


@app.post("/proposals/{slug}/delete")
def proposal_delete(slug: str):
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
            answer=None,
            snippets=[],
            llm_configured=llm.is_configured(),
        ),
    )


@app.post("/ask")
def ask_submit(request: Request, question: str = Form(...)):
    user = access.current_user(request)
    # US-7: Rechte-Filter VOR der Trefferauswahl, das LLM sieht nur Erlaubtes.
    snippets = wiki.search_snippets(question, user)
    answer = llm.ask_llm(question, snippets)
    return templates.TemplateResponse(
        request,
        "ask.html",
        ctx(
            request,
            question=question,
            answer=answer,
            snippets=snippets,
            llm_configured=llm.is_configured(),
        ),
    )
