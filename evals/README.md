# Evals

This directory contains evaluation rubrics and manual setup instructions for the K-12 teacher
skills published in this repository. They were developed jointly by **Learning Commons** and
**Anthropic** as part of a shared commitment to transparent, field-grounded quality standards
for AI in K-12 education. This is part of a larger eval harness that we plan to publish in full
at a later date.

The goal is AI-generated instructional materials that are **defensible by default** — where
every output traces back to validated academic standards, learning science research, and
high-quality instructional materials, not an approximation of them.

The rubrics are designed to be used as LLM-as-judge prompts, though the underlying criteria can
be applied by human evaluators or adapted for deterministic scoring. We publish them openly so
that other developers, researchers, and AI-in-education practitioners can inspect our standards,
reuse them, and help improve them. This is a living framework: the criteria here are grounded in
extensive literature review and expert input, and we intend to revise them as the field learns
more – we eagerly hope for your feedback.

---

## Evals directory structure

```
evals/
├── README.md                       ← you are here
├── k12-lesson-planning/
│   └── rubrics/
│       ├── shared.csv               # core criteria applied to all lesson plan outputs
│       ├── math.csv                 # math-specific criteria
│       ├── ela.csv                  # ELA-specific criteria
│       ├── science.csv              # science-specific criteria
│       └── social_studies.csv       # social studies-specific criteria
└── k12-lesson-differentiation/
    └── rubrics/
        ├── differentiation.csv      # criteria for tiered differentiation outputs
        └── clarifying_question.csv  # scorer for model clarification behavior
```

---

## How to use these rubrics

Each rubric is a CSV with the following fields:

| Field | Description |
| ----- | ----- |
| `ID` | Unique criterion identifier (e.g., `P1`, `R3`) |
| `Bucket` | Top-level category: `P` (Pedagogy), `R` (Rigor), `O` (Output/Formatting), or `M` (Model Scaffolding) |
| `Criterion` | Short name for the criterion |
| `What pass requires` | The specific, scoreable condition that constitutes a pass |
| `Notes` | Rationale or design notes (not shown to the judge) |
| `Conditional` | If non-empty, the criterion applies only when this tag is active for the run (e.g., `K-5-CGI`, `Gr8+-argument-writing`) |

For lesson plan generation, apply `shared.csv` first, then layer in the relevant
subject-specific file. Subject-specific criteria extend the shared set. For a 7th grade ELA
lesson, you'd score against `shared.csv` + `ela.csv`. `ID`s are unique across the files you
compose for a single run, so the judge sees one flat list of criteria.

Conditional criteria (marked in the `Conditional` column) apply only when the specified tag is
active for the run. For example, `K-5-CGI` applies a Cognitively Guided Instruction number-talk
criterion to K-5 math only; `Gr6-12-quantitative-data` applies a quantitative-reasoning criterion
to grade 6-12 science only. If the condition isn't met, the criterion is skipped (not failed). If
you don't carry conditional metadata in your runner, the safe default is to treat all non-empty
`Conditional` rows as inactive — i.e., grade against only the unconditional rows.

Criteria score independently — a failing `R2` tells you something specific about cognitive
demand, not just that the output is "bad." Depending on your situation, consider tracking
per-criterion pass rates across a prompt suite rather than relying on aggregate scores, since
aggregate pass rates can mask meaningful gaps.

### Running as LLM judge

You'll have to do some manual setup to use the rubrics, or you can feed them into an existing
eval harness you have running.

1. Start with a set of lesson materials (you can utilize the skills in this repo to generate a
   new set).
2. Pass the lesson materials, the model's final chat response, and the associated rubric CSVs
   (you might want to compose multiple) to an LLM along with an LLM-as-judge prompt that
   instructs the model to score the materials as pass/fail (`true`/`false`) against each
   criterion.

Each criterion is judged against one of two sources, which you derive from its `Bucket`:
`M`-bucket criteria are judged against the model's chat response (`source: chat`); every other
bucket is judged against the produced documents (`source: documents`). Pass that `source` to the
judge alongside each criterion.

You can utilize this system prompt to setup your LLM as judge:

```
You are a rigorous educational content evaluator. Your job is to assess whether
AI-generated lesson plan documents meet specific rubric criteria.

You will receive:
  1. The lesson-plan documents as attached files.
  2. The model's final chat response (the text it sent back to the user).
  3. A rubric with criteria and the source each criterion should be judged against.

Grading rules:
  - Criteria whose "source" is "documents" must be judged solely against the
    attached document files. Do NOT pass a document criterion based only on a
    claim made in the chat response — the content must actually be present in
    the documents.
  - Criteria whose "source" is "chat" must be judged against the chat response.
  - Pass means the criterion is clearly and fully met. Fail means it is absent,
    incomplete, or only partially met.

Respond ONLY with a valid JSON array — no preamble, no markdown fences, no
trailing text. Each element: {"id": "...", "pass": true|false,
"explanation": "one sentence"}.
```

