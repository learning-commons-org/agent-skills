"""Shared-content helpers used by all artifact renderers.

The master lesson JSON has a `shared` block holding every piece of content that appears in more
than one artifact (standard, anchor task, problems, exit ticket, look-fors, vocabulary,
misconceptions, sentence frames). Renderers expand it via `expand_from_shared`, so shared
content is written once and can never drift between artifacts.
"""
from __future__ import annotations

import re

# ---- render-time print-safety repair ---------------------------------------------------
# Two failure classes survive prompt instructions and are repaired structurally instead:
# (1) markdown pipe tables drawn inside prose fields print as literal '|' rows — convert
#     them to real `table` blocks; (2) the ■ unknown-number symbol appearing in an artifact
#     with no defining sentence in THAT artifact (look-fors carry ■ into the observation
#     sheet via from_shared, where the model writes no prose) — append the skill's standard
#     definition line to the first section that uses it.

_PIPE_LINE = re.compile(r"[^|\n]*\|[^|\n]+\|")            # a line with >=2 pipe chars
_SEP_LINE = re.compile(r"^\s*\|?[\s:|\-]+\|?\s*$")        # |---|:---| separator row
UNKNOWN_SYMBOL = "■"
_UNKNOWN_DEFINED = re.compile(
    r"(use|using|write|stands for|symbol|means)[^.]{0,50}■"
    r"|■[^.]{0,50}(for the|stands for|means|is the|if you need)", re.IGNORECASE)


def _parse_pipe_rows(lines: list[str]) -> list[list[str]]:
    rows = []
    for ln in lines:
        if _SEP_LINE.match(ln):
            continue
        rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    width = max((len(r) for r in rows), default=0)
    return [r + [""] * (width - len(r)) for r in rows]


_INLINE_SEP = re.compile(r"\|\s*:?-{2,}")  # an inline |--- separator (table collapsed to one line)
_BULLET_LINE = re.compile(r"^\s*(?:[•▪‣◦]|[-–])\s+")

# Enumerated sub-parts written mid-prose — "… from Task 1: (a) Predict … (b) Describe …" —
# read as a wall of text. Insert a line break before each "(a)"/"(1)" marker that follows
# sentence-ending punctuation, so every sub-part starts on its own line. Both renderers
# preserve single newlines as line breaks.
_ENUM_MIDPROSE = re.compile(r"(?<=[.!?:;])[ \t]+(?=\((?:[a-h]|\d{1,2})\)\s)")


def _repair_enum_breaks(blk: dict) -> list[dict]:
    """Put mid-prose enumerated sub-parts ('(a) …', '(2) …') on their own lines."""
    if blk.get("type") == "group":
        return [dict(blk, blocks=[rb for b in blk.get("blocks", [])
                                  for rb in _repair_enum_breaks(b)])]
    if blk.get("type") == "columns":
        return [dict(blk,
                     left=[rb for b in blk.get("left", []) for rb in _repair_enum_breaks(b)],
                     right=[rb for b in blk.get("right", []) for rb in _repair_enum_breaks(b)])]
    if blk.get("type") in ("paragraph", "labeled", "callout") and isinstance(blk.get("text"), str):
        fixed = _ENUM_MIDPROSE.sub("\n", blk["text"])
        if fixed != blk["text"]:
            return [dict(blk, text=fixed)]
    return [blk]


