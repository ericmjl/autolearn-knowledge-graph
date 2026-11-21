---
type: "evergreen"
title: "Zone maps, characterization tests, and durable research artifacts make brownfield changes trustworthy"
created_at: "2026-11-21T09:03:22Z"
updated_at: "2026-11-21T09:03:22Z"
inputs: ["notes-on-brownfield-agentic-engineering", "agents-degrade-on-repo-tasks-and-may-falsely-report-success", "self-verifying-agents-need-fast-oracle-backed-loops-not-just-stronger-models"]
provenance_urls: ["https://addyo.substack.com/p/brownfield-agentic-engineering", "https://arxiv.org/abs/2401.07339", "https://addyosmani.com/blog/ai-coding-workflow/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/"]
refutation_status: "untested"
---
Agent synthesis

Brownfield agentic engineering makes cheap changes trustworthy by making hidden constraints visible: a zone map drawn by blast radius, characterization tests that pin today's behavior, and a durable research memo that outlives the session.

An old codebase is no longer a complete description of how the system behaves. Institutional knowledge, duct tape, legacy services, and other teams' dependencies live outside the tree, and an agent left unsupervised will still fix behavior the business actually runs on. So the map should carry only what the code cannot say: business nuance, trade-offs, guidelines, external constraints, and the history behind counter-intuitive implementations. Within that map, a person draws the zones, not the agent, because left to choose, the agent starts in the scariest file, where the names are most interesting. Green zones (good tests, isolation) get a tight loop; yellow zones get tests first; red zones (auth, billing, permissions) get a human on every step or not happen at all. Zones only move when earned: yellow becomes green once characterization tests exist and the module owner reviews the agent's first changes.

The evidence is concrete. SWE Refactor Bench reports only 28 of 520 agent runs passed its migration audit, and tests can stay green while a replacement still calls the legacy implementation. Bun's Zig-to-Rust port ran about 50 workflows over 11 days from a 535,000-line codebase with two adversarial reviewers per unit and the entire pre-existing test suite as the merge gate; hours went into a porting guide before any agent ran. Stripe's migration was done with codemods, with agents handling the exception queue. The evidence needed to choose between options has not changed, even though agents have lowered the price of trying several plausible implementations. (See: agents degrade on repo tasks and may falsely report success.)

Once behavior is pinned and the map is durable, parallelize last: one unit with a dependable judge, recovery path, and review format people can absorb. Automation leads with intent, changed invariants, test results, parity mismatches, and the rollback route; human attention goes first to the largest blast radius and weakest oracle. Track lead time, review minutes, human interventions, escaped defects, rollbacks, and oracle mismatches, not lines generated. A green suite with all traffic still on the old path is busywork. Start with zero-risk work, a synthetic user journey instead of guesswork when a surface only production traffic really understands, and finish one route end to end, including its deletion.

## Where it comes from

- [[notes-on-brownfield-agentic-engineering|Brownfield Agentic Engineering]]

## What this builds on

- [[agents-degrade-on-repo-tasks-and-may-falsely-report-success|Agents degrade on repo tasks and may falsely report success]]
- [[self-verifying-agents-need-fast-oracle-backed-loops-not-just-stronger-models|Self-verifying agents need fast, oracle-backed loops, not just stronger models]]
