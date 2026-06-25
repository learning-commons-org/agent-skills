#!/usr/bin/env bash
# Render all three HTML previews (lesson plan, student materials, observation template)
# from one lesson.json in a single invocation. Fail-fast: any renderer error stops the run.
#
# Usage: bash scripts/render_all.sh lesson.json "$OUTPUT_DIR"
set -euo pipefail

json="${1:?usage: render_all.sh LESSON_JSON OUTPUT_DIR}"
outdir="${2:?usage: render_all.sh LESSON_JSON OUTPUT_DIR}"
here="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$outdir"
python "$here/render_lesson_html.py" "$json" -o "$outdir/lesson_plan_preview.html"
python "$here/render_supporting.py" "$json" --which both --format html --outdir "$outdir"
