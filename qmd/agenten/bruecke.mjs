// Einbettungsbruecke: haelt das Modell im Speicher und antwortet auf Zuruf.
//
// Warum es das gibt: `qmd query` startet je Abfrage einen eigenen Prozess und
// laedt drei Modelle neu, das kostet zwoelf bis fuenfundvierzig Sekunden. Hier
// wird das Einbettungsmodell EINMAL geladen und bleibt; eine Anfrage kostet
// danach die reine Rechenzeit des Modells.
//
// Warum nicht `qmd mcp`: Der MCP-Dienst bietet nur `get`, `multi_get`, `query`
// und `status`. Rohe Einbettungsvektoren, die suche.py fuer eigene Aehnlichkeit
// und den Dedup braucht, liefert er nicht, und `query` faehrt die volle Kette
// samt Reranking, das nach AE-05 abgeschaltet ist.
//
// Protokoll: eine JSON-Zeile hinein, eine JSON-Zeile hinaus. Jede Antwortzeile
// beginnt mit dem Kennzeichen unten. Alles ohne dieses Kennzeichen ist Rauschen
// der Modellbibliothek und wird von suche.py verworfen -- node-llama-cpp
// schreibt Ladehinweise auf stdout, die sonst das Protokoll zerstoeren wuerden.
//
//   -> {"id":1,"op":"embed","texte":["..."]}
//   <- @@QMDBR@@{"id":1,"ok":true,"vektoren":[[...]],"dim":2048}
//   -> {"id":2,"op":"ping"}
//   <- @@QMDBR@@{"id":2,"ok":true,"modell":"hf:NeoRoth/...","geraet":"vulkan"}
//   -> {"id":3,"op":"close"}   beendet den Prozess
//
// Die Praefixe (`query: `) und das abgeschaltete BOS-Token kommen aus dem
// Projektpatch patches/apply.mjs, weil hier dieselben qmd-Funktionen gerufen
// werden wie im regulaeren Suchpfad.

import { createInterface } from "node:readline";
// Direkter Dateipfad statt Paketname: `exports` in package.json von @tobilu/qmd
// gibt `./dist/llm.js` nicht frei (ERR_PACKAGE_PATH_NOT_EXPORTED).
import {
  getDefaultLlamaCpp,
  formatQueryForEmbedding,
  resolveEmbedModel,
  withNativeStdoutRedirectedToStderr,
} from "../node_modules/@tobilu/qmd/dist/llm.js";

const KENNZEICHEN = "@@QMDBR@@";
const MODELL = resolveEmbedModel();

function antworte(objekt) {
  process.stdout.write(KENNZEICHEN + JSON.stringify(objekt) + "\n");
}

const llm = getDefaultLlamaCpp();

async function embed(texte) {
  // Der native Teil der Modellbibliothek schreibt auf stdout. Waehrend des
  // Aufrufs wird das nach stderr umgeleitet; die Protokollzeile schreiben wir
  // erst danach, wenn stdout wieder uns gehoert.
  return await withNativeStdoutRedirectedToStderr(async () => {
    const vektoren = [];
    for (const text of texte) {
      const formatiert = formatQueryForEmbedding(text, MODELL);
      const ergebnis = await llm.embed(formatiert);
      if (!ergebnis || !ergebnis.embedding) {
        throw new Error("Einbettung fehlgeschlagen (embed lieferte null)");
      }
      vektoren.push(ergebnis.embedding);
    }
    return vektoren;
  });
}

const zeilen = createInterface({ input: process.stdin });

for await (const zeile of zeilen) {
  const roh = zeile.trim();
  if (!roh) continue;

  let anfrage;
  try {
    anfrage = JSON.parse(roh);
  } catch {
    antworte({ id: null, ok: false, fehler: "kein gueltiges JSON" });
    continue;
  }

  const id = anfrage.id ?? null;
  try {
    if (anfrage.op === "close") {
      antworte({ id, ok: true, geschlossen: true });
      process.exit(0);
    } else if (anfrage.op === "ping") {
      antworte({
        id,
        ok: true,
        modell: MODELL,
        geraet: process.env.QMD_LLAMA_GPU ?? "auto",
      });
    } else if (anfrage.op === "embed") {
      const texte = anfrage.texte;
      if (!Array.isArray(texte) || texte.some((t) => typeof t !== "string")) {
        throw new Error("Feld 'texte' muss eine Liste von Zeichenketten sein");
      }
      const vektoren = await embed(texte);
      antworte({
        id,
        ok: true,
        vektoren,
        dim: vektoren.length ? vektoren[0].length : 0,
      });
    } else {
      throw new Error("unbekannte Operation: " + String(anfrage.op));
    }
  } catch (fehler) {
    antworte({ id, ok: false, fehler: String(fehler && fehler.message ? fehler.message : fehler) });
  }
}
