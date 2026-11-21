---
type: "source-note"
title: "Notes on: Agentic Verification"
raw: "agentic-verification"
url: "https://addyo.substack.com/p/agentic-verification"
created_at: "2026-11-21T03:07:01Z"
updated_at: "2026-11-21T03:07:01Z"
---

# Notes on: Agentic Verification

- Archived full text: [[agentic-verification|Full archived text, with credits]]
- Link: <https://addyo.substack.com/p/agentic-verification>

## What it says

Addy Osmani argues that the bottleneck for LLM agents has moved from writing code to verifying it. A self-verifying agent writes a change, runs a check, reads the output, and retries until the check passes, which is far more valuable than a slightly better model. He lays out a spectrum of tests suited to agents: E2E tests as the strongest oracle, property-based tests for what must never happen, differential tests against the old system during rewrites, and fast, deterministic loops so the agent learns the right incentives.

## Claims drawn from this source

- **Verification, not code-writing, is now the bottleneck.** Today's models are good enough that the major bottleneck is not code-writing but the ability to verify that the code they've written is correct.
- **Self-verifying agents beat human-dominated feedback loops.** If the agent can test its own output, it writes a change, runs the check, reads the output, and tries again over and over until it can pass the check. I would always prefer a much better feedback loop to a slightly better model.
- **Tests are how agents sense the world.** Tests are also how your agent senses the world and knows when it's done.
- **E2E tests are the best oracle for agents.** An E2E test is what a human would do and is very hard to trick: either the whole thing works, or it doesn't. They define 'done' ('Make this E2E test pass'), tell the agent what's wrong, and work on the agent's local configuration and deployment environment.
- **Property-based tests reverse the premise of example-based tests.** The agent makes up its own test examples that succeed based on its own internal logic; properties force it to deal with any input generated. Tools include fast-check for JS/TS, Hypothesis for Python, and proptest for Rust.
- **Differential testing uses the old system as the oracle.** Run old and new systems side by side with the same randomly generated inputs and replay sample live traffic; mismatches are bugs or documented breaking changes.
- **Slow or flaky tests teach the agent the wrong lesson.** If the tests are slow or unstable, the agent will learn that sometimes just restarting the test is better than trying to fix the problem; for the core loop, subsecond is great, and flakiness should be isolated and removed immediately.
