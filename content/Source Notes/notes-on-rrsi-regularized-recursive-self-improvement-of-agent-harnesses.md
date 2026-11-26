---
type: "source-note"
title: "Notes on: RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
raw: "rrsi-regularized-recursive-self-improvement-of-agent-harnesses"
url: "https://arxiv.org/html/2609.24972v1"
created_at: "2026-11-26T13:02:12Z"
updated_at: "2026-11-26T13:02:12Z"
---
- Archived full text: [[rrsi-regularized-recursive-self-improvement-of-agent-harnesses|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2609.24972v1>

## What it says

RRSI (Regularized Recursive Self-Improvement of Agent Harnesses), from Google Cloud AI Research, constrains how finite evolve-set feedback guides harness evolution so recursively evolved harnesses transfer instead of memorizing the benchmark. It regularizes both proposal and selection: an annealed L0-style edit budget, evidence-aware credit assignment, and structured exploration on the proposal side, plus leakage screening, a noise-adjusted stability floor, Ridge-like cost-aware acceptance, and Lasso-like structural pruning on the selection side. Across eight benchmarks in three domains (coding, agentic workspace, engineering design), RRSI gains up to 14.1 points on the evolve split and up to 4.7 points out of distribution, while running on about 30% fewer policy tokens than unregularized evolution.

## Claims drawn from this source

- **Harness-evolution overfitting comes from three coupled behaviors.** The evolution search can encode benchmark-specific patterns, promote candidates favored by evaluation noise, or accumulate complexity that improves evolve-set scores without improving the underlying agent mechanism.
- **Proposal-side constraints keep edits sparse and attributable.** An annealed L0-style budget limits how many independently attributable edits one candidate may bundle (from b_max down to b_min across rounds), so early rounds can try several coordinated changes while later rounds stay sparse and attributable.
- **Evidence-aware credit assignment and stalled-search exploration.** Every evaluated candidate logs the component, hypothesis, diff, and score/cost changes; rejected mechanisms remain negative evidence and successful ones keep explicit credit, and when the search stalls the proposal budget reserves slots for unexplored components (a diversity-like regularizer).
- **Selection-side regularizers stop benchmark-specific gains from becoming permanent.** A critic screens candidate diffs for task names, entity names, task-specific values, answers, or inert machinery before evaluation; a candidate must beat a noise-adjusted floor delta*S > delta; additional inference cost must be justified by measured improvement; components with no strictly positive recent gain are removed as deletion targets.
- **Regularized evolution transfers out of distribution.** RRSI gains 6.0 points on Terminal-Bench 2.1, 4.9 on EngDesign and 1.1 on Harvey LAB, and improves all six held-out splits, up to 4.7 points out of distribution (43.6 vs 39.7 average) with no held-out regression; Meta-Harness adds only 0.9 OOD and AHE and TTHE finish below the unevolved harness.
- **Transfer is not an artifact of judge grading.** Harvey LAB, JobBench and GDPval are all scored by a judging model, but EngDesign and Frontier-Eng tasks are graded by their own frozen simulators, and the gains survive there unchanged with deterministic grading.
- **Evolved harnesses survive a backbone the search never used.** The final coding harness, evolved with Gemini 3.5 Flash, evaluated unchanged with Gemini 3.1 Flash Lite (a smaller model that never took part in the search) rose from 11.2 to 14.6 on Terminal-Bench 2.1, a 30.4% relative gain.
- **RRSI produces the lightest evolved harness and needs evolve-set-only tuning.** It runs 26.3 steps per trial against 27.3 to 34.6 for prior methods (AHE: 3.82M tokens vs 2.42M for RRSI), while all its hyperparameters are calibrated on the evolve environment only, with held-out and OOD benchmarks never used for tuning.
