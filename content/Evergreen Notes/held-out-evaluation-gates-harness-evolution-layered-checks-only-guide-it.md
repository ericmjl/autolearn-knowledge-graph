---
type: "evergreen"
title: "Held-out evaluation gates harness evolution, layered checks only guide it"
created_at: "2026-11-22T17:01:52Z"
updated_at: "2026-11-22T17:01:52Z"
inputs: ["notes-on-harnessopt-bench-evaluating-llms-at-harness-optimization", "layered-evals-work-best-split-across-separate-calls", "harness-evolution-makes-the-harness-itself-the-optimization-target"]
provenance_urls: ["https://arxiv.org/html/2608.06301v1", "https://hamel.dev/blog/posts/evals/", "https://blog.anthropic.com/building-effective-agents", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How do layered evals interact with agentic harness evolution, where the harness itself is being optimized?"]
---
Agent synthesis

Harness optimization is gated by held-out evaluation, not by the checks the harness itself runs. When the harness becomes the object being optimized, the eval stack splits into two jobs: the fast in-loop checks that let the optimizer search, and the held-out test partition that tells it whether real improvement happened. HarnessOpt-Bench pins this split: development feedback supports diagnosis, validation feedback supports selection, and the test partition stays inaccessible throughout search, with the optimizer budget measured in case passes. Layered evals (unit tests, model eval, A/B) deliver cheap, frequent signal inside the product loop, but they cannot separate real harness improvement from evaluation noise. The mechanism is cost: where evaluation is cheap, selection over many candidates substitutes for reasoning; where it is expensive and stochastic, reasoning from prior evidence becomes the capability itself, which is exactly the regime harness optimization lives in.

The evidence is concrete. HarnessOpt-Bench finds the median optimizer uses 8 evaluation calls (4%) but 82% of its case-pass allowance, and that visible validation scores are optimistic: most candidates test lower than the best validation score seen during search. The harness-evolution note ties this to the evolver loop: self-verifying agents need fast, oracle-backed loops, and eval discipline from the cybersecurity side matters because outcome grading with held-out splits stops the evolver from overfitting its own signal. The layered-evals note adds the in-loop discipline: separate LLM calls, separate checks, rising cost and cadence.

The synthesis is a two-tier design: layered, cheap, frequent evals inside the loop to guide the optimizer, plus a held-out partition, fixed verifier, and budget-bounded trusted boundary outside it. Optimization targets must not adapt the checks they are scored by. Layered evals tell you the harness is sound; held-out evaluation tells you it improved. Freeze the evaluation boundary, keep the held-out split inaccessible, and let the layered in-loop checks guide search while the held-out tier gates deployment.

## Where it comes from

- [[notes-on-harnessopt-bench-evaluating-llms-at-harness-optimization|HarnessOpt-Bench: Evaluating LLMs at Harness Optimization]]

## What this builds on

- [[layered-evals-work-best-split-across-separate-calls|Layered evals work best split across separate calls]]
- [[harness-evolution-makes-the-harness-itself-the-optimization-target|Harness evolution makes the harness itself the optimization target]]
