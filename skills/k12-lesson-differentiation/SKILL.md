---
name: k12-lesson-differentiation
description: Adapts an existing K-12 lesson (math, ELA, science, or social studies) for students at different proficiency levels (below / at / above grade level). Do NOT load this skill when the request is only for grading, a rubric, assessment feedback, or a quiz. Triggers on explicit asks to differentiate, tier, or scaffold a lesson, and on implicit signals like "my students are at different levels" or "I have struggling and advanced students". Produces 1 teacher-facing differentiation plan + 3 student-ready tier documents in Turn 1, all rendered from one master JSON via bundled scripts (HTML previews first, editable Word documents on confirmation; shared content is written once so tiers cannot drift). Uses the Learning Commons Knowledge Graph when connected; works without it. Not for creating a new lesson from scratch (use k12-lesson-planning), forming reading groups, grading, or quizzes.
---

# K-12 Lesson Differentiation

Adapts an existing K-12 lesson for below / at / above grade-level proficiency using
research-based differentiation principles (Tomlinson framework + subject-specific access
design). Works with or without the Learning Commons Knowledge Graph connector.

"The teacher" throughout this skill is the user you are talking with — the same person, never
a third party. "Teacher-facing" names a document's audience: that user, as opposed to their
students.

---

## Step 0 — Route (silent, before anything else)

1. **Subject.** Detect math / ELA / science / social studies from the source lesson or the
   request, then read the matching reference file NOW using the `view` action on the file
   editor tool:

   - math → `references/math.md`
   - ELA → `references/ela.md`
   - science → `references/science.md`
   - social studies → `references/social_studies.md`

   **Loading the matching reference file is mandatory.** It carries the pedagogy for Steps 1
   and 3 (source-lesson identification, curriculum detection, the eight differentiation rules
   R1–R8, the document content templates, and the differentiation.json mapping).
   Differentiating without first reading the subject reference is a critical failure on par
   with skipping the Knowledge Graph.
2. **Curriculum.** The subject file's "Identify the source lesson" section includes curriculum
   detection (Illustrative Mathematics / OpenSciEd). When confirmed, use that
   curriculum's discourse language and structures in the teacher plan, per the subject file.

   **Curriculum is confirmed when:** the teacher explicitly names it, OR the uploaded source
   lesson references it (a lesson from an IM unit or an OpenSciEd unit
   counts — the upload is implicit confirmation).

   **If curriculum is NOT confirmed** (not detectable from upload or link, no explicit mention):
   never name a specific module, unit number, lesson number, or proprietary routine name anywhere
   in the output OR in any chat message — even if you recognize the routine from training.
   Paraphrase the instructional move without curriculum attribution ("a compare-strategies
   discussion", not the routine's trademarked name). This is a hard rule; violating it fails P9,
   and chat messages count. See **Copyright guardrail** (after Step 3) for the companion rule on
   verbatim reproduction.
3. **Connector.** Check whether the Learning Commons Knowledge Graph tools (e.g.
   `find_standard_statement`) are available in this conversation. This decides which path
   Step 2 takes. The skill is fully functional without the connector.

4. **State.** Before any KG call, scan the conversation and any uploaded source lesson for
state signals and store as `state`:
   - Teacher says "I teach in [state]," "I'm in [state]," or "We're in [state]"
   - Standard codes in the prompt or source lesson follow a state-specific format:
     TEKS 1xx.x.x → Texas; SOL → Virginia; OAS/PASS → Oklahoma; MA → Massachusetts;
     CA/HSS or CA/CCSS → California; other state-prefixed codes → check state
   - Source lesson URL includes a state agency domain (tea.texas.gov, etc.)

   If state found: store `state = [state name]`. Pass as `jurisdiction="<state>"` in every
   `find_standard_statement` call in Step 2. Use state framework codes (not national proxies)
   in all output.

   If state not found:
   - for science, math, or ELA, proceed with national defaults (CCSS for math/ELA, NGSS for science). Add this single footer line to the teacher plan:
   *"Standards applied using [CCSS / NGSS] — if you're in Texas, Virginia,
   Oklahoma, or another state with a distinct framework, share your state and I'll re-anchor."*
   - for social studies, ask the teacher what state they teach in before proceeding.



---

## Step 1 — Identify the source lesson

Follow the subject file's source-lesson section: Scenario A (lesson exists earlier in this
conversation — use it directly, do not re-ask), Scenario B (teacher uploads a lesson — read it
first; if unreadable, say so and ask to re-share, never silently fabricate), Scenario B2
(teacher links a lesson by URL — fetch and read it with the web fetch tool; if the fetch fails,
ask them to paste or upload; fetching completes Step 1 only — the KG calls in Step 2 are still
mandatory), or Scenario C (no source lesson present — ask the subject file's ONE question before
proceeding).