def _repair_inline_bullets(blk: dict) -> list[dict]:
    """Split prose containing bullet-marked lines ('• item') into prose + bullets blocks.
    A paragraph renders newlines as spaces, so bullets written inside a text string run
    together into one unreadable line."""
    if blk.get("type") == "group":
        return [dict(blk, blocks=[rb for b in blk.get("blocks", [])
                                  for rb in _repair_inline_bullets(b)])]
    if blk.get("type") == "columns":
        return [dict(blk,
                     left=[rb for b in blk.get("left", []) for rb in _repair_inline_bullets(b)],
                     right=[rb for b in blk.get("right", []) for rb in _repair_inline_bullets(b)])]
    if blk.get("type") not in ("paragraph", "labeled") or not isinstance(blk.get("text"), str) \
            or "\n" not in blk["text"]:
        return [blk]
    lines = blk["text"].split("\n")
    if not any(_BULLET_LINE.match(ln) for ln in lines):
        return [blk]
    out: list[dict] = []
    buf: list[str] = []
    items: list[str] = []
    first = True

    def flush_text():
        nonlocal first
        t = "\n".join(buf).strip()
        if t:
            out.append(dict(blk, text=t) if first else {"type": "paragraph", "text": t})
            first = False
        buf.clear()

    def flush_items():
        nonlocal first
        if items:
            if first and blk.get("type") == "labeled" and blk.get("label"):
                # The block opens with bullets — keep its label as a lead-in line
                # instead of silently dropping it.
                out.append({"type": "labeled", "label": blk["label"], "text": ""})
            out.append({"type": "bullets", "items": list(items)})
            first = False
            items.clear()

    for ln in lines:
        if _BULLET_LINE.match(ln):
            flush_text()
            items.append(_BULLET_LINE.sub("", ln, count=1).strip())
        elif ln.strip():
            flush_items()
            buf.append(ln)
        else:
            buf.append(ln)  # blank line — stays in whichever prose run is open
    flush_items()
    flush_text()
    return out or [blk]


def _repair_pipe_tables(blk: dict) -> list[dict]:
    """Split a prose block containing a markdown pipe-table run into prose + table blocks."""
    if blk.get("type") == "group":
        return [dict(blk, blocks=[rb for b in blk.get("blocks", [])
                                  for rb in _repair_pipe_tables(b)])]
    if blk.get("type") == "columns":
        return [dict(blk,
                     left=[rb for b in blk.get("left", []) for rb in _repair_pipe_tables(b)],
                     right=[rb for b in blk.get("right", []) for rb in _repair_pipe_tables(b)])]
    if blk.get("type") in ("bullets", "checklist"):
        # A pipe table inside a bullet item: split the list around it and lift the table out.
        out: list[dict] = []
        cur: list = []
        for item in blk.get("items", []):
            if isinstance(item, str) and _INLINE_SEP.search(item):
                pieces = _repair_pipe_tables({"type": "paragraph", "text": item})
                if any(p.get("type") == "table" for p in pieces):
                    if cur:
                        out.append(dict(blk, items=cur))
                        cur = []
                    out.extend(pieces)
                    continue
            cur.append(item)
        if cur:
            out.append(dict(blk, items=cur))
        return out or [blk]
    if blk.get("type") not in ("paragraph", "labeled", "callout") \
            or not isinstance(blk.get("text"), str):
        return [blk]
    text = blk["text"]
    if "\n" not in text and _INLINE_SEP.search(text):
        # Table collapsed onto one line — restore row boundaries ("| |" marks a row break).
        text = re.sub(r"\|\s+\|", "|\n|", text)
        blk = dict(blk, text=text)
    lines = blk["text"].split("\n")
    if any(_INLINE_SEP.search(ln) for ln in lines):
        # Prose sharing a line with a table row would be swallowed into the table —
        # split "intro text: | a | b |" and "| x | y | trailing text" onto separate lines.
        norm: list[str] = []
        for ln in lines:
            m = re.match(r"^([^|]*[^|\s])\s*(\|.+\|)\s*$", ln)
            if m and not _SEP_LINE.match(ln):
                norm += [m.group(1), m.group(2)]
                continue
            m = re.match(r"^\s*(\|.+\|)\s*([^|]+)$", ln)
            if m and not _SEP_LINE.match(ln):
                norm += [m.group(1), m.group(2)]
                continue
            norm.append(ln)
        lines = norm
    out: list[dict] = []
    buf: list[str] = []
    i, first = 0, True

    def flush():
        nonlocal first
        t = "\n".join(buf).strip()
        if t:
            out.append(dict(blk, text=t) if first else {"type": "paragraph", "text": t})
            first = False
        buf.clear()

    while i < len(lines):
        if _PIPE_LINE.search(lines[i]):
            j = i
            while j < len(lines) and (_PIPE_LINE.search(lines[j]) or _SEP_LINE.match(lines[j])):
                j += 1
            if sum(1 for k in range(i, j) if not _SEP_LINE.match(lines[k])) >= 2:
                flush()
                rows = _parse_pipe_rows(lines[i:j])
                out.append({"type": "table", "headers": rows[0],
                            "rows": rows[1:] or [[""] * len(rows[0])]})
                first = False
                i = j
                continue
        buf.append(lines[i])
        i += 1
    flush()
    return out or [blk]


