---
type: "source-note"
title: "Notes on: How many of your agent's calls actually need a frontier model?"
raw: "how-many-of-your-agent-s-calls-actually-need-a-frontier-model"
url: "https://www.langchain.com/blog/switchyard-agent-routing-benchmark"
created_at: "2026-11-25T03:02:01Z"
updated_at: "2026-11-25T03:02:01Z"
---
- Archived full text: [[how-many-of-your-agent-s-calls-actually-need-a-frontier-model|Full archived text, with credits]]
- Link: <https://www.langchain.com/blog/switchyard-agent-routing-benchmark>

## What it says

LangChain ran its Deep Agents eval suite (145 multi-step tasks, ~6.3 calls each across support, incident investigation, and workflow automation) through NVIDIA NeMo Switchyard's LLM classifier in escalation mode. Only 7% of turns went to the frontier model (Claude Opus 4.8), which carried 68.4% of spend; the 30B open model handled 93% of calls for 10.4% of spend. Routing cost 74% less than Opus alone ($3.00 vs $11.45 per run) but retained only 93% accuracy (80.0% vs 86.0%), with the judge model itself taking 21.2% of routed spend.

## Claims drawn from this source

- **Only ~7% of agent turns need a frontier model.** Across 145 multi-step tasks averaging 6.3 calls each, the router sent about 7% of calls (mean 6.9%, range 4.1-9.1%) to the frontier model; a 30B parameter model handled the other 93% for 10.4% of the spend.
- **The frontier model carries most of the bill despite few calls.** Opus calls were 7% of calls but 68.4% of spend; the last six points of accuracy cost 3.5x more per completed task.
- **A cheap model alone may beat routing on saturated workloads.** Nemotron 3.5 Lightning alone scored 77.7% for $0.72 per run vs 80.0% for $3.00 routed and 86.0% for $11.45 Opus alone; the routing-vs-cheap gap (2.3 points) is smaller than run-to-run variance (~2.7 points).
- **Escalation mode starts cheap and promotes after repeated bad turns.** A small judge reads each completed turn and votes; two consecutive negative verdicts (confirmations = 2) route the task to the frontier model going forward. Restarting a task's expensive model after the cheap model struggled scored 2.3 points better than the cheap model on everything, which is inside noise.
- **The judge is the second-largest line item.** The judge (gemini-3.1-flash-lite) runs every turn until escalation and gets no prompt-cache benefit; it took 21.2% of routed spend, about a third of what Opus costs.
- **Routing pays only when the price gap covers the judge tax.** Minimum offload = judge cost / (expensive cost - cheap cost); for their pairing that was 5.9% of turns and they offloaded 93%. When models are close in price the formula demands offloading more than 100% of turns, which is impossible; a locally hosted cheap model widens the gap and makes routing viable.
- **The judge is the highest-leverage knob, with confirmations as the second.** The strike count (confirmations) controls escalation frequency; lower it means more expensive calls. The judge can be cheaper or skip turns clearly going fine.
- **Cost ranges widen with a router while average spend drops.** Frontier traffic across five runs ranged 4.1-9.1%, moving cost between $2.16 and $3.61 per run (about 67% range) on the same workload; plan against the top of the range.
