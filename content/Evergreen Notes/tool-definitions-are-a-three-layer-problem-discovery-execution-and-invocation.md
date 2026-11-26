---
type: "evergreen"
title: "Tool definitions are a three-layer problem: discovery, execution, and invocation"
created_at: "2026-11-26T15:02:13Z"
updated_at: "2026-11-26T15:02:13Z"
inputs: ["notes-on-introducing-advanced-tool-use-for-claude", "tool-design-deserves-prompt-engineering-attention"]
provenance_urls: ["https://www.anthropic.com/research/advanced-tool-use", "https://blog.anthropic.com/building-effective-agents", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["How much does tool-definition design affect token cost and agent accuracy in practice, and what is the evidence?"]
---
Agent synthesis

Tool definitions are a three-layer problem: discovery, execution, and invocation. Anthropic's advanced tool use work quantifies why: a five-server MCP setup loads ~55K tokens in definitions before work begins, and at Anthropic, tool definitions have consumed 134K tokens before optimization. Loading everything upfront wastes context and accuracy, because the most common failures are wrong tool selection and incorrect parameters, not invalid JSON.

The mechanism is layered. Tool Search Tool defers loading so only ~500 tokens of the search tool and three to five relevant tools (~3K tokens) sit in context, cutting total consumption from ~77K to ~8.7K tokens, an 85% reduction, while improving MCP evaluation accuracy (Opus 4: 49% to 74%; Opus 4.5: 79.5% to 88.1%). Programmatic Tool Calling moves orchestration into code, so intermediate results never enter context, cutting average usage from 43,588 to 27,297 tokens (37%) and improving internal knowledge retrieval from 25.6% to 28.5% and GIA benchmarks from 46.5% to 51.2%. Tool Use Examples carry the conventions JSON schemas cannot express, pushing accuracy from 72% to 90% on complex parameter handling.

This extends the sampled tool-design note from a qualitative rule (tool definitions deserve prompt-engineering attention) into a quantitative stack. CodeAgent's four strategies and Anthropic's three features converge on the same structure: optimize how tools are found, how they run, and how they are called. Together they say the unit of tool design is not the definition but the whole tool-use pipeline (see: tool design deserves prompt-engineering attention).

Start with the largest bottleneck. For context bloat, defer discovery; for large intermediate results, move orchestration into code; for parameter errors, add examples. Layer the rest only when measurements justify it.

## Where it comes from

- [[notes-on-introducing-advanced-tool-use-for-claude|Introducing advanced tool use for Claude]]

## What this builds on

- [[tool-design-deserves-prompt-engineering-attention|Tool design deserves prompt-engineering attention]]
