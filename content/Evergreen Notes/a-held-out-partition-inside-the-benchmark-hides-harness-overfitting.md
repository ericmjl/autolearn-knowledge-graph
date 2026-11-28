---
type: "evergreen"
title: "A held-out partition inside the benchmark hides harness overfitting"
created_at: "2026-11-28T09:03:48Z"
updated_at: "2026-11-28T09:03:48Z"
inputs: ["notes-on-transharness-from-benchmark-overfitting-to-transferable-harness-evolution", "held-out-evaluation-gates-harness-evolution-layered-checks-only-guide-it"]
provenance_urls: ["https://arxiv.org/html/2611.33757v1", "https://arxiv.org/html/2608.06301v1", "https://hamel.dev/blog/posts/evals/", "https://blog.anthropic.com/building-effective-agents", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["When the harness changes, how do you keep the held-out evaluation partition representative and detect when it stops being valid?"]
---
Agent synthesis

Held-out evaluation inside the evolution benchmark does not keep harness gains honest. Selection on any partition correlated with the source distribution rewards recurring benchmark characteristics, not transferable improvement. TransHarness quantifies the failure: Meta-Harness gains 2.0 points on the evolution set but loses 4.1 points on DeepSWE v1.1, while Self-Harness and RRSI recover failures in 13.3% and 11.5% of paired executions but regress in 13.0% and 11.2%, netting 0.3 points. The fix couples three moves: an evolution set that shares nothing with the target, a harness frozen before target evaluation, and policies retained by cross-task replay plus independent semantic selection, which test selectivity and source-independence.

The existing held-out note already splits the stack into fast in-loop checks that guide the optimizer and a held-out partition that gates deployment. TransHarness sharpens that split with a stricter rule: a partition that is merely inaccessible during search still shares the benchmark's task distribution, repositories, and failure modes, so transfer-relevant signal never gets tested. The paper's independent set spans 11 repositories and none of DeepSWE's 91, raises mean domain-distribution distance from 0.13 to 0.70 on DeepSWE and from 0.18 to 0.64 on Terminal-Bench, and the frozen harness reaches 76.4% and 95.5% on those benchmarks, beating GPT-6 Astra by 2.4 and 5.6 points. HarnessOpt-Bench shows the same blind spot from the other side: validation scores are optimistic, and most candidates test lower than the best validation score seen during search. (see: held-out evaluation gates harness evolution, layered checks only guide it)

The mechanism is regression economics. Net change equals (1-p0) times recovery minus p0 times regression. Higher base success leaves fewer failures to recover and lowers the allowable regression rate, so a fair target must expose both sides of the ledger. Benchmark-internal selection cannot do that, because the same tasks that drive evolution also determine the losses. TransHarness recovers 13.0% with only 9.7% regressions, reaching 76.4% and 95.5% on DeepSWE and Terminal-Bench and beating Meta-Harness (+2.0 source, -4.1 target) and RRSI (+0.3 net). Place the held-out target outside the evolution distribution, freeze the harness before testing, and read the score as recovery minus regression, not as a single pass rate.

## Where it comes from

- [[notes-on-transharness-from-benchmark-overfitting-to-transferable-harness-evolution|TransHarness: From Benchmark Overfitting to Transferable Harness Evolution]]

## What this builds on

- [[held-out-evaluation-gates-harness-evolution-layered-checks-only-guide-it|Held-out evaluation gates harness evolution, layered checks only guide it]]
