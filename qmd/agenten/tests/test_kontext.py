"""T-K: der Kontext als forkbare Datenstruktur (Plan 09, Abschnitt 3 und 10).

Geprueft wird, was die Zwischenspeicherung traegt: der Praefix ist nach dem Versiegeln
unveraenderlich, alle Forks teilen ihn byteweise, und der Zwischenspeicherpunkt sitzt an
der einzigen Stelle, an der er sitzen darf.
"""
from __future__ import annotations

import json

import pytest

from kontext import CACHE_CONTROL, Block, Dokument, Kontext


def dok(i: int, collection: str = "intern") -> Dokument:
    return Dokument(quelle=f"projektlaufwerk/fall/2013/d{i}.md", titel=f"Titel {i}",
                    collection=collection, text=f"Volltext {i}", score=0.9 - i / 100)


def basis(n_dok: int = 2) -> Kontext:
    """Der gemeinsame Anfang aus Abschnitt A: Systemprompt, Antrag, Basisdokumente."""
    k = Kontext()
    k.append(Block.system("ONBOARDING"), Block.system("BEWERTUNGSLOGIK"))
    k.append(Block.user("ANTRAG"))
    k.append(Block.dokumente_block([dok(i) for i in range(n_dok)], quelle="vorsuche"))
    return k.freeze()


# --- T-K1: fork veraendert das Original nicht, append nach freeze wirft --------


def test_fork_laesst_das_original_unberuehrt():
    b = basis()
    vorher = json.dumps(b.messages(), ensure_ascii=False)
    f = b.fork()
    f.append(Block.user("PERSONA"))
    f.append(Block.dokumente_block([dok(7)]))
    assert json.dumps(b.messages(), ensure_ascii=False) == vorher
    assert len(b.dokumente()) == 2
    assert len(f.dokumente()) == 3


def test_append_auf_versiegelter_basis_wirft():
    b = basis()
    with pytest.raises(ValueError, match="versiegelt"):
        b.append(Block.user("PERSONA"))


def test_fork_vor_freeze_wirft():
    k = Kontext()
    k.append(Block.system("X"))
    with pytest.raises(ValueError, match="freeze"):
        k.fork()


def test_freeze_ist_mehrfach_ungefaehrlich():
    b = basis()
    assert b.freeze() is b
    assert b.freeze().fingerprint() == b.fingerprint()


# --- T-K2: alle vier Forks teilen den Fingerabdruck ---------------------------


def test_vier_forks_teilen_den_fingerabdruck():
    b = basis()
    forks = []
    for rolle in ("betriebsrat", "cfo", "it", "ceo"):
        f = b.fork()
        f.append(Block.user(f"PERSONA {rolle}"))
        f.append(Block.dokumente_block([dok(50 + len(forks))]))
        forks.append(f)
    abdruecke = {f.fingerprint() for f in forks}
    assert len(abdruecke) == 1
    assert abdruecke == {b.fingerprint()}


def test_fingerabdruck_haengt_am_inhalt_nicht_am_score():
    a = Kontext()
    a.append(Block.system("S"), Block.user("U"))
    a.append(Block.dokumente_block([Dokument("q.md", "T", "intern", "Text", score=0.9)]))
    b = Kontext()
    b.append(Block.system("S"), Block.user("U"))
    b.append(Block.dokumente_block([Dokument("q.md", "T", "intern", "Text", score=0.1)]))
    assert a.freeze().fingerprint() == b.freeze().fingerprint()

    c = Kontext()
    c.append(Block.system("S"), Block.user("U ANDERS"))
    c.append(Block.dokumente_block([Dokument("q.md", "T", "intern", "Text")]))
    assert c.freeze().fingerprint() != a.fingerprint()


def test_fingerabdruck_ohne_praefix_wirft():
    with pytest.raises(ValueError, match="freeze"):
        Kontext().fingerprint()


# --- Der Zwischenspeicherpunkt ------------------------------------------------


def test_zwischenspeicherpunkt_sitzt_am_ende_des_praefix():
    f = basis().fork()
    f.append(Block.user("PERSONA"))
    f.append(Block.dokumente_block([dok(9)]))
    msgs = f.messages()

    # Nachricht 1 ist der geteilte Anfang: Antrag plus zwei Basisdokumente.
    assert len(msgs) == 2
    praefix_inhalt = msgs[0]["content"]
    assert len(praefix_inhalt) == 3
    assert praefix_inhalt[-1].get("cache_control") == dict(CACHE_CONTROL)
    # Davor und danach steht keiner.
    assert all("cache_control" not in b for b in praefix_inhalt[:-1])
    assert all("cache_control" not in b for b in msgs[1]["content"])


def test_systemprompt_traegt_einen_eigenen_punkt():
    f = basis().fork()
    f.append(Block.user("PERSONA"))
    sysm = f.system()
    assert [b["text"] for b in sysm] == ["ONBOARDING", "BEWERTUNGSLOGIK"]
    assert sysm[-1].get("cache_control") == dict(CACHE_CONTROL)
    assert "cache_control" not in sysm[0]


def test_systemblock_hinter_dem_praefix_wirft():
    """Persona im Systemprompt waere der haeufigste Weg, die Zwischenspeicherung
    still zu verlieren."""
    f = basis().fork()
    with pytest.raises(ValueError, match="Systemprompt"):
        f.append(Block.system("PERSONA"))


# --- Rendern ------------------------------------------------------------------


def test_dokumente_werden_mit_zitaten_gerendert():
    f = basis(1).fork()
    inhalt = f.messages()[0]["content"]
    d = inhalt[1]
    assert d["type"] == "document"
    assert d["citations"] == {"enabled": True}
    assert d["source"]["data"] == "Volltext 0"
    assert d["title"] == "Titel 0"
    assert "corpus/projektlaufwerk/fall/2013/d0.md" in d["context"]


def test_dokumentenreihenfolge_entspricht_dem_zitatindex():
    f = basis(2).fork()
    f.append(Block.user("PERSONA"))
    f.append(Block.dokumente_block([dok(5), dok(6)]))
    doks = f.dokumente()
    assert [d.titel for d in doks] == ["Titel 0", "Titel 1", "Titel 5", "Titel 6"]

    gerendert = [b for m in f.messages() for b in m["content"] if b["type"] == "document"]
    assert [b["title"] for b in gerendert] == [d.titel for d in doks]


def test_unbekannte_blockart_wirft():
    with pytest.raises(ValueError, match="Blockart"):
        Block(art="assistant", inhalt="x")


# --- Ablage -------------------------------------------------------------------


def test_speichern_und_laden_erhalten_den_fingerabdruck(tmp_path):
    b = basis()
    pfad = tmp_path / "lauf" / "basis.json"
    b.speichern(pfad)
    geladen = Kontext.laden(pfad)
    assert geladen.fingerprint() == b.fingerprint()
    assert [d.quelle for d in geladen.dokumente()] == [d.quelle for d in b.dokumente()]
    # Der geladene Kontext ist versiegelt und laesst sich forken.
    geladen.fork().append(Block.user("PERSONA"))


def test_laden_erkennt_einen_veraenderten_praefix(tmp_path):
    pfad = tmp_path / "basis.json"
    basis().speichern(pfad)
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    daten["praefix"][1]["inhalt"] = "ANTRAG, heimlich geaendert"
    pfad.write_text(json.dumps(daten, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="Fingerabdruck"):
        Kontext.laden(pfad)
