---
type: "evergreen"
title: "Harness evolution adapts on dense execution traces, gated by held-out oracles"
created_at: "2026-11-21T21:07:17Z"
updated_at: "2026-11-25T07:03:32Z"
inputs: ["notes-on-rethinking-the-evaluation-of-harness-evolution-for-agents", "harness-evolution-makes-the-harness-itself-the-optimization-target", "notes-on-1-introduction"]
provenance_urls: ["https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent", "https://arxiv.org/html/2607.08124v3"]
refutation_status: "untested"
answers_questions: ["What do the harness-evolution methods say about drift when the oracle signal is slow or flaky, and how does the verifier stay outside the evolver's loop in practice?", "How do held-out oracles get constructed for harness evolution, and what makes them dense enough to guide revisions?"]
---
Agent synthesis

Harness evolution adapts on dense execution traces, not on a correctness oracle in the loop: proposers and judges reason over traces and execution-derived proxies, while the held-out oracle stays outside as a post-selection gate. On Terminal-Bench 2.1, automatic harness evolution loses to simple test-time scaling under a matched budget (67.4 pass@1 without unit tests against Parallel Sampling's 72.3, and 69.7 with tests against 82.0, with Sequential Refinement still leading pass@5 at 87.1 against 79.0). The mechanism is identity collision plus noisy signal: the evolved harness is selected against the same tasks it is graded on, so revisions encode task-specific shortcuts, and gains on the search set reflect adaptation to instances, not reusable design. The reversal happens in out-of-distribution, feedback-rich settings like ARC-AGI-3 and EdgeBench, where task-specific harness scaling beats fixed-harness sequential refinement by 79.0% and 81.0% and by 13.3% and 8.5% under the same budget.

The new source note shows what the adaptation loop itself consumes: TTHE evolves a population of candidate harnesses on each unlabeled batch, with three proposer roles (conservative repair, exploratory, adversarial) and a judge that selects on traces plus proxies: execution health, round-trip consistency, and public-test pass rate. It reaches 48.7% mean execution accuracy on BIRD against a 12.7% fixed ReAct baseline (a ten-run consistency-voting control only reaches 16.0%), Terminal-Bench 2.1 rises from 55.1% to 67.8%, and claw-eval from 48.9% to 69.4%. Evolved harnesses become inspectable policies: database probes before SQL generation, reproduce-first workflows with root-cause localization, low-cost paths with escalation after public-test failure, and pre-delivery completeness checks that require citations of retrieved record identifiers. Batch-specific evolved harnesses also transfer across models, improving MiMo V2.5 from 32.0% to 56.0% and GPT-5.5 from 36.0% to 68.0% with no further evolution.

Read together, the two sources say something neither states alone. The held-out oracle's job shifts: it stops being the driver of adaptation and becomes the post-selection check, while dense execution evidence does the steering. Once the oracle leaves the loop, the bottleneck moves to selection. The judge commits to a 50.0% harness on BIRD where an oracle over the same final candidates reaches 64.0% (32/50), a 14-point regret, and an oracle over all evaluated candidates reaches 70.0% (35/50). Execution success coexists with semantic errors, agreeing candidates can still be wrong, so proxies must be presented with candidate code and traces rather than aggregated into one scalar. The harness-evolution note still stands for the grading role: the verifier scores held-out tasks after commitment, the evolver never grades its own revisions on the same batch, and gains stay suspect until scored against test-time-scaling baselines at matched budgets.

Run adaptation on trace and proxy evidence, keep the held-out scorer outside the loop, audit selection regret with oracle-over-final-candidates comparisons, and re-check every evolved harness against held-out tasks before trusting it.

## Where it comes from

- [[notes-on-rethinking-the-evaluation-of-harness-evolution-for-agents|Rethinking the Evaluation of Harness Evolution for Agents]]
- [[notes-on-1-introduction|1 Introduction]]

## What this builds on

- [[harness-evolution-makes-the-harness-itself-the-optimization-target|Harness evolution makes the harness itself the optimization target]]
