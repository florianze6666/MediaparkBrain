"""View-Models der Kompass-Oberflaeche (Design-Handoff v8).

Reine Funktionen: rein gehen Nutzer-ID und Domaenenobjekte, raus kommen dicts,
die die Templates unter `templates/kompass/` erwarten. Kein Request, keine
Seiteneffekte - deshalb ohne TestClient testbar.

Zwei Regeln, die hier nirgends gebrochen werden:

1. **Rechte.** Es wird ausschliesslich ueber `wiki.list_pages(user)`,
   `proposals.list_proposals(user)` und `access.readable_domains(user)`
   gelesen. Keine Funktion hier filtert selbst; sie bekommt nur zu sehen, was
   der Nutzer ohnehin sehen darf.
2. **Ehrlich statt schoen.** Wo keine Daten existieren, steht "–". Erfundene
   Zahlen gibt es nicht; wo eine Zahl abgeleitet ist, steht warum im Kommentar.

Was heute fehlt und deshalb "–" oder 0 ist:
- Zugriffszahlen je Dokument (kein Zugriffs-Logging pro Seite) -> `hits='–'`
- Deadlines je Antrag (kein Feld im Vorschlag) -> `deadline='–'`
- Gremiumstermin (nur ueber Env `MPB_BOARD_DATE`) -> sonst "–"
- Quellen der Bewertung (die Bewertung liest kein Wiki-Wissen, nur die
  Antragsunterlagen) -> `sources=[]`, `source_count=0`
- Eskalationen (es gibt keine) -> 0
"""
from __future__ import annotations

import math

import markdown as md

import os
import re
from datetime import date, datetime

from . import access, evaluation, evaluation_cache, proposals, stats, wiki

# ---------------------------------------------------------------------------
# Rollen und Schwellen (README "Datenmapping")
# ---------------------------------------------------------------------------

# Anzeigekuerzel -> Schluessel in evaluation.ROLE_CRITERIA
ROLE_KEYS = (("BR", "betriebsrat"), ("CFO", "cfo"), ("IT", "it"), ("CEO", "ceo"))

SCORE_OK = 7      # ab hier gruen
SCORE_WARN = 4    # ab hier gelb, darunter rot
COMPLETE_OK = 13  # 13 von 15 Pflichtfeldern -> gruen
COMPLETE_WARN = 8

PFLICHTFELDER: tuple[tuple[str, str], ...] = (
    ("projektname", "Projektname"),
    ("beschreibung", "Beschreibung des Vorhabens"),
    ("zielsetzung", "Zielsetzung"),
    ("nutzen", "Fachlicher und organisatorischer Nutzen"),
    ("geschaeftsprozesse", "Betroffene Geschäftsprozesse"),
    ("organisationseinheiten", "Betroffene Organisationseinheiten"),
    ("business_case", "Business Case"),
    ("kosten", "Erwartete Kosten"),
    ("wirtschaftlicher_nutzen", "Erwarteter wirtschaftlicher Nutzen"),
    ("laufzeit", "Laufzeit / Einführungszeitraum"),
    ("technische_abhaengigkeiten", "Technische Abhängigkeiten"),
    ("organisatorische_abhaengigkeiten", "Organisatorische Abhängigkeiten"),
    ("risikoanalyse", "Risikoanalyse"),
    ("begruendung", "Begründung des Vorteils"),
    ("anbieterinformationen", "Anbieter- und Produktinformationen"),
)
FIELD_LABELS = dict(PFLICHTFELDER)

# Felder der Grundinfo (stehen im Antrag selbst, nicht im Pflichtfeld-Kopf)
BASE_FIELDS: tuple[tuple[str, str], ...] = (
    ("name", "Projektname"),
    ("description", "Vorhaben"),
    ("cost", "Kosten"),
    ("benefit", "Nutzen"),
    ("duration", "Laufzeit"),
)

# Felder des Wissens-Uploads (kommen aus llm_metadata.generate_header)
KNOWLEDGE_FIELDS: tuple[tuple[str, str], ...] = (
    ("titel", "Titel"),
    ("dokumenttyp", "Dokumenttyp"),
    ("datum", "Datum"),
    ("verfasser", "Verfasser"),
    ("domaene", "Domäne"),
    ("vertraulichkeit", "Vertraulichkeit"),
    ("empfaenger", "Empfänger"),  # nur bei vertraulich relevant (Gruppen/IDs, kommagetrennt)
)

MISSING = "–"  # Gedankenstrich: es gibt den Wert nicht (nicht: er ist null)


# ---------------------------------------------------------------------------
# Nutzer
# ---------------------------------------------------------------------------


def initials(display_name: str) -> str:
    """Bis zu zwei Initialen aus dem Anzeigenamen. "CFO / Controlling" -> "CC"."""
    words = re.findall(r"[A-Za-zÄÖÜäöüß0-9]+", display_name or "")
    return "".join(w[0].upper() for w in words[:2]) or "?"


