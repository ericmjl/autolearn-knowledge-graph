---
type: "evergreen"
title: "Eval-driven model routing keeps agents on the cost-accuracy frontier"
created_at: "2026-11-27T07:03:09Z"
updated_at: "2026-11-27T07:03:09Z"
inputs: ["notes-on-model-routing-as-an-eval-problem-mercor-enterprise", "optimize-agent-cost-and-accuracy-jointly-not-accuracy-alone"]
provenance_urls: ["https://www.mercor.com/blog/mercor-model-routing-eval-problem/", "https://arxiv.org/abs/2407.01502", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["What optimization methods do practitioners use to find the cost-accuracy Pareto frontier for agent workloads?"]
---
Agent synthesis

A cost-accuracy-joint agent stays on the Pareto frontier only when its routing decisions are evaluated against its real workload, since lower token spend is ambiguous without measurement: it may mean the agent grew more efficient, or it may mean it skipped work, mishandled edge cases, or failed exactly where the cost dashboard cannot see. The mechanism is that the evaluation suite, not any single model's leaderboard score, is the system of record: it defines what good means for this agent in this environment, and every model swap, routing rule, and harness change gets judged against that bar. The Mercor routing essay turns this into three concrete strategies - static selection, query classification, and dynamic delegation - each matched to the shape of the workload.

Static selection fits concentrated-difficulty workloads, where a full model sweep across the suite reveals a knee in the cost-performance curve and static selection mostly solves routing. Query classification struggles when difficulty is not visible in the query text: classifiers overfit to the tasks they were tuned on and misroute hard tasks to weak models while handing easy tasks to expensive ones, which lowers accuracy while raising cost. Dynamic delegation moves the routing decision inside the agent - a frontier model keeps the plan, the ambiguous calls, and the final review, while cheaper models handle the token-heavy middle of the trajectory, exploration, test runs, mechanical edits - which is where most tokens go. Delegation is not free: it runs a frontier orchestrator on every task including the easy ones, so its payoff is an empirical question for the same suite.

Set beside the cost-accuracy note, the synthesis goes beyond both inputs: the evergreen argues joint optimization is the right target, but the new source note supplies the how - static sweep, query classification, or dynamic delegation, chosen by the difficulty spread the eval suite reveals, with the eval suite itself as the decision layer that keeps the agent on the frontier as the model landscape shifts. The shared conclusion with the cost-accuracy note is that optimizing accuracy alone is a trap; whether cost and accuracy move together depends on the evaluation suite, not on the leaderboard number.

Build the eval suite first: the verifiers need the production workload's tasks, failure costs, and domain-expert acceptance criteria, and then every model swap is judged by whether performance held, what tradeoffs appeared, and what it cost. (see: optimize agent cost and accuracy jointly, not accuracy alone)

## Where it comes from

- [[notes-on-model-routing-as-an-eval-problem-mercor-enterprise|Model Routing as an Eval Problem | Mercor Enterprise]]

## What this builds on

- [[optimize-agent-cost-and-accuracy-jointly-not-accuracy-alone|Optimize agent cost and accuracy jointly, not accuracy alone]]
