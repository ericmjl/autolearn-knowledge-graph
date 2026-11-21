---
type: "evergreen"
title: "Self-verifying agents need fast, oracle-backed loops, not just stronger models"
created_at: "2026-11-21T03:07:58Z"
updated_at: "2026-11-21T03:07:58Z"
inputs: ["notes-on-agentic-verification", "notes-on-your-ai-product-needs-evals-hamel-husain"]
provenance_urls: ["https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/"]
refutation_status: "untested"
---
Agent synthesis

Self-verifying agents outperform stronger models under human review because verification, not code-writing, is now the bottleneck. The mechanism is a shift of where quality comes from: an agent that can check its own work writes a change, runs the check, reads the output, and retries until the check passes, while the human-dominated loop (diff, run tests, read app, report, repeat) stays slow and costly and does not scale past one human. Addy Osmani's note calls out three oracles in this loop: E2E tests as the hardest to trick (either the whole thing works or it does not), property-based tests for what must never happen (fast-check for JS/TS, Hypothesis for Python, proptest for Rust), and differential tests that treat the old system as the oracle during rewrites, comparing outputs on randomly generated inputs with the intended changes tracked in an approved-changes list. Testing must run fast and deterministically, or the agent learns to retry flaky tests instead of fixing them, so the core loop aims for subsecond runs with seeded randomness and isolated state. Hamel Husain's evals note adds the task-specific angle: evals tailored to users' tasks beat generic benchmarks, with fast, scoped assertions on every change and holdout discipline to avoid overfitting. The synthesis is that these task-aligned evals only reach that status when the agent runs them itself: a test the agent can pass on its own becomes the definition of done, not a scoreboard for a reviewer (see: product-specific evals beat generic benchmarks). Start with one E2E check or one property the agent can run in a subsecond loop, and treat every false pass as a broken oracle, not a flake.

## Where it comes from

- [[notes-on-agentic-verification|Agentic Verification]]
- [[notes-on-your-ai-product-needs-evals-hamel-husain|Your AI Product Needs Evals (Hamel Husain)]]

## What this builds on

- None yet.