def current_user_vm(user_id: str | None) -> dict:
    user = access.get_user(user_id)
    return {
        "key": user["id"],
        "display_name": user["name"],
        "initials": initials(user["name"]),
    }


# ---------------------------------------------------------------------------
# Zeit
# ---------------------------------------------------------------------------


def _fmt_date(value: str) -> str:
    """ISO-Zeit oder "2026-09-06 10:20 UTC" -> "06.09.2026". Unlesbares -> "–"."""
    if not value:
        return MISSING
    text = value.strip().replace(" UTC", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(text, fmt).strftime("%d.%m.%Y")
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text).strftime("%d.%m.%Y")
    except ValueError:
        return MISSING


def _fmt_datetime(value: str) -> str:
    if not value:
        return MISSING
    try:
        return datetime.fromisoformat(value.strip().replace(" UTC", "")).strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return _fmt_date(value)


def board_date() -> date | None:
    """Gremiumstermin aus Env MPB_BOARD_DATE (ISO). Nicht gesetzt -> None."""
    raw = (os.environ.get("MPB_BOARD_DATE") or "").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Vollstaendigkeit
# ---------------------------------------------------------------------------


def _state(value: int, ok: int, warn: int) -> str:
    if value >= ok:
        return "ok"
    if value >= warn:
        return "warn"
    return "bad"


def completeness(proposal: proposals.Proposal) -> dict:
    """Die 15 Pflichtfelder aus PLAN.md Sec. 2 gegen den Vorschlag geprueft.

    Werte kommen aus dem Kopf des Vorschlags. `projektname` und `beschreibung`
    zaehlen zusaetzlich als gefuellt, wenn Name bzw. Beschreibung des Antrags
    gesetzt sind - beides steht im Antrag selbst und muss nicht doppelt
    getippt werden.
    """
    felder = dict(proposal.felder or {})
    if proposal.project_name:
        felder.setdefault("projektname", proposal.project_name)
    if (proposal.description or "").strip():
        felder.setdefault("beschreibung", proposal.description.strip())

    missing = [
        {"key": key, "label": label}
        for key, label in PFLICHTFELDER
        if not (felder.get(key) or "").strip()
    ]
    total = len(PFLICHTFELDER)
    done = total - len(missing)
    return {
        "done": done,
        "total": total,
        "pct": round(done / total * 100),
        "state": _state(done, COMPLETE_OK, COMPLETE_WARN),
        "missing": missing,
        "fields": felder,
    }


# ---------------------------------------------------------------------------
# Bewertung (nur aus dem Cache - nie geschaetzt)
# ---------------------------------------------------------------------------


def _score_of(entry) -> int | None:
    if not isinstance(entry, dict):
        return None
    if entry.get("status") != "BEWERTET":
        return None
    score = entry.get("score")
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return None
    return int(round(score))


def role_scores(data: dict | None) -> list[dict]:
    """[{key BR|CFO|IT|CEO, score int|None, state}] aus einem Cache-Eintrag.

    Ohne Cache-Eintrag (oder bei einem Fehlerergebnis) hat jede Rolle
    `score=None` und `state='none'` - kein Ersatzwert.
    """
    rows = []
    for label, key in ROLE_KEYS:
        score = _score_of((data or {}).get(key)) if data and "error" not in data else None
        rows.append({
            "key": label,
            "eval_key": key,
            "score": score,
            "state": "none" if score is None else _state(score, SCORE_OK, SCORE_WARN),
        })
    return rows


def _total(roles: list[dict]) -> tuple[float | None, str]:
    scores = [r["score"] for r in roles if r["score"] is not None]
    if not scores:
        return None, "none"
    avg = round(sum(scores) / len(scores), 1)
    return avg, _state(avg, SCORE_OK, SCORE_WARN)


def is_decided(proposal: proposals.Proposal) -> bool:
    return (proposal.status or "").strip().lower() in proposals.DECIDED_STATUS


def owner_name(proposal: proposals.Proposal) -> str:
    """Anzeigename des Einreichers: der Rollen-Snapshot aus dem Kopf, sonst
    der Anzeigename der Nutzer-ID."""
    if proposal.rolle and proposal.rolle != access.UNKNOWN_CREATOR:
        return proposal.rolle
    return access.user_name(proposal.meta.erstellt_von)


def herkunft(proposal: proposals.Proposal) -> dict:
    """Herkunft eines Antrags (US-10): wer ihn eingebracht hat, in welcher Rolle.

    Altbestand ohne Kopf hat keine Herkunft - das wird gesagt, nicht kaschiert.
    Gleiche Aussage und gleiche Woerter wie die Herkunftsbox der alten Ansicht.
    """
    meta = proposal.meta
    quelle = {"upload": "Quelle: Upload", "proposal": "Quelle: Projektvorschlag"}.get(
        meta.quelle, ""
    )
    if meta.erstellt_von == access.UNKNOWN_CREATOR:
        return {"unknown": True, "text": "Herkunft unbekannt (Altbestand)",
                "name": "", "id": "", "rolle": "", "quelle": quelle,
                "domaene": meta.domaene, "vertraulichkeit": meta.vertraulichkeit,
                "zeit": _fmt_datetime(meta.erstellt_am)}
    name = access.user_name(meta.erstellt_von)
    return {
        "unknown": False,
        "text": f"Eingebracht von {name}",
        "name": name,
        "id": meta.erstellt_von,
        "rolle": proposal.rolle if proposal.rolle != access.UNKNOWN_CREATOR else name,
        "quelle": quelle,
        "domaene": meta.domaene,
        "vertraulichkeit": meta.vertraulichkeit,
        "zeit": _fmt_datetime(meta.erstellt_am),
    }


