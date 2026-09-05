from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .access import PageMeta, default_confidentiality_for_user

DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def is_configured() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


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
"""

    try:
        from anthropic import Anthropic

        client = Anthropic()
        model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Dateiname: {filename}\n\nDokument-Auszug:\n{preview}",
                }
            ],
        )
        llm_response = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()

        # Extrahiere YAML Frontmatter
        if "---" in llm_response:
            parts = llm_response.split("---", 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                parsed_dict = yaml.safe_load(frontmatter_text) or {}
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
                title = parsed_dict.get("titel") or Path(filename).stem
                return llm_response, meta, title

        # Fallback falls LLM kein valides Frontmatter lieferte
        return build_fallback_header(
            preview, filename, user_id, custom_domain, custom_confidentiality
        )
    except Exception as e:
        print(f"LLM-Header-Generierung fehlgeschlagen: {e} -> Fallback")
        return build_fallback_header(
            preview, filename, user_id, custom_domain, custom_confidentiality
        )
