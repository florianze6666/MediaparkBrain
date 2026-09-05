from __future__ import annotations

from pathlib import Path

import markdown as md
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import llm, stats, wiki

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


@app.get("/dashboard")
def dashboard(request: Request):
    pages = wiki.list_pages()
    dashboard_stats = stats.get_dashboard_stats()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"pages": pages, "stats": dashboard_stats},
    )


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