def status_sentence(proposal: proposals.Proposal, comp: dict, rated: int) -> str:
    """Ein Satz aus Status, Vollstaendigkeit und Anzahl Bewertungen - abgeleitet,
    nicht generisch. Solange es keinen Orchestrator gibt, der einen eigenen Satz
    setzt, ist das die ehrlichste Aussage, die die Daten hergeben."""
    if is_decided(proposal):
        return f"Entschieden: {proposal.status}"
    if comp["missing"]:
        n = len(comp["missing"])
        return f"Warten auf {n} Pflichtfeld" + ("" if n == 1 else "er")
    if rated == 0:
        return "Vollständig, Bewertung noch nicht gestartet"
    if rated < 4:
        return f"{rated} von 4 Rollen bewertet, Prüfung läuft"
    return "4 Rollen bewertet, Entscheidung offen"


def next_step(proposal: proposals.Proposal, comp: dict, rated: int) -> tuple[str, str, str]:
    """(Schritt, Verantwortlicher, Sprungmarke) - offene Eskalation gibt es
    heute nicht, deshalb: Vollstaendigkeit > Bewertung > Entscheidung."""
    if is_decided(proposal):
        return "Abgeschlossen", MISSING, "entscheidung"
    if comp["missing"]:
        return "Felder ergänzen", owner_name(proposal), "vollstaendigkeit"
    if rated == 0:
        return "Bewertung starten", "Kompass", "bewertung"
    if rated < 4:
        return "Bewertung vervollständigen", "Kompass", "bewertung"
    return "Entscheiden", "Gremium", "entscheidung"


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

SORT_KEYS = {
    "name": lambda r: r["name"].lower(),
    "completeness": lambda r: -r["completeness_pct"],
    "score": lambda r: -(r["total"] if r["total"] is not None else -1),
    "submitted": lambda r: r["_submitted_sort"],
    "deadline": lambda r: r["name"].lower(),  # keine Deadlines vorhanden -> stabile Ordnung
}


def dashboard_rows(user: str, sort: str | None = None) -> list[dict]:
    """Eine Zeile je Vorschlag, den `user` sehen darf."""
    rows = []
    for p in proposals.list_proposals(user):
        comp = completeness(p)
        roles = role_scores(evaluation_cache.load(p.slug))
        rated = sum(1 for r in roles if r["score"] is not None)
        total, total_state = _total(roles)
        step, step_owner, anchor = next_step(p, comp, rated)
        rows.append({
            "slug": p.slug,
            "name": p.project_name,
            "owner": herkunft(p)["text"],
            "owner_name": owner_name(p),
            "owner_key": p.meta.erstellt_von,
            "status_sentence": status_sentence(p, comp, rated),
            "completeness_pct": comp["pct"],
            "completeness_state": comp["state"],
            "roles": roles,
            "rated_count": rated,
            "total": total,
            "total_state": total_state,
            "next_step": step,
            "next_owner": step_owner,
            "next_anchor": anchor,
            "submitted_date": _fmt_date(p.submitted_at or p.meta.erstellt_am),
            # Kein Deadline-Feld im Vorschlag - nichts erfinden.
            "deadline": MISSING,
            "deadline_urgent": False,
            # `running` dimmt die Zeile. Wir wissen nicht, ob gerade ein Lauf
            # laeuft (die Bewertung ist synchron), also nie dimmen.
            "running": False,
            "_submitted_sort": p.submitted_at or p.meta.erstellt_am or "",
        })
    if sort in SORT_KEYS:
        rows.sort(key=SORT_KEYS[sort], reverse=(sort == "submitted"))
    return rows


def kpi(user: str, rows: list[dict]) -> dict:
    """Kopfzahlen des Dashboards. `running` = angefangen, aber nicht fertig
    bewertet (1 bis 3 von 4 Rollen)."""
    mine = sum(1 for r in rows if r["owner_key"] == user)
    running = sum(1 for r in rows if 1 <= r["rated_count"] <= 3)
    board = board_date()
    return {
        "mine": mine,
        "others": len(rows) - mine,
        "running": running,
        "days_to_board": (board - date.today()).days if board else MISSING,
        "board_date": board.strftime("%d.%m.") if board else MISSING,
    }


# ---------------------------------------------------------------------------
# Antragsdetail
# ---------------------------------------------------------------------------