**Learner needs check (silent, runs every time):** Before generating, scan the conversation
for any mention of ELL levels, WIDA levels, IEP goal areas, 504 accommodations, or specific
student needs. If found, incorporate into the tier design — especially the Below tier.

If no learner needs are mentioned AND the pre-generation R8 ask hasn't fired (scope was already
specified), add one sentence to the FIRST response: "No specific learner needs were provided —
I've applied UDL defaults (sentence frames and vocabulary across all tiers). Share any ELL
levels, IEP goals, or specific student data and I'll adjust."

This check must run even when scope is specified. Learner variability information should be
captured before generation, not after.


---

## Step 2 — Ground in standards

**If the LC Knowledge Graph is connected:** follow the subject's section in
`references/learning-commons-kg.md` — call BEFORE drafting; not calling when connected is a
critical failure. This applies no matter how the source lesson was obtained — uploaded, pasted,
or fetched from a URL. Retrieving the lesson never satisfies this step.

**If not connected:** proceed from best knowledge and add this footer to the teacher plan:
*"Generated without the Learning Commons KG. Standard text, prerequisite grounding, and
misconceptions reflect general best practice."* Do not invent KG citations.

---

## Step 3 — The differentiation rules

Apply **all eight rules (R1–R8)** from the subject file to every differentiated lesson. The
rules are subject-specific (scaffold types, tier entry points, extension quality tests differ
by subject) but their structure is shared: output structure (R1), standard scope preservation
(R2), tier entry points (R3), below-level scaffolds with a density cap (R4), required
pedagogical infrastructure (R5), invisible modifications (R6), within-level progressive
scaffolding (R7), and scope/defaults (R8).

---

## Copyright guardrail

Always write original content. When the source lesson draws from a named curriculum (IM,
OpenSciEd), use it to understand structure, scope, task context, and standards
alignment only — never reproduce student-facing text, activity narratives, investigation
prompts, comprehension questions, or problem contexts verbatim from curriculum materials.
Each subject reference file carries a **Copyright** line with subject-specific details.

If curriculum is NOT confirmed (see Step 0.2 detection rules), never name a specific
curriculum, module, unit number, lesson number, or proprietary routine name anywhere in the
output or in any chat message — even if recognizable from training. See Step 0.2 for the
full rule (P9).

---

## Step 4 — Output (Turn 1)

Four artifacts — **1 teacher-facing plan + 3 student tier documents (below / at / above)** —
are all rendered by a bundled script from **one master `differentiation.json`**. Anything that
appears in more than one artifact (standard, problem/task set, exit ticket, vocabulary,
sentence frames, misconceptions) lives ONCE in the JSON's `shared` block and is pulled into
each document with `{"type": "from_shared", "key": …}` blocks, so the teacher plan and the
tier documents cannot drift apart — and R6 (same context, same core tasks across tiers) is
enforced structurally.

Never write layout code, never re-type content into another format, and never edit a generated
HTML/Word document directly — every change goes into `differentiation.json` and is re-rendered
(re-rendering is instant).

**Plain language with the teacher.** The machinery above is invisible to the teacher: never
mention JSON, HTML, schemas, scripts, rendering, file names (`differentiation.json`), or code
in any teacher-facing message. Say *"Here's your differentiation plan — the three tier
documents are on their way"*, not *"I've rendered the HTML preview from differentiation.json"*.
The only format words a teacher sees are **"preview"** and **"editable copy"** (the Word document).
This applies to every turn: presenting artifacts, the satisfaction ask, revision summaries,
and error messages (if generation fails, say the documents couldn't be created — not that a
script or JSON failed).

**Density rules — hard requirements for every document.** Teachers consistently flag dense
walls of text. Structure beats prose:

- A `paragraph` or `labeled` block is at most 3 sentences. Longer → split it, bullet it, or
  table it.
- Bullets are fragments — one idea each, ≤ ~15 words; never chain clauses with semicolons.
- Parallel tier content (Below / At / Above doing the same phase differently) goes in ONE
  `table` block — rows = phases or features, columns = tiers, ≤ ~25 words per cell — never
  three back-to-back multi-sentence paragraphs.
- An aside longer than one sentence (misconception watch-fors, confer prompts, deployment
  guidance) becomes its own `callout` block, not a sentence buried in a paragraph.
