---
type: "source-note"
title: "Notes on: Building effective agents (Anthropic)"
raw: "building-effective-agents-anthropic"
url: "https://blog.anthropic.com/building-effective-agents"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[building-effective-agents-anthropic|Full archived text, with credits]]
- Link: <https://blog.anthropic.com/building-effective-agents>

## What it says

Anthropic argues that effective agentic systems are built with simple, composable patterns rather than complex frameworks, and distinguishes workflows (LLMs orchestrated through predefined code paths) from agents (LLMs dynamically directing their own processes and tool use). The post recommends starting with the simplest viable solution—often single LLM calls with retrieval and in-context examples—and adding complexity only when it demonstrably improves outcomes, since agentic systems trade latency and cost for performance. It catalogs common workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) and describes agents as LLMs using tools in a feedback loop, best suited to open-ended problems in trusted environments. It also stresses careful tool and agent-computer interface (ACI) design, transparency, and simplicity as core principles, with extensive testing in sandboxed environments for autonomous agents.

## Claims drawn from this source

- **Simple composable patterns beat complex frameworks.** The most successful implementations used simple, composable patterns rather than complex frameworks or specialized libraries.
- **Workflows differ from agents architecturally.** Workflows use predefined code paths; agents let LLMs dynamically direct their own processes and tool usage.
- **Start simple; add complexity only when needed.** Optimizing single LLM calls with retrieval and in-context examples is usually enough; agentic systems trade latency and cost for better task performance.
- **Frameworks obscure underlying prompts and responses.** Abstraction layers make debugging harder and tempt unnecessary complexity; developers should start with LLM APIs directly and understand framework internals.
- **Augmented LLM is the foundational building block.** An LLM enhanced with retrieval, tools, and memory is the base; capabilities should be tailored to the use case with a well-documented interface, e.g. via Model Context Protocol.
- **Parallelization improves complex tasks.** Sectioning independent subtasks and voting across multiple attempts yield better results; guardrails and evals work better when split across separate LLM calls.
- **Agents need environmental ground truth and guardrails.** Agents should gain ground truth from tool results or code execution each step, use stopping conditions, and be tested extensively in sandboxed environments due to compounding errors and higher costs.
- **Tool design matters as much as prompts.** Tool definitions need prompt-engineering attention; formats should be easy for the model to write, tools should be documented like docstrings, tested, and poka-yoke'd (e.g., absolute filepaths).
