---
type: "source-note"
title: "Notes on: Model Routing as an Eval Problem | Mercor Enterprise"
raw: "model-routing-as-an-eval-problem-mercor-enterprise"
url: "https://www.mercor.com/blog/mercor-model-routing-eval-problem/"
created_at: "2026-11-27T07:02:24Z"
updated_at: "2026-11-27T07:02:24Z"
---
- Archived full text: [[model-routing-as-an-eval-problem-mercor-enterprise|Full archived text, with credits]]
- Link: <https://www.mercor.com/blog/mercor-model-routing-eval-problem/>

## What it says

Mercor argues model routing is a cost-quality optimization problem, not a leaderboard choice: the goal is the least expensive model that still delivers required performance, and an agent-specific evaluation suite is the system of record that finds and keeps the agent on the Pareto frontier as models change. It gives three routing strategies (static model selection, query-classification routing, dynamic delegation), maps each to the shape of the workload, warns that difficulty classifiers overfit and misroute, and argues the eval suite is the hard part because its verifiers need deep company context.

## Claims drawn from this source

- **Model routing is a Pareto problem: run the least expensive model that delivers the required performance, not the best model everywhere.** Frontier models are both more capable and more expensive, and the most capable model is rarely the right model for every task. The goal is an operating point on the frontier of tradeoffs between performance and cost, not the best model everywhere.
- **A rigorous evaluation suite is the system of record for cost optimization.** The same suite defines what good means for a specific agent on its actual workload in its actual environment; every model swap, routing rule, and harness change can then be judged by whether performance held, what tradeoffs appeared, and what it cost.
- **Without measurement, lower token spend is ambiguous.** Lower token spend may mean the agent got more efficient, or it may mean it started skipping work, mishandling edge cases, or failing where the cost dashboard cannot see. Public leaderboards cannot tell you which model your specific agent needs.
- **Static selection works when task difficulty is concentrated.** Sweep every candidate model across the full evaluation suite, then pick the single model that delivers required performance at the lowest cost; in bounded-complexity agents a full sweep reveals a knee in the cost-performance curve and static selection mostly solves the routing problem.
- **Query-classification routing fails when difficulty is not visible in the query.** Score each incoming request by difficulty and route to a model sized for it, but classifiers only see the query, not the work, and tend to over-fit to tuned tasks rather than generalized judgment of what tasks are hard; wrong classification hands cheap models tasks they cannot finish and expensive models tasks weaker models could fulfill, lowering accuracy while raising cost.
- **Dynamic delegation moves the routing decision inside the agent.** Keep a frontier model as the main agent and let it decide at runtime, with full context, which subtasks to hand to cheaper subagents; the frontier model keeps the plan, ambiguous calls, and final review while cheaper models handle the token-heavy middle (exploration, test runs, mechanical edits), which is where most tokens go.
- **Delegation is not free and its payoff is empirical.** Delegation pays for reliability by running a frontier model as the orchestrator on every task including easy ones; it can win when difficulty is uneven and hard to predict up front, but that is an empirical question for the evaluation suite to answer.
- **The eval suite is the hard part, not the infrastructure.** Logging, tracing, and scoring harnesses are commodity; knowing what to measure is not. Verifiers need deep company context - which tasks show up in production, which failures carry real business cost, what the environment looks like, and what a domain expert would consider acceptable - and an eval suite built without that context measures a workload that does not exist.
