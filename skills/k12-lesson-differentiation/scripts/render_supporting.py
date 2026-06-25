#!/usr/bin/env python3
"""Render the two supporting artifacts — Student-Facing Materials and the Teacher Observation
Template — from the SAME master lesson JSON used for the lesson plan.

Both documents are composed almost entirely from the `shared` block (anchor task, problems,
exit ticket, look-fors, vocabulary, misconceptions, sentence frames), so they cannot drift from
the lesson plan. The optional `student_materials` / `observation_template` objects in the JSON
only add titles, instructions, and extra blocks.

Usage:
    python render_supporting.py lesson.json --which both --format both
    python render_supporting.py lesson.json --which worksheet --format html -o worksheet.html
Outputs default to: student_materials.{html,docx}, observation_template.{html,docx}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lesson_common import coerce_shared, expand_from_shared  # noqa: E402


# ------------------------------------------------------------------ document builders
def _meta(shared: dict, extra: str = "") -> str:
    bits = [shared.get("standard_code"), shared.get("grade"), extra]
    return " · ".join(str(b) for b in bits if b)


def _exit_ticket_sort_blocks(shared: dict) -> list[dict]:
    """Sort criteria live in shared.exit_ticket.buckets but the observation template
    previously only named the labels — so a teacher sorting responses in the field had
    no rubric to hand. Surface the per-bucket criteria next to the prompt they apply to."""
    et = (shared or {}).get("exit_ticket") or {}
    rows = [
        [b.get("label", ""), b.get("criteria") or b.get("description") or ""]
        if isinstance(b, dict) else [str(b), ""]
        for b in (et.get("buckets") or [])
    ]
    if not rows:
        return [{"type": "paragraph", "text": "(no exit-ticket sort criteria defined)"}]
    blocks: list[dict] = []
    if et.get("prompt"):
        blocks.append({"type": "callout", "kind": "student-task", "label": "Exit-ticket prompt",
                       "text": et["prompt"]})
    blocks.append({"type": "table", "headers": ["Sort bucket", "What this looks like"],
                   "rows": rows})
    return blocks


import re  # noqa: E402

_INLINE_CHOICES = re.compile(r"\s+(?=\*{0,2}[A-F]\)\s)")


def _default_workspace(shared: dict, has_choices: bool) -> int:
    """Per-problem work space. SME guidance (Sofia, 6/2 audit): students need roughly a third
    of a page to show their thinking on each problem, more in early grades. Grade-banded
    defaults; any problem can override with `work_space_pt`."""
    if has_choices:
        return 60  # choices carry the answer; box is for showing work
    g = str(shared.get("grade", "")).lower()
    m = re.search(r"\d+", g)
    if "kind" in g or g.strip() == "k":
        n = 0
    elif m and not any(w in g for w in ("algebra", "geometry", "calculus", "statistics")):
        n = int(m.group(0))
    else:
        n = 9  # named HS courses and unparseable grades
    return 170 if n <= 2 else 150 if n <= 5 else 120


def _problem_blocks(i: int, p: dict, shared: dict) -> list[dict]:
    """One practice problem -> blocks. Multiple-choice options go on their own lines."""
    text = str(p.get("text", ""))
    choices = p.get("choices") or []
    if not choices and len(_INLINE_CHOICES.split(text)) >= 3:
        # Defensive: the model inlined "A) ... B) ... C) ..." inside the text — split it out.
        parts = _INLINE_CHOICES.split(text)
        text, choices = parts[0], [re.sub(r"^\*{0,2}[A-F]\)\s*", "", c).strip(" *") for c in parts[1:]]
    blocks: list[dict] = [{"type": "labeled", "label": f"{i}", "text": text}]
    if choices:
        letters = "ABCDEF"
        blocks.append({"type": "bullets",
                       "items": [f"**{letters[j]})**  {c}" for j, c in enumerate(choices[:6])]})
    blocks.append({"type": "answer_box",
                   "height_pt": p.get("work_space_pt", _default_workspace(shared, bool(choices)))})
    # Keep each problem's prompt, choices, and workspace on the same page.
    return [{"type": "group", "blocks": blocks}]


def _doc_eyebrow(data: dict, shared: dict, label: str) -> str:
    """Supporting-document eyebrow. Prefer the lesson's own grade/subject; fall
    back to the lesson plan's eyebrow lead segment. NEVER default the subject —
    a hardcoded "Mathematics" stamped ELA/science student pages and contradicted
    the plan's header."""
    bits = [str(x) for x in (shared.get("grade", ""), shared.get("subject", "")) if x]
    if bits:
        return " ".join(bits).strip() + f" · {label}"
    lead = str(data.get("eyebrow", "")).split("·")[0].strip()
    return f"{lead} · {label}" if lead else label