def _doc_text(sections: list[dict]) -> str:
    parts: list[str] = []

    def walk(v):
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)

    walk(sections)
    return "\n".join(parts)


def _bul(items):
    return {"type": "bullets", "items": items}


_TASK_LEAD = re.compile(r"\s*\**\s*(task|problem|question)\s*\d", re.IGNORECASE)
_TASK_TITLE = re.compile(
    r"^\s*((?:task|problem|question)\s*\d+\s*(?:[—–-]\s*[^.:!?\n]{1,60})?[.:]?)[ \t]*",
    re.IGNORECASE)


def _task_prefix(i: int, p: dict) -> str:
    """Number a task — unless its text already starts with 'Task N'/'Problem N', which
    would render as the double-numbered '1. Task 1 — …'."""
    return "" if _TASK_LEAD.match(str(p.get("text", ""))) else f"**{i}.** "


def _bold_task_lead(text: str) -> str:
    """Bold a 'Task N — Title.' lead so tasks carry the same visual weight as the labeled
    blocks around them. No-op when the lead is already bold or absent. Newlines after the
    title are preserved — they are the boundary between the title line and the body."""
    m = _TASK_TITLE.match(text)
    if m and "**" not in m.group(1):
        rest = text[m.end():]
        sep = "" if rest.startswith("\n") else "\n" if rest else ""
        return f"**{m.group(1).strip()}**{sep}{rest}"
    return text


def coerce_shared(shared: dict) -> dict:
    """Tolerate slightly-off shapes (strings where dicts/lists are expected) so a render never
    fails on a minor schema deviation."""
    s = dict(shared or {})
    et = s.get("exit_ticket")
    if isinstance(et, str):
        s["exit_ticket"] = {"prompt": et, "buckets": ["Got it", "Almost there", "Needs re-teaching"]}
    if isinstance(s.get("anchor_task"), dict):
        s["anchor_task"] = s["anchor_task"].get("text") or s["anchor_task"].get("prompt") or ""
    for key, field in (("problems", "text"), ("vocabulary", "term"),
                       ("look_fors", "name"), ("misconceptions", "what"),
                       ("sentence_frames", None)):
        val = s.get(key)
        if isinstance(val, list):
            fixed = []
            for item in val:
                if isinstance(item, dict) or field is None and isinstance(item, str):
                    fixed.append(item)
                elif isinstance(item, str) and field:
                    fixed.append({field: item})
                elif isinstance(item, dict) and field is None:
                    fixed.append(str(item))
            s[key] = fixed
        elif isinstance(val, str) and val:
            s[key] = [val] if field is None else [{field: val}]
    return s