- Quote the standard verbatim exactly once (the target-standard callout, from `shared`).
  Everywhere else — prerequisite grounding, forward connections — reference by code plus a
  gist of ten words or fewer; never re-paste full standard text.
- A section that runs past about half a page of continuous prose must be restructured
  (table, bullets, or split into two sections) before rendering.

**Pre-write cross-check — run ALL checks before calling the render script. Do not render until every item passes.**

**O6 — Artifact alignment (both directions):**
1. **Plan → tier documents.** List every task the plan says students do — tier problems/tasks,
   exit ticket, the anchor activity, anything assigned to "early finishers." Each must have a
   printed student-facing block on at least one tier document (the anchor activity on all
   three, via `from_shared: anchor_activity`). A task that exists only as a plan description
   fails.
2. **Tier documents → plan.** For each tier document, list every printed task — each
   problem/task, the extension and each of its printed sub-parts, anything printed on one tier
   only, the exit ticket, "If you finish early," "Reflect." Each must appear in that tier's
   **Worksheet tasks** line in the plan, with its scaffold named (e.g., "P1 (tape diagram +
   sentence frame)" not just "P1"). A printed task the plan never names fails — a named
   scaffold the worksheet does not print fails — and so does a plan line naming a task or
   organizer no tier document prints.

Shared content is guaranteed by `from_shared` blocks; the check targets document-specific
blocks and plan prose. Also confirm the exact `shared.standard_code` string appears in each of
the three tier documents' `eyebrow` (`"[Grade] [Subject] · [standard_code]"`) — the standard
must be named on every tier, not only in the teacher plan. Fix mismatches before rendering.

