"""Tests fuer das PDF-Einlesen (Arbeitspaket 8).

Die Test-PDFs werden hier erzeugt, weil `test project data/` ausschliesslich
DOCX und XLSX enthaelt - kein einziges PDF.
"""
from __future__ import annotations

import io

import pytest

from app import pdf_ingest

reportlab_canvas = pytest.importorskip(
    "reportlab.pdfgen.canvas", reason="reportlab wird nur zum Bauen der Test-PDFs gebraucht"
)


# ---------------------------------------------------------------------------
# Test-PDFs bauen
# ---------------------------------------------------------------------------


def _pdf(draw) -> bytes:
    buf = io.BytesIO()
    c = reportlab_canvas.Canvas(buf, pagesize=(595, 842))  # A4 in Punkten
    draw(c)
    c.save()
    return buf.getvalue()


def folien_pdf() -> bytes:
    """Zwei Folien: grosse Ueberschrift, darunter wenige Stichpunkte."""

    def draw(c):
        c.setFont("Helvetica-Bold", 28)
        c.drawString(60, 760, "Wirtschaftlichkeit CONI")
        c.setFont("Helvetica", 14)
        c.drawString(60, 700, "Total One-Off 450 TEUR")
        c.drawString(60, 670, "Avg Recurrent 90 TEUR")
        c.showPage()
        c.setFont("Helvetica-Bold", 28)
        c.drawString(60, 760, "Zeitplan und Rollout")
        c.setFont("Helvetica", 14)
        c.drawString(60, 700, "Go-Live Q3 2027")
        c.showPage()

    return _pdf(draw)


def fliesstext_pdf() -> bytes:
    """Drei Seiten Fliesstext mit wiederkehrender Fusszeile.

    Seite 1 endet mitten im Satz, Seite 2 setzt ihn fort.
    """
    def draw(c):
        for seite in range(3):
            y = 800
            # Nur die erste Seite traegt eine Ueberschrift; die Folgeseiten
            # setzen den Text fort, wie in einem echten Bericht.
            if seite == 0:
                c.setFont("Helvetica-Bold", 20)
                c.drawString(60, y, "Wirtschaftlichkeit der Sammelrechnung")
                y -= 40
            c.setFont("Helvetica", 11)
            if seite == 1:
                # Fortsetzung des Satzes, der auf Seite 1 abbricht.
                c.drawString(60, y, "eine hoehere Rechnungsqualitaet.")
                y -= 18
            for i in range(18):
                if seite == 0 and i == 17:
                    c.drawString(60, y, "Der erwartete Nutzen entsteht vor allem durch")
                else:
                    # Bewusst unterschiedliche Zeilen: echter Fliesstext
                    # wiederholt sich nicht wortgleich.
                    c.drawString(
                        60,
                        y,
                        f"Abschnitt {seite}.{i}: Die Sammelrechnung senkt den "
                        f"administrativen Aufwand bei Grosskunden spuerbar.",
                    )
                y -= 18
            # Fusszeile am unteren Seitenrand, auf jeder Seite identisch
            c.setFont("Helvetica", 8)
            c.drawString(60, 40, "Company 1 - vertraulich - Seite")
            c.showPage()

    return _pdf(draw)


def bild_pdf() -> bytes:
    """PDF ganz ohne Textlayer - nur Rechtecke, wie ein Scan."""

    def draw(c):
        for _ in range(2):
            c.rect(60, 400, 400, 300, fill=1)
            c.showPage()

    return _pdf(draw)


# ---------------------------------------------------------------------------
# Folien
# ---------------------------------------------------------------------------


def test_folien_werden_als_folien_erkannt():
    res = pdf_ingest.extract_pdf(folien_pdf(), "vorstellung.pdf")
    assert res.ok
    assert res.layout == "folien"
    assert res.page_count == 2


def test_folie_behaelt_ueberschrift_und_seitenzahl():
    res = pdf_ingest.extract_pdf(folien_pdf(), "vorstellung.pdf")
    assert "## Wirtschaftlichkeit CONI" in res.markdown
    # Die Seitenzahl ist die Belegstelle, die ein Mensch nachschlagen kann.
    assert "*(Seite 1)*" in res.markdown
    assert "*(Seite 2)*" in res.markdown


