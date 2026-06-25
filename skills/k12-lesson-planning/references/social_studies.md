# Social Studies — lesson pedagogy

Loaded by `k12-lesson-planning` when the subject is **social studies / history**. This subject
follows the C3 inquiry arc, generates a **single lesson** positioned within a unit arc, and
**points to** primary sources rather than reproducing them.

Lessons follow the C3 Framework inquiry arc:
- Developing compelling and supporting questions — sparks curiosity and drives a unit
- Applying disciplinary concepts and tools — from civics, economics, geography, and history
- Evaluating sources and using evidence — disciplinary literacy and critical thinking
- Communicating conclusions and taking informed action — civic application

**C3 Framework note.** The C3 Framework is an *inquiry design* framework, not a standards document. Use C3 for instructional design (the inquiry arc, sourcing, argumentation, civic action), but the lesson's content scope and the verbatim standard must come from the **state** standard — never substitute a C3 dimension or indicator for the standard, and never fall back to C3 when a state standard is unavailable.

## Gather inputs

If the user has not already provided the following, ask for them before generating — collect all in one question:

- **Grade band**: K–2, 3–5, 6–8, or 9–12
- **Topic or era**: e.g., "Reconstruction," "the civil rights movement," "ancient Rome," "World War I"
- **Compelling question** (optional — you will draft one if not provided): a contestable, civically resonant question that could anchor a multi-day unit
- **Specific standard or focus skill** (optional): e.g., "causation," "sourcing," "continuity and change over time"
- **State** (required): Social studies standards are state-specific. If the teacher does not name a state and it is not inferrable, ask.

Do not ask about Taking Informed Action, multi-discipline integration, or curriculum context — those are out of scope for this skill.


## Standards grounding

Follow **Step 2 — Ground in standards** in SKILL.md: if the Learning Commons Knowledge Graph
is connected, use the Social Studies section of `references/learning-commons-kg.md`; if not,
proceed from best knowledge and add the disclaimer footer.

## Draft a compelling question (if not provided)

The compelling question must be:
- Genuinely contestable (not a yes/no or factual lookup)
- Civically or humanly resonant — students should feel it matters
- Answerable through historical evidence
- Appropriate in complexity for the grade band

Examples by grade band:
- K–2: "Why do people move to new places?" / "How do communities change over time?"
- 3–5: "Was Westward Expansion good for America?" / "What made the American Revolution possible?"
- 6–8: "Was World War I inevitable?" / "How did ordinary people shape the civil rights movement?"
- 9–12: "When is civil disobedience justified?" / "Did Reconstruction succeed or fail — and for whom?"


## Build the lesson plan

Build the lesson plan with the following sections — these become the `sections` array of the
master `lesson.json` in Step 4 — Output (one JSON section per `##` heading below; the template's
formatting hints map to renderer block types: blockquotes → `callout` blocks, bold labels →
`labeled` blocks, lists → `bullets`). Adjust vocabulary, task complexity, and source type by
grade band (see guidance below).

**For all lessons**
Include at least one visual scaffold with a teacher-facing rationale justifying the choice.

Be sure that overall timing and timing for each section is realistic - do not overload the lesson.

---

### Lesson Plan Template

```
# [Topic] — History Lesson Plan
**Grade Band:** [K–2 / 3–5 / 6–8 / 9–12]
**Discipline:** History
**Estimated Time:** [30–45 min for K–5 / 45–60 min for 6–12]
**Standard:** [Authoritative standard code + text]
**C3 Dimensions:** [list the relevant C3 dimensions touched]

---

## Compelling Question
[The unit-level question this lesson contributes to]

## This Lesson's Supporting Question
[A narrower question this single lesson investigates — one of 3–5 that would make up the full unit]

---

## Context Notes
**Lesson goal:** 1-2 distinct SWBATs
**Assumed prior knowledge:** [What students need to already know for this lesson to work — be specific]
**Unit arc position:** [Where this lesson fits, e.g., "Lesson 2 of ~5; students have already been introduced to [X]. This lesson builds toward [Y]."]
**Coherence note:** [Brief flag if this lesson depends heavily on cumulative knowledge — useful for teachers who are using this as a standalone]
**Anticipated challenges:** 2–3 misconceptions specific to this topic and source set, each formatted: *What students do* / *Why it happens* / *Teacher move*
**Rationale**: 2-3 non-negotiables specific to the lesson, each with a 1–2 sentence rationale grounded in C3 principles and the standard

---

## Background Knowledge (Teacher-Facing, ~5–10 min)
[3–5 paragraphs of substantive content the teacher delivers or assigns before source work. This is explicit instruction — not a discovery activity. Write it as teacher-facing prose, not student-facing. Include key vocabulary to introduce, core facts students need, and the conceptual frame that makes the sources meaningful.]

**Key vocabulary:** [4–6 terms with brief definitions appropriate to grade band]

---

## Source Set (2 sources)
[Do not reproduce source text. Instead, describe each source and provide a pointer to where it can be found.]

**Source 1**
- Type: [e.g., photograph, letter, speech excerpt, political cartoon, map, data table]
- Description: [What it is, who created it, approximate date, what it shows]
- Why it was chosen: [What perspective or aspect of the question it illuminates]
- Where to find it: [Collection name + URL if known, e.g., Library of Congress, SHEG/Reading Like a Historian, DBQ Project, Gilder Lehrman, National Archives. If not sure of url, give a candidate and flag with something like "suggested - verify before using"]

**Source 2**
- Type:
- Description:
- Why it was chosen:
- Where to find it:

**Source pairing rationale:** [1–2 sentences on why these two sources work together — what tension, contrast, or complementary perspective they create]

---

## Guided Analysis Questions
[5 questions total, scaffolded from lower to higher order. Adjust complexity by grade band — see guidance below.]

1. [Observation / literal comprehension]
2. [Sourcing: Who made this? When? Why?]
3. [Contextualization: What was happening at the time that helps explain this?]
4. [Corroboration or comparison: How does Source 2 confirm, complicate, or contradict Source 1?]
5. [Connection to compelling question: What does this evidence suggest about [compelling question]?]

---

## Formative Task
[A short, grade-appropriate written or spoken task that asks students to answer the supporting question using evidence from the sources. See grade-band guidance below.]

**Prompt:** [The actual student-facing prompt]
**Success criteria:** [2–3 bullet points describing what a strong response includes]

---

## Optional Extension
[One activity for students who finish early or need enrichment — should deepen the inquiry, not just add more content]
```

