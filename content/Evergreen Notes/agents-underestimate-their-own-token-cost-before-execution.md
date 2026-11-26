---
type: "evergreen"
title: "Agents underestimate their own token cost before execution"
created_at: "2026-11-26T12:02:05Z"
updated_at: "2026-11-26T12:02:05Z"
inputs: ["notes-on-how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic", "agentic-workflows-trade-latency-and-cost-for-performance"]
provenance_urls: ["https://arxiv.org/html/2604.22750v3", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do teams measure and forecast token cost fluctuation for agentic workflows over time?"]
---
Agent synthesis

Agents systematically underestimate their own token cost before execution, so the latency-and-cost trade in agentic workflows is an unseen budget, not a planned exchange. The mechanism is self-prediction: the executing agent inspects the task, its tools, and its environment, then reports a token estimate. Empirically those estimates carry weak-to-moderate correlations with realized usage (max 0.39 for Sonnet 4.5 output tokens) and lean systematically low, with the bias worst exactly where agents spend most, on input tokens that balloon across rounds.

The agentic-workflows-trade-latency-and-cost-for-performance note frames the cost side as a real, rising burden against fixed human costs. The new measurement study adds the forecasting failure mode: runs on the same task differ up to 30x in total tokens, the most expensive run doubles the cheapest one, and overspending clusters in high-cost, low-accuracy runs with repeated file-view and modify actions. GPT-5 and GPT-5.2 stay near the efficient region (mild failure-subset increase), while Kimi-K2 and Claude Sonnet-4.5 burn over 1.5 million more tokens on the same tasks, even on tasks every model solves. Human labels do not close the gap: expert difficulty correlates only weakly with actual token cost (Kendall tau_b 0.32), and 6.7% of under-15-minute tasks cost more than the average hour-plus task.

Together, the notes show that the cost side of agentic workflows is not a one-time, knowable number; it is a wide, stochastic distribution that agents and humans both mis-read. The practical takeaway is to treat pre-execution estimates as a coarse triage signal for early budget alerts, not a precise invoice, and to enforce runtime budget caps rather than trust self-reports (see: agentic workflows trade latency and cost for performance).

## Where it comes from

- [[notes-on-how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic|How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks]]

## What this builds on

- [[agentic-workflows-trade-latency-and-cost-for-performance|Agentic workflows trade latency and cost for performance]]
