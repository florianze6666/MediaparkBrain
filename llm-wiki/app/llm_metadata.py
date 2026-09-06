from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .access import PageMeta, default_confidentiality_for_user
from .llm import chat as llm_chat
from .llm import is_configured


log = logging.getLogger(__name__)

HEADER_MAX_TOKENS = 4000

_YAML_ZEILE = re.compile(r"^([A-Za-z_]\w*):\s*(.*)$")
_CODE_FENCE = re.compile(r"^[ \t]*```[A-Za-z0-9_-]*[ \t]*$", re.MULTILINE)


def strip_code_fences(text: str) -> str:
    """Entfernt Markdown-Code-Zaeune (``` mit optionalem Sprachkuerzel).

    Modelle legen den Kopf gern in ```yaml ... ``` - auch mit Text davor oder
    danach. Die Zaunzeilen selbst fliegen raus, der Rest bleibt in Reihenfolge.
    """
    return _CODE_FENCE.sub("", text).strip()


def extract_frontmatter(text: str) -> tuple[str, str] | None:
    """Schneidet den Block zwischen den ersten beiden `---`-Zeilen heraus.

    Rueckgabe: (frontmatter_text, rest_nach_dem_block) oder None, wenn kein
    vollstaendiger Block vorhanden ist. Nur Zeilen, die genau aus `---`
    bestehen, zaehlen als Begrenzer - ein `---` mitten im Text nicht.
    """
    lines = text.splitlines()
    delims = [i for i, line in enumerate(lines) if line.strip() == "---"]
    if len(delims) < 2:
        return None
    start, end = delims[0], delims[1]
    frontmatter = "\n".join(lines[start + 1:end])
    rest = "\n".join(lines[end + 1:])
    return frontmatter, rest


def _yaml_reparieren(block: str) -> str:
    """Quotiert Skalarwerte, damit unquotiertes Modell-YAML noch lesbar wird.

    Modelle schreiben je nach Lauf `titel: Sitzung: Einfuehrung` oder
    `rolle: -` - beides ist ungueltiges YAML und liess bisher den kompletten
    generierten Kopf verfallen, obwohl der Inhalt brauchbar war. Listen und
    bereits quotierte Werte bleiben unangetastet; json.dumps liefert einen
    korrekt escapten Double-Quoted-Skalar, den YAML genauso liest.
    """
    zeilen = []
    for zeile in block.splitlines():
        treffer = _YAML_ZEILE.match(zeile)
        if not treffer:
            zeilen.append(zeile)
            continue
        schluessel, wert = treffer.group(1), treffer.group(2).strip()
        if not wert or wert[0] in "[{\"'":
            zeilen.append(zeile)
            continue
        zeilen.append(f"{schluessel}: {json.dumps(wert, ensure_ascii=False)}")
    return "\n".join(zeilen)


