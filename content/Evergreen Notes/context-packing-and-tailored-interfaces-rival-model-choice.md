---
type: "evergreen"
title: "Context packing and tailored interfaces rival model choice"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-my-llm-coding-workflow-going-into-2026-addy-osmani", "notes-on-building-effective-agents-anthropic"]
provenance_urls: ["https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
---

# Context packing and tailored interfaces rival model choice

Agent synthesis

Packing extensive context and designing tailored interfaces matter as much as model choice, because agents are steered by what they are given and how tools are presented, not by raw capability alone. The mechanism is that an agent's output is bounded by the information and interfaces it can see: missing context leaves it guessing, and undocumented or awkward tools force it off-script, regardless of how strong the underlying model is.

Addy Osmani's 2026 workflow treats context and model choice as parallel, co-equal recommendations: feed the model relevant code, docs, constraints, and pitfalls (via MCP, gitingest, or repo2txt), while also swapping or running models per task and using the newest pro-tier versions when quality matters. Anthropic's guide makes the interface side explicit: the augmented LLM is the foundational building block, capabilities should be tailored to the use case with a well-documented interface (e.g., via Model Context Protocol), and tool definitions need prompt-engineering attention—easy-to-write formats, docstring-style documentation, testing, and poka-yoke constraints such as absolute filepaths. Anthropic also warns that frameworks obscure prompts and responses, so direct, well-understood interfaces beat abstraction layers.

Together, the two sources show that the leverage in agentic work sits in the scaffolding around the model—context packaging, rules and examples, documented and tested tools—rather than in the model selection itself. No single source makes the full claim: Osmani lists context and model choice as separate steps without declaring one dominant, and Anthropic ties interface design to prompts rather than to model choice. The combination is that both treat context and interface as first-class engineering concerns on par with model selection, which is the strongest honest reading of the sources.

## Where it comes from

- [[notes-on-my-llm-coding-workflow-going-into-2026-addy-osmani|My LLM coding workflow going into 2026 (Addy Osmani)]]
- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]

## What this builds on

- None yet.