def build_worksheet_doc(data: dict) -> dict:
    shared = coerce_shared(data.get("shared", {}))
    sm = data.get("student_materials", {}) or {}
    if not isinstance(sm, dict):
        sm = {}
    title = sm.get("title") or data.get("title", "Student Materials")
    problems = shared.get("problems", [])
    # Section headings are overridable so non-math subjects can rename them
    # (e.g. practice -> "Text-dependent questions" for ELA, "Investigation" for science).
    headings = {"warmup": "Warm up together", "practice": "Practice problems",
                "exit": "Show what you know"}
    headings.update(sm.get("headings") or {})

    practice_blocks: list[dict] = []
    if sm.get("instructions"):
        practice_blocks.append({"type": "callout", "kind": "student-note", "label": "Remember",
                                "text": sm["instructions"]})
    if shared.get("sentence_frames"):
        practice_blocks.append({"type": "list", "label": "Sentence frames",
                                "items": [f"*{s}*" for s in shared["sentence_frames"]]})
    for i, p in enumerate(problems, 1):
        practice_blocks.extend(_problem_blocks(i, p if isinstance(p, dict) else {"text": p}, shared))
    if sm.get("exit_ticket_own_page"):
        # Break BEFORE the next section so its bar starts the new page (never stranded).
        practice_blocks.append({"type": "page_break"})

    ref_blocks = sm.get("reference_blocks")
    sections = [
        {"heading": headings["warmup"], "color": "green", "blocks": [
            {"type": "group", "blocks": expand_from_shared("anchor_task", shared, "student")
             + [{"type": "answer_box", "height_pt": 110}]}]},
    ]
    if ref_blocks:
        sections.append({"heading": sm.get("reference_heading", "Reference"),
                         "color": "teal", "blocks": ref_blocks})
    sections += [
        {"heading": headings["practice"], "color": "blue", "blocks": practice_blocks},
        {"heading": headings["exit"], "color": "amber", "blocks": [
            {"type": "group", "blocks": expand_from_shared("exit_ticket", shared, "student")
             + [{"type": "answer_box", "height_pt": 140}]}]},
    ]

    theme = dict(data.get("theme") or {})
    theme.setdefault("body_size", 11.5)  # student-facing: larger type
    return {
        "audience": "student",
        "eyebrow": sm.get("eyebrow") or _doc_eyebrow(data, shared, "Student Materials"),
        "title": title,
        "meta": "Name: ____________________    Date: ____________    Partner: ____________________",
        "theme": theme,
        "shared": shared,
        "sections": sections,
        "footer_note": sm.get("footer_note") or _meta(shared, title),
    }


