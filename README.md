# Learning Commons Agent Skills

Instructional agent skills + the evaluations rubrics used to help develop and grade their outputs.

This repo serves two audiences:

- **You want to install a skill in your Claude environment.** Head to
  [`skills/`](skills/). Each subdirectory is a self-contained skill bundle
  (instructions + reference docs + bundled scripts) that can be installed
  directly without anything else in this repo.
- **You want to grade a skill's output yourself.** Head to [`evals/`](evals/).
  It contains the rubric CSVs each skill is graded against, plus the
  LLM-as-judge prompt that consumes them. You can run the same grading process
  against your own outputs in your own harness.

## What's here

| Path | Contents |
|------|----------|
| [`skills/`](skills/) | Publishable skill bundles. One folder per skill. |
| [`skills/README.md`](skills/README.md) | Skill catalog + example prompts to try each skill on. |
| [`evals/`](evals/) | Rubrics and judge prompt — grading materials, not a runnable harness. |
| [`evals/README.md`](evals/README.md) | How the rubrics work + the LLM-as-judge prompt + the Conditional column. |

## Skills

| Skill | What it does |
|-------|--------------|
| [`k12-lesson-planning`](skills/k12-lesson-planning/) | Creates a lesson plan, student-facing materials, and observation template for math, ELA, science, or social studies. |
| [`k12-lesson-differentiation`](skills/k12-lesson-differentiation/) | Adapts an existing K-12 lesson for below / at / above grade-level proficiency. |

## License

See [`LICENSE`](LICENSE).
