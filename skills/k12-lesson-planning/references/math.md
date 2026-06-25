# Math — lesson pedagogy

Loaded by `k12-lesson-planning` when the subject is **math**.

## Clarify (one question max)
Before asking anything, assess the following from all available conversation signals:

**1. State detection** Scan the conversation for any state signal — teacher mentions a state name, uses state-specific codes (TEKS, SOL, OAS, CA-CCSS, etc.), or says "I teach in [state]." If found, store as state = [state name] and pass it as jurisdiction in the KG standard lookup. Update the default standard framework to match.

**2. Curriculum detection.** Before asking anything, determine whether the teacher is likely using IM (Illustrative Mathematics) curriculum. Look for signals anywhere in the conversation — not just the current prompt: explicit name ("IM", "Illustrative Mathematics", "IM 360"), IM-specific terminology (MLRs, cool-down, "Stronger and Clearer Each Time", IM unit or lesson references), or context that makes IM use probable. If signals are present, treat as **IM-confirmed** and proceed. If absent, treat as **not IM-confirmed**.

Then ask at most ONE question. Priority: (1) grade level if missing, (2) topic if missing, (3) curriculum if not inferable, (4) state if not inferable. Infer everything else. Defaults applied silently: 45–60 min, universal access design, CCSS (overridden by the detected state's framework when State Detection finds one).

---

## Standards grounding

Follow **Step 2 — Ground in standards** in SKILL.md: if the Learning Commons Knowledge Graph
is connected, use the Mathematics section of `references/learning-commons-kg.md`; if not,
proceed from best knowledge and add the disclaimer footer.

## Build the lesson

**For all lessons**
Include at least one visual scaffold with a teacher-facing rationale justifying the choice.

Be sure that overall timing and timing for each section is realistic - do not overload the lesson.

### Curriculum branching — apply before drafting

**If IM-confirmed:**
Use **Launch → Explore → Discuss → Synthesize → Exit Ticket** exactly. Apply IM-specific features:
- Discourse: *Compare and Connect*, *Stronger and Clearer Each Time*, *Think-Pair-Share*
- MLRs: use KG recommendations; otherwise default to MLR 2 (Collect and Display) in Explore, MLR 7 (Compare and Connect) in Discuss, MLR 8 (Discussion Supports) for sentence frames
- Name 2–3 SMPs verbatim in Section 1; keep tone teacher-friendly, not academic

**If not IM-confirmed:**
Use **Launch → Explore → Discuss → Synthesize → Exit Ticket** (problem-based). Do NOT use IM-specific terminology: no MLR names, no *Compare and Connect*, no *Stronger and Clearer Each Time*. Use Think-Pair-Share and Turn-and-Talk.
- **K–2**: CGI — Explore must include at least one start-unknown and one change-unknown problem; exit ticket must target start-unknown or change-unknown; no strategy modeling before student attempt
- **3–5**: Problem-based, gradual release; array/area models in Discuss
- **6–8**: Problem-based; ratio tables, double number lines, coordinate graphs
- **9–12**: Mathematical modeling; formalize notation in Synthesize, not Launch

### Problem set — structural variety is required, not optional

Before writing `shared.problems`, ENUMERATE the standard's structural cases — the full span
from the baseline case (the one every student must clear) to the structurally hardest case
(the one students most often get wrong: start-unknown for K–2 story problems; a product
smaller than both factors for decimal multiplication; the missing-leg case for the
Pythagorean theorem; a midpoint or just-below-boundary number for rounding; a
linear-but-not-proportional relationship for proportionality; and so on for other
standards). Then write the set so EVERY enumerated case is a numbered, required problem (or
the exit ticket), with its case named in that problem's `situation` tag.

Coverage rules:
- A structural case that appears only in prose — the SWBAT, an anticipated challenge, a
  teacher move, or the Discuss notes — does NOT count as covered. If the plan's prose names
  a case, a numbered problem must present it to students.
- Emphasizing the hardest case never licenses dropping the baseline case: a set of all-hard
  problems fails coverage exactly as a set of all-easy ones does.
- The standard's number domain is part of the variety: if the standard or SWBAT says
  rational numbers, at least one required problem uses fractions or decimals —
  whole-number-only sets do not cover it.
- Never relegate a required structural case to an optional extension or bonus — if it only
  appears as a challenge add-on, most students never meet it.

### Section structure — both paths

1. **At a Glance** — standard verbatim in a `special` callout (the ONE verbatim quote — everywhere else standards go by code + ≤10-word gist); materials; SMPs named
2. **Learning Goal** — Big Idea (enduring understanding, 1 sentence); SWBAT; Prerequisite (prior standard verbatim + 1 sentence on prior knowledge assumed)
3. **Vocabulary & Anticipated Challenges** — 3–5 key terms with brief definitions; 2–3 misconceptions each as: *What students do* / *Why it happens* / *Teacher move*
4. **Rationale** — 2–3 non-negotiables teachers must preserve, with brief rationale for each
5. **Lesson Sequence** — phases per curriculum branch above; **Discuss gets at least 10 minutes** (in a short warm-up-style request, shrink the other phases, not Discuss); in Explore: 3+ look-fors each naming the student response, why it matters, and what to do with it — and if the anchor task admits more than one correct response or equation, one look-for must say so explicitly so the teacher accepts all of them; in Discuss: at least one named student-to-student talk move (Think-Pair-Share, Turn-and-Talk, partner compare, agree/disagree) + specific discourse prompts (not generic) + 2–3 sentence frames

## Exit ticket guidance

The exit ticket is the last phase in Lesson Sequence (`from_shared:exit_ticket` under its phase header). It IS the **structurally hardest enumerated case** (from the problem-set enumeration above; K–2: start-unknown or change-unknown), never a mid-difficulty stand-in. Pick it with the **misconception test**: a student who holds the lesson's primary anticipated misconception must get the exit ticket WRONG. If that student would get it right, you picked an affirming instance — swap it for the discriminating one (a lesson distinguishing X from not-X exits on the not-X case; a lesson fixing a placement habit exits where that habit produces a wrong answer). Write the case's name into `shared.exit_ticket.case` using the same wording as the matching problem's `situation` tag. 3 sort buckets — *Got it* / *Almost there* / *Needs re-teaching* — **each with explicit criteria** describing what a response in that bucket contains (e.g. "Got it: correct equation with the unknown where it lives in the story", not the bare label); all three criteria appear in the lesson plan, never truncated to labels.

---

## Writing lesson.json — math mapping

When you reach Step 4 (Output) in SKILL.md, map math content to the master JSON like this:

- `shared.subject`: `"Mathematics"`
- `shared.anchor_task`: the anchor task / launch problem
- `shared.problems[]`: the practice problem set (with `difficulty`; multiple-choice items get a `choices[]` array)
- `shared.exit_ticket`: the exit ticket prompt + the three sort buckets, each bucket as `{"label": …, "criteria": …}`
- `shared.smps`: the 2-3 Standards for Mathematical Practice, named verbatim
- Artifact set: **all three** (lesson plan + student materials + observation template)
- Worked example: `references/example_lesson.json`
