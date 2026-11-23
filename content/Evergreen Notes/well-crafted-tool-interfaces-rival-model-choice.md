---
type: "evergreen"
title: "Well-crafted tool interfaces rival model choice"
created_at: "2026-11-22T04:02:42Z"
updated_at: "2026-11-22T04:02:42Z"
inputs: ["notes-on-designing-tools-for-agents-the-agent-computer-interface-agentengineering-org", "context-packing-and-tailored-interfaces-rival-model-choice"]
provenance_urls: ["https://agentengineering.org/articles/designing-tools-for-agents/", "https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["What distinguishes a well-crafted tool interface (docstrings, poka-yoke constraints) from an awkward one, and how much of that matters versus model choice?"]
---
Agent synthesis

A tool surface designed like onboarding docs, with wrong calls made unrepresentable, keeps an agent on-task more reliably than a stronger model behind a sloppy surface. The mechanism is that an agent programs against only what the interface exposes: names, descriptions, parameter schemas, and error text land in context fresh on every call, so the interface decides what the agent can express even when the underlying model is strong.
The new source walks the tool call in four stages, and nearly every production failure traces to one of them: an endpoint-shaped surface dumps raw logs instead of assembled context, a free-text parameter accepts a job name where a run identifier belongs, and an unfiltered result sends the agent's attention to a symptom instead of the cause. Anthropic's fixes, validated on SWE-bench Verified and a web-search bug fixed by description work alone, are description precision, poka-yoke schemas (pattern-constrained ids, enums, no model-supplied identity, no re-asked arguments already known), context-shaped responses (UUIDs resolved to names, response_format enums cutting concise output to a third of detailed tokens), and errors that name the confusion, the tool producing the missing value, and whether retrying helps.
Read against the sampled note on context packing, the two converge on the same ranking: context and interface come first, model choice second. Context tells the agent what it can see; the tool surface tells it what it can express. A stronger model behind an awkward surface still guesses at parameters, mis-selects tools, and retries unretryable calls, while the same model behind a good surface nearly never does.
No single input carries the full claim. The sampled note lists context and interface as parallel levers without declaring the mechanism; the new source supplies the mechanism and the evidence but treats tools as independent of models. Together they show interface and context together outweigh model selection, and the newer evidence makes that ranking concrete. (see: context packing and tailored interfaces rival model choice)
Start with tool design as prompt engineering under version control: one tool per decision, an intern-facing description, schema-enforced arguments, and first-call selection evals against held-out cases before touching the model.

## Where it comes from

- [[notes-on-designing-tools-for-agents-the-agent-computer-interface-agentengineering-org|Designing Tools for Agents: The Agent-Computer Interface | AgentEngineering.org]]

## What this builds on

- [[context-packing-and-tailored-interfaces-rival-model-choice|Context packing and tailored interfaces rival model choice]]