def build_observation_doc(data: dict) -> dict:
    shared = coerce_shared(data.get("shared", {}))
    ob = data.get("observation_template", {}) or {}
    if not isinstance(ob, dict):
        ob = {}
    look_fors = shared.get("look_fors", [])
    columns = ob.get("columns") or ["Strategies Seen", "Misconceptions Seen"]

    lookfor_rows = [[lf.get("name", ""),
                     f"{lf.get('what_it_means', '')} **Move:** {lf.get('teacher_move', '')}", ""]
                    for lf in look_fors]
    def _row_count(val, default: int) -> int:
        # blank_rows / tracker_rows are row COUNTS — but models sometimes write a list of
        # labels here; never crash on that, just fall back to the default count.
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    # Blank rows must match the (overridable) column count — a 3-column override used to get
    # 2-cell rows, which rendered as a broken grid (SME-flagged formatting issue).
    blank_rows = [[""] * len(columns) for _ in range(_row_count(ob.get("blank_rows"), 6))]
    # Pre-selection table: seed one row per look-for so the teacher selects work that
    # surfaces each strategy; share order is theirs to fill during Explore.
    preselect_rows = [["", lf.get("name", ""), ""] for lf in look_fors] or [["", "", ""]]
    tracker_rows = [["", "", "", ""] for _ in range(_row_count(ob.get("tracker_rows"), 12))]

    sections = [
        {"heading": "How to use", "color": "green", "blocks": [
            {"type": "paragraph", "text": ob.get(
                "instructions",
                "Circulate during Explore and partner work. Tally or jot student initials next to "
                "each look-for; capture strategies and misconceptions in the grid below; pre-select "
                "and sequence student work for the Discuss phase; track individual students for "
                "the exit-ticket sort.")}]},
        {"heading": "Look-fors", "color": "blue", "blocks": [
            {"type": "table",
             "headers": ["Look-for", "What it tells you / teacher move", "Students observed · notes"],
             "rows": lookfor_rows}]},
        {"heading": "Strategies & misconceptions observed", "color": "amber", "blocks": [
            {"type": "table", "headers": columns, "rows": blank_rows},
            {"type": "subheading", "text": "Quick reference: anticipated misconceptions"},
        ] + expand_from_shared("misconceptions", shared, "teacher")},
        {"heading": "Pre-selection: choosing & sequencing student work for Discuss",
         "color": "purple", "blocks": [
            {"type": "paragraph",
             "text": "While circulating, select the student work to share in Discuss and decide "
                     "the share order (typically concrete to abstract, or misconception to "
                     "resolution)."},
            {"type": "table",
             "headers": ["Share order", "Student / work selected", "Why share it (strategy or "
                         "idea it surfaces)"],
             "rows": preselect_rows}]},
        {"heading": "Per-student tracker", "color": "teal", "blocks": [
            {"type": "paragraph",
             "text": "One row per student observed. Use the last column for the exit-ticket "
                     "sort (Got it / Almost there / Needs re-teaching)."},
            {"type": "table",
             "headers": ["Student name", "Strategies / look-fors seen", "Evidence",
                         "Exit-ticket sort"],
             "rows": tracker_rows}]},
        {"heading": "Exit-ticket sort criteria", "color": "teal",
         "blocks": _exit_ticket_sort_blocks(shared)},
    ]
    if ob.get("extra_blocks"):
        sections.append({"heading": ob.get("extra_heading", "Notes"), "color": "teal",
                         "blocks": ob["extra_blocks"]})

    return {
        "audience": "teacher",
        "eyebrow": "Teacher Observation Template",
        "title": ob.get("title") or f"{data.get('title', 'Lesson')} — Observation",
        "meta": _meta(shared, "Date: ____________"),
        "theme": data.get("theme") or {},
        "shared": shared,
        "sections": sections,
        "footer_note": ob.get("footer_note", ""),
    }


# ------------------------------------------------------------------ rendering
def render_doc(doc: dict, stem: str, fmt: str, outdir: Path) -> list[str]:
    written = []
    if fmt in ("html", "both"):
        from render_lesson_html import render as render_html
        path = outdir / f"{stem}.html"
        path.write_text(render_html(doc), encoding="utf-8")
        written.append(str(path))
    if fmt in ("docx", "both"):
        from render_lesson_docx import render as render_docx
        path = outdir / f"{stem}.docx"
        render_docx(doc, str(path))
        written.append(str(path))
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="master lesson JSON")
    ap.add_argument("--which", choices=["worksheet", "observation", "both"], default="both")
    ap.add_argument("--format", choices=["html", "docx", "both"], default="html")
    ap.add_argument("--outdir", default=None,
                    help="output directory (default: alongside the input JSON)")
    args = ap.parse_args()

    input_path = Path(args.input)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    outdir = Path(args.outdir) if args.outdir else input_path.resolve().parent
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    if args.which in ("worksheet", "both"):
        written += render_doc(build_worksheet_doc(data), "student_materials", args.format, outdir)
    if args.which in ("observation", "both"):
        written += render_doc(build_observation_doc(data), "observation_template", args.format, outdir)
    print("wrote " + ", ".join(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
