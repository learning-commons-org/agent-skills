---
name: k12-lesson-planning
description: >
  Creates a lesson plan, student-facing materials, and observation template. Use when a K-12 teacher needs to build a math, ELA, science, or social studies lesson from scratch for a specific topic, standard, or grade. Do NOT load this skill when the request is only for grading, a rubric, assessment feedback, a quiz, or a standards lookup — answer those directly without it. Triggers on both explicit requests (math/ELA/science/history lesson plan, mini-lesson, unit plan, daily plan, reading lesson, writing lesson, phonics lesson) and implicit teacher intent — when a teacher describes upcoming content they need to teach: "I'm teaching long division to 5th graders," "planning a lesson on RL.4.3 next week," "need to teach photosynthesis tomorrow," "2nd grade phonics on long vowels." Core signal: teacher has a topic/standard + grade and needs new instructional content created. Not for differentiating an existing lesson (use k12-lesson-differentiation) or passage rewrites.
---

# K-12 Lesson Planning

Produces a teacher-ready, standards-aligned lesson plan + student-facing materials + teacher
observation template as native files in Turn 1, rendered from one master JSON via bundled
scripts (HTML previews first, editable Word documents on confirmation). Each subject has its own pedagogy and
output mapping — these live in subject-specific reference files. This skill routes to the
right one. Works with or without the Learning Commons Knowledge Graph.

"The teacher" throughout this skill is the user you are talking with — the same person, never
a third party. "Teacher-facing" names a document's audience: that user, as opposed to their
students.

---

## Step 0 — Route (silent, before anything else)

1. **Subject.** Determine the subject of the requested lesson from the prompt and any prior
   conversation:

   - **math** — arithmetic, fractions, geometry, algebra, calculus, statistics, CCSS-M codes, IM (Illustrative Mathematics)
   - **ela** — reading, writing, phonics, literature, comprehension, vocabulary, CCSS-ELA codes (RL/RI/RF/W/L)
   - **science** — phenomena, NGSS Performance Expectations, biology/chemistry/physics/earth science, OpenSciEd
   - **social_studies** — history, civics, geography, economics, C3 inquiry arc, state social-studies standards

   Then read the matching reference file NOW:

   - math → `references/math.md`
   - ELA → `references/ela.md`
   - science → `references/science.md`
   - social studies → `references/social_studies.md`

   **Loading the matching reference file is mandatory.** Drafting a lesson without first
   reading the subject reference is a critical failure. The reference file carries the
   complete subject-specific instructions: clarify priorities, curriculum branching,
   grade-band structures, section structure, non-negotiables, and the lesson.json mapping.
   Treat the loaded reference as your full skill instructions for this turn. If the subject
   is genuinely ambiguous or the prompt spans multiple subjects, it becomes the one question
   in Step 1.

2. **Curriculum.** If the teacher names or implies a curriculum (Illustrative Mathematics,
   OpenSciEd, …), the subject file's curriculum branch covers it — each subject
   file carries its curriculum's structures and language inline (curriculum and subject are
   1:1: IM→math, OpenSciEd→science). If they use a curriculum the subject
   file doesn't cover, follow its "no curriculum named" path and do not fake
   curriculum-specific terminology.
3. **Connector.** Check whether the Learning Commons Knowledge Graph tools (e.g.
   `find_standard_statement`) are available in this conversation. This decides which path
   Step 2 takes. The skill is fully functional without the connector.

---

## Step 1 — Clarify (one question max)

Follow the subject file's clarify section: ask at most ONE question, using its priority order;
infer everything else; apply its defaults silently.

---

## Step 2 — Ground in standards

**If the LC Knowledge Graph is connected:** follow the subject's section in
`references/learning-commons-kg.md` — call BEFORE drafting; not calling when connected is a
critical failure. Extract only what each call specifies, then proceed directly to Step 3 — do
not summarize findings in chat.

