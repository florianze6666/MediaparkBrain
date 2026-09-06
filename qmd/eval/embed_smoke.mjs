// Rauchtest fuer das Embedding-Modell, unabhaengig vom QMD-Index.
//
// Prueft direkt ueber node-llama-cpp (dieselbe Bibliothek, die QMD benutzt):
//   1. das GGUF laedt auf dem gewaehlten Geraet (GPU automatisch, --cpu erzwingt CPU)
//   2. Vektorlaenge, Pooling, Trainingskontext
//   3. BOS-Verhalten des Tokenizers (Nemotron-3-Embed ist ohne <s> trainiert)
//   4. Semantik: passende Frage/Passage-Paare liegen deutlich ueber unpassenden
//   5. Tempo pro Einbettung
//
// Aufruf aus qmd/:   node eval\embed_smoke.mjs [--cpu] [--model <pfad.gguf>]
// Exit-Code 1, wenn eine Pruefung faellt.

import { getLlama, LlamaLogLevel } from "node-llama-cpp";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const QMD_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const cpu = args.includes("--cpu");
const modelArg = args.includes("--model") ? args[args.indexOf("--model") + 1] : null;

function modelPathFromConfig() {
    const yml = join(QMD_DIR, ".qmd", "index.yml");
    const m = existsSync(yml) ? readFileSync(yml, "utf-8").match(/^\s*embed:\s*(\S+)/m) : null;
    const uri = m?.[1] ?? process.env.QMD_EMBED_MODEL ?? "";
    // QMD legt hf:<owner>/<repo>/<datei> als hf_<owner>_<datei> im Modellcache ab.
    const hf = uri.match(/^hf:([^/]+)\/[^/]+\/(.+)$/);
    if (hf) return join(QMD_DIR, ".cache", "qmd", "models", `hf_${hf[1]}_${hf[2]}`);
    return uri;
}

const modelPath = modelArg ?? modelPathFromConfig();
if (!existsSync(modelPath)) {
    console.error(`Modell nicht gefunden: ${modelPath}`);
    process.exit(2);
}

const PAIRS = {
    queries: {
        q_glaswerk: "query: Warum ist beim Projekt Glaswerk Nord die Marge verloren gegangen?",
        q_zeiterfassung: "query: Welche Regeln gelten fuer die Zeiterfassung der Mitarbeiter?",
        q_budget: "query: Gibt es Sonderfreigaben ausserhalb des Investitionsbudgets?",
    },
    passages: {
        p_glaswerk: "passage: Kalkuliert und ausgelegt haben wir auf 420 °C am Auskoppelpunkt als Dauerwert. "
            + "Diese Angabe kam aus einem Gespräch mit der Betriebsleitung des Kunden. Gemessen wurden im "
            + "Mittel 348 °C, der kalkulierte Deckungsbeitrag ist damit aufgezehrt.",
        p_zeiterfassung: "passage: Die Betriebsvereinbarung regelt die Nutzung des Zeiterfassungssystems und "
            + "die Auswertung personenbezogener Daten durch den Arbeitgeber.",
        p_budget: "passage: Der Investitionsrahmen für 2027 sieht keine Sonderfreigaben außerhalb des "
            + "genehmigten Budgets vor; Ausnahmen entscheidet die Geschäftsführung.",
    },
};
// Erwartung: jede Frage findet ihre eigene Passage (gleicher Suffix) als beste.
const EXPECT = { q_glaswerk: "p_glaswerk", q_zeiterfassung: "p_zeiterfassung", q_budget: "p_budget" };

const cos = (a, b) => {
    let dot = 0, na = 0, nb = 0;
    for (let i = 0; i < a.length; i++) { dot += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i]; }
    return dot / (Math.sqrt(na) * Math.sqrt(nb));
};

let failures = 0;
const check = (ok, msg) => { console.log(`${ok ? "OK " : "FEHLER"}  ${msg}`); if (!ok) failures++; };

