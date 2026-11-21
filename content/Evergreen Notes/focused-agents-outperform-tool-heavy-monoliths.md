---
type: "evergreen"
title: "Focused agents outperform tool-heavy monoliths"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-langgraph-multi-agent-workflows-langchain", "notes-on-multi-agent-system-wikipedia"]
provenance_urls: ["https://blog.langchain.dev/langgraph-multi-agent-workflows/", "https://en.wikipedia.org/wiki/Multi-agent_system"]
refutation_status: "untested"
---
Agent synthesis

Splitting tools and responsibilities across focused agents with separate prompts outperforms one agent selecting from dozens of tools. The mechanism is decomposition: each agent gets its own prompt, LLM, tools, and custom code, with agents represented as nodes in a graph whose edges manage control flow and shared state, so each agent can be evaluated and improved independently without breaking the larger application.

The LangGraph: Multi-Agent Workflows (LangChain) source states directly that grouping tools and responsibilities with separate prompts—including their own instructions, few-shot examples, or fine-tuned LLMs—can give better results than a single agent selecting from dozens of tools, and that multi-agent designs enable individual evaluation and improvement of each agent. The Multi-agent system (Wikipedia) source reinforces the boundary: multi-agent systems can solve problems that are difficult or impossible for an individual agent or a monolithic system, with LLM-based MAS extending this through more sophisticated interaction and coordination.

Together, the two sources show that focused decomposition is not merely an organizational preference but a capability gain: a monolithic agent is constrained by its tool selection and single prompt, while a graph of focused agents gains specialized instructions, independent evaluation, and the ability to tackle problems beyond single-agent reach. Neither source alone makes this full case—the LangGraph source supplies the mechanism and the direct claim, while the Wikipedia source supplies the broader rationale and the caveat that unstructured LLM interaction introduces emergent dialects, protocol drift, and observability gaps, so the benefit of focused agents depends on deliberate graph structure rather than open-ended swarming.

## Where it comes from

- [[notes-on-langgraph-multi-agent-workflows-langchain|LangGraph: Multi-Agent Workflows (LangChain)]]
- [[notes-on-multi-agent-system-wikipedia|Multi-agent system (Wikipedia)]]

## What this builds on

- None yet.
