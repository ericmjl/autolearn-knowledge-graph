---
type: "evergreen"
title: "Held-out tasks still share one protocol, so harness gains need protocol stress-tests"
created_at: "2026-11-23T01:02:34Z"
updated_at: "2026-11-23T01:02:34Z"
inputs: ["notes-on-bad-genius-counterfactual-guided-harness-evolution-beyond-task-specific-shortcuts", "harness-evolution-pays-off-only-with-a-dense-held-out-oracle"]
provenance_urls: ["https://arxiv.org/abs/2609.18366", "https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How much held-out signal does harness evolution need before the held-out oracle itself becomes the bottleneck?"]
---
Agent synthesis

Held-out task scoring does not certify that a harness is genuinely better, because the held-out tasks still share the benchmark's protocol: the same issue formatting, tool-output field order, and scoring conventions that the in-loop selection saw. The dense held-out oracle from the sampled note fixes what tasks are graded but not the protocol that produced the grade, so a harness whose gains come from formatting conventions survives held-out scoring unchanged and looks real.

The mechanism breaks in both directions. A fixed protocol inside the oracle hides shortcuts that a protocol change would expose, while held-out task scoring alone cannot see them. CHASE attacks the same blind spot from the other side: a Proposer edits the harness around a fixed foundation model, a Challenger searches for a protocol change that preserves the tasks but cuts the updated harness's gain over the initial harness, and executable checks confirm the transformation preserves task semantics before the loss is trusted. Confirmed gain losses enter an archive that constrains later updates, so the evolver cannot re-encode the same shortcut.

The evidence shows the gap is real. On SWE-Bench Pro V2 certification tasks, changing the issue formatting and tool-output field order drops HarnessEvolve's gain from 8.57 to 3.81 percentage points, while the final CHASE harness keeps 10.48 of its 11.43-point gain under the same change. On Syn-Ledger, removing the known shortcuts yields 38.30% for CHASE against 18.27% for HarnessEvolve. This extends the sampled note's dense-oracle rule by saying where its blind spot sits: the held-out oracle still inherits the protocol it grades under, so a verifier that never perturbs the protocol is measuring one recipe of the benchmark, not the harness (see: harness evolution pays off only with a dense, held-out oracle).

Before crediting harness evolution, re-run the held-out harness under at least one protocol change and report retained gain alongside the held-out score; treat a flat held-out result on a shared protocol as a hint that the gain lives in the protocol, not the harness.

## Where it comes from

- [[notes-on-bad-genius-counterfactual-guided-harness-evolution-beyond-task-specific-shortcuts|Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts]]

## What this builds on

- [[harness-evolution-pays-off-only-with-a-dense-held-out-oracle|Harness evolution pays off only with a dense, held-out oracle]]
