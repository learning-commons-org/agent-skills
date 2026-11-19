# Using data: k12-fixing-lesson-plans

When the Learning Commons Knowledge Graph tools are connected, the claims below come from them,
not recall. Each entry's Fallback applies whenever its data isn't there: the tools aren't
connected, or a tool returns nothing, including for a subject, grade, or curriculum it doesn't
serve. The skill still runs either way.

## Standards text

- **Tools:** `find_standard_statement`, called with each standard code the lesson cites or the
  teacher names.
- **Grounds:** the full text of each cited standard and its sub-standards, used to judge whether
  the lesson teaches the whole standard or part of it, whether a skill the lesson claims appears
  in any cited standard, and whether a task demands more than the standard asks.
- **Why:** lessons quote and label standards selectively, and a printed label is a claim to
  test, not a fact to repeat. Without the full text, the audit compares a code to a code and
  can't catch half a standard being called a whole lesson.
- **Extract:** for every cited standard, its code and full statement text, plus each
  sub-standard's code and text, all verbatim. The lesson's own quotation of a standard is part
  of what is audited; standard text the teacher supplies separately wins over the returned text
  where the two differ.
- **Fallback:** the lesson's printed wording or general knowledge; the standard text is
  unsourced.

## Rigor bar for the grade

- **Tools:** `find_learning_components_from_standard`, for each cited standard.
  `find_standards_progression_from_standard`, called with `direction` `backward` and again
  `forward`, for each cited standard.
- **Grounds:** the standard's learning components, used to judge which parts of the standard
  the lesson's highest-demand task reaches. The standards just before and after it in the
  progression, used to judge whether that task's demand sits at, below, or above the grade.
- **Why:** judging whether the highest-demand task meets the standard needs a fixed bar for that
  demand at that grade. Without one, the audit rebuilds the bar from its own reading each time,
  so rigor findings drift from run to run and can't serve as a standard a coach would trust.
- **Extract:** every learning component for each cited standard, verbatim. From each
  progression direction, the code and statement text of each returned standard, verbatim; on a
  partial match, also the learning components returned with each one.
- **Fallback:** the bar comes from the standard text alone (from the standards text entry),
  with progression neighbors from general knowledge; both are unsourced.

## Documented misconceptions

- **Tools:** `find_misconceptions_for_standard`, with `subject` `Mathematics`, for each cited
  standard.
- **Grounds:** the documented misconceptions for each cited standard, used to judge whether
  the lesson's tasks and checks anticipate how students go wrong, and to tie each
  recommendation to a named pattern.
- **Why:** "add a reasoning task" is generic advice; naming the misconception the missing task
  would leave unaddressed gives the teacher a targeted revision.
- **Extract:** each misconception, rewritten in a sentence, with its source. From approximate
  matches, only those whose matched construct fits the standard.
- **Fallback:** misconceptions from general knowledge; each is predicted, not documented.