def build_fallback_header(
    text_preview: str,
    filename: str,
    user_id: str,
    custom_domain: str | None = None,
    custom_confidentiality: str | None = None,
) -> tuple[str, PageMeta, str]:
    """Erzeugt deterministisch einen Header gemaess Vorlage, falls kein LLM verfuegbar ist."""
    stem = Path(filename).stem
    # Titel aus Dateiname saeubern
    clean_title = stem.replace("_", " ").replace("-", " ").strip()
    clean_title = re.sub(r"\s+", " ", clean_title)
    if not clean_title:
        clean_title = "Hochgeladenes Dokument"

    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    today_iso = datetime.now().strftime("%Y-%m-%d")
    year_month = datetime.now().strftime("%Y-%m%d")

    vertraulichkeit = custom_confidentiality or default_confidentiality_for_user(user_id)
    domaene = custom_domain or "projekt"

    doc_id = f"LTT-{year_month}-UPLOAD-001"

    meta_dict = {
        "doc_id": doc_id,
        "titel": clean_title,
        "dokumenttyp": "Dokument",
        "datum": today_iso,
        "verfasser": user_id,
        "rolle": "-",
        "organisationseinheit": "PMO",
        "empfaenger": [],
        "projekt": clean_title,
        "geschaeftsbereich": "-",
        "vertraulichkeit": vertraulichkeit,
        "domaene": domaene,
        "informationsdomaene": [domaene],
        "ablageort": "projektlaufwerk",
        "erstellt_von": user_id,
        "erstellt_am": now_iso,
        "quelle": "upload",
        "original_datei": filename,
    }

    meta = PageMeta.from_dict(meta_dict)

    frontmatter_lines = ["---"]
    for k, v in meta_dict.items():
        if isinstance(v, list):
            frontmatter_lines.append(f"{k}: [{', '.join(v)}]")
        else:
            frontmatter_lines.append(f"{k}: {v}")
    frontmatter_lines.append("---")

    fliess_lines = [
        f"# {clean_title}\n",
        f"**Lahnberg Thermotechnik GmbH & Co. KG** - {meta.organisationseinheit}",
        f"Dokument: {clean_title}\n",
        f"Von:       {meta.verfasser}",
        f"Datum:     {today_iso}",
    ]
    if vertraulichkeit != "intern":
        fliess_lines.append(f"Einstufung: {vertraulichkeit}")

    full_header = "\n".join(frontmatter_lines) + "\n\n" + "\n".join(fliess_lines)
    return full_header, meta, clean_title


