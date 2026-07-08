# Skills

This directory contains Learning Commons' agent skills for K-12 education — each one packages the instructions, references, and guardrails an AI agent needs to reliably complete a specific teaching workflow, like planning a standards-aligned lesson or differentiating it across proficiency levels.

These skills are one part of Learning Commons AI developer tools for education. They are designed to be cross-platform and model-agnostic, and they produce stronger, better-grounded results when paired with Learning Commons [Knowledge Graph](https://github.com/learning-commons-org/knowledge-graph) — which supplies the standards, curriculum, learning progressions, and learning science datasets the skills draw on.

## **Available skills**

| Skill | What it does |
| :---- | :---- |
| [k12-lesson-planning/](k12-lesson-planning/) | Builds classroom-ready, standards-aligned lesson plans, optionally aligned to a teacher's curriculum. |
| [k12-lesson-differentiation/](k12-lesson-differentiation/) | Adapts an existing lesson into tiered versions (below / at / above proficiency-level) and for specific student needs, keeping core content consistent across tiers. |

Each skill folder includes its own instructions (`SKILL.md`). See [example-prompts.md](example-prompts.md) for example prompts that exercise each workflow.

## **Installation**

```shell
npx skills add learning-commons-org/agent-skills
```

> **Note for Claude Code:** if your project doesn't have a `.claude/` directory yet, run `mkdir -p .claude` before installing.

## **How the skills work**

The skills are grounded in Learning Commons [Knowledge Graph](https://github.com/learning-commons-org/knowledge-graph) through a set of MCP tools that let the agent resolve standards, understand their more granular learning components, trace learning progressions, and find aligned curriculum lessons and common misconceptions. When Knowledge Graph is unavailable, the skills still run and fall back to the model's general knowledge — but outputs grounded in Knowledge Graph are more accurate and better aligned to specific state standards.

## **Pedagogical foundations**

These skills don't just generate plausible-looking materials — they're grounded in research-backed principles and refined with expert practitioners. Every skill is anchored in:

* **Pedagogical principles**, to ensure the output reflects sound instructional design: standards alignment, prerequisite and forward connections, appropriate instructional model, discourse structures, attention to student struggle, and visual/representational choices.  
* **Rigor**, to ensure the output maintains grade-level cognitive demand.  
* **Usability**, to ensure that outputs are classroom-ready. Artifacts default to universal design, and teachers who want to adapt have a principled basis for knowing what to preserve.