def _role_detail(row: dict, data: dict | None, all_scores: list[int]) -> dict:
    entry = (data or {}).get(row["eval_key"]) or {}
    if not isinstance(entry, dict):
        entry = {}
    criteria = evaluation.ROLE_CRITERIA[row["eval_key"]]
    fehlt = [str(x) for x in (entry.get("fehlende_informationen") or []) if str(x).strip()]
    reason = str(entry.get("begruendung") or "").strip()

    if row["score"] is None:
        # Kein Score: die Begruendung erklaert, was fehlt (Status "INFORMATION FEHLT").
        missing_text = "; ".join(fehlt) or reason or "Noch nicht bewertet."
    else:
        missing_text = "; ".join(fehlt) or MISSING

    # "Konflikt mit anderen Rollen" ist abgeleitet, nicht vom Modell benannt:
    # Ein Abstand von 3 Punkten oder mehr zum hoechsten bzw. niedrigsten Score
    # der anderen Rollen ist der einzige Konflikt, den die Daten hergeben.
    conflict = MISSING
    others = [s for s in all_scores if s != row["score"]]
    if row["score"] is not None and others:
        spread = max(abs(row["score"] - s) for s in others)
        if spread >= 3:
            conflict = f"Bewertet {row['score']}, andere Rollen zwischen {min(others)} und {max(others)}."
        else:
            conflict = "Kein nennenswerter Abstand zu den anderen Rollen."

    return {
        **row,
        "name": criteria["name"],
        "criteria": criteria["kriterien"],
        # Die Bewertung liest heute nur die Antragsunterlagen, kein Wiki-Wissen.
        "sources": [],
        "reason": reason or MISSING,
        "improve": ("Ergänzen: " + "; ".join(fehlt)) if fehlt else MISSING,
        "missing": missing_text,
        "conflict": conflict,
    }


def _dialog_vm(proposal: proposals.Proposal) -> list[dict]:
    out = []
    for entry in proposal.dialog or []:
        author = entry.get("author") or access.UNKNOWN_CREATOR
        name = access.user_name(author)
        out.append({
            "author_initials": initials(name),
            "kind": entry.get("kind") or "message",
            "text": entry.get("text") or "",
            "meta": f"{name} · {_fmt_datetime(entry.get('zeit', ''))}",
            "action_label": "",
            "action_url": "",
        })
    return out


def _docs_vm(proposal: proposals.Proposal) -> list[dict]:
    out = []
    for name in proposal.files:
        path = proposal.upload_dir / name
        size = f"{path.stat().st_size / 1024:.0f} kB" if path.exists() else MISSING
        out.append({
            "name": name,
            "size": size,
            "url": f"/proposals/{proposal.slug}/files/{name}",
        })
    return out


def _versions_vm(proposal: proposals.Proposal) -> list[dict]:
    """Versionen = Commits der Antragsdatei. Ungetrackt -> leere Liste."""
    commits = stats._git_log(proposal.path.parent, proposal.path.name)
    out = []
    for i, (author, iso) in enumerate(reversed(commits), start=1):
        out.append({"label": f"v{i}", "time": _fmt_datetime(iso), "note": author})
    return list(reversed(out))


def proposal_vm(proposal: proposals.Proposal | None, user: str, mode: str = "view") -> dict:
    """Alles, was `kompass/proposal_detail.html` braucht (Kopfkommentar dort ist
    die Spezifikation). Ohne Vorschlag (mode='new') ein leeres Geruest."""
    if proposal is None:
        empty = {"done": 0, "total": len(PFLICHTFELDER), "pct": 0, "state": "bad",
                 "missing": [{"key": k, "label": l} for k, l in PFLICHTFELDER], "fields": {}}
        return {
            "slug": "", "name": "", "owner": access.user_name(user),
            "herkunft": {"unknown": False, "text": "", "name": "", "id": "",
                         "rolle": "", "quelle": "", "domaene": "",
                         "vertraulichkeit": "", "zeit": ""},
            "cost": "", "benefit": "", "duration": "", "description": "",
            "step": 1, "board_date": "", "completeness": empty,
            "total": None, "total_state": "none", "rated_count": 0, "source_count": 0,
            "roles": [], "dialog": [], "docs": [], "versions": [],
            "evaluated": False, "decision_enabled": False, "primary_action": None,
        }

    comp = completeness(proposal)
    data = evaluation_cache.load(proposal.slug)
    rows = role_scores(data)
    rated = sum(1 for r in rows if r["score"] is not None)
    total, total_state = _total(rows)
    scores = [r["score"] for r in rows if r["score"] is not None]
    roles = [_role_detail(r, data, scores) for r in rows]

    # Schritt 1..5 aus Status, Vollstaendigkeit und Bewertung.
    step = 1
    if not comp["missing"]:
        step = 2
    if rated >= 1:
        step = 3
    if rated == 4:
        step = 4
    if is_decided(proposal):
        step = 5

    board = board_date()
    _, _, anchor = next_step(proposal, comp, rated)
    step_label, _, _ = next_step(proposal, comp, rated)
    primary = None if is_decided(proposal) else {"label": step_label, "url": f"#{anchor}"}

    return {
        "slug": proposal.slug,
        "name": proposal.project_name,
        "owner": owner_name(proposal),
        "herkunft": herkunft(proposal),
        "cost": comp["fields"].get("kosten") or MISSING,
        "benefit": comp["fields"].get("nutzen") or MISSING,
        "duration": comp["fields"].get("laufzeit") or MISSING,
        "description": proposal.description,
        "description_html": md.markdown(proposal.description or "", extensions=["fenced_code", "tables"]),
        "status": proposal.status,
        "step": step,
        "board_date": board.strftime("%d.%m.") if board else "",
        "completeness": comp,
        "total": total,
        "total_state": total_state,
        "rated_count": rated,
        # Die Bewertung nutzt kein Wiki-Wissen -> ehrlich 0 Dokumente.
        "source_count": 0,
        "roles": roles,
        "dialog": _dialog_vm(proposal),
        "docs": _docs_vm(proposal),
        "versions": _versions_vm(proposal),
        "evaluated": data is not None,
        "decision_enabled": rated == 4 and not is_decided(proposal),
        "primary_action": primary,
    }