**If not connected:** draft from best knowledge and add this footer to the lesson plan:
*"Generated without the Learning Commons Knowledge Graph. Standards and misconceptions reflect
general best practice."* Do not invent KG citations or attribute content to curriculum
materials you have not seen.

---

## Step 3 — Build the lesson

Follow the subject file's build section: curriculum branching, grade-band structure, section
structure, and non-negotiables. Respect the **Copyright guardrail** below — never reproduce
curriculum student-facing text verbatim.

---

## Copyright guardrail

Always write original content. KG curriculum materials inform structure, scope, text
selection, phenomenon selection, problem context, and lesson-arc design only — never
reproduce student-facing text, teacher notes, comprehension questions, investigation
prompts, discussion questions, activity narratives, or problem contexts verbatim from KG
curriculum materials.

If the loaded reference identifies a source curriculum (e.g., IM for math, OpenSciEd for science) and the teacher is not curriculum-confirmed for it, never name
that curriculum anywhere in the output or in any chat message — not in headers, footnotes,
rationale sections, facilitation notes, or your message presenting the artifacts. The KG
data is internal scaffolding.

---

## Step 4 — Output (Turn 1)

The artifacts are rendered by bundled scripts from **one master `lesson.json`**. The artifact
set is the same for every subject — lesson plan + student materials + observation template —
and the subject file's "Writing lesson.json" section defines how its content maps to the
JSON. Anything that appears in more than one artifact (standard, anchor task, problems/tasks,
exit ticket, look-fors, vocabulary, misconceptions, sentence frames) lives ONCE in the JSON's
`shared` block and is pulled into each artifact by the renderers, so the artifacts cannot
drift apart.

Never write layout code, never re-type lesson content into another format, and never edit a
generated HTML/Word document directly — every change goes into `lesson.json` and is re-rendered
(re-rendering is instant). **Do not open, cat, head, or grep the renderer scripts** — their
behavior is fully specified by the commands and output paths in §4a–4e, and
`references/example_lesson.json` is the complete schema. Reading script source tells you
nothing this file doesn't already state.

**Plain language with the teacher.** The machinery above is invisible to the teacher: never
mention JSON, HTML, schemas, scripts, rendering, file names (`lesson.json`), or code in any
teacher-facing message. Say *"Here's your lesson plan — the student materials and observation
template are on their way"*, not *"I've rendered the HTML preview from lesson.json"*. The only
format words a teacher sees are **"preview"** and **"editable copy"** (the Word document). This
applies to every turn: presenting artifacts, the satisfaction ask, revision summaries, and
error messages (if generation fails, say the documents couldn't be created — not that a
script or JSON failed).

**Density rules — hard requirements for every document.** Teachers consistently flag dense
walls of text. Structure beats prose:

- A `paragraph` or `labeled` block is at most 3 sentences. Longer → split it, bullet it, or
  table it.
- Bullets are fragments — one idea each, ≤ ~15 words; never chain clauses with semicolons.
- Parallel variants (per-group supports, per-phase differentiation, tiered look-fors) go in
  ONE `table` block — rows = phases or features, columns = variants, ≤ ~25 words per cell —
  never back-to-back multi-sentence paragraphs.
- An aside longer than one sentence (misconception watch-fors, confer prompts, teacher
  moves) becomes its own `callout` block, not a sentence buried in a paragraph.
- Quote the standard verbatim exactly once (the target-standard callout, from `shared`).
  Everywhere else — prerequisite grounding, forward connections — reference by code plus a
  gist of ten words or fewer; never re-paste full standard text.
- A section that runs past about half a page of continuous prose must be restructured
  (table, bullets, or split into two sections) before rendering.

### 4a. Write the complete `lesson.json` (Turn 1)

Write ONE `lesson.json` containing everything for all three artifacts, in this order:

- Top-level `eyebrow` / `title` / `meta`.
- The **`shared` block** (write this FIRST — see the subject mapping for what goes in
  `subject`, `anchor_task`, `problems[]`, `exit_ticket`, plus `look_fors[]`, `vocabulary[]`,
  `misconceptions[]`, `sentence_frames[]`, and the standard verbatim).
