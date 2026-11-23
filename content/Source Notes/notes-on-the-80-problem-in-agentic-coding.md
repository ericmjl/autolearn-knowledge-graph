---
type: "source-note"
title: "Notes on: The 80% Problem in Agentic Coding"
raw: "the-80-problem-in-agentic-coding"
url: "https://addyo.substack.com/p/the-80-problem-in-agentic-coding"
created_at: "2026-11-23T04:01:17Z"
updated_at: "2026-11-23T04:01:17Z"
---
- Archived full text: [[the-80-problem-in-agentic-coding|Full archived text, with credits]]
- Link: <https://addyo.substack.com/p/the-80-problem-in-agentic-coding>

## What it says

Addy Osmani argues that agentic coding has shifted from a 70%-completion tool to an 80%-plus one, with the nature of the problem changing from syntax bugs to conceptual failures. AI-assisted development produces more code faster but moves the bottleneck to review and comprehension: high-adoption teams merged 98% more PRs while review times ballooned 91% and PR size grew 154%. The human role inverts from implementer to orchestrator, and the cost is comprehension debt: generation and discrimination are different capabilities, and heavy reliance erodes manual skill and supervision quality. The durable response is deliberate supervision patterns: declarative success criteria, fresh-context review, automated verification, TDD, pairing, explaining-to-AI, and alternating manual work to maintain muscle memory.

## Claims drawn from this source

- **Agentic coding crossed an 80% threshold.** Karpathy moved from ~80% manual+autocomplete to 80% agent coding in weeks in late 2025; Boris Cherney reports 100% AI-written code shipped across 22-27 PRs a day; Armin Ronacher's 5,000-developer poll found 44% write less than 10% of code manually.
- **AI errors evolved from syntax bugs to conceptual failures.** Assumption propagation, abstraction bloat, dead code accumulation, and sycophantic agreement persist despite system prompts, CLAUDE.md instructions, and plan mode because agents optimize for coherent output rather than questioning premises.
- **The verification bottleneck overtook code generation.** Only 48% of developers consistently check AI-assisted code before committing, and 38% find reviewing AI-generated logic requires more effort than reviewing human code; high-adoption teams merged 98% more PRs while review times rose 91% and PR size grew 154% (Faros AI, DORA 2025).
- **Comprehension debt is the hidden cost of agentic coding.** Generation and discrimination are different cognitive capabilities; over time you may understand less of your own codebase and review degrades into rubber-stamping, captured by the addiction loop where the final 10% feels tantalizingly close.
- **The durable supervision patterns are declarative success criteria and automated verification.** Spend 70% of effort on problem definition and verification strategy and 30% on execution; write tests first and let the agent iterate until they pass; fresh-context code reviews catch agent mistakes; CI/CD and linters act as guardrails.
- **Skill atrophy needs deliberate counter-patterns.** Junior developers who rely on AI for everything report less problem-solving confidence; counter-patterns are TDD (write tests or think through cases first), pairing with seniors, asking the AI to justify its approach, and alternating some manual implementation to maintain muscle memory.
- **The human role shifts from implementer to orchestrator.** Engineers who thrive reconceptualize their role as architectural oversight and quality control rather than line-by-line coding, which feels a lot like management.
