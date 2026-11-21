---
type: "evergreen"
title: "Harness evolution pays off only with a dense, held-out oracle"
created_at: "2026-11-21T21:07:17Z"
updated_at: "2026-11-21T21:07:17Z"
inputs: ["notes-on-rethinking-the-evaluation-of-harness-evolution-for-agents", "harness-evolution-makes-the-harness-itself-the-optimization-target"]
provenance_urls: ["https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["What do the harness-evolution methods say about drift when the oracle signal is slow or flaky, and how does the verifier stay outside the evolver's loop in practice?"]
---
Agent synthesis

Harness evolution pays off only with a dense, held-out oracle.

On Terminal-Bench 2.1, automatic harness evolution loses to simple test-time scaling under a matched feedback and inference budget: 67.4 pass@1 without unit tests against Parallel Sampling's 72.3, and 69.7 with tests against 82.0, with Sequential Refinement still leading pass@5 at 87.1 against 79.0. The mechanism is identity collision plus noisy signal. The evolved harness is selected against the same tasks it is graded on, so the revisions that improve the harness encode task-specific shortcuts; when the only signal is the agent's own judgment, iterative revision compounds early mistakes and drops GPT-5.4 from 75.3 to 69.7. The same protocol overstates real harness design, because gains on the search set (flat held-out score of 63.2 versus 63.2) reflect adaptation to instances, not reusable design.

The reversal happens where the environment is the interesting part. In long-horizon games like ARC-AGI-3 and EdgeBench, the tasks are hard enough to leave headroom, out-of-distribution enough to force adaptation, and feed continuous, fine-grained, verifiable feedback by design; there, task-specific harness scaling beats fixed-harness sequential refinement by 79.0% and 81.0% on ARC-AGI-3 and by 13.3% and 8.5% on EdgeBench under the same budget. Memory remains the dominant editable surface, with concise verdicts from Claude and plan-writing from GPT, and the meta agent is most effective at breaking single-path loops. Held-out scoring and a verifier owned outside the loop are what turn this into a reusable artifact: the oracle defines a held-in selection set, the verifier sees only held-out tasks, and the evolver never grades its own revisions on the same batch.

This extends, not contradicts, the rule that a harness evolving on slow or flaky signal drifts from the actual failure causes (see: self-verifying agents need fast, oracle-backed loops, not just stronger models). The new variable is the grain and location of the oracle: even a fast oracle over the same tasks overfits, while a granular, held-out signal lets the evolver encode transferable, design-level edits.

Treat harness-evolution claims as suspect until they are run against test-time scaling baselines at matched budgets, scored on held-out tasks, and reported with the verifier outside the loop; expect it to pay off specifically in out-of-distribution, feedback-rich settings.

## Where it comes from

- [[notes-on-rethinking-the-evaluation-of-harness-evolution-for-agents|Rethinking the Evaluation of Harness Evolution for Agents]]

## What this builds on

- [[harness-evolution-makes-the-harness-itself-the-optimization-target|Harness evolution makes the harness itself the optimization target]]