# ---------------------------------------------------------------------------
# Wissen
# ---------------------------------------------------------------------------

STOPWORDS = {
    "aber", "aller", "alles", "andere", "anderen", "auch", "auf", "aus", "bei", "beim",
    "dabei", "damit", "dann", "dass", "dazu", "dein", "denen", "dessen", "diese",
    "diesem", "diesen", "dieser", "dieses", "doch", "durch", "eine", "einem", "einen",
    "einer", "eines", "etwa", "fuer", "für", "gegen", "haben", "hier", "ihre", "ihrem",
    "ihren", "ihrer", "immer", "jede", "jeden", "jeder", "kann", "kein", "keine",
    "koennen", "können", "mehr", "muss", "muessen", "müssen", "nach", "nicht", "noch",
    "oder", "ohne", "schon", "sein", "seine", "sich", "sind", "sowie", "ueber", "über",
    "unter", "vom", "von", "vor", "waehrend", "während", "wenn", "werden", "wird",
    "wurde", "wurden", "zum", "zur", "zwischen",
}
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß0-9-]{4,}")

KNOWLEDGE_SORT = {
    "title": lambda d: d["title"].lower(),
    "department": lambda d: (d["department"], d["title"].lower()),
    "hits": lambda d: d["title"].lower(),        # keine Zugriffszahlen -> Titel
    "last_access": lambda d: d["_sort_date"],
    "edits": lambda d: d["edits"],
    "readers": lambda d: (d["readers"], d["title"].lower()),
}


def _readers_text(domain: str) -> str:
    spec = access.load_permissions()["domaenen"].get(domain) or {}
    groups = list(spec.get("lesen") or [])
    return ", ".join(groups) if groups else MISSING


def _cloud(pages: list[wiki.Page]) -> list[dict]:
    """Top-14 Woerter ab 5 Zeichen aus den lesbaren Seiten, Gewicht 1..6."""
    counts: dict[str, int] = {}
    for page in pages:
        for word in WORD_RE.findall(f"{page.title} {page.content}"):
            low = word.lower()
            if low in STOPWORDS:
                continue
            counts[low] = counts.get(low, 0) + 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:14]
    if not top:
        return []
    high = top[0][1]
    low = top[-1][1]
    span = max(high - low, 1)
    return [
        {"word": word, "weight": 1 + round((count - low) / span * 5)}
        for word, count in top
    ]


# Der Graph ist die Uebersicht, nicht die Liste: Pro Domaene stehen nur wenige
# Dokumente, der Rest sammelt sich in "+N weitere". Mehr Pillen passen um einen
# Ring aus neun Domaenen schlicht nicht, ohne sich zu ueberdecken - die volle
# Aufzaehlung steht in der Tabelle darunter.
GRAPH_MAX_DOCS = 4          # mehr wird zu "+N weitere" zusammengefasst
GRAPH_LABEL_LEN = 13        # Zeichen, danach "…" (voller Titel im title-Attribut)

# Der Graph wird auf einer gedachten Flaeche in Pixeln gerechnet und erst am
# Ende in Prozent umgerechnet. Grund: Die Knoten haben feste Groessen (Kreise,
# Textpillen), die Positionen aber sind relativ - nur wenn beide dieselbe
# Bezugsbreite haben, stimmen die Abstaende. Die Flaeche waechst mit der Zahl
# der Domaenen; der Container uebernimmt ihr Seitenverhaeltnis und ihre
# Mindestbreite (min_px), auf schmalen Schirmen scrollt er waagerecht.
_RING_MIN = 190             # kleinster Radius des Domaenenrings in Pixeln
_RING_PER_DOMAIN = 28       # Radiuszuwachs je Domaene: der Ring braucht Umfang
_RING_FLAT = 0.55           # Der Ring ist eine flache Ellipse - breite Schirme
                            # haben waagerecht mehr Platz als senkrecht.
