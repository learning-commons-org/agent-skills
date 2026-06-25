# Skills

Each subdirectory is a self-contained skill bundle. To install one, copy the
folder into the location your Claude environment loads skills from (or follow
your runtime's skill-installation flow).

## Catalog

### [`k12-lesson-planning`](k12-lesson-planning/)

Creates a lesson plan + student-facing materials + observation template as
native files in a single turn, rendered from one master JSON via the bundled
scripts. Routes by subject (math / ELA / science / social studies) to the
matching reference file, which carries the subject-specific pedagogy.

**Example prompts to try**

*Math*
```
I'm teaching counting money to my 2nd graders next week — dollar bills,
quarters, dimes, nickels, pennies, word problems with $ and cent symbols.
Lesson plan plus something they can practice on.
```
```
3rd grade fractions on a number line. Tomorrow. My students think 1/4 is
bigger than 1/3 and they have never seen a fraction past 1. 45 minutes.
```
```
Plan a lesson on transformation of functions for my Alg 2 class.
```

*ELA*
```
Create a 2nd grade lesson to help students write a short opinion piece about
their favorite book, with a clear reason and a closing sentence.
```
```
I need a lesson for my 7th graders on analyzing how an author develops a
central idea across two informational texts. We're in the middle of a unit
on environmental issues.
```

*Science*
```
Create a 3rd grade NGSS-aligned lesson on the life cycle of plants — I want
students to sequence the stages and explain what each plant needs to survive.
```
```
Create a lesson plan on periodic trends, especially how electronegativity
impacts bonding, for Texas high school chemistry.
```

*Social studies*
```
Create a lesson for 8th grade on the causes of the American Revolution —
I want students to evaluate which cause was most significant and back it
up with evidence. We're in Texas.
```
```
I need a lesson for 4th grade on how geography influenced where early
communities settled in California. We're about halfway through our state
history unit.
```

---

### [`k12-lesson-differentiation`](k12-lesson-differentiation/)

Adapts an existing K-12 lesson for below / at / above grade-level proficiency.
Produces 1 teacher-facing differentiation plan + 3 student-ready tier
documents in a single turn, rendered from one master JSON so shared content
cannot drift across tiers.

Works best when you attach or link the source lesson; if you don't, the skill
will ask for it.

**Example prompts to try**

*Math*
```
Differentiate this 2nd grade addition and subtraction lesson for students
below / at / and above proficiency level. [attach or link the lesson]
```
```
Differentiate this Algebra 2 transformations of functions lesson for
students below / at / and above proficiency level. [attach or link]
```

*ELA*
```
Differentiate this 7th grade central-idea-across-informational-texts lesson
for students below / at / and above proficiency level. [link]
```
```
Differentiate the attached 2nd grade informational writing lesson for
students below / at / and above proficiency level.
```

*Science*
```
I'm in Florida. Differentiate this lesson on forces & motion. [attach or link]
```
```
Differentiate this 10th grade natural selection lesson for students below /
at / and above proficiency level. [link]
```

*Social studies*
```
Differentiate this 8th grade causes-of-the-American-Revolution lesson for
students below / at / and above proficiency level. [link]
```
```
Differentiate this 11th grade Great Migration lesson for students below /
at / and above proficiency level. [link]
```

## Knowledge Graph

Both skills can optionally call the Learning Commons Knowledge Graph to ground
standards, prerequisites, misconceptions, and curriculum context. Both skills
are fully functional without the connector — they fall back to general best
practice and add a footer noting the absence.
