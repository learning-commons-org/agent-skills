<img style="width:100%" alt="Knowledge Graph banner logo" src="https://raw.githubusercontent.com/learning-commons-org/.github/refs/heads/main/assets/agent_skills_hero.jpg" />

## **About Agent Skills**

Agent Skills are open, ready-to-use skills that help AI assistants produce high-quality, standards-aligned K-12 teaching materials. Each skill packages the instructions, references, and guardrails an agent needs to reliably complete a teacher workflow — so the same task produces consistent, classroom-ready results.

The skills are developed to be grounded in learning science and leverage Learning Commons [Knowledge Graph](https://github.com/learning-commons-org/knowledge-graph). They are built to be cross-platform and model-agnostic: usable with any agent runtime that supports the open skills format.

Use cases include:

* **Lesson planning**: Builds classroom-ready, standards-aligned lesson plans, optionally aligned to a teacher's curriculum.  
* **Lesson differentiation**: Adapts an existing lesson into tiered versions (below / at / above proficiency-level) and for specific student needs, keeping core content consistent across tiers.

Both of these initial set of skills and rubrics were co-developed with [Anthropic](https://www.anthropic.com/). A companion [repository from Anthropic](https://github.com/anthropics/PLACEHOLDER) accompanies this work.

To get started, see [Quick Start](#quick-start) below and the [skills/](skills/) directory for what each skill does.

## **Repository contents**

| Path | Description |
| :---- | :---- |
| [skills/](skills/) | The published agent skills and example prompts to use the skills |
| [evals/](evals/) | Evaluation rubrics used to benchmark the quality of skill outputs |
| [LICENSE](LICENSE) | Open source license details |

## **Quick Start**

This quick start guide walks you through getting set up with the Learning Commons skills and MCP server inside a coding agent. It's an easy install and a great way to explore how the skills work. You can also clone this repo and use these skills and the MCP server with an LLM directly through APIs — the route you'd take to build them into your own product experience.

### 1\. Install the skills

```shell
npx skills add learning-commons-org/agent-skills
```

This installs the skills into any agent runtime that supports the open skills format (e.g. Claude Code, Cursor, Codex).

### 2\. Connect Knowledge Graph (recommended)

The skills are grounded in Learning Commons [Knowledge Graph](https://github.com/learning-commons-org/knowledge-graph) via its MCP server — not required, but strongly recommended for accurate, standards- and pedagogy-aligned output. Create an API key in the [Learning Commons Platform](https://platform.learningcommons.org/), then add the server to your agent. Knowledge Graph datasets carry various licenses, some tools might be inaccessible for certain users. For example, in Claude Code:

```shell
claude mcp add --transport http learning-commons-kg \
  https://kg.mcp.learningcommons.org/mcp \
  --header "Authorization: Bearer $LC_API_KEY"
```

### 3\. Try it out

Prompt your agent with a typical teaching request — the matching skill loads automatically:

- *"I need a lesson for tomorrow on rounding to the nearest hundred for my 3rd graders."*  
- *"Differentiate this 6th grade food webs lesson for students below / at / and above proficiency level (find the lesson here: https://www.calacademy.org/educators/lesson-plans/how-stable-is-your-food-web)"*

See [skills/example-prompts.md](skills/example-prompts.md) for more examples.

### 4\. Evaluate the output

Check the generated materials against the same rubrics we use to benchmark these skills — pedagogy, rigor, formatting, and model scaffolding. See [evals/](evals/) for the rubrics and instructions on running them as an LLM-as-judge.

## **Support & Feedback**

We want to hear from you. For questions or feedback, please [open an issue](https://github.com/learning-commons-org/agent-skills/issues) or reach out to us at [support@learningcommons.org](mailto:support@learningcommons.org).

## **Partner with us**

**Learn more about our work or partner with us to:**

* Co-develop new skills for K-12 workflows  
* Get early access to new skills, tools, and Knowledge Graph  
* Receive personalized support from the Learning Commons team

Contact us [here](https://learningcommons.org/contact/?utm_source=github&utm_medium=agent-skills&utm_campaign=partner).

## **Reporting Security Issues**

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@learningcommons.org](mailto:security@learningcommons.org).

## **Disclaimer**

The resources provided in this repository are made available "as-is", without warranties or guarantees of any kind. They may contain inaccuracies, limitations, or other constraints depending on the context of use. Use of these resources is subject to [our Terms of Use](https://learningcommons.org/terms-of-use/).

By accessing or using these resources, you acknowledge that:

* You are responsible for evaluating their suitability for your specific use case.  
* Learning Commons makes no representations about the accuracy, completeness, or fitness of these resources for any particular purpose.  
* Any use of the materials is at your own risk, and Learning Commons is not liable for any direct or indirect consequences that may result.

Please refer to each resource's README, license, and associated docs for any additional limitations, attribution requirements, or guidance specific to that resource.