---

## The P/R/O/M framework

All criteria fall into one of four buckets. The buckets reflect two paired goals: **quality**
(does the output reflect strong pedagogy and appropriate rigor?) and **usability** (is the output
formatted and scaffolded in a way that a real teacher can actually use it?).

### P — Pedagogy

Pedagogy criteria evaluate whether the output reflects sound instructional design: standards
alignment, prerequisite and forward connections, appropriate instructional model, discourse
structures, attention to student struggle, and visual/representational choices. These are the
criteria most directly grounded in curriculum research and learning science.

Key pedagogical commitments threaded through the P criteria:

* **Curriculum coherence.** Skills should help teachers work within their adopted curriculum.
  When a teacher uses a high-quality instructional material (HQIM), outputs should be coherent
  with that curriculum's design logic.
* **Discipline-specific instructional models.** The rubrics branch by subject. Math rubrics
  measure full standards coverage and student discourse. ELA rubrics are grounded in the science
  of reading and look for any unsupported practices that should be removed from lessons. Science
  rubrics require inquiry, writing, and quantitative reasoning. Social studies rubrics focus on
  sourcing and argumentation.
* **Anticipating struggle.** Rather than only naming "misconceptions" (which implies incorrect
  beliefs), P criteria require attention to *points of difficulty* more broadly: patterns, why
  they arise, and teacher moves for each. Generic "some students may struggle" language fails.

### R — Rigor

Rigor criteria evaluate whether the output maintains grade-level cognitive demand. R criteria are
designed to catch any downward drift in the intellectual work students are asked to do.

Three specific checks:

* **Grade-level access for all students.** No materials simplify below the standard's cognitive
  demand without a scaffold that preserves the core challenge. Access supports are additive, not
  reductive. This applies across tiers in differentiated materials — below-level materials
  include the full standard, including its hardest cases, with scaffolding, not a simplified
  version of the task.
* **Critical thinking demanded.** At least one task or prompt must require students to explain
  reasoning, evaluate a strategy, or connect representations, not just produce a correct answer.
* **Student agency.** Student-facing materials must include at least one open-ended or reflective
  prompt, not only guided or structured practice.

### O — Output/Formatting

Output criteria evaluate the artifact itself: correct file structure, appropriate length,
teacher- vs. student-facing separation, universal design features, and teacher rationale notes.
These exist because a pedagogically strong lesson plan that is too long, confusingly formatted,
or missing student materials has limited real-world utility.

One criterion worth calling out: **designed for teacher adaptation.** Teacher-facing outputs
should explicitly note which elements are non-negotiable (curriculum sequence, grade-level
demand, discourse structure) and why — so teachers who want to adapt have a principled basis for
knowing what to preserve.

### M — Model Scaffolding

Model Scaffolding criteria evaluate the model's conversational behavior, not the artifact
content: whether it asks for missing information before generating, whether it proactively
produces student-facing materials without re-prompting, and whether it offers meaningful
follow-up options at the close of Turn 1.

---

## Data dependency

These skills depend on Learning Commons' Knowledge Graph (KG) — a curated, structured dataset of
academic standards, learning progressions, misconceptions, and high-quality instructional
materials. Rubric criteria that reference specific KG-sourced content (e.g., standard
progressions, IM misconceptions, learning components) will require KG access to score accurately
against real model outputs. To get set up with the Learning Commons MCP, [see
here](https://learningcommons.org).

---

## Contributing and feedback

We developed these rubrics through literature review, expert review, and iterative testing
against real model outputs — but this work is not finished. We know of specific areas where the
rubrics are still developing (e.g., ELL scaffolding precision, social studies sourcing criteria,
K-2 foundational literacy). We also expect the rubric to evolve as AI capabilities and the
education field's understanding of AI quality both mature.

We welcome:

* **Bug reports** — a criterion that is ambiguous, unscorable, or fires incorrectly
* **Coverage gaps** — pedagogical priorities we've missed
* **Subject-specific input** — particularly from curriculum authors and content-area specialists
* **Reuse and adaptation** — if you adapt this rubric for another context, we'd love to know

We want to hear from you. For questions or feedback, please open an issue or reach out to us at
support@learningcommons.org.
