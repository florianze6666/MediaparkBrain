#!/usr/bin/env bash
# Holt den aktuellen Korpus der Demo-Firma (LTT) und legt ihn unter data/ ab.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
git clone -q --depth 1 https://github.com/Eckhard-Siegmann/startplatz_hackathon.git "$TMP/ref"
rsync -a --exclude '.DS_Store' "$TMP/ref/corpus/" "$ROOT/data/drive/"
rsync -a --exclude '.DS_Store' "$TMP/ref/canon/" "$ROOT/data/canon/"
cp "$TMP/ref/source/Fikive_Geschäftsentwicklung.md" "$ROOT/data/canon/00_Unternehmenschronik.md"
cp "$TMP/ref/LICENSE" "$ROOT/data/LICENSE-democompany.txt"
SHA=$(git -C "$TMP/ref" rev-parse HEAD); DATE=$(git -C "$TMP/ref" log -1 --format=%ci)
sed -i '' -e "s/^- Commit: .*/- Commit: $SHA/" -e "s/^- Stand: .*/- Stand: $DATE/" "$ROOT/data/DEMOCOMPANY-SOURCE.md"
rm -rf "$TMP"
echo "Demo-Firma aktualisiert auf $SHA ($DATE)"
