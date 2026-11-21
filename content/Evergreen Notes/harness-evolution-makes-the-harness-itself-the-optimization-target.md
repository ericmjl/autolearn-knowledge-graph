---
type: "evergreen"
title: "Harness evolution makes the harness itself the optimization target"
created_at: "2026-11-21T08:03:13Z"
updated_at: "2026-11-21T08:03:13Z"
inputs: ["notes-on-harness-engineering-for-self-improvement", "self-verifying-agents-need-fast-oracle-backed-loops-not-just-stronger-models", "cybersecurity-evals-reward-outcomes-over-methods-and-harness-structure"]
provenance_urls: ["https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
---
Agent synthesis

Harness evolution turns the harness into the thing being optimized, and it works only when the evaluator and permission controls live outside the loop that evolves it. The mechanism is a progression of what gets optimized: instruction prompts, then structured context, then workflow, then harness code, then optimizer code. As the base model improves, each step moves the target deeper, from hand-written prompts toward general machinery that produces better answers, not just better outputs.

The concrete implementations make the shape visible. Agentic Context Engineering (ACE) keeps context as a playbook of (identifier, description) bullets that a generator, reflector, and curator merge deterministically, so context grows as structured state instead of a lengthening prompt. Meta-Harness goes one level deeper, treating the code that decides what is stored, retrieved, and presented as the optimized object, with a coding agent proposing harness candidates over a file system. Self-Harness runs a propose-evaluate-accept loop: cluster failures into verifier-grounded patterns, propose bounded edits, and accept only candidates with no regression on held-in and held-out splits. Agentic Harness Engineering splits the loop into three observability pillars, component, experience, and decision, so each edit is a file-level, falsifiable claim with a predicted impact. Self-Harness and AHE both keep the runs directory, tracer, verifier, and LLM configuration read-only while edits land only in the harness workspace, which disables reward hacks like disabling the verifier.

The evidence is concrete. Self-Harness learns model-specific harness instructions that target different weaknesses of different base models and improves held-out pass rates on Terminal-Bench-2. AHE beats human-designed harnesses (OpenCode, Terminus-2, Codex) on Terminal-Bench-2 except in the Hard tier, and a frozen harness transfers to SWE-bench-verified, meaning it encodes engineering experience rather than benchmark-specific tricks. Lin et al. also found harness-updating capability is wide: a 9B proposer can write a skill procedurally isomorphic to Opus, but utilizing the updated harness needs correct, timely tool use and long-horizon instruction following.

The synthesis with existing wiki notes is sharp: self-verifying agents need fast, oracle-backed loops (see: self-verifying agents need fast, oracle-backed loops, not just stronger models), because a harness evolving on slow or flaky signal drifts from the actual failure causes; and eval discipline from the cybersecurity side matters here too (see: cybersecurity evals reward outcomes over methods and harness structure), because outcome grading with transcript audits and held-out splits is what stops the evolver from overfitting its own signal. The harness becomes the product, but only when permission boundaries and the verifier stay outside the loop and the human keeps oversight at the decision points. Start by freezing the harness workspace, keeping runs and verifier read-only, and letting the evolver edit only the harness components.

## Where it comes from

- [[notes-on-harness-engineering-for-self-improvement|Harness Engineering for Self-Improvement]]

## What this builds on

- [[self-verifying-agents-need-fast-oracle-backed-loops-not-just-stronger-models|Self-verifying agents need fast, oracle-backed loops, not just stronger models]]
- [[cybersecurity-evals-reward-outcomes-over-methods-and-harness-structure|Cybersecurity evals reward outcomes over methods and harness structure]]
