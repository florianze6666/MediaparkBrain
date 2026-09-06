"""Kontext als anhaengbare, forkbare Datenstruktur (Plan 09, Abschnitt 3 und 4.1).

Der tragende Gedanke: der gemeinsame Anfang wird EINMAL gebaut, dann versiegelt.
Ein Fork teilt sich diesen Anfang und kann ihn nicht mehr veraendern. Damit ist die
Byte-Gleichheit des Praefix eine Eigenschaft der Datenstruktur und keine Vereinbarung,
an die sich alle halten muessen. Der Fingerabdruck belegt sie nachtraeglich.

Invarianten, die die Tests T-K1 und T-K2 pruefen:
  1. fork() veraendert das Original nicht.
  2. append() auf einem versiegelten Kontext wirft ValueError.
  3. Alle Forks derselben Basis liefern denselben fingerprint().

## Wo der Zwischenspeicherpunkt sitzt, und woran man einen Fehler erkennt

Es gibt ZWEI Punkte, beide auf geteiltem, rollenneutralem Inhalt:

  1. auf dem letzten Systemblock -- der Systemprompt ist ueber alle vier Rollen und
     ueber alle drei Modellaufrufe identisch, auch ueber Zug B, der eigene Nachrichten
     baut;
  2. auf dem letzten Inhaltsblock des versiegelten Praefix in `messages` -- also hinter
     Antrag und Basisdokumenten, unmittelbar vor Persona und Kalibrierung.

**Woran man erkennt, dass es kaputt ist:** `usage.cache_read_input_tokens` bleibt bei
den Rollen zwei bis vier null. Dann steht rollenspezifischer Inhalt vor dem Punkt. Der
haeufigste Weg dorthin ist, Persona oder Kalibrierung in den Systemprompt zu schieben;
`append` verbietet deshalb Systembloecke ausserhalb des Praefix und wirft dabei laut.
Der zweite Weg ist ein veraenderlicher Wert im Praefix, etwa ein Zeitstempel; dagegen
hilft der Fingerabdruck, der bei allen vier Rollen gleich sein muss.

Kennt nicht: Modell, Suche, Rollen.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Zwischenspeicherpunkt: sitzt auf dem LETZTEN Block des versiegelten Praefix.
CACHE_CONTROL: dict[str, str] = {"type": "ephemeral"}

ARTEN = ("system", "user", "dokumente")


@dataclass(frozen=True)
class Dokument:
    """Ein Wissensdokument im Kontext. `quelle` ist der Pfad relativ zu corpus/."""

    quelle: str
    titel: str
    collection: str
    text: str
    score: float = 0.0


@dataclass(frozen=True)
class Block:
    """art: 'system' | 'user' | 'dokumente'.

    Ein 'user'-Block eroeffnet eine neue Nachricht; 'dokumente'-Bloecke haengen sich an
    die zuletzt eroeffnete Nachricht an. Damit steuert der Aufrufer die Nachrichtengrenzen
    ueber die Reihenfolge, ohne dass der Block eine Nummer tragen muesste.
    """

    art: str
    inhalt: str = ""
    dokumente: tuple[Dokument, ...] = ()
    quelle: str = ""

    def __post_init__(self) -> None:
        if self.art not in ARTEN:
            raise ValueError(f"unbekannte Blockart {self.art!r}; erlaubt: {', '.join(ARTEN)}")

    @classmethod
    def system(cls, inhalt: str, quelle: str = "") -> "Block":
        return cls(art="system", inhalt=inhalt, quelle=quelle)

    @classmethod
    def user(cls, inhalt: str, quelle: str = "") -> "Block":
        return cls(art="user", inhalt=inhalt, quelle=quelle)

    @classmethod
    def dokumente_block(cls, dokumente: list[Dokument], quelle: str = "") -> "Block":
        return cls(art="dokumente", dokumente=tuple(dokumente), quelle=quelle)


def _kanonisch(b: Block) -> dict[str, Any]:
    """Was in den Fingerabdruck eingeht. Der Score bleibt draussen: er ist ein
    Suchartefakt, kein Inhalt, den das Modell sieht."""
    return {
        "art": b.art,
        "inhalt": b.inhalt,
        "quelle": b.quelle,
        "dokumente": [
            {"quelle": d.quelle, "titel": d.titel, "collection": d.collection, "text": d.text}
            for d in b.dokumente
        ],
    }


def _dok_block(d: Dokument) -> dict[str, Any]:
    return {
        "type": "document",
        "source": {"type": "text", "media_type": "text/plain", "data": d.text},
        "title": d.titel,
        "context": f"Aus der Wissensbasis. Quelle: corpus/{d.quelle}",
        "citations": {"enabled": True},
    }


class Kontext:
    """Praefix (versiegelt, geteilt) plus Rest (eigen, anhaengbar)."""

    def __init__(self, praefix: tuple[Block, ...] = (), versiegelt: bool = False) -> None:
        self._praefix: tuple[Block, ...] = tuple(praefix)
        self._rest: list[Block] = []
        self._versiegelt: bool = versiegelt

    # -- Aufbau ------------------------------------------------------------

    def append(self, *bloecke: Block) -> "Kontext":
        """Haengt an. Auf einer versiegelten Basis verboten, auf einem Fork erlaubt.

        Rueckgabe: self, damit sich Aufrufe verketten lassen.
        """
        if self._versiegelt:
            raise ValueError(
                "append auf einem versiegelten Kontext: der gemeinsame Anfang ist "
                "unveraenderlich. Erst fork() aufrufen, dann anhaengen."
            )
        for b in bloecke:
            if b.art == "system" and self._praefix:
                raise ValueError(
                    "Systemblock hinter dem Praefix: Persona und Kalibrierung gehoeren "
                    "NICHT in den Systemprompt, sonst ist der Anfang nicht mehr geteilt "
                    "und die Zwischenspeicherung faellt aus (Plan 09, Abschnitt 5)."
                )
            self._rest.append(b)
        return self

    def fork(self) -> "Kontext":
        """Neuer Kontext mit demselben versiegelten Praefix und leerem, eigenem Rest."""
        if not self._versiegelt:
            raise ValueError(
                "fork() auf einem unversiegelten Kontext: erst freeze() aufrufen, sonst "
                "waere der geteilte Anfang leer."
            )
        return Kontext(praefix=self._praefix, versiegelt=False)

    def freeze(self) -> "Kontext":
        """Versiegelt den bisherigen Inhalt als Praefix. Rueckgabe: self."""
        if self._versiegelt:
            return self
        self._praefix = self._praefix + tuple(self._rest)
        self._rest = []
        self._versiegelt = True
        return self

    # -- Kennung -----------------------------------------------------------

    def fingerprint(self) -> str:
        """sha256 ueber den versiegelten Praefix, 16 Hexzeichen.

        Bei allen Forks derselben Basis gleich; wandert als `prompt_version` ins
        Protokoll (NFR-10).
        """
        if not self._praefix:
            raise ValueError("fingerprint() ohne versiegelten Praefix: erst freeze() aufrufen.")
        roh = json.dumps([_kanonisch(b) for b in self._praefix],
                         ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(roh.encode("utf-8")).hexdigest()[:16]

    # -- Rendern -----------------------------------------------------------

    def _alle(self) -> list[Block]:
        return list(self._praefix) + list(self._rest)

    def system(self) -> list[dict[str, Any]]:
        """Systembloecke in API-Form, der letzte mit cache_control.

        Der Systemprompt ist rollenneutral und ueber alle drei Modellaufrufe identisch,
        deshalb lohnt hier ein eigener Punkt: auch Zug B, der eigene Nachrichten baut,
        liest ihn aus dem Zwischenspeicher.
        """
        bloecke = [
            {"type": "text", "text": b.inhalt}
            for b in self._alle()
            if b.art == "system" and b.inhalt
        ]
        if bloecke:
            bloecke[-1]["cache_control"] = dict(CACHE_CONTROL)
        return bloecke

    def messages(self) -> list[dict[str, Any]]:
        """Nachrichten in API-Form. Dokumente als document-Bloecke mit Zitaten.

        Der letzte Inhaltsblock des Praefix traegt cache_control; alles davor ist ueber
        die vier Rollen byteweise gleich.
        """
        grenze = len(self._praefix)
        nachrichten: list[dict[str, Any]] = []
        letzter_praefix_block: dict[str, Any] | None = None

        for i, b in enumerate(self._alle()):
            if b.art == "system":
                continue
            if b.art == "user":
                nachrichten.append({"role": "user", "content": [{"type": "text", "text": b.inhalt}]})
            else:  # dokumente
                if not nachrichten:
                    nachrichten.append({"role": "user", "content": []})
                nachrichten[-1]["content"].extend(_dok_block(d) for d in b.dokumente)
            if i < grenze and nachrichten and nachrichten[-1]["content"]:
                letzter_praefix_block = nachrichten[-1]["content"][-1]

        if letzter_praefix_block is not None:
            letzter_praefix_block["cache_control"] = dict(CACHE_CONTROL)
        return nachrichten

    def dokumente(self) -> list[Dokument]:
        """Alle Dokumente in Reihenfolge, Praefix zuerst.

        Die Reihenfolge entspricht dem `document_index` der API-Zitate.
        """
        return [d for b in self._alle() if b.art == "dokumente" for d in b.dokumente]

    # -- Ablage ------------------------------------------------------------

    def speichern(self, pfad: Path) -> None:
        """basis.json: Praefix und Fingerabdruck. Ermoeglicht den Einzel-Neulauf einer
        gescheiterten Rolle, ohne die uebrigen drei zu wiederholen."""
        pfad.parent.mkdir(parents=True, exist_ok=True)
        daten = {
            "fingerprint": self.fingerprint(),
            "praefix": [
                {
                    "art": b.art,
                    "inhalt": b.inhalt,
                    "quelle": b.quelle,
                    "dokumente": [
                        {"quelle": d.quelle, "titel": d.titel, "collection": d.collection,
                         "text": d.text, "score": d.score}
                        for d in b.dokumente
                    ],
                }
                for b in self._praefix
            ],
        }
        pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def laden(cls, pfad: Path) -> "Kontext":
        """Liest basis.json zurueck; der geladene Kontext ist versiegelt."""
        daten = json.loads(Path(pfad).read_text(encoding="utf-8"))
        bloecke = tuple(
            Block(
                art=b["art"],
                inhalt=b.get("inhalt", ""),
                dokumente=tuple(
                    Dokument(quelle=d["quelle"], titel=d["titel"], collection=d["collection"],
                             text=d["text"], score=float(d.get("score") or 0.0))
                    for d in b.get("dokumente", [])
                ),
                quelle=b.get("quelle", ""),
            )
            for b in daten["praefix"]
        )
        k = cls(praefix=bloecke, versiegelt=True)
        erwartet = daten.get("fingerprint")
        if erwartet and k.fingerprint() != erwartet:
            raise ValueError(
                f"basis.json: Fingerabdruck stimmt nicht ({k.fingerprint()} statt {erwartet}); "
                "die Datei passt nicht zu diesem Stand."
            )
        return k
