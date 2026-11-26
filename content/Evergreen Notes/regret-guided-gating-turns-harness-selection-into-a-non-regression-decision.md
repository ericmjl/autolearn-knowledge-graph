---
type: "evergreen"
title: "Regret-guided gating turns harness selection into a non-regression decision"
created_at: "2026-11-26T04:03:51Z"
updated_at: "2026-11-26T04:03:51Z"
inputs: ["notes-on-guard-stabilizing-recursive-self-improvement-with-regret-guidance", "harness-evolution-pays-off-only-with-a-dense-held-out-oracle"]
provenance_urls: ["https://arxiv.org/html/2611.23476v1", "https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent", "https://arxiv.org/html/2607.08124v3"]
refutation_status: "untested"
answers_questions: ["How does the judge-vs-oracle selection regret in harness evolution (50.0% judge vs 64.0%/70.0% oracle) translate into a concrete selection method?"]
---
Agent synthesis

Regret-guided gating turns harness selection into a non-regression decision. The GUARD source supplies the mechanism: decompose each task into a pre-execution checklist of atomic binary predicates, grade trajectories against it with a two-layer self-reviewer (deterministic sandbox checks plus semantic trace judgments), and rank criteria by paired directional regret, so a criterion the latest promotion broke outranks one that is merely unsolved and mastered criteria are pinned against overwriting. The sampled harness-evolution note supplies the reason this matters: a dense execution-trace judge that picks a harness against the same tasks it is graded on selects 50.0% where an oracle over the same final candidates reaches 64.0% (and 70.0% over all evaluated candidates), a 14-point regret, so the judge is steering on proxy evidence while the oracle sits outside as a post-selection gate.

The synthesis none of the two inputs states alone is what the oracle becomes once the selection machinery is explicit. The harness-evolution note says the held-out scorer moves from the driver of adaptation to a post-selection check, with dense traces doing the steering; GUARD turns that into a repeatable loop: analysis by paired regret, proposal by parallel group-relative pooling (two candidates beats sequential search and cuts rejected gate rounds by 64%), and promotion gated by Soft-HURT, which admits an edit only when its gains exceed induced regressions. What this does is replace a scalar fitness score that cannot tell a regression from a gap with a ranking that pins mastered rules, targets fresh regressions, and logs rejected edits in a ledger so refused changes are not repeated verbatim. The regression gate doubles as the trust region that stands in for the gradient the frozen model never takes.

The numbers carry the claim. GUARD achieves 19/19 non-regressive execution-gated promotions across Drift Gauntlet, EvoHarnessBench, and the professional suites (15 strictly positive, 4 ties), zero stream-mean drops across 12 block transitions with zero post-block forgetting on all four Drift Gauntlet streams, the only method with no negative backward or forward transfer on EvoHarnessBench, and a 54.5% cut in tokens per task. Dense checklist grading removes the passive-observation 1/epsilon penalty that scalar gap signals pay. The practical implication is that a harness-evolution system should invest in selection gates rather than in stronger models: the judge is a steering device, the oracle is the auditor, and the gap between the two is a measurable regret you can close with regression-aware selection, not more data (see: harness evolution adapts on dense execution traces, gated by held-out oracles).

Build the selector before you tune the harness: run paired-regret analysis on a per-criterion checklist, pool candidates and promote only through a non-regression gate, and keep the held-out scorer outside as an audit step whose 14-point regret gap you can measure and shrink. Audit every evolved harness against held-out tasks before trusting it.

## Where it comes from

- [[notes-on-guard-stabilizing-recursive-self-improvement-with-regret-guidance|GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance]]

## What this builds on

- [[harness-evolution-pays-off-only-with-a-dense-held-out-oracle|Harness evolution adapts on dense execution traces, gated by held-out oracles]]