def expand_from_shared(key: str, shared: dict, audience: str = "teacher",
                       blk: dict | None = None) -> list[dict]:
    """Expand a `{"type": "from_shared", "key": ...}` block into plain renderer blocks.

    audience: "teacher" (lesson plan / observation) or "student" (worksheet) — controls wording.
    blk: the original from_shared block, for option keys (e.g. problems' "only").
    """
    shared = coerce_shared(shared)
    if key == "standard":
        # Stored as standard_code/standard_text, not under a "standard" key — must be
        # resolved BEFORE the generic empty-value guard below, which silently dropped
        # the target-standard callout from every document that requested it.
        if not (shared.get("standard_text") or shared.get("standard_code")):
            return []
        return [{"type": "callout", "kind": "special",
                 "label": f"{shared.get('standard_code', '')} — Target Standard".strip(" —"),
                 "text": shared.get("standard_text", "")}]
    val = shared.get(key)
    if not val:
        return []

    if key == "anchor_task":
        label = "Anchor task" if audience == "teacher" else "Try this together"
        return [{"type": "callout", "kind": "student-task", "label": label, "text": str(val)}]

    if key == "vocabulary":
        # Headerless two-column table — the table itself is the visual marker for "this is a
        # vocab list" (first column bolds automatically). Short lists stay as bullets.
        if len(val) >= 5:
            return [{"type": "table",
                     "rows": [[v.get("term", ""), v.get("definition", "")] for v in val]}]
        return [_bul([f"**{v.get('term', '')}** — {v.get('definition', '')}" for v in val])]

    if key == "misconceptions":
        return [{"type": "table",
                 "headers": ["What students do", "Why it happens", "Teacher move"],
                 "rows": [[m.get("what", ""), m.get("why", ""), m.get("move", "")] for m in val]}]

    if key == "look_fors":
        return [_bul([f"**{lf.get('name', '')}** — {lf.get('what_it_means', '')} "
                      f"*Teacher move: {lf.get('teacher_move', '')}*" for lf in val])]

    if key == "sentence_frames":
        return [_bul([f"*{s}*" for s in val])]

    if key == "exit_ticket":
        blocks = [{"type": "callout", "kind": "student-task",
                   "label": "Exit ticket" if audience == "teacher" else "",
                   "text": val.get("prompt", "")}]
        if audience == "teacher" and val.get("buckets"):
            # Buckets may be plain labels ("Got it") or dicts with explicit sort criteria
            # ({"label": ..., "criteria": ...}) — render criteria when present.
            blocks.append({"type": "h3", "text": "Sort student work"})
            blocks.append({"type": "cards", "items": [
                ({"title": b.get("label", ""),
                  "text": b.get("criteria") or b.get("description") or ""}
                 if isinstance(b, dict) else {"title": str(b), "text": ""})
                for b in val["buckets"]]})
        return blocks

    if key == "problems":
        letters = "ABCDEF"
        sel = list(enumerate(val, 1))
        only = (blk or {}).get("only")
        if only:  # {"type": "from_shared", "key": "problems", "only": 2} → just task 2
            # Tolerate malformed values ("1-2", "Task 2") — fall back to the whole set
            # rather than crashing the render on a minor schema deviation.
            try:
                wanted = {int(x) for x in (only if isinstance(only, (list, tuple)) else [only])}
            except (TypeError, ValueError):
                wanted = None
            if wanted:
                sel = [(i, p) for i, p in sel if i in wanted]
        if audience == "teacher":
            # Ordered list only when showing the full set 1..N — a subset via `only` must
            # keep the original numbers so the teacher plan and student worksheet agree.
            indices = [i for i, _ in sel]
            full_set = indices == list(range(1, len(indices) + 1))
            items = []
            for i, p in sel:
                tag = f" *({p['difficulty']})*" if p.get("difficulty") else ""
                choices = p.get("choices") or []
                ch = ("  " + "  ".join(f"**{letters[j]})** {c}" for j, c in enumerate(choices[:6]))
                      if choices else "")
                prefix = "" if full_set else _task_prefix(i, p)
                items.append(_bold_task_lead(f"{prefix}{p.get('text', '')}") + f"{tag}{ch}")
            if full_set:
                return [{"type": "list", "ordered": True, "items": items}]
            return [_bul(items)]
        # Student worksheets: each task is its own block group with writing space after it
        # (grade-banded by the renderer), so students always have room to answer — and a
        # tier document can interleave scaffolds using "only".
        blocks = []
        for i, p in sel:
            group: list[dict] = [{"type": "paragraph",
                                  "text": _bold_task_lead(
                                      f"{_task_prefix(i, p)}{p.get('text', '')}")}]
            choices = p.get("choices") or []
            if choices:
                group.append(_bul([f"**{letters[j]})**  {c}" for j, c in enumerate(choices[:6])]))
            space: dict = {"type": "answer_box"}
            if p.get("work_space_pt"):
                space["height_pt"] = p["work_space_pt"]
            elif choices:
                space["height_pt"] = 60  # choices carry the answer; space is for showing work
            group.append(space)
            blocks.append({"type": "group", "blocks": group})
        return blocks

    return [{"type": "paragraph", "text": str(val)}]


def expand_blocks(blocks: list, shared: dict, audience: str = "teacher") -> list[dict]:
    """Replace any from_shared blocks in a block list (recursing into columns)."""
    out: list[dict] = []
    for blk in blocks or []:
        btype = blk.get("type")
        if btype == "from_shared":
            out.extend(expand_from_shared(blk.get("key", ""), shared, audience, blk))
        elif btype == "columns":
            out.append({"type": "columns",
                        "left": expand_blocks(blk.get("left", []), shared, audience),
                        "right": expand_blocks(blk.get("right", []), shared, audience)})
        else:
            out.append(blk)
    return out


