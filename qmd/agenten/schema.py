"""Kapitel-17-Schema und Kapitel-16-Aggregation der Bewertungslogik.

Zwei Modelle, bewusst getrennt:

* `Bewertungsfelder` ist die reine Form fuer Zug B (Structured Output der Messages-API).
  Sie traegt keine Kopplungsregel, damit ein formal gueltiges, inhaltlich regelwidriges
  Modellergebnis nicht schon im SDK explodiert, sondern erst in `Zeile` als
  17.5-Verstoss sichtbar wird.
* `Zeile` ist das Kapitel-17-Objekt: genau acht Felder, flach, mit den drei harten Regeln
  aus 17.2 und der Validierung aus 17.5. Nach AE-04 ist das die JSONL-Zeile je Rolle;
  Laufmetadaten (Essay, Zitate, Abfragen, Modell, Zeitpunkt) gehoeren nicht hinein.

`validiere_zeilen` und `aggregiere` sind die Orchestrator-Seite: 17.5 je Zeile, dann
Kapitel 16 nur ueber gueltige Zeilen. KEIN SCORE ist nicht 0.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

ROLLEN: tuple[str, ...] = ("betriebsrat", "cfo", "it", "ceo")
Rolle = Literal["betriebsrat", "cfo", "it", "ceo"]
Status = Literal["BEWERTET", "INFORMATION FEHLT"]

# Reihenfolge der acht Felder in der JSONL-Zeile, wie in Kapitel 17.1.
FELDER: tuple[str, ...] = (
    "rolle",
    "status",
    "score",
    "begruendung",
    "fehlende_informationen",
    "praezedenz",
    "entscheidungsrelevanter_hinweis",
    "quellen",
)

# Z8: ab diesem Abstand zwischen zwei Rollen gilt ein Paar als Konflikt.
KONFLIKT_ABSTAND = 4


def _als_ganzzahl(v):
    """Score-Werte: keine Booleans, keine Dezimalstellen (Kapitel 9)."""
    if v is None:
        return None
    if isinstance(v, bool):
        raise ValueError("score darf kein Wahrheitswert sein")
    if isinstance(v, float):
        if not v.is_integer():
            raise ValueError("score muss ganzzahlig sein (Kapitel 9)")
        return int(v)
    if isinstance(v, int):
        return v
    raise ValueError("score muss eine ganze Zahl oder null sein")


class FragenBuendel(BaseModel):
    """Zug 1 im Rollenlauf (Plan 09): genau 3 gezielte Recherchefragen per Structured Output."""

    fragen: list[str] = Field(
        min_length=3,
        max_length=3,
        description="Genau 3 präzise, eigenständige Recherchefragen an die Wissensbasis",
    )


class Bewertungsfelder(BaseModel):
    """Zug B: die sechs Felder, die das Modell per Structured Output liefert.

    Reine Form. Alle Felder sind Pflicht (auch die optionalen Werte muessen als null
    vorkommen), damit das JSON-Schema fuer die API vollstaendig ist.
    """

    status: Status = Field(description="BEWERTET oder INFORMATION FEHLT")
    score: Optional[int] = Field(
        description="Ganze Zahl von 0 bis 10. Bei INFORMATION FEHLT immer null, nie ein Ersatzwert."
    )
    begruendung: str = Field(
        description="Fliesstext nach Kapitel 8: mit woertlichem Zitat und Betrag oder Regelbezug."
    )
    fehlende_informationen: list[str] = Field(
        description="Leer bei BEWERTET, sonst die konkreten Luecken."
    )
    praezedenz: Optional[str] = Field(
        description="Frueherer Fall, an den das Vorhaben erinnert, oder null."
    )
    entscheidungsrelevanter_hinweis: Optional[str] = Field(
        description="Hoechstens drei Zeilen, oder null."
    )


class Zeile(BaseModel):
    """Das Kapitel-17-Objekt. Genau acht Felder, keine weiteren (17.2 Regel 3)."""

    model_config = ConfigDict(extra="forbid")

    rolle: Rolle
    status: Status
    score: Optional[int] = None
    begruendung: str
    fehlende_informationen: list[str] = Field(default_factory=list)
    praezedenz: Optional[str] = None
    entscheidungsrelevanter_hinweis: Optional[str] = None
    quellen: list[str] = Field(default_factory=list)

    @field_validator("score", mode="before")
    @classmethod
    def _score_form(cls, v):
        return _als_ganzzahl(v)

    @field_validator("begruendung")
    @classmethod
    def _begruendung_nicht_leer(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("begruendung ist leer (Kapitel 8)")
        return v

    @model_validator(mode="after")
    def _kopplung(self) -> "Zeile":
        if self.status == "INFORMATION FEHLT":
            if self.score is not None:
                raise ValueError(
                    "INFORMATION FEHLT verlangt score null, kein Ersatzwert (17.2 Regel 1)"
                )
        else:
            if self.score is None:
                raise ValueError("BEWERTET verlangt einen Score von 0 bis 10 (17.2 Regel 1)")
            if not 0 <= self.score <= 10:
                raise ValueError(f"score {self.score} liegt ausserhalb von 0 bis 10 (Kapitel 7)")
        return self

    @classmethod
    def aus_feldern(cls, rolle: str, felder: Bewertungsfelder, quellen: list[str]) -> "Zeile":
        return cls(
            rolle=rolle,
            status=felder.status,
            score=felder.score,
            begruendung=felder.begruendung,
            fehlende_informationen=list(felder.fehlende_informationen),
            praezedenz=felder.praezedenz,
            entscheidungsrelevanter_hinweis=felder.entscheidungsrelevanter_hinweis,
            quellen=list(quellen),
        )

    def als_dict(self) -> dict:
        return {k: getattr(self, k) for k in FELDER}

    def als_jsonl(self) -> str:
        return json.dumps(self.als_dict(), ensure_ascii=False)


class ZeilenFehler(BaseModel):
    rolle: Optional[str] = None
    fehler: str
    zeile: str


def validiere_zeilen(zeilen: list[str]) -> tuple[list[Zeile], list[ZeilenFehler]]:
    """Kapitel 17.5: je Zeile gueltiges JSON, Pflichtfelder, Rolle aus der Menge und genau
    einmal, Status gueltig, Kopplung eingehalten. Eine durchgefallene Zeile wird nicht
    verworfen, sondern als Fehler gemeldet und bei der Aggregation wie ein Agent ohne
    Score behandelt (16.2)."""
    gueltig: list[Zeile] = []
    fehler: list[ZeilenFehler] = []
    gesehen: set[str] = set()
    for roh in zeilen:
        roh_str = roh.strip()
        if not roh_str:
            continue
        try:
            daten = json.loads(roh_str)
        except json.JSONDecodeError as e:
            fehler.append(ZeilenFehler(fehler=f"kein gueltiges JSON: {e}", zeile=roh_str[:200]))
            continue
        rolle = daten.get("rolle") if isinstance(daten, dict) else None
        try:
            z = Zeile.model_validate(daten)
        except ValidationError as e:
            kurz = "; ".join(
                f"{'.'.join(str(p) for p in err['loc']) or 'objekt'}: {err['msg']}"
                for err in e.errors()
            )
            fehler.append(ZeilenFehler(rolle=rolle if isinstance(rolle, str) else None,
                                       fehler=kurz, zeile=roh_str[:200]))
            continue
        if z.rolle in gesehen:
            fehler.append(ZeilenFehler(rolle=z.rolle, fehler="Rolle kommt mehr als einmal vor (17.5)",
                                       zeile=roh_str[:200]))
            continue
        gesehen.add(z.rolle)
        gueltig.append(z)
    return gueltig, fehler


# ---------------------------------------------------------------------------
# Kapitel 16
# ---------------------------------------------------------------------------


class Rollenergebnis(BaseModel):
    rolle: str
    status: Status
    score: Optional[int]
    begruendung: str
    fehlende_informationen: list[str]
    praezedenz: Optional[str] = None
    entscheidungsrelevanter_hinweis: Optional[str] = None
    quellen: list[str] = Field(default_factory=list)


class Konflikt(BaseModel):
    rolle_a: str
    rolle_b: str
    score_a: int
    score_b: int
    abstand: int


class Zusammenfassung(BaseModel):
    lauf_id: str
    zeitpunkt: str
    gesamtstatus: Status
    gesamtscore: Optional[float]
    anzahl_bewertet: int
    anzahl_gueltige_zeilen: int
    rollen: list[Rollenergebnis]
    fehlende_informationen: list[str]
    spanne: Optional[int]
    konflikte: list[Konflikt]
    technische_fehler: list[dict]
    zeilenfehler: list[ZeilenFehler]
    # Tokenverbrauch ueber alle Rollen (Summe der Protokolle, siehe treiber._erfasse_usage);
    # kein Bestandteil von Kapitel 16, nur Betriebsinformation.
    tokens: Optional[dict] = None


def aggregiere(
    gueltig: list[Zeile],
    zeilenfehler: list[ZeilenFehler],
    lauf_id: str,
    technische_fehler: list[dict] | None = None,
    zeitpunkt: str | None = None,
) -> Zusammenfassung:
    """Kapitel 16 ueber die gueltigen Zeilen.

    16.1 arithmetischer Durchschnitt der gueltigen Scores, auf eine Dezimalstelle.
    16.2 INFORMATION FEHLT geht nicht ein; KEIN SCORE ist nicht 0.
    16.3 Einzelbewertungen bleiben vollstaendig neben dem Gesamtscore.
    16.5 ohne gueltigen Score: Gesamtstatus INFORMATION FEHLT, Luecken zusammengefuehrt.
    Z8   Spanne und Rollenpaare mit Abstand ab KONFLIKT_ABSTAND.
    """
    bewertet = [z for z in gueltig if z.status == "BEWERTET" and z.score is not None]
    scores = [z.score for z in bewertet]
    gesamtscore = round(sum(scores) / len(scores), 1) if scores else None
    gesamtstatus: Status = "BEWERTET" if scores else "INFORMATION FEHLT"

    luecken: list[str] = []
    for z in gueltig:
        if z.status == "INFORMATION FEHLT":
            for info in z.fehlende_informationen:
                eintrag = f"{z.rolle}: {info}"
                if eintrag not in luecken:
                    luecken.append(eintrag)

    konflikte: list[Konflikt] = []
    for i, a in enumerate(bewertet):
        for b in bewertet[i + 1:]:
            abstand = abs(a.score - b.score)
            if abstand >= KONFLIKT_ABSTAND:
                konflikte.append(Konflikt(rolle_a=a.rolle, rolle_b=b.rolle,
                                          score_a=a.score, score_b=b.score, abstand=abstand))
    spanne = (max(scores) - min(scores)) if scores else None

    return Zusammenfassung(
        lauf_id=lauf_id,
        zeitpunkt=zeitpunkt or datetime.now(timezone.utc).isoformat(),
        gesamtstatus=gesamtstatus,
        gesamtscore=gesamtscore,
        anzahl_bewertet=len(scores),
        anzahl_gueltige_zeilen=len(gueltig),
        rollen=[Rollenergebnis(**z.als_dict()) for z in gueltig],
        fehlende_informationen=luecken,
        spanne=spanne,
        konflikte=konflikte,
        technische_fehler=list(technische_fehler or []),
        zeilenfehler=list(zeilenfehler),
    )