**P8 — Flexible grouping (confirm in teacher plan JSON):**
- The `Flexible Grouping` section states the evidence or basis used to assign students to each
  tier (e.g., a specific prior exit ticket, diagnostic score, or "Default profile applied — no
  diagnostic data available"). A blank or generic statement fails.
- The section includes an explicit statement that tier assignments are revisable based on
  formative evidence from THIS lesson (not a standing ability track).

**O4 — Rationale notes (confirm in teacher plan JSON):**
- `Why this works (1)` and `Why this works (2)` sections are present and each name a specific
  tier design choice with a stated reason. Generic statements ("scaffolds help learners") fail.
  These sections are required and cannot be dropped to meet page caps — tighten other content
  instead.

### 4a. Write the complete `differentiation.json` (Turn 1)

1. Write `differentiation.json`: top-level `theme`, the **`shared` block** (write this FIRST —
   see the subject mapping for `subject`, `anchor_task`, and `problems[]`, plus the standard
   verbatim, `exit_ticket`, `vocabulary[]`, `sentence_frames[]`, `misconceptions[]`,
   `anchor_activity` (early-finisher task in student-facing second person — directions only,
   no rationale), `reflect_prompt` (the closing reflective question)), and a `documents` array
   with 4 entries: `{"id": "teacher_plan", "audience": "teacher", …}` and
   `{"id": "worksheet_below" / "worksheet_at" / "worksheet_above", "audience": "student", …}`.
   Each document's `sections` follow the subject file's document content templates.

   **Schema** — the complete field skeleton (`blocks` shows one of each type). This is
   sufficient — **do not open, cat, head, or grep the renderer scripts**:

   ```
   theme: {primary: "#…"}
   shared:
     subject, grade, standard_code, standard_text,
     anchor_task, anchor_activity, reflect_prompt, sentence_frames[]
     vocabulary[]:    {term, definition}
     problems[]:      {text, difficulty}
     exit_ticket:     {prompt, buckets[]}
     misconceptions[]:{what, why, move}
   documents[]: {id: teacher_plan|worksheet_below|worksheet_at|worksheet_above,
                 audience: teacher|student, eyebrow, title, meta,
                 sections[]: {heading, blocks[]}}
     block types:
       {type: from_shared, key, only?: int}
       {type: labeled, label, text} | {type: paragraph, text}
       {type: callout, kind: special|student-task|teacher-note|student-note, label, text}
       {type: h2, text} | {type: h3, text} | {type: list, label?, ordered?, items[]}
       {type: phase_header, name, minutes}   (science teacher plan; supported by all renderers)
       {type: table, headers[]?, rows[[]], empty_row_height_pt?}
       {type: cards, items[{title, text}]} | {type: workspace, size: small|med|large}
   ```

   (`references/example_differentiation.json` is a filled-in worked example if
   values-in-context would help, but reading it is not required.) Keep writing tight; no emoji in JSON content.
   The density rules above are hard requirements for every text field.
   **Which block when** — pick by what the content *is*, not how it should look:

   | Block | Use it for |
   |---|---|
   | `callout` `kind: special` | The one anchoring fact per artifact — the target standard. Typically once. |
   | `callout` `kind: student-task` | Any task students do: anchor task, exit ticket prompt, a tier task shown in the plan. |
   | `callout` `kind: teacher-note` | An aside the teacher reads but does not say aloud: conferring moves, a watch-for. |
   | `callout` `kind: student-note` | A reminder students read on their worksheet: sentence frames, a hint card. |
   | `list` `ordered: true` | A numbered sequence — the problem set, procedure steps. Unordered otherwise. |
   | `list` with `label` | A titled enumeration — several discrete items under one label. |
   | `cards` | 2–4 parallel items of roughly equal length — tier summaries, sort buckets. Never for long or unbalanced items. |
   | `table` (no `headers`) | Term/definition pairs, label/value reference rows. |
   | `table` with `headers` | Real tabular data with column labels (per-tier scaffolds, misconceptions). |
   | `workspace` | Student writing space; `size: small|med|large` or grade-banded default. |
   Tabular content — data tables, "complete the table" tasks, row-and-column organizers — must
   be a `{"type": "table", "headers": [...], "rows": [[...]]}` block (a row of empty strings
   renders as ruled writing space). Never draw a table inside a `text` field: markdown pipe
   rows, box-drawing characters, ASCII art, and symbol glyphs (■, □) print literally on the
   page and fail print-safety. Never write bullet characters (•, -) inside a `text` string
   — use a `bullets` block; a paragraph collapses line breaks and the bullets run together
   into one line. Use `workspace` blocks for writing space — they render as
   open whitespace sized by grade automatically (lower grades get much more room, and K–5
   prose answers get ruled lines; math work space stays open for drawing). Set `height_pt`
   only when a task needs more than the default: 130–150 for full written explanations and
   exit tickets, 90–110 for short extension questions. Empty table cells are writing space
   and get a grade-banded minimum height automatically — don't set `empty_row_height_pt`
   below ~70pt for prose rows. This applies to
   every prose field in all four documents.
2. The three tier documents (in the same `documents` array) differ ONLY in their scaffolding
   and extension blocks (R6).
   **Every tier document pulls task text with `from_shared` blocks — never re-type, reword,
   or split task text into a document's own blocks** (so the plan and all three tiers stay
   verbatim-consistent — reworded tasks drift apart in revision). Pull tasks ONE AT A TIME
   so scaffolds sit with their task:
   `{"type": "from_shared", "key": "problems", "only": 1}` renders Task 1 with its writing
   space already included (grade-sized). Other prompts students answer (the exit ticket,
   Reflect, If you finish early, a tier-only extension) are followed by a `workspace` block.
   The required order within the section is strict: for each task N — at most ONE
   scaffold block for task N (merge multiple supports into one labeled block; never two
   "Before Task N" blocks), then the task via `"only": N`. A scaffold must NEVER appear
   after its target task, and nothing sits between a scaffold and its task.
   That is how the R7 fade pattern is expressed — Task 1 gets a scaffold block, Task 2's is
   lighter, later tasks have none. A tier-only task (the Above extension, an Above-only
   sub-question) is its own headed block — never an edit to shared task text. Below-tier scaffolds follow R4; the Above-tier extension passes R7's quality
   test. Asset framing rules (below) apply to every student-facing block.

### 4b. Render all four previews — one command, same turn

```bash
bash scripts/render_all.sh differentiation.json "$OUTPUT_DIR"
```

This writes `$OUTPUT_DIR/teacher_plan.html`, `$OUTPUT_DIR/worksheet_below.html`,
`$OUTPUT_DIR/worksheet_at.html`, and `$OUTPUT_DIR/worksheet_above.html` in one invocation —
no copy step needed. Present all four to the teacher together (teacher plan first in your
message).

### 4c. The close (every output turn)

The chat message that delivers artifacts ends with three things, in order. Each must appear in
the chat message itself — saying it only inside the printed plan does not count.