_MARGIN_X = 80              # halbe Pillenbreite plus Luft zum Rand
_MARGIN_Y = 34              # Luft zum Rand, unten sitzt die Legende
_DOC_RINGS = (78, 116, 154)  # Abstaende Dokument <-> Domaene, reihum vergeben:
                             # benachbarte Dokumente liegen so nie gleich weit
                             # aussen und koennen sich schlechter ueberdecken
_FAN_MAX = 116              # groesster Oeffnungswinkel des Dokumentfaechers in Grad
_FAN_SPREAD = 420           # geteilt durch die Domaenenzahl: Oeffnungswinkel,
                            # damit benachbarte Faecher nicht ineinandergreifen
_RELAX_PASSES = 90          # Durchlaeufe der Ueberlappungskorrektur
_NODE_GAP = 9               # Mindestluft zwischen zwei Knoten in Pixeln


def _graph_label(title: str) -> str:
    return (title[:GRAPH_LABEL_LEN] + "…") if len(title) > GRAPH_LABEL_LEN else title


def _node_box(node: dict) -> tuple[float, float]:
    """Ungefaehre Kantenlaengen eines Knotens in Pixeln (fuer die Entzerrung)."""
    kind = node["kind"]
    if kind == "project":
        return 64.0, 64.0
    if kind == "dept":
        return 48.0, 48.0
    if kind == "dept-outline":
        return 34.0, 34.0
    # Dokumentpille: Breite folgt der Beschriftung, gedeckelt.
    return min(140.0, 22.0 + 6.5 * len(node["label"])), 26.0


def _relax(nodes: list[dict], w: float, h: float) -> None:
    """Ueberlappende Dokumentknoten auseinanderschieben.

    Zentrum und Domaenen bleiben stehen - der Ring ist das, was den Graphen
    lesbar macht. Bewegt werden nur die Dokumente: Bei zwei Dokumenten weicht
    jedes um die halbe Ueberdeckung aus, gegen einen festen Knoten um die
    ganze. Feste Reihenfolge, kein Zufall - gleicher Stand, gleiches Bild.
    """
    movable = [n for n in nodes if n["kind"] == "doc"]
    if not movable:
        return
    boxes = {id(n): _node_box(n) for n in nodes}
    for _ in range(_RELAX_PASSES):
        schub = 0.0
        for a in movable:
            aw, ah = boxes[id(a)]
            for b in nodes:
                if a is b:
                    continue
                bw, bh = boxes[id(b)]
                dx = a["px"] - b["px"]
                dy = a["py"] - b["py"]
                frei_x = (aw + bw) / 2 + _NODE_GAP - abs(dx)
                frei_y = (ah + bh) / 2 + _NODE_GAP - abs(dy)
                if frei_x <= 0 or frei_y <= 0:
                    continue        # beruehren sich nicht
                anteil = 0.5 if b["kind"] == "doc" else 1.0
                # Auf der Achse ausweichen, auf der weniger Weg noetig ist.
                if frei_x * (ah + bh) < frei_y * (aw + bw):
                    a["px"] += frei_x * anteil * (1.0 if dx >= 0 else -1.0)
                    schub += frei_x
                else:
                    a["py"] += frei_y * anteil * (1.0 if dy >= 0 else -1.0)
                    schub += frei_y
            # In der Flaeche halten; unten bleibt Platz fuer die Legende.
            a["px"] = min(max(a["px"], aw / 2 + 4), w - aw / 2 - 4)
            a["py"] = min(max(a["py"], ah / 2 + 4), h - ah / 2 - 34)
        if schub < 0.5:
            break


def _zuschneiden(nodes: list[dict], w: float, h: float) -> tuple[float, float]:
    """Flaeche auf den belegten Bereich schrumpfen und Knoten mitverschieben.

    Domaenen ohne Dokumente lassen ganze Ecken leer. Ohne Zuschnitt bliebe der
    Kasten unnoetig gross - auf dem Handy waere der sichtbare Ausschnitt dann
    vor allem Leerraum.
    """
    links = oben = math.inf
    rechts = unten = -math.inf
    for n in nodes:
        bw, bh = _node_box(n)
        links = min(links, n["px"] - bw / 2)
        rechts = max(rechts, n["px"] + bw / 2)
        oben = min(oben, n["py"] - bh / 2)
        unten = max(unten, n["py"] + bh / 2)

    rand_x, rand_oben, rand_unten = 16.0, 16.0, 34.0   # unten sitzt die Legende
    neu_w = min(w, rechts - links + 2 * rand_x)
    neu_h = min(h, unten - oben + rand_oben + rand_unten)
    for n in nodes:
        n["px"] -= links - rand_x
        n["py"] -= oben - rand_oben
    return round(neu_w, 1), round(neu_h, 1)


