---
type: "evergreen"
title: "Regularized selection keeps evolved harnesses from memorizing their benchmarks"
created_at: "2026-11-26T13:03:41Z"
updated_at: "2026-11-26T13:03:41Z"
inputs: ["notes-on-rrsi-regularized-recursive-self-improvement-of-agent-harnesses", "harness-evolution-makes-the-harness-itself-the-optimization-target"]
provenance_urls: ["https://arxiv.org/html/2609.24972v1", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How do self-evolving harnesses avoid overfitting to their own eval signal beyond held-out splits?"]
---
Agent synthesis

Harness evolution overfits when reused feedback is converted into permanent harness state without discipline, and regularization fixes that at the proposal and selection layers rather than by narrowing what the harness may change. RRSI leaves the open harness edit space, prompts, control flow, tools, memory, and context management, fully editable while constraining the search through it, because an adaptive loop over a finite evolve set can encode benchmark-specific patterns, chase evaluation noise, and stack complexity. On the proposal side, an annealed L0-style budget caps the number of independently attributable edits per candidate: early rounds bundle several coordinated changes, late rounds stay sparse, rejected mechanisms remain negative evidence across the whole run, and a stall reserves budget for unexplored components. On the selection side, a critic rejects edits that encode benchmark specifics before they are even scored, a noise-adjusted floor keeps only candidates that beat empirical tolerance from becoming permanent, added inference cost must be justified by measured improvement, and components with no recent positive gain are pruned as deletion targets rather than accumulating in the retained harness.

That makes the sampled harness-evolution note concrete: freezing runs, verifier, and LLM configuration keeps the evolver honest, but the evaluation signal itself still needs discipline. RRSI's measurements show what that discipline buys: 6.0 points on Terminal-Bench 2.1, 4.9 on EngDesign, and 1.1 on Harvey LAB on the evolve split, then 43.6 out of distribution against 39.7 for the base harness, with Meta-Harness adding only 0.9 OOD and AHE and TTHE finishing below baseline, 26.3 steps per trial against 27.3 to 34.6 for prior methods, and roughly 30% fewer policy tokens than unregularized evolution. The transfer survives deterministic grading, where no judge model scores the work, and even a backbone the search never used: a harness evolved with Gemini 3.5 Flash improved the smaller Gemini 3.1 Flash Lite from 11.2 to 14.6 on Terminal-Bench 2.1, a 30.4% relative gain.

The practical rule: keep the harness editable, but treat the evolution loop as an adaptive estimator of a signal it is itself refining, and put sparsity, noise floors, and cost discipline inside the loop rather than in the benchmark you score on. That is how a recursively self-improving harness becomes a reusable mechanism instead of a memorized benchmark: proposal-side sparseness, selection-side conservatism, and a transfer-tested objective (see: harness evolution makes the harness itself the optimization target).

## Where it comes from

- [[notes-on-rrsi-regularized-recursive-self-improvement-of-agent-harnesses|RRSI: Regularized Recursive Self-Improvement of Agent Harnesses]]

## What this builds on

- [[harness-evolution-makes-the-harness-itself-the-optimization-target|Harness evolution makes the harness itself the optimization target]]
