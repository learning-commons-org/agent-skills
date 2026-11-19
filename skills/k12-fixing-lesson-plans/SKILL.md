---
name: k12-fixing-lesson-plans
description: "Audit a K-12 lesson plan against the standards it cites — name specific instructional shortcomings, rank them by severity, explain what each costs student learning, and save two files: a teacher-ready audit with paste-ready fixes, and a separate ready-to-teach revised lesson."
---

# K-12 Fixing Lesson Plans

This is the check a teacher runs when a lesson feels slightly off and there is no time to
rebuild it, and the check a coach runs before materials reach a classroom. It exists to catch
what a quick read misses: half a standard called a complete lesson, a "differentiated" version
that quietly lowers the ceiling, a task that never asks a student to revise their thinking.

## What the run produces

Two files, both written to disk before the final reply (Markdown unless the user asks for
something else), both named for the lesson:

- `audit-<lesson-slug>.md` contains the verdict, findings, fix plan, and open questions. The teacher
  reads it once to decide what to change.
- `revised-<lesson-slug>.md` contains the whole lesson with every fix written in place. The teacher
  opens it every time she teaches the lesson and can hand it to a co-teacher or sub as it is. Its
  change marks point back to the audit's numbered findings. Every explanation of why a change was
  made stays in the audit.

They are separate files because they do separate jobs at separate times. A revised lesson
embedded in the audit has to be cut out and cleaned up before anyone can teach from it.

The final chat message is short: the verdict sentence and a pointer to each file, not a second
copy of the audit.

A run that describes findings and fixes in chat and then asks whether to export them has done
all the work and delivered nothing the teacher can keep, print, or forward. Where scope is
genuinely uncertain, write both files with the analysis that exists and name the open question
inside the audit. The question comes after the artifacts, not instead of them.

## Workflow

1. **Read the actual lesson.** Judge the plan's own words: objective line, task prompts,
   question wording, timings, materials, assessment. Quote or locate whatever you are judging so
   the teacher can find it in their own copy. Where the plan cites something it does not contain
   (a standard code, a textbook page, a rubric, a prior lesson), treat that citation as a claim to test.
2. **Look up the standards before judging alignment or rigor** → `references/using-data.md` for
   which claims come from Learning Commons data, the tool for each, and what to do when it isn't
   there. Standard text, learning components, progression neighbors, and documented
   misconceptions are lookup-dependent. They count as sourced only when a tool call or web search
   in this run actually returned them. When no lookup ran or none succeeded, the same claims come
   from general knowledge, and the file labels them that way ("predicted misconception," "progression
   from general knowledge"). Presenting them in the vocabulary of a database that was never queried
   gives the teacher a citation with nothing behind it.
3. **Run the lenses and assign severity** → `references/audit-lenses.md`. Keep track of which lenses
   you examined and which you didn't, because the file reports both.
4. **Draft fixes, then audit the fixes** against your own findings and against their own arithmetic.
   Each fix arrives carrying the material it names, answers both ends of the range, and has model
   answers checked against the task's own conditions. See "Drafting fixes that survive their own
   audit" in the same file.
5. **Write the audit file** → `references/audit-report.md` for section order, tone, and a worked
   finding to imitate. The audit file contains the lens coverage checklist and one effort-and-impact
   table of fixes.
6. **Write the revised lesson file** → "The revised lesson file" in `references/audit-report.md`.
   It holds the whole lesson with every fix in place and bare change marks.
7. **Reply short**, pointing at both saved files.

## Reference files

| For | Read |
| --- | --- |
| Which claims come from Learning Commons data, the tool for each, and what to do without it | `references/using-data.md` |
| The lenses, the severity scale, and how to draft fixes that don't reintroduce flagged gaps | `references/audit-lenses.md` |
| The audit file's section order, tone, a worked finding to pattern-match, and the revised lesson file | `references/audit-report.md` |