def test_folieninhalt_steht_im_selben_absatz_wie_die_ueberschrift():
    """Stichpunkte allein sind zu wortarm, um gefunden zu werden."""
    res = pdf_ingest.extract_pdf(folien_pdf(), "vorstellung.pdf")
    abschnitt = res.markdown.split("## ")[1]
    assert "450" in abschnitt
    assert "Wirtschaftlichkeit CONI" in abschnitt


def test_titel_kommt_aus_der_ersten_ueberschrift():
    res = pdf_ingest.extract_pdf(folien_pdf(), "vorstellung.pdf")
    assert res.title == "Wirtschaftlichkeit CONI"


# ---------------------------------------------------------------------------
# Fliesstext
# ---------------------------------------------------------------------------


def test_fliesstext_wird_als_fliesstext_erkannt():
    res = pdf_ingest.extract_pdf(fliesstext_pdf(), "bericht.pdf")
    assert res.ok
    assert res.layout == "fliesstext"


def test_satz_ueber_den_seitenumbruch_wird_zusammengefuegt():
    res = pdf_ingest.extract_pdf(fliesstext_pdf(), "bericht.pdf")
    assert "Der erwartete Nutzen entsteht vor allem durch eine hoehere Rechnungsqualitaet." in res.markdown


def test_wiederkehrende_fusszeile_wird_entfernt():
    res = pdf_ingest.extract_pdf(fliesstext_pdf(), "bericht.pdf")
    assert "Company 1 - vertraulich - Seite" not in res.markdown


# ---------------------------------------------------------------------------
# Leerpruefung - der eigentliche Kern des Pakets
# ---------------------------------------------------------------------------


def test_pdf_ohne_textlayer_wird_abgelehnt():
    res = pdf_ingest.extract_pdf(bild_pdf(), "scan.pdf")
    assert not res.ok
    assert res.markdown == ""
    assert "Textlayer" in res.reason


def test_ablehnung_nennt_den_grund_verstaendlich():
    res = pdf_ingest.extract_pdf(bild_pdf(), "scan.pdf")
    assert "OCR" in res.reason
    assert "Textlayer" in res.reason


def test_kaputte_datei_wird_abgelehnt_statt_zu_werfen():
    res = pdf_ingest.extract_pdf(b"das ist gar kein PDF", "kaputt.pdf")
    assert not res.ok
    assert res.markdown == ""
    assert res.reason


# ---------------------------------------------------------------------------
# Tabellen
# ---------------------------------------------------------------------------


def test_tabelle_wird_zu_markdown():
    md = pdf_ingest._table_to_markdown(
        [["Position", "Betrag"], ["One-Off", "450 TEUR"], ["Recurrent", "90 TEUR"]]
    )
    assert md.splitlines()[0] == "| Position | Betrag |"
    assert md.splitlines()[1] == "|---|---|"
    assert "| One-Off | 450 TEUR |" in md


def test_leere_tabelle_ergibt_nichts():
    assert pdf_ingest._table_to_markdown([]) == ""
    assert pdf_ingest._table_to_markdown([[None, ""], ["", None]]) == ""


# ---------------------------------------------------------------------------
# Abnahmekriterium: der Inhalt ist danach ueber "Frag das Wiki" auffindbar
# ---------------------------------------------------------------------------


def test_eingelesenes_pdf_ist_ueber_die_suche_auffindbar(pages_env):
    """Das "Fertig wenn" aus Paket 8, end-to-end."""
    import app.wiki as wiki
    from app.access import PageMeta

    res = pdf_ingest.extract_pdf(folien_pdf(), "vorstellung.pdf")
    assert res.ok

    wiki.save_page(
        wiki.slugify(res.title),
        res.title,
        res.markdown,
        PageMeta(
            erstellt_von="florian",
            erstellt_am="2026-09-05T12:00:00",
            vertraulichkeit="intern",
            domaene="projekt",
            ablageort="projektlaufwerk",
            quelle="vorstellung.pdf",
        ),
    )

    treffer = wiki.search_snippets("Wie hoch ist der One-Off Betrag fuer CONI?", "projektmanager")
    assert treffer, "das eingelesene PDF taucht nicht als Quelle auf"
    assert any("450" in t.paragraph for t in treffer)
    assert any(t.page.meta.quelle == "vorstellung.pdf" for t in treffer)