- `sections` for the subject's section structure. **Inside `sections`, never re-type shared
  content — use `{"type": "from_shared", "key": …}` blocks** (keys: standard, anchor_task,
  vocabulary, misconceptions, look_fors, problems, exit_ticket, sentence_frames).
- `student_materials` (title, student-facing instructions, `headings{warmup, practice, exit}`
  overrides, `exit_ticket_own_page: true` — always; the exit ticket is collected separately).
  Its substance — problems/tasks, exit ticket — comes from `shared` automatically; do not
  restate it. When the lesson plan calls for material students consult while working (e.g., a
  data table the problems analyze, a labeled source list with title/author/date/excerpt, a
  reference chart), put it in `reference_blocks` so it renders on the worksheet before the
  practice set under `reference_heading` (default "Reference"); most lessons have none.
  Student materials must contain **zero teacher-directed text** — no "the teacher
  places…", no look-fors, no assessment rationale. For K–2
  tasks the teacher administers aloud, the administration script goes in
  `observation_template.instructions` (or the lesson plan), never on the student page; the
  student page carries only what the student sees.
- `observation_template` (instructions, columns; `blank_rows` and `tracker_rows` are integer
  row counts, never lists — `blank_rows` max 8, with space for 4–5 lines of handwriting per
  row). Its substance — look-fors, misconceptions, exit ticket — comes from `shared`
  automatically; the renderer also adds a pre-selection (select-and-sequence for Discuss)
  table and a per-student tracker automatically.

**Schema** — the complete field skeleton (`blocks` shows one of each type; all string values
are free text unless an enum is shown). This is sufficient — do not read any other file for
the schema:

```
eyebrow, title, meta, footer_note
shared:
  grade, subject, duration, curriculum, standard_code, standard_text,
  prerequisite_standard, smps[] (math only), anchor_task, sentence_frames[]
  vocabulary[]:     {term, definition}
  problems[]:       {text, situation, difficulty, choices[]?}   (choices[] for multiple-choice items; omit otherwise)
  exit_ticket:      {prompt, case, buckets[]: {label, criteria}}
  look_fors[]:      {name, what_it_means, teacher_move}
  misconceptions[]: {what, why, move}
sections[]: {heading, blocks[]} — block types:
  {type: from_shared, key} | {type: paragraph, text} | {type: labeled, label, text}
  {type: callout, kind: special|student-task|teacher-note, label, text}
  {type: h2, text} | {type: h3, text} | {type: list, label?, ordered?, items[]}
  {type: phase_header, name, minutes} | {type: table, headers[]?, rows[[]]}
  {type: cards, items[{title, text}]}
student_materials:    {title, instructions, exit_ticket_own_page: true,
                       headings{warmup, practice, exit}, reference_heading?, reference_blocks[]?}
observation_template: {instructions, columns[], blank_rows: int, tracker_rows: int}
```

(`references/example_lesson.json` is a filled-in worked example if values-in-context would
help, but reading it is not required.) Keep writing tight; no emoji in
JSON content. The density rules above are hard requirements for every text field.
Print-safety in every text field: never markdown pipe tables (use the schema's `table`
block); never flatten a visual model into a bare digit string ("500 600 538 rounds to ___" is
unreadable on paper) — describe number lines and diagrams in words.

**Which block when** — pick by what the content *is*, not how it should look:

| Block | Use it for |
|---|---|
| `callout` `kind: special` | The one anchoring fact per artifact — the target standard. Typically once. |
| `callout` `kind: student-task` | Any task students do: anchor task, exit ticket prompt, a practice problem shown in the plan. |
| `callout` `kind: teacher-note` | An aside the teacher reads but does not say aloud: "don't resolve yet", conferring moves, a watch-for. |
| `list` `ordered: true` | A numbered sequence — the problem set, procedure steps. Unordered otherwise. |
| `list` with `label` | A titled enumeration — several discrete items under one label. |
| `h2` | Sub-sections inside a section — the lesson-sequence phases use `phase_header`, which renders as h2 with minutes; the `minutes` across all phase headers should sum to `shared.duration`. |
| `h3` | A title above one block (a table, a list group, the look-fors). |
| `cards` | 2–4 parallel items of roughly equal length — exit-ticket sort buckets, tier summaries. Never for long or unbalanced items; use a `list` for those. |
| `table` (no `headers`) | Term/definition pairs, label/value reference rows. |
| `table` with `headers` | Real tabular data with column labels (misconceptions, scaffolds, differentiation grid). |

