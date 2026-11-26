---
type: "evergreen"
title: "Lineage validity, not state freshness, authorizes an action"
created_at: "2026-11-26T06:01:54Z"
updated_at: "2026-11-26T06:01:54Z"
inputs: ["notes-on-fresh-memory-stale-plans-dependency-scoped-validation-for-distributed-llm-agent-memory", "software-agents-are-autonomous-goal-directed-entities-acting-on-their-environment"]
provenance_urls: ["https://arxiv.org/html/2609.03340v1", "https://en.wikipedia.org/wiki/Agent", "https://arxiv.org/abs/2210.03629", "https://arxiv.org/abs/2005.11401"]
refutation_status: "untested"
answers_questions: ["How do you detect and repair a stale or wrong external source that an agent loop keeps re-reading?"]
---
Agent synthesis

An action is authorized by the lineage of its plan, not by the freshness of the state the executor holds. State freshness can coexist with an obsolete derivation: an agent can install the newest requirement and still act on a plan that was derived from the previous one. The fix is to make the plan cite the exact records it used, declare the dependency set a tool wrapper can affect, and re-check that set against owner heads at the moment of execution, replans once on mismatch, and blocks when validation cannot finish.

The PlanFence paper shows the failure mode in live five-agent systems: reading the newly revised requirement without checking the plan produced the stale action in all 30 reservation, fulfillment, and deployment tasks, while a lineage-validated executor completed 30/30. The mechanism separates safety from cost policy: the invariant is exact lineage validity at the protected action, while the choice between proactive synchronization and action-time validation is a systems dial. At low churn, per-update synchronization avoids action-time owner round trips; at churn >= 4 updates per action, PlanFence leads by 1.5x to 7.1x. Dependency scoping compounds the win: validating only the action's declared keys cuts median stall from 199.2 to 66.0 ms/action and traffic from 81.7 to 8.1 KiB/action when an action depends on a sparse subset of shared state, and the advantage shrinks to a tie precisely when the dependency set reaches the full keyspace.

This is the other half of the loop-over-live-state stance from the autonomy note. That note argues the agent must loop over live external state because the agent cannot hold freshness in memory across steps. The PlanFence evidence adds that the loop itself must verify the plan-to-state lineage at the action boundary: fresh memory without lineage still issues the stale action, and a check that is cheap alone becomes expensive the moment every action validates every shared key. The evidence: controlled replay where every freshness-only policy issued 330/330 invalid actions while every exact-lineage policy completed 330/330, and live-workflow audits where the same stale-action pattern appeared in 15/30 exploratory runs.

Build the loop so the action boundary is the only freshness check that matters: re-read the declared dependency set at execution time, keep the plan's parent chain exact, replan once on mismatch, and fail closed on incomplete validation. (see: software agents are autonomous goal-directed entities acting on their environment)

## Where it comes from

- [[notes-on-fresh-memory-stale-plans-dependency-scoped-validation-for-distributed-llm-agent-memory|Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory]]

## What this builds on

- [[software-agents-are-autonomous-goal-directed-entities-acting-on-their-environment|Software agents are autonomous goal-directed entities acting on their environment]]
