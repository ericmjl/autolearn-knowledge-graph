---
type: "evergreen"
title: "Tool evaluation must measure more than accuracy"
created_at: "2026-11-22T13:02:14Z"
updated_at: "2026-11-22T13:02:14Z"
inputs: ["notes-on-writing-effective-tools-for-ai-agents", "tool-design-deserves-prompt-engineering-attention"]
provenance_urls: ["https://www.anthropic.com/research/writing-tools-for-agents", "https://blog.anthropic.com/building-effective-agents", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["What does tool-use strategy optimization actually change, and how do teams measure it beyond task accuracy?"]
---
Agent synthesis

Tool evaluation must measure more than accuracy, because tools, calls, and context are where an agent's performance is won or lost. Anthropic's guide frames tools as contracts between deterministic systems and non-deterministic agents, and advises generating dozens of grounded tasks with verifiable outcomes, then judging agents on total runtime, tool-call counts, token consumption, and tool errors alongside top-level accuracy. The existing note on tool design deserves prompt-engineering attention adds that tool definitions and the strategy for using them jointly determine performance, with CodeAgent reporting 18.1% to 250% gains from five tools and four strategies. Together they show the gap: accuracy-only scoring hides whether an agent grasps a tool's purpose, avoids redundant calls, or burns context on intermediate outputs. Track call counts, tokens, errors, and verifier-checked outcomes on held-out tasks, and let the evaluation drive tool selection, consolidation, and description refinements, because held-out sets reveal improvements beyond what expert implementations achieve. Start with a few consolidated, well-described tools, then scale only when the evaluation says the extra tool pays. (see: tool design deserves prompt-engineering attention)

## Where it comes from

- [[notes-on-writing-effective-tools-for-ai-agents|Writing effective tools for AI agents]]

## What this builds on

- [[tool-design-deserves-prompt-engineering-attention|Tool design deserves prompt-engineering attention]]