_PROMPT_TYPES = ("paragraph", "labeled", "callout", "bullets", "subheading")


def _pair_writing_space(blocks: list[dict]) -> list[dict]:
    """Glue a prompt block to the answer_box that follows it so a page break can never
    separate a question from its writing space (renderers keep groups together)."""
    out: list[dict] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if (b.get("type") in _PROMPT_TYPES and i + 1 < len(blocks)
                and blocks[i + 1].get("type") == "answer_box"):
            out.append({"type": "group", "blocks": [b, blocks[i + 1]]})
            i += 2
            continue
        out.append(b)
        i += 1
    return out


def _strip_heading_echo(section: dict) -> dict:
    """Drop a leading repeat of the section heading from the first text block —
    'If you finish early' + text starting 'If you finish early: …' prints twice."""
    heading = str(section.get("heading", "")).strip().rstrip(":").strip()
    blocks = section.get("blocks") or []
    if not heading or len(heading) < 4 or not blocks:
        return section
    first = blocks[0]
    btype = first.get("type")
    target = first if btype in ("paragraph", "labeled", "callout") else None
    if btype == "group" and first.get("blocks"):
        inner = first["blocks"][0]
        target = inner if inner.get("type") in ("paragraph", "labeled", "callout") else None
    if not target or not isinstance(target.get("text"), str):
        return section
    m = re.match(r"\s*\**" + re.escape(heading) + r"\**\s*[:!.—–-]\s*", target["text"],
                 re.IGNORECASE)
    if not m or not target["text"][m.end():].strip():
        return section
    fixed = dict(target, text=target["text"][m.end():])
    if btype == "group":
        new_first = dict(first, blocks=[fixed] + first["blocks"][1:])
    else:
        new_first = fixed
    return {**section, "blocks": [new_first] + blocks[1:]}


def expand_document(data: dict, audience: str = "teacher") -> dict:
    """Return a copy of a document dict with all from_shared blocks expanded."""
    shared = data.get("shared", {})
    doc = dict(data)
    doc["sections"] = [
        {**s, "blocks": expand_blocks(s.get("blocks", []), shared, audience)}
        for s in data.get("sections", [])
    ]
    # Print-safety repair pass — post-expansion so it covers model prose AND shared content,
    # in every artifact and both output formats (HTML and docx render through here).
    doc["sections"] = [
        {**s, "blocks": _pair_writing_space(
            [rb for b in s.get("blocks", [])
             for eb in _repair_enum_breaks(b)
             for tb in _repair_pipe_tables(eb)
             for rb in _repair_inline_bullets(tb)])}
        for s in doc["sections"]
    ]
    doc["sections"] = [_strip_heading_echo(s) for s in doc["sections"]]
    text = _doc_text(doc["sections"])
    if UNKNOWN_SYMBOL in text and not _UNKNOWN_DEFINED.search(text):
        for s in doc["sections"]:
            if UNKNOWN_SYMBOL in _doc_text([s]):
                s.setdefault("blocks", []).append(
                    {"type": "paragraph",
                     "text": "*The symbol ■ stands for the unknown number.*"})
                break
    return doc


# ============================================================================
# Shared rendering primitives — format-agnostic helpers used by every renderer.
# Moved from render_lesson_html.py so render_lesson_docx.py can import the same
# theme, alias, callout, and grade-band logic without duplication.
# ============================================================================

DEFAULT_THEME = {
    "primary": "#17A267", "title_color": "#14613F",
    "text": "#222222", "muted": "#666666", "rule": "#D0D4D8", "border": "#CBD2D8",
    "title_size": 22, "body_size": 10.5,
}
HEX = re.compile(r"^#[0-9A-Fa-f]{3,8}$")

# Legacy block-type names -> canonical names. Keeps existing lesson JSONs rendering.
ALIASES = {"subheading": "h3", "bullets": "list", "answer_box": "workspace"}


def btype(blk: dict) -> str:
    t = blk.get("type") or "paragraph"
    return ALIASES.get(t, t)