### 4b. Render all three previews — one command, same turn

```bash
bash scripts/render_all.sh lesson.json "$OUTPUT_DIR"
```

This writes `$OUTPUT_DIR/lesson_plan_preview.html`, `$OUTPUT_DIR/student_materials.html`, and
`$OUTPUT_DIR/observation_template.html` in one invocation — no copy step needed. Present all
three to the teacher together (lesson plan first in your message).

### 4c. The satisfaction ask + iteration options (every output turn)

End the turn with EXACTLY ONE closing message that does two things:

1. Asks whether the teacher is satisfied with **every artifact produced** or wants changes,
   and states that the next step is sending editable copies — e.g. *"When you're happy with the
   lesson plan, the student materials, and the observation template, I'll send whichever ones
   you want as editable Word documents."* Do not render them before the teacher confirms, and
   do not skip the ask.
2. Offers 3–4 high-leverage, **specific** iteration options customized to the subject and
   topic. Do not write "let me know if you want changes" — that's a non-offer. For example,
   for a 3–5 ELA reading comprehension lesson: *"Would you like to (1) add more scaffolds for
   English learners, (2) differentiate by proficiency level, or (3) adapt to be specific to
   your state standards?"*

### 4d. Revisions — one edit, every artifact stays in sync

Make **targeted edits to `lesson.json`**, then re-render all previews (instant). Rules that
keep the artifacts consistent:

- If the change touches shared content (story/text/phenomenon context, numbers, problem set,
  exit ticket, look-fors, vocabulary, timing of phases the observation template references),
  edit it **in `shared`** — the renderers propagate it to every artifact automatically.
- **Consistency sweep after any context/number/task change:** after editing `shared`, re-read
  every prose block in `sections` (modeling, worked examples, discussion prompts,
  differentiation, rationale) plus `student_materials.instructions` and
  `observation_template.instructions`, and update every sentence that still mentions the old
  context, names, or numbers. When you are done, no artifact may reference the replaced
  content anywhere — stale prose is the most common consistency failure.
- A change aimed at one artifact (e.g. "more workspace on the worksheet", "add a column to the
  observation grid") goes in that artifact's object (`student_materials` /
  `observation_template`) — never by forking shared content.
- Styling: `theme` fields (`primary`, `title_size`, `body_size`) apply to every artifact.
  Artifacts use minimal color so they print cleanly in black-and-white; do not set
  per-section or per-phase colors.

### 4e. Render editable Word documents (only after the teacher confirms, any subset)

```bash
pip list 2>/dev/null | grep -qi python-docx || pip install -q "python-docx==1.1.2"
python scripts/render_lesson_docx.py lesson.json -o lesson_plan.docx          # lesson plan
python scripts/render_supporting.py lesson.json --which both --format docx    # supporting two (or --which worksheet/observation)
```

Deliver the requested documents. Because every renderer consumes the same `lesson.json` with
the same theme constants, the editable copies match the previews the teacher approved.

If a script errors, fix `lesson.json` (it is almost always malformed JSON) and rerun. If file
generation fails entirely, say so clearly — do not silently fall back to a chat-only delivery.

### 4f. Fallback — bespoke generation code (exception path only)

Only if the user explicitly asks for an artifact or layout the bundled renderers cannot express
(a different document type, landscape poster, slide deck, etc.): write generation code from
scratch for that artifact. Source its content from the same `lesson.json` (especially `shared`)
so it stays consistent with the other artifacts. Tell the user this path is slower.
