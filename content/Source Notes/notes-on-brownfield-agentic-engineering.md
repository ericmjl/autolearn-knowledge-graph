---
type: "source-note"
title: "Notes on: Brownfield Agentic Engineering"
raw: "brownfield-agentic-engineering"
url: "https://addyo.substack.com/p/brownfield-agentic-engineering"
created_at: "2026-11-21T09:02:01Z"
updated_at: "2026-11-21T09:02:01Z"
---
- Archived full text: [[brownfield-agentic-engineering|Full archived text, with credits]]
- Link: <https://addyo.substack.com/p/brownfield-agentic-engineering>

## What it says

Addy Osmani argues that agentic engineering in old codebases is about making hidden constraints visible and cheap changes trustworthy: draw zones (green/yellow/red) by blast radius and test quality, record what the code cannot say, make research durable across sessions, use harness-like enforcement for repeated corrections, start with zero-risk work and characterization tests, migrate in complete units, parallelize last, and track agents' visible cost on ambiguity rather than lines generated.

## Claims drawn from this source

- **Draw zones by blast radius, not by agent preference.** Green zones get a tight agent loop, yellow zones require characterization tests first, red zones (auth, billing, permissions) require a human and are not unsupervised rewrites. A person draws the map, not the agent, and zones only move when earned.
- **Give agents only what the code cannot say.** Agents infer a lot from source; the durable value is business nuance, trade-offs, guidelines, domain rules, external constraints, and historical context behind counter-intuitive implementations.
- **Make agent research durable across sessions.** Yellow and red work needs a separate read-only pass that produces a short comprehension memo (entry points, owners, callers, abstractions, tests, production signals, history, open questions) with claims citing files, issues, ownership records, or dashboards, because chat history is not a system of record.
- **Pin behavior with characterization tests before agents improve it.** Characterization tests pin today's behavior including ugly parts, because some of that behavior is what the business runs on; when an agent makes them pass, a separate pass or a person should pin the behavior first, or the green suite encodes the implementation just invented.
- **A migration is complete only when the old dependency is removed.** Half-finished migrations confuse agents: search returns the old approach in forty files, the replacement in twelve, and a shim presenting both as current; SWE Refactor Bench found only 28 of 520 agent runs passed the migration audit, and tests can stay green while a replacement still calls the legacy implementation.
- **Parallelize last, review automation with intent.** Software factories can run many changes at once only after one unit has a dependable judge, recovery path, and review format; automation should lead with intent, changed invariants, test results, parity mismatches, and rollback route, with human attention going first to the largest blast radius and weakest oracle.
- **Agents put a visible price on ambiguity.** Track lead time, review minutes, human interventions, escaped defects, rollbacks, oracle mismatches, and suppressions; tribal conventions become recurring review comments; GitHub, Shopify and Spotify examples show the pattern, and for migrations track remaining old imports, traffic on the new path, parity mismatches, and legacy dependencies removed.
