---
type: "evergreen"
title: "Held-out tool tests, not end-to-end scores, prove tool-selection quality"
created_at: "2026-11-26T08:04:02Z"
updated_at: "2026-11-26T08:04:02Z"
inputs: ["notes-on-building-trust-in-ai-agents-a-production-ready-evaluation-framework-with-amazon-bedrock", "well-crafted-tool-interfaces-rival-model-choice"]
provenance_urls: ["https://aws.amazon.com/blogs/machine-learning/building-trust-in-ai-agents-a-production-ready-evaluation-framework-with-amazon-bedrock-agentcore/", "https://agentengineering.org/articles/designing-tools-for-agents/", "https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["What does a first-call tool-selection eval against held-out cases look like in practice — how do you build the held-out set and what do you measure?"]
---
Agent synthesis

Held-out tool tests, not end-to-end scores, prove tool-selection quality. An agent can answer a full question correctly while a single tool quietly degrades, so the held-out test comes before the agent does: each critical tool is tested on its own against inputs where the correct answer is already known. Only tool responses already confirmed correct are frozen into the replay dataset, which means a score difference between two candidates reflects the agent's reasoning, not tool variance.

Mechanism: the sampled tool-interfaces note argues the tool surface decides what the agent can express; this source note supplies the layered measurement around that surface. Each tool gets a deterministic ground-truth contract (customer identification must resolve to the exact canonical entity or fail). The sentinel set, a curated selection of 15 highest-risk scenarios, runs in minutes on every staging deploy and is reviewed monthly; one caught disambiguation regression (unresolved entities for a subset of account name formats) blocked a deployment automatically. A separate 200-question held-out pass runs the full candidate end-to-end, scored by an LLM-as-judge, and shuts the gate on aggregate regression, a loss to the production baseline, or a per-question threshold breach.

Drift stays in the loop. Ten percent of live traffic is sampled through the same evaluators, and the Quality-State Calculator surfaces deviations in minutes; when a stock-ticker and shorthand-name query pattern dropped 98 percent to 80 percent across three consecutive 30-minute windows, the low-scoring sessions were promoted into the golden set and accuracy recovered within the next evaluation cycle. The canary cadence, 30-minute windows with 90-minute confirmation, keeps the tool-level sentinel the first alarm rather than the agent-level average.

Put tool-level held-out tests in front of every end-to-end score: freeze validated tool answers into replay datasets, run sentinels on each deploy, and promote every degraded live session back into the golden set. (see: well-crafted tool interfaces rival model choice)

## Where it comes from

- [[notes-on-building-trust-in-ai-agents-a-production-ready-evaluation-framework-with-amazon-bedrock|Building trust in AI agents: A production-ready evaluation framework with Amazon Bedrock AgentCore | Amazon Web Services]]

## What this builds on

- [[well-crafted-tool-interfaces-rival-model-choice|Well-crafted tool interfaces rival model choice]]
