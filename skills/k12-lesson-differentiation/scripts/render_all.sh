#!/usr/bin/env bash
# Render all four HTML previews (teacher plan + three tier worksheets) from one
# differentiation.json in a single invocation. Fail-fast: any renderer error stops the run.
#
# Usage: bash scripts/render_all.sh differentiation.json "$OUTPUT_DIR"
set -euo pipefail

json="${1:?usage: render_all.sh DIFFERENTIATION_JSON OUTPUT_DIR}"
outdir="${2:?usage: render_all.sh DIFFERENTIATION_JSON OUTPUT_DIR}"
here="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$outdir"
python "$here/render_documents.py" "$json" --format html --outdir "$outdir"
