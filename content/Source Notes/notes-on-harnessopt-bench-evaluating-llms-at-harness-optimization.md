---
type: "source-note"
title: "Notes on: HarnessOpt-Bench: Evaluating LLMs at Harness Optimization"
raw: "harnessopt-bench-evaluating-llms-at-harness-optimization"
url: "https://arxiv.org/html/2608.06301v1"
created_at: "2026-11-22T17:01:12Z"
updated_at: "2026-11-22T17:01:12Z"
---
- Archived full text: [[harnessopt-bench-evaluating-llms-at-harness-optimization|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2608.06301v1>

## What it says

HarnessOpt-Bench is a benchmark for end-to-end harness optimization: an LLM optimizer with a coding harness edits a target agent's seed harness under a fixed evaluation budget, and its nominated candidate is scored by normalized gain over the pinned seed on a held-out test partition that stays inaccessible throughout search. It separates the optimizer model from the coding harness it acts through by using a shared harness across models, and finds that model choice moves gain about 1.8x more than harness choice, native harnesses give no consistent advantage, broader intervention in harness levers is positively associated with held-out gain, and visible validation scores are optimistic relative to held-out test.

## Claims drawn from this source

- **Harness optimization is a held-out-scored capability, not a single-prompt task.** An optimizer, an LLM paired with a coding harness, receives a target agent's seed harness, graded development and validation feedback, and a fixed target-evaluation budget, then edits the harness and nominates a final candidate, scored by normalized gain over the seed on a held-out test partition inaccessible throughout search.
- **Optimizer model matters more than the coding harness it acts through.** Holding task and harness fixed, changing the optimizer model moves gain by 0.142 on average; holding task and model fixed, changing the harness moves it by 0.079, about 1.8x smaller.
- **Native harnesses are not consistently superior.** Across the 20 model-task pairs evaluated under both conditions, the shared harness wins 11 and the native harness wins 9 with zero ties; native harnesses provide no consistent advantage.
- **Broader intervention in harness levers is associated with greater held-out gain.** The fraction of eight harness levers touched during search is positively associated with gain on every task, with rho ranging from +0.34 to +0.88; detailed failure-trace reading is negatively associated with gain from -0.31 to -0.64.
- **Visible validation scores are optimistic.** Most cells fall below the identity line: the submitted candidate's test score is lower than the best validation score observed during search.
- **Case passes, not evaluation calls, bind.** Each partition allows 200 evaluation invocations and four full case passes; the median optimizer uses 8 calls (4%) but 82% of its case allowance, and 55 of 100 cells exhaust at least one partition's case budget.
- **Defense against evaluation gaming is paired disclosure with a trusted boundary.** Disjoint development/validation/test splits with partition-specific disclosure, a trusted execution environment enforcing budget and held-out access, and K=3-pooled scoring constitute the protocol; per-run jitter in cases, tool behavior, and verifier implementation is still an open future direction.