def _graph(user: str, pages: list[wiki.Page]) -> dict:
    """Sternfoermiges Netz: Wissensbasis in der Mitte, Domaenen auf einem Ring,
    ihre Dokumente nach aussen aufgefaechert.

    Deterministisch aus der Reihenfolge in permissions.yaml berechnet: kein
    Zufall, bei gleichem Stand immer dasselbe Bild. Nicht lesbare Domaenen
    haengen als Umriss mit im Ring (gesperrt ist nicht dasselbe wie nicht
    vorhanden), aber ohne ihre Dokumente. Pro Domaene stehen hoechstens sechs
    Dokumente plus ein Knoten "+N weitere".

    Alle Positionen verlassen die Funktion als Prozent der Flaeche - dieselbe
    Einheit, die Knoten (left/top) und SVG-Linien im Template benutzen.
    """
    domains = access.list_domains()
    readable_set = set(access.readable_domains(user))

    by_domain: dict[str, list[wiki.Page]] = {}
    for page in pages:
        by_domain.setdefault(page.meta.domaene, []).append(page)

    count = max(len(domains), 1)
    # Erst der Ring: sein Umfang muss die Domaenen tragen. Dann die Flaeche
    # drumherum - gerade so gross, dass die Dokumentfaecher hineinpassen.
    # Andersherum (feste Flaeche, Ring als Anteil davon) entstand entweder
    # toter Rand oder abgeschnittene Dokumente.
    rx = float(max(_RING_MIN, count * _RING_PER_DOMAIN))
    ry = rx * _RING_FLAT
    # Nur die Ringe zaehlen, die auch belegt sind: eine duenne Wissensbasis
    # bekommt so keine halbleere Flaeche.
    voll = max((len(by_domain.get(d, [])) for d in domains if d in readable_set), default=0)
    genutzt = min(max(voll, 1), len(_DOC_RINGS))
    reach = _DOC_RINGS[genutzt - 1] + 22   # weiteste Dokumentpille plus Luft
    w = round(2 * (rx + reach + _MARGIN_X), 1)
    h = round(2 * (ry + reach + _MARGIN_Y), 1)
    cx, cy = w / 2, h / 2

    nodes: list[dict] = [{
        "id": "__wissen__", "label": "Wissen", "title": "Gesamte Wissensbasis",
        "kind": "project", "px": cx, "py": cy, "w": None,
        "locked": False, "dept": "", "href": "/knowledge",
    }]
    # (Domaenenknoten, Dokumentknoten) - Kanten entstehen erst nach der Entzerrung.
    links: list[tuple[dict, dict]] = []

    for i, dom in enumerate(domains):
        # Start oben, dann im Uhrzeigersinn - unabhaengig von den Rechten, damit
        # der Ring fuer alle Rollen gleich aussieht.
        theta = -math.pi / 2 + 2 * math.pi * i / count
        dept = {
            "id": dom, "label": dom,
            "kind": "dept" if dom in readable_set else "dept-outline",
            "px": cx + rx * math.cos(theta), "py": cy + ry * math.sin(theta),
            "w": None, "dept": dom, "href": f"/knowledge?dept={dom}",
        }
        dept["locked"] = dom not in readable_set
        dept["title"] = f"Domäne {dom}" if not dept["locked"] else f"🔒 {dom} · für Sie gesperrt"
        nodes.append(dept)
        if dept["locked"]:
            continue

        docs = sorted(
            by_domain.get(dom, []),
            key=lambda p: (p.meta.geaendert_am or p.meta.erstellt_am or "", p.title),
            reverse=True,
        )
        rest = len(docs) - GRAPH_MAX_DOCS
        entries: list[dict] = [
            {"id": p.slug, "label": _graph_label(p.title), "title": p.title,
             "kind": "doc", "more": False, "href": f"/knowledge/{p.slug}"}
            for p in docs[:GRAPH_MAX_DOCS]
        ]
        if rest > 0:
            entries.append({
                "id": f"{dom}--more", "label": f"+{rest} weitere",
                "title": f"{rest} weitere Dokumente in {dom}",
                "kind": "doc", "more": True, "href": f"/knowledge?dept={dom}",
            })
        if not entries:
            continue

        # Faecher nach aussen: hoechstens so breit wie der Platz bis zur
        # Nachbardomaene, sonst greifen die Faecher ineinander.
        fan = math.radians(min(_FAN_MAX, _FAN_SPREAD / count))
        step = fan / max(len(entries) - 1, 1)
        for j, entry in enumerate(entries):
            angle = theta + (j - (len(entries) - 1) / 2) * step
            radius = _DOC_RINGS[j % len(_DOC_RINGS)]
            entry.update({
                "px": dept["px"] + radius * math.cos(angle),
                "py": dept["py"] + radius * math.sin(angle),
                "locked": False, "dept": dom,
            })
            nodes.append(entry)
            links.append((dept, entry))

    _relax(nodes, w, h)
    w, h = _zuschneiden(nodes, w, h)

    edges: list[dict] = []
    center = nodes[0]
    for n in nodes:
        if n["kind"] in ("dept", "dept-outline"):
            edges.append({"x1": _pct(center["px"], w), "y1": _pct(center["py"], h),
                          "x2": _pct(n["px"], w), "y2": _pct(n["py"], h),
                          "dept": n["dept"]})
    for dept, entry in links:
        edges.append({"x1": _pct(dept["px"], w), "y1": _pct(dept["py"], h),
                      "x2": _pct(entry["px"], w), "y2": _pct(entry["py"], h),
                      "dept": dept["dept"]})

    for n in nodes:
        box_w, _ = _node_box(n)
        n["x"] = _pct(n.pop("px"), w)
        n["y"] = _pct(n.pop("py"), h)
        n["w"] = round(box_w / w * 100, 2) if n["kind"] == "doc" else None

    return {"nodes": nodes, "edges": edges,
            "min_px": int(w), "ratio": round(w / h, 3)}