const llama = await getLlama({ gpu: cpu ? false : "auto", logLevel: LlamaLogLevel.error });
console.log(`Geraet: ${llama.gpu === false ? "CPU" : "GPU " + llama.gpu}` + (llama.gpu !== false ? ` (${(await llama.getVramState()).total / 2 ** 30 | 0} GB VRAM)` : ` (${llama.cpuMathCores} Rechenkerne)`));
console.log(`Modell: ${modelPath}`);

const t0 = Date.now();
const model = await llama.loadModel({ modelPath });
console.log(`Geladen in ${Date.now() - t0} ms`);
check(model.embeddingVectorSize === 2048, `Vektorlaenge ${model.embeddingVectorSize} (erwartet 2048)`);
console.log(`Trainingskontext: ${model.trainContextSize}, Vokabular: ${model.vocabularyType}`);

// BOS: llama.cpp haelt den Pixtral-Pre-Tokenizer fuer BOS-pflichtig. Das HF-Referenzmodell
// (sentence-transformers) setzt kein <s>. QMD schaltet das per Patch ab; hier wird beides gemessen.
const bosDefault = model.tokens.shouldPrependBosToken;
console.log(`BOS-Vorgabe des GGUF/llama.cpp: ${bosDefault}`);

const ctx = await model.createEmbeddingContext({ contextSize: 2048 });
async function embedAll(texts) {
    const out = {};
    for (const [k, v] of Object.entries(texts)) out[k] = Array.from((await ctx.getEmbeddingFor(v)).vector);
    return out;
}

const t1 = Date.now();
const withBos = { ...(await embedAll(PAIRS.queries)), ...(await embedAll(PAIRS.passages)) };
const n = Object.keys(withBos).length;
console.log(`Tempo: ${((Date.now() - t1) / n).toFixed(0)} ms je Einbettung (${n} Texte, mit BOS=${bosDefault})`);

model.tokens._shouldPrependBosToken = false;
const noBos = { ...(await embedAll(PAIRS.queries)), ...(await embedAll(PAIRS.passages)) };
check(model.tokens.shouldPrependBosToken === false, "BOS abschaltbar ueber tokens._shouldPrependBosToken (QMD-Patch verlaesst sich darauf)");

const norm = (v) => Math.sqrt(v.reduce((s, x) => s + x * x, 0));
console.log(`L2-Norm (ohne BOS): ${norm(noBos.q_glaswerk).toFixed(4)}`);

let minSame = 1;
for (const k of Object.keys(withBos)) minSame = Math.min(minSame, cos(withBos[k], noBos[k]));
console.log(`Kosinus mit/ohne BOS, Minimum ueber ${n} Texte: ${minSame.toFixed(4)}`);

console.log("\nKosinus Frage x Passage (ohne BOS, wie HF-Referenz):");
const pk = Object.keys(PAIRS.passages);
console.log("".padEnd(18) + pk.map(p => p.padStart(16)).join(""));
for (const q of Object.keys(PAIRS.queries)) {
    const row = pk.map(p => cos(noBos[q], noBos[p]));
    console.log(q.padEnd(18) + row.map(x => x.toFixed(3).padStart(16)).join(""));
    const best = pk[row.indexOf(Math.max(...row))];
    const sorted = [...row].sort((a, b) => b - a);
    check(best === EXPECT[q] && sorted[0] - sorted[1] >= 0.05,
        `${q}: beste Passage ${best}, Abstand zur zweiten ${(sorted[0] - sorted[1]).toFixed(3)} (erwartet ${EXPECT[q]}, Abstand >= 0.05)`);
}

await ctx.dispose();
await model.dispose();
await llama.dispose();
console.log(failures ? `\n${failures} Pruefung(en) gefallen.` : "\nAlle Pruefungen bestanden.");
process.exit(failures ? 1 : 0);
