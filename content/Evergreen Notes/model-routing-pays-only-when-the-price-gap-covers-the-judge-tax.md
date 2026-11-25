---
type: "evergreen"
title: "Model routing pays only when the price gap covers the judge tax"
created_at: "2026-11-25T03:02:47Z"
updated_at: "2026-11-25T03:02:47Z"
inputs: ["notes-on-how-many-of-your-agent-s-calls-actually-need-a-frontier-model", "agentic-spend-is-engineered-not-priced-by-the-token"]
provenance_urls: ["https://www.langchain.com/blog/switchyard-agent-routing-benchmark", "https://managed-code.com/blog-post/are-ai-agents-more-expensive-than-humans", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do teams decide which tasks warrant expensive model routing versus cheap models, and what signals predict a task will fail automated verification?"]
---
Agent synthesis

Model routing pays only when the price gap between cheap and frontier models is wide enough to cover the judge tax. The mechanism is two-sided: a judge runs on every turn until a task escalates and gets no prompt-cache credit, so it becomes the second-largest line item in the routed arm; meanwhile the frontier model carries about 7% of calls yet two-thirds of the spend. The LangChain benchmark across 145 Deep Agents tasks measured 93% of calls on a 30B model for 10.4% of spend, 74% total savings, six points less accuracy, and a run-to-run cost band of $2.16 to $3.61 driven by which turns the router escalates. The minimal offload is judge cost divided by the price gap, and when the two models sit close together the formula asks for more than 100% offload, so no judge configuration can fix that pairing. The spend note frames routing as one of the levers in managing the fixed-human-cost problem, and the new source shows the lever has a price of its own: it works as a cost device on saturated, easy workloads, and only earns its keep on harder workloads where the model gap is wider.

The evidence in the new source is specific: the judge carried 21.2% of routed spend at about a third of what the frontier model costs, the strike count (confirmations = 2) is the highest-leverage knob for tuning escalation, and the accuracy-cost trade of 74% cheaper for 6 points less materializes on workloads where cheap and frontier models diverge. Against the existing spend note, the new source adds the exact arithmetic a team needs before building the router: compute the price gap, compute the judge tax, and check whether the offload needed clears that bar. If not, hosting the cheap model yourself widens the gap enough to make routing viable again.

Route the routine majority cheaply, budget the judge line as a real expense, and plan against the top of the cost band, not the average, before shipping a router.

## Where it comes from

- [[notes-on-how-many-of-your-agent-s-calls-actually-need-a-frontier-model|How many of your agent's calls actually need a frontier model?]]

## What this builds on

- [[agentic-spend-is-engineered-not-priced-by-the-token|Agentic spend is engineered, not priced by the token]]
