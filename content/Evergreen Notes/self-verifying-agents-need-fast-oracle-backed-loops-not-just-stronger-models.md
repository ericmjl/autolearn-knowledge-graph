---
type: "evergreen"
title: "Self-verifying agents need fast, oracle-backed loops, not just stronger models"
created_at: "2026-11-21T03:07:58Z"
updated_at: "2026-11-21T16:14:13Z"
inputs: ["notes-on-agentic-verification", "notes-on-your-ai-product-needs-evals-hamel-husain", "notes-on-how-we-used-agentic-ai-to-automate-fixes-for-flaky-tests"]
provenance_urls: ["https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://konghq.com/blog/engineering/how-we-used-agentic-ai-to-fix-kong-gateways-flakiest-tests"]
refutation_status: "untested"
answers_questions: ["How do self-verifying agents handle flaky tests and oracle rot in fast feedback loops?"]
---
Agent synthesis

Self-verifying agents outperform stronger models under human review because verification, not code-writing, is now the bottleneck, and a broken or flaky oracle is the sharpest cost of that loop. The mechanism is a shift of where quality comes from: an agent that can check its own work writes a change, runs the check, reads the output, and retries until the check passes, while the human-dominated loop (diff, run tests, read app, report, repeat) stays slow and costly and does not scale past one human. Addy Osmani's note calls out three oracles in this loop: E2E tests as the hardest to trick (either the whole thing works or it does not), property-based tests for what must never happen (fast-check for JS/TS, Hypothesis for Python, proptest for Rust), and differential tests that treat the old system as the oracle during rewrites, comparing outputs on randomly generated inputs with the intended changes tracked in an approved-changes list. Testing must run fast and deterministically, or the agent learns to retry flaky tests instead of fixing them, so the core loop aims for subsecond runs with seeded randomness and isolated state. Hamel Husain's evals note adds the task-specific angle: evals tailored to users' tasks beat generic benchmarks, with fast, scoped assertions on every change and holdout discipline to avoid overfitting. The synthesis is that these task-aligned evals only reach that status when the agent runs them itself: a test the agent can pass on its own becomes the definition of done, not a scoreboard for a reviewer (see: product-specific evals beat generic benchmarks).

The Kong identify-fix-verify workflow shows what this loop looks like when the check itself is flaky. Its Opus orchestrator pulls CI failure logs for a seeded flaky test, spawns an Opus flake-fixer subagent that produces exactly one analysis and one fix and hands a summary back so context stays small, then launches a cheap Haiku verifier that polls each rerun and filters noise from other flaky tests in the suite. The orchestrator keeps spawning fresh flake-fixers until the full rerun streak is clean or a max attempt count is hit, then opens a PR for human review. A single run proves nothing about an intermittent failure, so verification by streak, fresh context between attempts, and human review before merge together answer what a single-check loop cannot. Over a week and a half this fixed 12 of 15 flakiest tests in 4-5 hours each using an average of 100-200k tokens, surfaced a conf_loader sorting bug and a concurrent auth race condition, and never touched the test files.

Together, the two sources show that oracle rot is a verification-design problem, not a model-strength problem: keep the check the agent runs itself, stable or streaked and noise-filtered, keep each fixer fresh so context does not rot, and treat every false pass or false failure as a broken oracle, not a flake. The sampled evergreen supplies the principle (the agent runs the check itself), and Kong's loop supplies the operating pattern that keeps an oracle too weak to trust usable (see: self-verifying agents need fast, oracle-backed loops, not just stronger models). Start with one E2E check or one property the agent can run in a subsecond loop, route any unstable check through a streak with a cheap verifier before trusting the loop at all, and treat every false pass as a broken oracle, not a flake.

## Where it comes from

- [[notes-on-agentic-verification|Agentic Verification]]
- [[notes-on-your-ai-product-needs-evals-hamel-husain|Your AI Product Needs Evals (Hamel Husain)]]
- [[notes-on-how-we-used-agentic-ai-to-automate-fixes-for-flaky-tests|How We Used Agentic AI to Automate Fixes for Flaky Tests]]

## What this builds on

- None yet.
