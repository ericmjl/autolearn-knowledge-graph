---
type: "evergreen"
title: "Model routing pays only when the price gap covers the judge tax"
created_at: "2026-11-25T03:02:47Z"
updated_at: "2026-11-27T18:03:02Z"
inputs: ["notes-on-how-many-of-your-agent-s-calls-actually-need-a-frontier-model", "agentic-spend-is-engineered-not-priced-by-the-token", "notes-on-auto-router-for-llms-when-automatic-model-routing-pays-off"]
provenance_urls: ["https://www.langchain.com/blog/switchyard-agent-routing-benchmark", "https://managed-code.com/blog-post/are-ai-agents-more-expensive-than-humans", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://blog.anthropic.com/building-effective-agents", "https://www.orcarouter.ai/blog/auto-router"]
refutation_status: "untested"
answers_questions: ["How do teams decide which tasks warrant expensive model routing versus cheap models, and what signals predict a task will fail automated verification?", "When does model routing pay off for a team with a small model price gap, and does the judge tax shrink with better judge models?"]
---
Agent synthesis

Model routing pays only when the price gap between cheap and frontier models is wide enough to cover the judge tax, and the tax now has two parts: a classification step on every request, and the judge model itself. The mechanism is two-sided. A judge runs on every turn until a task escalates and gets no prompt-cache credit, so it becomes the second-largest line item in the routed arm, while the frontier model carries about 7% of calls yet two-thirds of the spend. Every request also pays a classification tax before the model starts: under 1ms at 50-65% accuracy for keyword rules, 50-200ms at 70-80% for a small classifier, 200-500ms at 85-95% for a trained domain classifier, and 1-5 seconds at 85-90% for LLM-as-judge, which is usually too slow for the savings to survive. Routing only survives when the cheap and frontier models differ enough in price: DeepSeek V4 Flash at $0.14/$0.28 per 1M tokens against Claude Opus 5 at $5.00/$25.00 is a 36x input spread, and the documented coding-session example went from $6.00 to $1.26, still 77% cheaper after the router's $0.10 per 100 requests. The minimal offload is judge cost divided by the price gap, and when the two models sit close together the formula asks for more than 100% offload, so no judge configuration can fix that pairing. The spend note frames routing as one of the levers in managing the fixed-human-cost problem, and the new source shows the lever has a price of its own: it works as a cost device on saturated, easy workloads, and only earns its keep on harder workloads where the model gap is wider.

The evidence in the new source is specific: a managed auto router with a quality floor and grading under 1ms measured 55ms median end-to-end overhead in production, and balanced routing saves 35-45% while aggressive routing saves 60-75% and conservative routing saves 10-15%. The router itself adds latency as well as cost, which is why it is the wrong answer for single-model setups, sub-300ms real-time traffic, tiny volume, auditable model choice, and unmeasured quality. A better judge does not shrink the tax: LLM-as-judge is the slowest, most expensive classification option, so the classification tax stays a cost line even when the judge is accurate. The accuracy it buys matters only against a measured quality floor: without one, cost routing silently degrades output, and RouteLLM-style results claim up to 85% savings only with a floor that stops the router cheaping out on requests that genuinely need the frontier. The existing note adds the arithmetic a team needs before building the router: compute the price gap, compute the judge tax, and check whether the offload needed clears that bar.

Route a slice of traffic through the router, measure cost and quality on a 50-prompt eval from your own prompts, force the hard cases so the router does not dump them on the cheap model, read the per-request routing logs, and plan against the top of the cost band rather than the average, before shipping a router.

## Where it comes from

- [[notes-on-how-many-of-your-agent-s-calls-actually-need-a-frontier-model|How many of your agent's calls actually need a frontier model?]]
- [[notes-on-auto-router-for-llms-when-automatic-model-routing-pays-off|Auto Router for LLMs: When Automatic Model Routing Pays Off]]

## What this builds on

- [[agentic-spend-is-engineered-not-priced-by-the-token|Agentic spend is engineered, not priced by the token]]