1. **Learner-variability statement (first output turn, when you didn't ask).** If you never
   asked about specific learner needs in this conversation (the R8 question), state in chat
   that UDL defaults were applied and invite specifics — e.g. *"I didn't have details on
   specific learner needs, so I applied UDL defaults — sentence stems and a vocabulary
   glossary on all three tier sheets. Tell me about any multilingual learners or students
   with IEPs or 504 plans and I'll tailor further."* Skip this only when the teacher already
   gave learner information (then reflect it instead: "the Below sheet builds in the sentence
   frames for your newcomer ELLs").
2. **Three lesson-specific next steps (first output turn).** Offer 3–4 iteration options in
   chat, one short line each, specific to THIS lesson (e.g., a tiered ELD layer with
   WIDA-banded sentence frames; IEP-goal-specific scaffolds for a named goal area; a fourth
   intervention tier below the prerequisite; tightening scope to the exit ticket only). The
   subject reference's FA follow-up prompt counts as one of them when it fits.
3. **The satisfaction ask.** Ask whether the teacher is satisfied with **all four artifacts**
   or wants changes, and state that the next step is sending editable copies. Do not render them
   before they confirm, and do not skip the ask — on every output turn, including revisions.

### 4d. Revisions — one edit, every artifact stays in sync

Make **targeted edits to `differentiation.json`**, then re-render all four previews (instant).
Rules that keep the artifacts consistent:

- If the change touches shared content (context, numbers, tasks, exit ticket, vocabulary,
  sentence frames, misconceptions), edit it **in `shared`** — it propagates to the teacher
  plan and every tier document automatically.
- **Consistency sweep after any context/number/task change:** after editing `shared`, re-read
  every prose block in all four documents' `sections` and update every sentence that still
  mentions the old context, names, or numbers. No artifact may reference the replaced content
  anywhere — stale prose is the most common consistency failure.
- A change aimed at one tier (e.g. "more scaffolding for below", "harder extension") goes in
  that tier document's blocks — never by forking shared content. Scaffold changes must keep
  the subject file's R4 rules and R7 fade pattern.
- Styling: top-level `theme` applies to all four documents; per-document `theme` overrides
  stay available.

### 4e. Render editable Word documents (only after the teacher confirms, any subset)

```bash
pip list 2>/dev/null | grep -qi python-docx || pip install -q "python-docx==1.1.2"
python scripts/render_documents.py differentiation.json --format docx           # all four
# or a subset: --only teacher_plan worksheet_below
```

Because every document renders from the same `differentiation.json` with the same theme,
the editable copies match the previews the teacher approved.

If the script errors, fix `differentiation.json` (it is almost always malformed JSON) and
rerun. If file generation fails entirely, say so clearly — do not silently fall back to a
chat-only delivery.

### 4f. Fallback — bespoke generation code (exception path only)

Only if the user explicitly asks for an artifact or layout the bundled renderer cannot express
(a different document type, landscape poster, slide deck, etc.): write generation code from
scratch for that artifact. Source its content from the same `differentiation.json` (especially
`shared`) so it stays consistent with the other artifacts. Tell the user this path is slower.

### Student-facing language — ALL tier documents

Student pages never use instructional-design terminology. Those are teacher words; on a
worksheet they read as labels about the student, not for the student.

- ❌ "CER" — write the organizer labels out: *Claim / Evidence / Reasoning*. ("Write a CER"
  becomes "Explain your claim with evidence and reasoning".)
- ❌ "sensemaking check", "formative check", "misconception", "scaffold", "tier",
  "differentiation", "anchor task" — use student words: *"Check your thinking"*, *"Try this
  together"*, *"If you finish early"*.
- Scaffold prompts get a SHORT student-friendly `h3` on its own line (e.g.
  *"Observe the data first"*, *"Check your thinking"*), then the prompt as a normal
  paragraph below it — never a long bold inline label like
  "**Before Task 2 — sensemaking check:** Complete this sentence…". The subheading names
  what the student does, not the pedagogy behind it.

### Asset framing — below-tier documents

Student-facing language must not signal reduced expectations. Scaffolds appear as natural task
design, not announced supports.

- ❌ "Task 1 (Scaffolded) / Task 2 (Guided) / Task 3 (Independent)" — a student who sees these labels knows they are on the easier version.
- ❌ "Use this if you need it" / "Here is a sentence starter" — names the support as a crutch.
- ❌ Any header, label, or aside that distinguishes scaffolded tasks from unscaffolded ones.
- ✓ The organizer, annotation frame, or sentence frame simply appears as part of the task layout.
- ✓ Tasks are numbered without scaffold-level labels.
- ✓ Sentence frames at the top of the document are introduced universally: "You can use these sentence frames:" — not "Use these if you get stuck."

---

## Step 5 — Complete

The skill is complete when the teacher has confirmed the previews (4c) and received the editable copies
they asked for (4e). The closing message pairs the FA follow-up prompt from the subject
reference's R8 section with the lesson-specific next-step options from 4c.