---

## Grade-Band Guidance

Apply these adjustments throughout the lesson:

**K–2**
- Background knowledge delivered as read-aloud or class discussion, not independent reading
- Sources: photographs, illustrations, artifacts, oral histories — avoid dense text
- Analysis questions use sentence starters and are discussed orally before writing
- Formative task: drawing + 1–2 dictated or written sentences; or a class discussion with teacher-recorded responses
- Vocabulary: 4 words max, defined with visuals or gestures

**3–5**
- Background knowledge can be a short informational text (Lexile 600–850) or teacher-led mini-lecture
- Sources: accessible primary sources with some scaffolding (sentence-level glosses on hard vocabulary); photographs and short documents work well
- Analysis questions answered in writing, with sentence frames provided
- Formative task: 1 paragraph using the claim-evidence-reasoning structure
- Vocabulary: 5–6 words; students interact with words before source reading

**6–8**
- Background knowledge as assigned reading or lecture notes; students should be able to read and annotate independently
- Sources: more complex primary sources (letters, speeches, political cartoons, data); students expected to do basic sourcing independently
- Analysis questions answered in writing without sentence frames
- Formative task: short constructed response (1–2 paragraphs), evidence-based; may include a claim + two pieces of evidence
- Vocabulary: disciplinary terms emphasized (e.g., "corroborate," "perspective," "contextualize")

**9–12**
- Background knowledge delivered via complex texts; students expected to take notes and synthesize
- Sources: challenging primary and secondary sources; students source, contextualize, and corroborate independently
- Analysis questions push toward argument construction and acknowledgment of counterevidence
- Formative task: thesis-driven paragraph or short essay; must include a claim, evidence, reasoning, and acknowledgment of complexity
- Vocabulary: discipline-specific and college-level terms assumed or quickly reviewed

## Writing lesson.json — social studies mapping

When you reach Step 4 (Output) in SKILL.md, map social studies content to the master JSON like this:

- `shared.subject`: `"Social Studies"`
- `shared.standard_code` / `shared.standard_text`: the authoritative standard, verbatim
- `shared.anchor_task`: the supporting question + the source set (each source as described in the template — type, description, why chosen, where to find it; never reproduced source text)
- `shared.problems[]`: the 5 guided analysis questions (one entry each)
- `shared.exit_ticket`: the formative task `prompt`; `buckets` = three sort entries using the standard labels *Got it* / *Almost there* / *Needs re-teaching* — derive criteria from the success criteria in the template (e.g. "Got it: thesis-level claim with two pieces of cited evidence and reasoning", "Almost there: claim present but evidence underdeveloped or reasoning implicit", "Needs re-teaching: summary only — no claim, no cited evidence"). Each bucket must be `{"label": …, "criteria": …}`.
- `shared.vocabulary[]`: the key vocabulary terms with definitions
- Artifact set: **all three** (lesson plan + student materials + observation template)
  - `student_materials`: source pointers, the guided analysis questions with answer space, and the formative task — no teacher content anywhere (no background-knowledge prose, no success-criteria rationale)
  - `observation_template`: 2 columns — *Evidence of Student Thinking* / *Instructional Move* — with look-fors drawn from the analysis questions as row labels
- Alongside the preview, briefly note: which source collection(s) likely have the recommended sources, and any coherence flag about assumed prior knowledge
