---
type: "evergreen"
title: "Eval suites stay honest when production failures feed back into them"
created_at: "2026-11-28T10:01:21Z"
updated_at: "2026-11-28T10:01:21Z"
inputs: ["notes-on-agent-observability-the-complete-guide-for-2026-articles-braintrust", "eval-driven-model-routing-keeps-agents-on-the-cost-accuracy-frontier"]
provenance_urls: ["https://www.braintrust.dev/articles/agent-observability-complete-guide-2026", "https://www.mercor.com/blog/mercor-model-routing-eval-problem/", "https://arxiv.org/abs/2407.01502", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["When the eval suite drives routing, how do you keep the suite itself honest as the workload drifts?"]
---
Agent synthesis

An eval suite that only runs golden cases before deployment drifts away from the workload and stops protecting the agent that actually ships. The mechanism is the feedback loop: online scoring attaches scorers to live production traces, failures get converted into eval cases, and CI gates enforce the bar on every merge. Routing decisions then inherit a living suite instead of a stale snapshot.

The eval-driven routing evergreen argues that the eval suite, not any leaderboard number, is the system of record for cost-accuracy routing. Braintrust adds the maintenance half: production traces that fail an online scorer become eval cases, so the suite grows from real user behavior rather than a fixed golden set. Offline evaluation and the CI gate run the same definitions before release, which keeps routing, model swaps, and harness changes judged against current reality.

Neither input alone closes the loop. Routing supplies the decision layer that keeps an agent on the frontier; the observability source supplies the mechanism that keeps that layer honest as the workload shifts. The combination is a suite that is measured against production traffic, not just a static benchmark, and it is how the system of record stays honest as the workload moves.

Pin the suite to production: trace live traces, score a sample online, promote failures into the eval set, and gate merges on the same scorers.

## Where it comes from

- [[notes-on-agent-observability-the-complete-guide-for-2026-articles-braintrust|Agent observability: The complete guide for 2026 - Articles - Braintrust]]

## What this builds on

- [[eval-driven-model-routing-keeps-agents-on-the-cost-accuracy-frontier|Eval-driven model routing keeps agents on the cost-accuracy frontier]]
