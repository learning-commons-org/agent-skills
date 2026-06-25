#!/usr/bin/env python3
"""Render lesson JSON -> a styled, self-contained HTML preview (the teacher-facing view).

Design-system spec (Figma "Artifact visual design principles", Jun 2026):
  - Minimal color. Callouts are distinguished by an icon prefix, not background fill, so they
    survive B+W printing. Student worksheets avoid color entirely.
  - Horizontal rule above each H1 section; no colored section bars.
  - Bullets over paragraphs wherever possible.
  - Shorter student tasks may use a 2-column layout to save pages.
  - Student worksheets follow: task -> instructions -> reminders -> workspace.

Block types (canonical names; legacy aliases accepted, see ALIASES in lesson_common):
  paragraph, labeled, list, h2, h3, callout, table, cards, columns, group, page_break,
  phase_header, fill_in, instructions, workspace, checklist

Usage:
    python render_lesson_html.py lesson.json -o lesson_preview.html
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lesson_common import (  # noqa: E402
    DEFAULT_THEME, Theme, CALLOUT_KINDS,
    btype as _btype, resolve_callout_kind as _resolve_callout_kind,
    answer_profile, expand_document, build_header, preamble_blocks,
    workspace_height, normalize_text, label_text, label_sep, table_row_height,
)

FILL_IN_SIZES = {"short": "6em", "med": "14em", "long": "100%"}


def md(text) -> str:
    t = escape(normalize_text(text), quote=True)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", t)
    # Preserve line structure: text fields use \n for meaningful line breaks (sub-parts,
    # multi-paragraph callouts). Collapsing them produced unreadable prose blobs.
    t = re.sub(r"[ \t]*\n[ \t]*", "<br>", t)
    return t


def answer_space(blk: dict, theme) -> str:
    """Open writing space — blank whitespace, or ruled lines for lower-grade prose."""
    h = workspace_height(blk, theme)
    if blk.get("ruled", theme.answer_gap is not None):
        gap = float(theme.answer_gap or 22)
        n = max(2, int(round(h / gap)))
        lines = f"<div class=\"ansline\" style=\"height:{gap:g}pt\"></div>" * n
        return f"<div class=\"ans\">{lines}</div>"
    return f"<div class=\"ans\" style=\"height:{h:g}pt\"></div>"


def css(theme: Theme) -> str:
    """All styling lives in theme.css (next to this script) so the designer can edit it
    directly. CSS custom properties carry the few themeable values."""
    css_path = Path(__file__).resolve().parent / "theme.css"
    base = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    if not base:
        print(f"warning: {css_path} not found — output will be unstyled", file=sys.stderr)
    try:
        title_size = float(theme.raw.get("title_size", DEFAULT_THEME["title_size"]))
    except (TypeError, ValueError):
        title_size = DEFAULT_THEME["title_size"]
    try:
        body_size = float(theme.raw.get("body_size", DEFAULT_THEME["body_size"]))
    except (TypeError, ValueError):
        body_size = DEFAULT_THEME["body_size"]
    root = (":root{"
            f"--primary:{theme.safe('primary')};--title-color:{theme.safe('title_color')};"
            f"--text:{theme.safe('text')};--muted:{theme.safe('muted')};"
            f"--rule:{theme.safe('rule')};--border:{theme.safe('border')};"
            f"--title-size:{title_size}pt;--body-size:{body_size}pt"
            "}")
    return root + "\n" + base


def render_block(blk: dict, theme: Theme) -> str:
    t = _btype(blk)
    if t == "paragraph":
        return f"<p>{md(blk.get('text', ''))}</p>"
    if t == "labeled":
        lbl = label_text(blk)
        return f"<p><b>{md(lbl)}{label_sep(lbl)}</b> {md(blk.get('text', ''))}</p>"
    if t == "h2":
        return f"<div class=\"h2\">{md(blk.get('text', ''))}</div>"
    if t == "h3":
        return f"<div class=\"h3\">{md(blk.get('text', ''))}</div>"
    if t == "instructions":
        return f"<p class=\"instr\">{md(blk.get('text', ''))}</p>"
    if t in ("list", "checklist"):
        cls = ' class="check"' if t == "checklist" else ""
        tag = "ol" if blk.get("ordered") else "ul"
        items = "".join(f"<li>{md(i)}</li>" for i in blk.get("items", []))
        head = (f"<p class=\"listlabel\"><b>{md(label_text(blk))}</b></p>"
                if blk.get("label") else "")
        return f"{head}<{tag}{cls}>{items}</{tag}>"
    if t == "callout":
        # Models sometimes write "body"/"content" for the content key — tolerate rather than
        # silently rendering an empty box.
        text = blk.get("text") or blk.get("body") or blk.get("content") or ""
        kind = _resolve_callout_kind(blk)
        icon, klass = CALLOUT_KINDS[kind]
        label = label_text(blk)
        head = (f"<div class=\"co-label\"><span class=\"co-icon\">{icon}</span>"
                f"<b>{md(label)}</b></div>" if label
                else f"<div class=\"co-label\"><span class=\"co-icon\">{icon}</span></div>")
        body = f"<p style=\"margin:0\">{md(text)}</p>" if text else ""
        return f"<div class=\"co {klass}\">{head}{body}</div>"
    if t == "cards":
        items = [c if isinstance(c, dict) else {"title": str(c), "text": ""}
                 for c in blk.get("items", [])]
        cards = "".join(
            "<div class=\"card\">"
            f"<div class=\"card-title\">{md(c.get('title', ''))}</div>"
            f"<div class=\"card-body\">{md(c.get('text', ''))}</div></div>"
            for c in items)
        return f"<div class=\"cards\">{cards}</div>"
    if t == "fill_in":
        size = FILL_IN_SIZES.get(str(blk.get("size", "med")).lower(), FILL_IN_SIZES["med"])
        line = f"<span class=\"fillin\" style=\"width:{size}\"></span>"
        if blk.get("label"):
            return f"<p class=\"fillin-row\"><b>{md(label_text(blk))}:</b> {line}</p>"
        return f"<p class=\"fillin-row\">{line}</p>"
    if t == "phase_header":
        mins = blk.get("minutes")
        right = f"<span class=\"mins\">{md(mins)} min</span>" if mins is not None else ""
        return (f"<div class=\"h2 phase\"><span>{md(blk.get('name', ''))}</span>"
                f"{right}</div>")
    if t == "group":
        inner = "".join(render_block(b, theme) for b in blk.get("blocks", []))
        return f"<div style=\"page-break-inside:avoid\">{inner}</div>"
    if t == "workspace":
        return answer_space(blk, theme)
    if t == "labeled_box":
        label = md(label_text(blk))
        head = f"<p class=\"listlabel\"><b>{label}</b></p>" if label else ""
        return f"{head}{answer_space(blk, theme)}"
    if t == "page_break":
        return "<hr class=\"pagebreak\">"
    if t == "table":
        headers = blk.get("headers") or []
        head = ""
        if headers:
            head = ("<tr>" + "".join(f"<th>{md(str(h).rstrip(': '))}</th>" for h in headers)
                    + "</tr>")
        rows = []
        for r in blk.get("rows", []):
            full_blank = not any(str(c).strip() for c in r)
            row_h = table_row_height(blk, theme, full_blank=full_blank)
            cells = []
            for c in r:
                style = ""
                if not str(c).strip():  # td height acts as a minimum; the row still grows
                    style = f" style=\"height:{row_h:g}pt\""
                cells.append(f"<td{style}>{md(c)}</td>")
            rows.append("<tr>" + "".join(cells) + "</tr>")
        klass = " class=\"headless\"" if not headers else ""
        return f"<table{klass}>{head}{''.join(rows)}</table>"
    if t == "columns":
        left = "".join(render_block(b, theme) for b in blk.get("left", []))
        right = "".join(render_block(b, theme) for b in blk.get("right", []))
        return f"<div class=\"cols\"><div>{left}</div><div>{right}</div></div>"
    # NEVER dump raw JSON into the page — a printed worksheet with {"type": ...} on it is a
    # blocking print-safety failure (caught in eval 6/2; "list" and "labeled_box" in the wild).
    if blk.get("text"):
        return f"<p>{md(blk.get('text'))}</p>"
    if blk.get("items"):
        return "<ul>" + "".join(f"<li>{md(i)}</li>" for i in blk.get("items", [])) + "</ul>"
    # Unknown type with no renderable content: emit nothing. (No debug comment — the type
    # string is model-controlled and could contain "-->" to break out of an HTML comment.)
    return ""


def render(data: dict) -> str:
    data = expand_document(data, data.get("audience", "teacher"))
    theme = Theme(data.get("theme"))
    theme.answer_height, theme.answer_gap, theme.answer_row = answer_profile(data)
    theme.student_doc = data.get("audience") == "student"
    hdr = build_header(data)
    out = ["<div class=\"hdr\">"]
    if hdr["eyebrow"]:
        out.append(f"<div class=\"eyebrow\">{md(hdr['eyebrow'])}</div>")
    out.append(f"<div class=\"title\">{md(hdr['title'])}</div>")
    if hdr["meta"]:
        out.append(f"<div class=\"meta\">{md(hdr['meta'])}</div>")
    out.append("</div>")
    if hdr["name_line"]:
        out.append(f"<p style=\"margin:6pt 0 22pt\">{md(hdr['name_line'])}</p>")

    for blk in preamble_blocks(data):
        out.append(render_block(blk, theme))

    LIGHT_TYPES = {"paragraph", "labeled", "list", "checklist", "h2", "h3", "callout",
                   "instructions"}
    HEAVY_TYPES = {"group", "workspace", "labeled_box"}
    for section in data.get("sections", []):
        h1 = (f"<div class=\"h1\"><span>{md(str(section.get('heading', '')).rstrip(': '))}"
              "</span></div>")
        # The section heading + leading light blocks + the first atomic item
        # (group/workspace) print as one unbreakable unit, so an instructions box never
        # strands above a page break while its first problem starts the next page.
        blocks = list(section.get("blocks", []))
        unit = [h1]
        glued = 0
        while blocks and glued < 4 and _btype(blocks[0]) in LIGHT_TYPES:
            unit.append(render_block(blocks.pop(0), theme))
            glued += 1
        if blocks and _btype(blocks[0]) in HEAVY_TYPES:
            unit.append(render_block(blocks.pop(0), theme))
        if len(unit) > 1:
            out.append("<div style=\"page-break-inside:avoid\">" + "".join(unit) + "</div>")
        else:
            out.append(h1)
        for blk in blocks:
            out.append(render_block(blk, theme))

    if data.get("footer_note"):
        out.append(f"<div class=\"footer\">{md(data['footer_note'])}</div>")

    title = escape(str(data.get("title", "Lesson Plan")), quote=True)
    return ("<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>" + title
            + "</title><style>" + css(theme) + "</style></head><body><div class=\"page\">"
            + "".join(out) + "</div></body></html>")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="lesson JSON file")
    ap.add_argument("-o", "--output", default="lesson_preview.html")
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    Path(args.output).write_text(render(data), encoding="utf-8")
    print(f"wrote {args.output} ({len(data.get('sections', []))} sections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
