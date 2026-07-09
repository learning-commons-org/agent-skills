#!/usr/bin/env bash
# Copyright 2026 Anthropic, PBC
# Copyright 2026 Learning Commons
# SPDX-License-Identifier: Apache-2.0

# Render every document in lesson.json (lesson plan, student materials, observation, and any
# others the model authored) from one material-source JSON. It holds a `documents[]` array;
# each entry's `id` becomes the output filename. Writes editable .docx (the teacher
# deliverable) and an .html twin of each (harness graders read the twin).
# Fail-fast: any renderer error stops the run.
#
# Usage: bash scripts/render_all.sh lesson.json "$OUTPUT_DIR"
set -euo pipefail

json="${1:?usage: render_all.sh LESSON_JSON OUTPUT_DIR}"
outdir="${2:?usage: render_all.sh LESSON_JSON OUTPUT_DIR}"
here="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$outdir"
# python-docx powers the .docx output; the .html twins render without it. If the install
# can't complete (offline container), render html now so the twins always exist.
if ! python -c "import docx" 2>/dev/null; then
  pip install -q "python-docx==1.1.2" || true
fi
if python -c "import docx" 2>/dev/null; then
  python "$here/render_documents.py" "$json" --format both --outdir "$outdir"
else
  # Render the html twins so graders have something, then fail loudly: the teacher's
  # .docx deliverables could not be produced.
  python "$here/render_documents.py" "$json" --format html --outdir "$outdir"
  echo "error: python-docx could not be installed — no .docx deliverables were produced" >&2
  exit 1
fi
# Preserve the legacy primary-artifact filename so downstream evals/reports keep working.
if [ -f "$outdir/lesson_plan.html" ] && [ ! -f "$outdir/lesson_plan_preview.html" ]; then
  cp "$outdir/lesson_plan.html" "$outdir/lesson_plan_preview.html"
fi
# Persist the source JSON alongside the rendered artifacts so the harness
# captures it (artifacts_count is patched to ignore *.json and *.html).
cp "$json" "$outdir/lesson.json" 2>/dev/null || true

# Delivery guarantee: when $OUTPUT_DIR is set and the render went elsewhere
# (a staging dir like /tmp/out), mirror EVERYTHING into $OUTPUT_DIR too.
# Downstream tooling reads the .html twins and lesson.json from $OUTPUT_DIR;
# hand-copying a subset there is the failure this removes.
if [ -n "${OUTPUT_DIR:-}" ] && [ "$(cd "$outdir" && pwd)" != "$(mkdir -p "$OUTPUT_DIR" && cd "$OUTPUT_DIR" && pwd)" ]; then
  cp -R "$outdir"/. "$OUTPUT_DIR"/
fi