# Callout kinds: semantic name -> (icon, css class). Legacy `style`/`role` values map in.
CALLOUT_KINDS = {
    "special":      ("⭐", "special"),
    "student-task": ("📌", "task"),
    "teacher-note": ("✋", "tnote"),
    "student-note": ("✋", "snote"),
}
CALLOUT_ALIASES = {
    "accent": "special", "standard": "special",
    "info": "student-task", "activity": "student-task",
    "note": "teacher-note", "tip": "teacher-note",
    "warning": "teacher-note", "caution": "teacher-note", "important": "special",
}


def resolve_callout_kind(blk: dict) -> str:
    raw = str(blk.get("kind") or blk.get("role") or blk.get("style") or "student-task").lower()
    return raw if raw in CALLOUT_KINDS else CALLOUT_ALIASES.get(raw, "student-task")


class Theme:
    def __init__(self, overrides: dict | None):
        t = dict(DEFAULT_THEME)
        t.update(overrides or {})
        self.raw = t
        self.answer_height, self.answer_gap, self.answer_row = 120.0, None, 96.0
        self.student_doc = False

    def safe(self, key: str) -> str:
        val = str(self.raw.get(key, DEFAULT_THEME.get(key, "")))
        return val if HEX.match(val) else str(DEFAULT_THEME.get(key, "#222222"))


def meta_text(meta) -> str:
    """Normalize `meta` to a display string. The schema says it's a string, but models
    sometimes emit a list of {label, value} dicts — join those as 'Label: value · …'."""
    if isinstance(meta, dict):
        meta = [meta]
    if isinstance(meta, (list, tuple)):
        parts = []
        for item in meta:
            if isinstance(item, dict):
                label = str(item.get("label") or "").rstrip(":").strip()
                value = str(item.get("value") or item.get("text") or "").strip()
                parts.append(f"{label}: {value}" if label and value else (value or label))
            elif item:
                parts.append(str(item))
        return " · ".join(p for p in parts if p)
    return str(meta) if meta else ""


def grade_number(data: dict):
    """Best-effort grade parse: 0 for K, 1-12, or None."""
    shared = data.get("shared") or {}
    for src in (data.get("grade"), shared.get("grade") if isinstance(shared, dict) else None):
        s = str(src or "").strip().lower()
        if not s:
            continue
        if s.startswith("k") or "kind" in s:
            return 0
        m = re.search(r"\d{1,2}", s)
        if m:
            return int(m.group(0))
    for which, src in (("eyebrow", data.get("eyebrow")), ("meta", meta_text(data.get("meta")))):
        s = str(src or "").lower()
        if "kindergarten" in s:
            return 0
        m = (re.search(r"\bgrade[:\s]*(k|\d{1,2})\b", s)
             or re.search(r"\b(\d{1,2})(?:st|nd|rd|th)[\s-]*grade\b", s))
        if not m and which == "eyebrow":
            m = re.search(r"^\s*(k|1[0-2]|[1-9])(?:st|nd|rd|th)?\b"
                          r"(?!\s*(?:min|minute|hour|problem|tier|page|point|task|question))", s)
        if m:
            g = m.group(1)
            return 0 if g == "k" else int(g)
    return None


def answer_profile(data: dict) -> tuple:
    """Grade-banded writing-space defaults: (height pt, ruled gap pt or None, table-row pt)."""
    n = grade_number(data)
    if n is None:
        return 120.0, None, 96.0
    shared = data.get("shared")
    shared = shared if isinstance(shared, dict) else {}
    # smps (Standards for Mathematical Practice) is the most reliable math signal — it is
    # math-only and the math reference mandates it, whereas shared.subject is often omitted.
    is_math = bool(shared.get("smps")) or "math" in " ".join(str(x or "") for x in (
        shared.get("subject"), data.get("eyebrow"), data.get("title"))).lower()
    if n <= 2:
        return 200.0, (None if is_math else 40.0), 160.0
    if n <= 5:
        return 150.0, (None if is_math else 28.0), 126.0
    if n <= 8:
        return 130.0, None, 108.0
    return 116.0, None, 96.0


WORKSPACE_SIZES = {"small": 70.0, "med": 130.0, "large": 220.0}
FILL_IN_CHARS = {"short": 12, "med": 28, "long": 60}  # underscore counts for non-CSS formats


