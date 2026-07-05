#!/usr/bin/env bash
# Build a self-contained Overleaf upload zip (no symlinks, no build artifacts).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
NAME="conference"
OUT="$ROOT/../${NAME}_overleaf.zip"
STAGE="$(mktemp -d)"

cleanup() { rm -rf "$STAGE"; }
trap cleanup EXIT

echo "Staging Overleaf package..."
rsync -a \
  --exclude='main.pdf' --exclude='main.aux' --exclude='main.log' --exclude='main.blg' --exclude='main.out' --exclude='main.bbl' \
  --exclude='__MACOSX' --exclude='.DS_Store' \
  --exclude='*_Report.md' --exclude='build_overleaf_zip.sh' \
  "$ROOT/" "$STAGE/$NAME/"

# Ensure figure_07 PNG is a real file (not symlink)
FIG_SRC="$ROOT/../../latex/figures/figure_07_node_importance.png"
FIG_DST="$STAGE/$NAME/figures/figure_07_node_importance.png"
if [[ ! -f "$FIG_DST" ]] || [[ -L "$FIG_DST" ]] || [[ $(wc -c < "$FIG_DST") -lt 1000 ]]; then
  cp "$FIG_SRC" "$FIG_DST"
fi

cd "$STAGE"
zip -r "$OUT" "$NAME" -x "*.DS_Store" -x "__MACOSX/*"
echo "Created: $OUT"
unzip -l "$OUT" | grep -E "figure_07|12_References|main.tex"