def _pct(value: float, total: float) -> float:
    return round(value / total * 100, 2)


def knowledge_vm(user: str, sort: str = "title", dir: str = "asc", dept: str = "") -> dict:
    all_pages = wiki.list_pages()          # ungefiltert, nur fuer die Gesamtzahl
    pages = wiki.list_pages(user)          # das, was der Nutzer sehen darf
    shown = [p for p in pages if not dept or p.meta.domaene == dept]

    docs = []
    for page in shown:
        docs.append({
            "slug": page.slug,
            "title": page.title,
            "department": page.meta.domaene,
            # Kein Zugriffs-Logging je Seite -> keine Zahl erfinden.
            "hits": MISSING,
            "last_access": _fmt_date(page.meta.geaendert_am or page.meta.erstellt_am),
            "edits": len(stats._git_history(page)),
            "readers": _readers_text(page.meta.domaene),
            # Kein "gilt bis"-Feld im Kopf -> nichts als ueberholt markieren.
            "stale_year": None,
            "_sort_date": page.meta.geaendert_am or page.meta.erstellt_am or "",
        })
    key = KNOWLEDGE_SORT.get(sort, KNOWLEDGE_SORT["title"])
    docs.sort(key=key, reverse=(dir == "desc"))

    return {
        "stats": {
            "total": len(all_pages),
            "departments": len(access.list_domains()),
            "visible": len(pages),
        },
        "docs": docs,
        "graph": _graph(user, pages),
        "cloud": _cloud(pages),
        "sort": sort,
        "dir": dir,
        "dept": dept,
    }


# ---------------------------------------------------------------------------
# Grundsaetze und Berechtigungen
# ---------------------------------------------------------------------------


def principles_stats(user: str) -> dict:
    """Zahlen der Grundsatzseite. Was das System nicht misst, ist 0 - nicht
    geschoent. (`user` wird gebraucht, weil "offene Felder" nur ueber Vorschlaege
    gezaehlt werden darf, die der Nutzer sehen darf.)"""
    open_fields = sum(
        len(completeness(p)["missing"]) for p in proposals.list_proposals(user)
    )
    today = datetime.now().strftime("%Y-%m-%d")
    log_entries = sum(1 for line in access.read_changelog(500) if line.startswith(today))
    return {
        "knowledge_total": len(wiki.list_pages()),
        "departments": len(access.list_domains()),
        "denied_today": access.deny_count(),
        "open_fields": open_fields,
        # Die Bewertung zitiert noch keine Wissensquellen.
        "sourced_pct": 0,
        # Kein Gueltigkeitsdatum im Dokumentkopf -> nichts als ueberholt bekannt.
        "stale": 0,
        # Eskalationen sind noch nicht gebaut.
        "escalations_open": 0,
        "log_entries": log_entries,
        # Es gibt keine automatischen Entscheidungen - und soll auch keine geben.
        "auto_decisions": 0,
    }


def _changelog_vm(n: int = 10) -> list[dict]:
    out = []
    for line in access.read_changelog(n):
        parts = line.split(" · ", 2)
        if len(parts) == 3:
            out.append({"time": _fmt_datetime(parts[0]), "text": f"{parts[1]}: {parts[2]}"})
        else:
            out.append({"time": MISSING, "text": line})
    return out


def permissions_matrix() -> dict:
    """Gruppe x Domaene aus permissions.yaml.

    Unser Modell kennt nur Lesegruppen je Domaene; Schreiben ist an Lesen
    gebunden (Write ⊆ Read, access.can_write). Eine Gruppe hat also entweder
    'rw' oder gar nichts - ein reines 'r' gibt es nicht. Die Oberflaeche darf
    trotzdem 'r' schicken; der POST behandelt 'r' wie 'rw'.
    """
    data = access.load_permissions()
    domains = list(data["domaenen"].keys())
    groups = []
    for group in data["gruppen"]:
        perms = {
            dom: ("rw" if group in ((spec or {}).get("lesen") or []) else "")
            for dom, spec in data["domaenen"].items()
        }
        groups.append({"name": group, "perms": perms})
    roles = [
        {"key": u["id"], "initials": initials(u["name"]),
         "display_name": u["name"], "groups": u["gruppen"]}
        for u in access.list_users()
    ]
    return {
        "domains": domains,
        "groups": groups,
        "roles": roles,
        "changelog": _changelog_vm(10),
    }
