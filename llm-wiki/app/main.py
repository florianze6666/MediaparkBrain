from __future__ import annotations

from pathlib import Path

import markdown as md
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import llm, proposals, wiki

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="MediaparkBrain LLM-Wiki")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def render_markdown(text: str) -> str:
    return md.markdown(text, extensions=["fenced_code", "tables"])


def seed_if_empty() -> None:
    if wiki.list_pages():
        return
    wiki.save_page(
        "start",
        "Start",
        "Willkommen im **LLM-Wiki** von MediaparkBrain.\n\n"
        "Dies ist die minimale Wissensbasis fuer das agentische "
        "KI-Wissensmanagement aus PLAN.md. Lege eigene Seiten an, "
        "verlinke sie und stelle unten Fragen - das Wiki sucht die "
        "passenden Stellen und lässt (bei konfiguriertem API-Key) "
        "ein LLM eine begruendete Antwort daraus formulieren.",
    )
    wiki.save_page(
        "vier-experten-agenten",
        "Vier Experten-Agenten",
        "Das System nutzt vier Stakeholder-Agenten: Betriebsrat, "
        "CFO/Controlling, IT/Architektur/Cybersecurity und CEO/Strategie. "
        "Jeder Agent bewertet einen Projektvorschlag aus seiner Perspektive "
        "mit Value Score, Risk Score und Strategy Score.\n\n"
        "Der Orchestrator-Agent koordiniert den Prozess, ist selbst aber "
        "kein fachlicher Gutachter.",
    )
    wiki.save_page(
        "wissensmanagement",
        "Wissensmanagement",
        "Die Wissensbasis basiert auf einem RAG-System und enthaelt sowohl "
        "internes Wissen (Richtlinien, Architektur, Budgets) als auch extern "
        "recherchierte Informationen (Hersteller, Zertifizierungen, "
        "Regulatorik).\n\n"
        "Dokumente koennen widerspruechlich oder veraltet sein - Agenten "
        "muessen Aktualitaet und Herkunft beruecksichtigen.",
    )


seed_if_empty()


@app.get("/")
def index(request: Request):
    pages = wiki.list_pages()
    start = wiki.get_page("start")
    html = render_markdown(start.content) if start else ""
    return templates.TemplateResponse(
        request,
        "index.html",
        {"pages": pages, "content_html": html, "page": start},
    )


@app.get("/wiki/{slug}")
def view_page(request: Request, slug: str):
    pages = wiki.list_pages()
    page = wiki.get_page(slug)
    if page is None:
        return RedirectResponse("/")
    html = render_markdown(page.content)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"pages": pages, "content_html": html, "page": page},
    )


@app.get("/wiki/{slug}/edit")
def edit_page_form(request: Request, slug: str):
    pages = wiki.list_pages()
    page = wiki.get_page(slug)
    return templates.TemplateResponse(
        request, "edit.html", {"pages": pages, "page": page, "slug": slug}
    )


@app.post("/wiki/{slug}/edit")
def edit_page_save(slug: str, title: str = Form(...), content: str = Form(...)):
    new_slug = wiki.slugify(title)
    if new_slug != slug:
        wiki.delete_page(slug)
    wiki.save_page(new_slug, title, content)
    return RedirectResponse(f"/wiki/{new_slug}", status_code=303)


@app.post("/wiki/{slug}/delete")
def delete_page_route(slug: str):
    wiki.delete_page(slug)
    return RedirectResponse("/", status_code=303)


@app.get("/new")
def new_page_form(request: Request):
    pages = wiki.list_pages()
    return templates.TemplateResponse(
        request,
        "edit.html",
        {"pages": pages, "page": None, "slug": None},
    )


@app.post("/new")
def new_page_save(title: str = Form(...), content: str = Form(...)):
    slug = wiki.slugify(title)
    wiki.save_page(slug, title, content)
    return RedirectResponse(f"/wiki/{slug}", status_code=303)


@app.get("/proposals")
def proposal_list(request: Request):
    pages = wiki.list_pages()
    return templates.TemplateResponse(
        request,
        "proposal_list.html",
        {"pages": pages, "proposals": proposals.list_proposals()},
    )


@app.get("/proposals/new")
def proposal_new_form(request: Request):
    pages = wiki.list_pages()
    return templates.TemplateResponse(
        request,
        "proposal_new.html",
        {"pages": pages, "error": None, "project_name": "", "description": ""},
    )


@app.post("/proposals/new")
async def proposal_new_save(
    request: Request,
    project_name: str = Form(...),
    description: str = Form(...),
    files: list[UploadFile] = File(default=[]),
):
    pages = wiki.list_pages()

    if proposals.already_submitted(project_name):
        return templates.TemplateResponse(
            request,
            "proposal_new.html",
            {
                "pages": pages,
                "error": (
                    f'Ein Projektvorschlag mit dem Namen "{project_name}" wurde '
                    "bereits eingereicht. Einreichung abgelehnt."
                ),
                "project_name": project_name,
                "description": description,
            },
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
    pages = wiki.list_pages()
    proposal = proposals.get_proposal(slug)
    if proposal is None:
        return RedirectResponse("/proposals")
    description_html = render_markdown(proposal.description)
    return templates.TemplateResponse(
        request,
        "proposal_view.html",
        {"pages": pages, "proposal": proposal, "description_html": description_html},
    )


@app.post("/proposals/{slug}/delete")
def proposal_delete(slug: str):
    proposals.delete_proposal(slug)
    return RedirectResponse("/proposals", status_code=303)


@app.get("/ask")
def ask_form(request: Request):
    pages = wiki.list_pages()
    return templates.TemplateResponse(
        request,
        "ask.html",
        {
            "pages": pages,
            "question": "",
            "answer": None,
            "snippets": [],
            "llm_configured": llm.is_configured(),
        },
    )


@app.post("/ask")
def ask_submit(request: Request, question: str = Form(...)):
    pages = wiki.list_pages()
    snippets = wiki.search_snippets(question)
    answer = llm.ask_llm(question, snippets)
    return templates.TemplateResponse(
        request,
        "ask.html",
        {
            "pages": pages,
            "question": question,
            "answer": answer,
            "snippets": snippets,
            "llm_configured": llm.is_configured(),
        },
    )