def workspace_height(blk: dict, theme: Theme) -> float:
    """Resolve a workspace block's height in points (format-agnostic)."""
    h = blk.get("height_pt")
    if h is None:
        h = WORKSPACE_SIZES.get(str(blk.get("size", "")).lower())
    if h is None:
        h = theme.answer_height
    try:
        return float(h)
    except (TypeError, ValueError):
        return float(theme.answer_height)


def label_text(blk: dict) -> str:
    """Normalized label string — strips a trailing colon so renderers can add their own
    consistently without doubling it."""
    return str(blk.get("label", "")).rstrip(":")


def label_sep(label: str) -> str:
    """Separator after a label: numeric labels (task numbers like "1", "2a") get a period;
    word labels ("Anchor task", "Exit ticket") get a colon. A label that already ends in a
    period gets no extra separator."""
    s = label.strip()
    if s.endswith("."):
        return ""
    return "." if re.fullmatch(r"\d+[a-z]?", s, re.IGNORECASE) else ":"


def normalize_text(text) -> str:
    """Format-agnostic text fixups applied before any inline-markdown parse."""
    t = str(text)
    t = re.sub(r"(?<!_)_{3,9}(?!_)", "______", t)
    t = re.sub(r"\s+\|\s+", " · ", t)
    return t


_MD_TOKEN = re.compile(r"(\*\*.+?\*\*|(?<!\*)\*(?!\s).+?(?<!\s)\*(?!\*)|\n)")


def md_tokens(text) -> list:
    """Parse mini-markdown into format-neutral tokens.

    Returns a list of (text, attrs) where attrs is a dict with optional 'bold',
    'italic', 'break' keys. normalize_text() is applied first."""
    t = normalize_text(text)
    out = []
    for part in _MD_TOKEN.split(t):
        if not part:
            continue
        if part == "\n":
            out.append(("", {"break": True}))
        elif part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], {"bold": True}))
        elif part.startswith("*") and part.endswith("*"):
            out.append((part[1:-1], {"italic": True}))
        else:
            out.append((part, {}))
    return out


def table_row_height(blk: dict, theme: Theme, *, full_blank: bool) -> float:
    """Minimum height (pt) for a table row containing empty writing-space cells.
    Honors explicit empty_row_height_pt; falls back to grade band for student docs."""
    try:
        explicit = float(blk.get("empty_row_height_pt", 0) or 0)
    except (TypeError, ValueError):
        explicit = 0.0
    band = theme.answer_row
    if theme.student_doc:
        return (max(explicit or band, 0.75 * band) if full_blank
                else max(0.45 * band, explicit))
    return explicit or 36.0


def preamble_blocks(data: dict) -> list[dict]:
    """Top-level standard / prerequisite / practices blocks rendered between the header
    and the first section. Shared by both formats so the preamble can never drift."""
    blocks: list[dict] = []
    if data.get("standard_text"):
        label = f"{data.get('standard_code', '')} — Target Standard".strip(" —")
        blocks.append({"type": "callout", "kind": "special", "label": label,
                       "text": data["standard_text"]})
    if data.get("prerequisite_standard"):
        blocks.append({"type": "labeled", "label": "Builds on",
                       "text": data["prerequisite_standard"]})
    if data.get("smps"):
        blocks.append({"type": "labeled", "label": "Mathematical practices",
                       "text": "; ".join(data["smps"])})
    return blocks


def build_header(data: dict) -> dict:
    """Format-agnostic header fields: eyebrow, title, meta string, optional name_line."""
    meta = meta_text(data.get("meta"))
    if not meta:
        bits = [data.get("standard_code"), data.get("grade"), data.get("duration"),
                data.get("curriculum")]
        if data.get("materials"):
            bits.append("Materials: " + ", ".join(data["materials"]))
        meta = " · ".join(str(b) for b in bits if b)
    name_line = ""
    if meta and data.get("audience") == "student" and re.search(r"name\s*:", meta, re.I):
        name_line, meta = meta, ""
    return {"eyebrow": data.get("eyebrow", ""), "title": data.get("title", "Lesson Plan"),
            "meta": meta, "name_line": name_line}
