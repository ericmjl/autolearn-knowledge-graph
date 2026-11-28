---
type: "source-note"
title: "Notes on: TransHarness: From Benchmark Overfitting to Transferable Harness Evolution"
raw: "transharness-from-benchmark-overfitting-to-transferable-harness-evolution"
url: "https://arxiv.org/html/2611.33757v1"
created_at: "2026-11-28T09:02:07Z"
updated_at: "2026-11-28T09:02:07Z"
---
- Archived full text: [[transharness-from-benchmark-overfitting-to-transferable-harness-evolution|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2611.33757v1>

## What it says

TransHarness argues that harness evolution gains measured on the tasks that drive evolution often fail to transfer to new benchmarks, because gains on source tasks can turn into losses on a new distribution. It evolves harness interventions from same-task success-failure contrasts: each policy pairs an executable trigger over observable execution context with diagnostic guidance that directs the agent to reassess against current-task evidence. Cross-task replay gates which triggers activate selectively, and independent semantic selection checks that diagnoses are supported and guidance does not depend on source-task solutions. The evolved harness is frozen before target evaluation, and the authors curate an independent evolution set (100 SWE-bench Pro tasks, 11 repositories, 300 trajectories) that shares none of DeepSWE's 91 repositories. With this, the evolved harness reaches 76.4% on DeepSWE v1.1 and 95.5% on Terminal-Bench 2.1, beating GPT-6 Astra by 2.4 and 5.6 points.

## Claims drawn from this source

- **Source-task gains can reverse on a new benchmark.** Meta-Harness gains 2.0 points on the independent evolution set but loses 4.1 points on DeepSWE v1.1. Self-Harness and RRSI recover failures in 13.3% and 11.5% of paired executions but regress in 13.0% and 11.2%, yielding net gains of only 0.3 points.
- **Net gain depends on the regression-to-recovery ratio.** With base success p0, rescue rate r and regression rate q, net change Delta = (1-p0)*r - p0*q. Higher baseline success leaves fewer failures to recover and lowers the allowable regression-to-rescue ratio, so at fixed recovery rate a higher baseline success rate allows a lower regression rate.
- **Interventions should pair triggers with diagnostic guidance, not prescribed corrections.** Delivering the same guidance at the first eligible event instead of the learned trigger cuts success to 72.6% with regressions rising from 9.7% to 13.3%. Replacing evidence-based reassessment with a prescribed correction cuts success to 65.5%, with recovery dropping to 8.8% and regressions rising to 16.5%.
- **Cross-task replay and semantic selection retain only transferable policies.** The replay gate rejects nearly indiscriminate event-triggered activation (more than 90% activation on both failed and successful executions) and policies that more often single out successful executions. Independent semantic selection then requires a supported diagnosis, independence from the source solution, and corrective actions grounded in failed checks or explicit task requirements.
- **An independent evolution set decouples search from target testing.** The 100-task evolution set (SWE-bench Pro, 11 repositories, 3 executions per task) shares none of DeepSWE's 91 repositories, and replacing a benchmark-internal evolution set with the independent one raises mean domain-distribution distance from 0.13 to 0.70 on DeepSWE and from 0.18 to 0.64 on Terminal-Bench.
- **Construction review converts unreviewed interventions into transferable ones.** A separately constructed harness with fourteen unreviewed interventions reaches 67.3%, while the reviewed seven-intervention harness reaches 76.4% with more recoveries and fewer regressions. Review repairs failures caused by the current change and reports unrelated ones instead of unconditionally fixing anything.
- **More source tasks reduce regression loss, not recovery count.** Harnesses built from 75 and 100 tasks gain 1.2 and 3.2 points respectively. The 50-task harness recovers more failures than the 100-task harness yet incurs larger regression loss, 17.1 versus 9.7 points, so the stronger result reflects fewer disrupted successes rather than more recoveries.
- **The evolved harness is frozen before target evaluation.** Construction and selection use source evidence alone; the selected policies are composed and frozen before testing on DeepSWE v1.1 (113 tasks) or Terminal-Bench 2.1 (89 tasks), with the base agent run three times per evolution task for outcome contrasts.
