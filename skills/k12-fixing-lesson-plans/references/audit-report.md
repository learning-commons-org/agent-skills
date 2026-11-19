# Writing the audit file and the revised lesson file

## Section order, and the distinct work each section does

The order is the main design choice here. A teacher reading under time pressure gets the biggest
thing first, and no section repeats a section above it.

1. **Verdict — one sentence.** Use as-is / use with the fixes below / rework before it reaches
   students, naming the single biggest finding. This is the sentence a teacher reads if they read
   nothing else, so it opens the file rather than closing it. A "net assessment" parked at the
   bottom of a long write-up is the sentence they needed and didn't reach.
2. **Two-minute summary.** Only what the verdict sentence did not already say, as a few bullets:
   - the findings at each severity, said in plain words with their numbers, so the teacher knows
     what each one is about and where to find it before reading any of them;
   - the one fix to make in the next ten minutes, by finding number;
   - what can wait for the next planning block, by finding number.
   Restating the verdict in fresh words spends the reader's first two sentences and returns
   nothing new.
3. **What was checked.** Scannable, not prose, and in three parts:
   - *Lesson and standard:* lesson identifier and grade, plus the standard code with the standard
     text quoted once in a block. The standard's language appears once in the file. Findings below
     point back to it ("the standard's *construct an argument*") instead of re-quoting it.
   - *Lens coverage:* a checklist naming every lens in `audit-lenses.md` (alignment, rigor ceiling,
     instructional arc from opening through closing, evidence of learning, range of proficiency,
     misconceptions, practicality), each marked examined or not examined, with a short reason for
     any not examined. Without this list, an audit that skipped the opening or the access check
     reads as complete.
   - *Sources:* each source consulted and how. For example, a tool call returned the standard text,
     a web search returned the progression, or the misconceptions came from general knowledge because
     no lookup was available. Unreachable sources are listed too. When the standard text wasn't
     retrieved, each standard-dependent finding carries "unverified against standard text — confirm
     before acting." A remembered standard reads as confident and is often subtly wrong, which
     leaves the teacher nothing to check it against.
4. **Findings, highest severity first.** Substantive findings come before timing and formatting
   notes, however cheap the formatting fix is. Substantive here means alignment, rigor, evidence,
   and access. Findings are numbered in this order, starting from Finding 1, and the number is
   the finding's one name everywhere it is referred to: the summary, the fix plan, and the revised
   lesson's change marks. Each finding uses the shape in the pattern below, number first.
5. **Fix plan — one table.** One row per fix, with these columns: the fix (short name), the number
   of the finding it answers, its impact (the severity tag), the teacher effort to put it in place
   (minutes of prep, and whether the period's timing changes), and whether it is core or optional.
   Order the rows by impact, then by effort. A teacher with twenty minutes before class picks from
   this table. Effort notes scattered through the findings make her rebuild it herself. A fix is
   known by its short name and the finding number it answers; it carries no number of its own, so
   the file has one numbering, not two.
6. **Revised lesson — pointer.** One line naming the revised lesson file (`revised-<lesson-slug>.md`)
   and stating that every fix in the table is written into it. The lesson itself lives in that
   file, not here. See "The revised lesson file" below.
7. **Open questions.** Decisions only the teacher can make, each stated as a question with the
   options and a recommended default — not as a request for permission to continue working.

## The revised lesson file

This is the document the teacher teaches from, so it reads as a lesson plan, not as an audit.

- **The whole lesson, every fix in place.** Carry untouched sections over in the plan's own words
  and order. A carried-over section holds its full text — the prompts, sample responses, tables,
  directions, and timings the original gives — so the revised file replaces the original and she
  teaches from one document. Where parts of the plan weren't supplied in full (a referenced page,
  a handout not included), keep each part's place in the sequence and name what belongs there. A
  set of revised excerpts still leaves her stitching the lesson back together.
- **Bare change marks.** Mark each changed or added passage with a tag like **[Revised — Finding 2]**,
  where the number is the audit's finding number, and nothing more. The reasoning behind a change
  (why it matters, what it fixes, what the other fixes depend on) belongs in the audit.
  Explanatory prose inside the lesson is text she has to delete before handing it to a co-teacher
  or a sub.
- **A short header.** Lesson title, grade, standard code, a credit line for the original source,
  and the name of the audit file the marks refer to. No findings, fix table, or open questions.

## Tone

Write it the way a coach says it out loud to a colleague whose work they respect: the plan's author
is a professional who ran out of time, not a suspect. Point at the plan rather than the planner
("the closing question asks students to summarize, so it won't show who can justify" rather than
"you failed to assess the objective"). Where a part of the lesson is genuinely strong, say so once
and specifically. That tells the teacher what to protect while they fix the rest. Findings stay
direct; the honesty is the respect.

## Pattern to imitate — one finding

> ### Finding 1 · [Blocks the objective] Students never revise their model
>
> **In the plan:** The Explore task (p. 2, 15 min) asks students to "draw a model showing where
> the water went." The closing has them "share their drawing with a partner." No step asks a
> student to change a drawing.
>
> **Why it costs learning:** The standard asks students to *develop a model to describe* the
> interaction. The demand sits in the revision, where a student meets evidence their first
> drawing can't explain. As written, a student who draws evaporation as "the water disappears"
> leaves with that idea intact, and that is the documented misconception for this skill.
>
> **Fix:** After the partner share, add 5 minutes and project this prompt as written: "Your
> partner's drawing shows something yours doesn't. Add it to yours, or write one sentence saying
> why you disagree — say what the water is made of in your sentence." Collect the drawings. An
> added arrow or label, or a written disagreement, shows a student reasoned; an unchanged drawing
> marked "we agreed" shows the check didn't run. A student whose first drawing already shows
> particles leaving the surface gets the harder case instead of a second partner: "Your model
> explains the open cup. Show what the same water does in a sealed jar, and say why the two differ."
> Expect wording like "it's still water but the tiny bits are in the air, and in the jar they bump
> the lid and come back." This replaces the second share round (p. 3), so the period is unchanged,
> and the revision step is core for everyone. The sealed-jar version is the top-end version of it,
> not an optional add-on.

That shape carries everything a finding needs: its number, severity, the quoted location, the
standard's own language used once, the misconception at stake, paste-ready wording, the harder
version for a student who already meets the target, expected student language, the discriminator
between reasoning and repetition, what it displaces, and whether it is core or optional.

When a fix leans on text the plan doesn't contain (a primary source, a passage, an excerpt, a
data table), the excerpt itself goes in the file at the length students will read, quoted from the
actual source rather than named or summarized, with its citation. A teacher handed only a title
still has the whole search in front of them, and an excerpt written from memory is the kind of
confident near-miss they have no way to check.
