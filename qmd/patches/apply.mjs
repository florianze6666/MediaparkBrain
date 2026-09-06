// Patch fuer @tobilu/qmd 2.8.3: Nemotron-3-Embed als Embedding-Modell.
//
// QMD kennt zwei Prompt-Formate fuer Embeddings, embeddinggemma/nomic
// ("task: search result | query: ...") und Qwen3-Embedding. Nemotron-3-Embed
// (nvidia/Nemotron-3-Embed-1B) verlangt die Praefixe "query: " und "passage: "
// und wurde ohne BOS-Token trainiert; llama.cpp setzt fuer dessen
// Pixtral-Tokenizer aber standardmaessig ein <s> voran. Beides wird hier in
// node_modules/@tobilu/qmd/dist/llm.js nachgezogen.
//
// Der Patch ist idempotent und laeuft als npm-postinstall, damit ein
// erneutes "npm install" ihn nicht verliert. Von Hand:
//     node patches\apply.mjs          # anwenden
//     node patches\apply.mjs --check  # nur pruefen, Exit 1 wenn nicht angewandt

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const QMD_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const TARGET = join(QMD_DIR, "node_modules", "@tobilu", "qmd", "dist", "llm.js");
const MARKER = "isNemotronEmbedModel";
const check = process.argv.includes("--check");

const EDITS = [
    {
        name: "Erkennung des Modells",
        anchor: `export function isQwen3EmbeddingModel(modelUri) {
    return /qwen.*embed/i.test(modelUri) || /embed.*qwen/i.test(modelUri);
}`,
        insert: `
/**
 * Detect Nemotron-3-Embed (nvidia). Prefixes "query: " / "passage: ", no BOS.
 * Projektpatch MediaparkBrain, siehe patches/apply.mjs.
 */
export function isNemotronEmbedModel(modelUri) {
    return /nemotron.*embed/i.test(modelUri) || /embed.*nemotron/i.test(modelUri);
}`,
    },
    {
        name: "Query-Praefix",
        anchor: `export function formatQueryForEmbedding(query, modelUri) {
    const uri = modelUri ?? resolveEmbedModel();`,
        insert: `
    if (isNemotronEmbedModel(uri)) {
        return "query: " + query;
    }`,
    },
    {
        name: "Passage-Praefix",
        anchor: `export function formatDocForEmbedding(text, title, modelUri) {
    const uri = modelUri ?? resolveEmbedModel();`,
        insert: `
    if (isNemotronEmbedModel(uri)) {
        // Nemotron-3-Embed: "passage: " prefix, title as first line when present
        return title ? "passage: " + title + "\\n" + text : "passage: " + text;
    }`,
    },
    {
        name: "BOS abschalten",
        anchor: `            const model = await llama.loadModel(this.modelLoadOptions(modelPath));
            this.embedModel = model;`,
        insert: `
            if (isNemotronEmbedModel(this.embedModelUri)) {
                // Nemotron-3-Embed ist ohne <s> trainiert (sentence-transformers). llama.cpp
                // haelt den Pixtral-Tokenizer fuer BOS-pflichtig; hier wie die Referenz.
                model.tokens._shouldPrependBosToken = false;
            }`,
    },
];

let src = readFileSync(TARGET, "utf-8");
const applied = src.includes(MARKER);

if (check) {
    const complete = applied && EDITS.every(e => src.includes(e.insert.trim()));
    console.log(complete ? "Patch ist angewandt: " + TARGET : "Patch FEHLT in " + TARGET);
    process.exit(complete ? 0 : 1);
}
if (applied) {
    console.log("Patch bereits angewandt, nichts zu tun.");
    process.exit(0);
}

for (const e of EDITS) {
    if (!src.includes(e.anchor)) {
        console.error(`Anker fuer "${e.name}" nicht gefunden. Ist @tobilu/qmd noch 2.8.3? Patch abgebrochen, Datei unveraendert.`);
        process.exit(1);
    }
    src = src.replace(e.anchor, e.anchor + e.insert);
}
writeFileSync(TARGET, src, "utf-8");
console.log(`Patch angewandt (${EDITS.length} Stellen): ${TARGET}`);
