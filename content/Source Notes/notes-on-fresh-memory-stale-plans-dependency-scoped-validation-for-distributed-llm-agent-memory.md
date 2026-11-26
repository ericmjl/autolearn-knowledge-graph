---
type: "source-note"
title: "Notes on: Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory"
raw: "fresh-memory-stale-plans-dependency-scoped-validation-for-distributed-llm-agent-memory"
url: "https://arxiv.org/html/2609.03340v1"
created_at: "2026-11-26T06:01:27Z"
updated_at: "2026-11-26T06:01:27Z"
---
- Archived full text: [[fresh-memory-stale-plans-dependency-scoped-validation-for-distributed-llm-agent-memory|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2609.03340v1>

## What it says

Distributed LLM-agent teams can read the latest shared state and still act on an obsolete plan. The plan's arguments derive from an earlier requirement, so state freshness alone cannot establish that a pending action is authorized. The authors call this stale-plan execution and introduce PlanFence, a dependency-scoped action-validation protocol: plans record the exact public records they used, tool wrappers declare which records can affect the pending action, and the executor validates only that declared dependency set against owner heads immediately before execution, replans once on mismatch, and blocks on incomplete validation. In 30 live five-agent workflows, a freshness-only executor issued an obsolete action in every task, while PlanFence and centralized lineage completed all tasks with no invalid action. At high churn (rho >= 4), PlanFence also uses lower stall and traffic than time-proactive synchronization and than all-key validation, though its advantage vanishes as the dependency set grows to the full keyspace.

## Claims drawn from this source

- **State freshness does not imply lineage validity.** A fresh executor can still act from a plan derived from an older requirement; the failure is in the derivation, not in the stored state, so the valid check is lineage validity at the protected action.
- **PlanFence validates only the action-relevant dependency set.** Each plan cites exact parent record IDs, tool wrappers declare D(a), and the executor checks only those keys against owner heads, fetching content only for changed dependencies.
- **Freshness-only execution is unsafe in every staged race.** Local replicas and owner-head freshness without lineage issued 330/330 invalid actions in the controlled replay, while every exact-lineage policy completed 330/330 valid actions.
- **Live agents act from stale plans despite reading revisions.** In the matched live study, owner-head freshness issued the stale action and failed all 30 reservation/fulfillment/deployment tasks; centralized lineage and PlanFence each completed 30/30 with one successful replan per task.
- **Proactive per-update sync wins at low churn, PlanFence wins at high churn.** At rho <= 1, per-update metadata sync has lower stall in 7 of 8 cells; at rho >= 4, PlanFence leads in all 8 cells by 1.5x to 7.1x.
- **Dependency scoping lowers cost while the action uses a sparse subset of state.** PlanFence lowers median stall from 115.5 to 67.8 ms/action at 8 loopback keys and from 199.2 to 66.0 ms/action at 128 keys versus batched all-key validation, with traffic near 8.1 KiB/action versus 16.4-81.7 KiB/action.
- **Dependency-scoped checks converge to all-key checks as the dependency set grows.** At d=1, PlanFence lowers stall 14.9% and traffic 50.6%; at d=2, stall is a practical tie with 32.0% lower traffic; at d=8=|X|, both stall and traffic become practical ties.
- **Lineage failures fail closed.** Missing parent, missing declaration, unavailable or malformed owner response, or a second version change blocks the action; validation without replanning blocks all 3,000 detected races, while replanning turns all of them into valid actions.