def generate_header(
    text_content: str,
    filename: str,
    user_id: str,
    custom_domain: str | None = None,
    custom_confidentiality: str | None = None,
) -> tuple[str, PageMeta, str]:
    """Laesst das LLM (oder Fallback) den vollstaendigen 2-teiligen Dokumentkopf generieren."""
    default_vert = custom_confidentiality or default_confidentiality_for_user(user_id)
    default_dom = custom_domain or "projekt"
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    today_iso = datetime.now().strftime("%Y-%m-%d")

    if not is_configured():
        return build_fallback_header(
            text_content[:2000],
            filename,
            user_id,
            custom_domain,
            custom_confidentiality,
        )

    # Erste 3000 Zeichen / ca. 600 Woerter fuer LLM Analyse
    preview = text_content[:4000].strip()
    if not preview:
        return build_fallback_header(
            "", filename, user_id, custom_domain, custom_confidentiality
        )

    system_prompt = f"""Du bist der Dokumentkopf- und Metadaten-Generator von MediaparkBrain.
Verbindliche Vorgabe ist der Standard aus Vorlage_dokument_kopfdaten.md.
Analysiere den uebergebenen Text und generiere AUSSCHLIESSLICH den 2-teiligen Dokumentkopf:

1. Teil: YAML-Frontmatter ganz oben (exakt diese Feldfolge):
---
doc_id: LTT-YYYY-MMDD-EINHEIT-NNN
titel: <Praegnanter Klartext-Titel aus dem Inhalt>
dokumenttyp: <Architekturentscheidung | Projektsteckbrief | Business Case | Protokoll | Betriebsratsinformation | Management Summary | Richtlinie | Notiz>
datum: <YYYY-MM-DD des Dokuments oder {today_iso}>
verfasser: <Name des Autors oder "{user_id}">
rolle: <Rolle der Person im Dokument oder "-">
organisationseinheit: <IT | Finanzen | HR | GF | BR | Einkauf | PMO | etc.>
empfaenger: [<Empfaengerliste oder []>]
projekt: <Projektname aus dem Dokument oder "-">
geschaeftsbereich: <Business Unit oder "-">
vertraulichkeit: <{default_vert}>
informationsdomaene: [{default_dom}]
ablageort: <sharepoint_gf | sharepoint_finance | sharepoint_hr | projektlaufwerk | mailarchiv | br_ablage | qm_lenkung | it_doku | einkauf_scm>
erstellt_von: {user_id}
erstellt_am: {now_iso}
quelle: upload
original_datei: {filename}
---

2. Teil: Fliessender Dokumentkopf direkt unter dem Frontmatter:
# <Titel>

**Lahnberg Thermotechnik GmbH & Co. KG** - <Organisationseinheit>
<Dokumenttyp / Vorlage>

Von:       <Verfasser, Rolle>
An:        <Empfaenger falls vorhanden>
Datum:     <Datum formatiert, z.B. {today_iso}>
Einstufung: <NUR angeben wenn vertraulichkeit != 'intern', bei 'intern' weglassen>

WICHTIGE REGELN:
- Felder, die keinen Sinn ergeben oder nicht im Text auffindbar sind, mit "-" oder [] belegen.
- Gib NUR den Header-Block (Frontmatter + Fliesskopf) zurueck, KEINEN weiteren Dokumentinhalt!
- Jeden Textwert im Frontmatter in doppelte Anfuehrungszeichen setzen, sonst ist das YAML
  ungueltig (etwa bei einem Doppelpunkt im Titel oder einem alleinstehenden "-"). Listen
  bleiben unquotiert: [] oder [projekt].
"""

    try:
        llm_response = llm_chat(
            system_prompt,
            f"Dateiname: {filename}\n\nDokument-Auszug:\n{preview}",
            # Denkende Modelle (Sonnet 5 ueber hybridai.one) verbrauchen das Budget
            # zuerst im Thinking-Block: bei 1000 kam fuer DOCX/PDF `finish=length`
            # mit leerem content zurueck, der Kopf fiel still auf den Dateinamen.
            max_tokens=HEADER_MAX_TOKENS,
        ).strip()
    except Exception as e:
        log.warning("LLM-Header-Generierung fehlgeschlagen (%s: %s) -> Fallback",
                    type(e).__name__, e)
        return build_fallback_header(
            preview, filename, user_id, custom_domain, custom_confidentiality
        )

    # Manche Modelle legen einen Markdown-Codeblock um das Frontmatter (auch
    # mit Text davor/danach). Der Zaun gehoert nicht in den Dokumentkopf.
    llm_response = strip_code_fences(llm_response)

    extracted = extract_frontmatter(llm_response)
    if extracted is None:
        log.warning("LLM-Header ohne Frontmatter-Block -> Fallback. Antwort: %.200r",
                    llm_response)
        return build_fallback_header(
            preview, filename, user_id, custom_domain, custom_confidentiality
        )
    frontmatter_text, rest = extracted
    # Der Kopf beginnt beim Frontmatter - Plauderei des Modells davor faellt weg.
    llm_response = f"---\n{frontmatter_text.strip()}\n---\n{rest.strip()}".rstrip()
    try:
        try:
            parsed_dict = yaml.safe_load(frontmatter_text) or {}
        except yaml.YAMLError:
            parsed_dict = yaml.safe_load(_yaml_reparieren(frontmatter_text)) or {}
        if not isinstance(parsed_dict, dict):
            raise ValueError(f"Frontmatter ist kein Mapping ({type(parsed_dict).__name__})")
    except Exception as e:
        log.warning("LLM-Header nicht lesbar (%s: %s) -> Fallback. Antwort: %.200r",
                    type(e).__name__, e, llm_response)
        return build_fallback_header(
            preview, filename, user_id, custom_domain, custom_confidentiality
        )

    # Ueberschreibe System-Felder sicherheitshalber
    parsed_dict["erstellt_von"] = user_id
    parsed_dict["erstellt_am"] = now_iso
    parsed_dict["quelle"] = "upload"
    parsed_dict["original_datei"] = filename
    if custom_confidentiality:
        parsed_dict["vertraulichkeit"] = custom_confidentiality
    if custom_domain:
        parsed_dict["domaene"] = custom_domain

    meta = PageMeta.from_dict(parsed_dict)
    title = str(parsed_dict.get("titel") or "").strip() or Path(filename).stem
    return llm_response, meta, title
