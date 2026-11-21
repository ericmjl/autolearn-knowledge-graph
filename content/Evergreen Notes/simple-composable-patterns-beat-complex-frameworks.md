---
type: "evergreen"
title: "Simple composable patterns beat complex frameworks"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
inputs: ["notes-on-building-effective-agents-anthropic", "notes-on-ai-agents-that-matter-kapoor-stroebl-siegel-nadgir-narayanan"]
provenance_urls: ["https://blog.anthropic.com/building-effective-agents", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
---
Agent synthesis

Simple, composable patterns outperform complex frameworks because accuracy-only optimization makes agents needlessly complex and costly. The mechanism is that when evaluation and design focus narrowly on accuracy, teams reach for heavier machinery—frameworks, specialized libraries, elaborate agentic loops—without evidence that the added complexity improves outcomes, while the underlying prompts and responses get obscured and debugging gets harder.

Anthropic's "Building effective agents" argues that the most successful implementations used simple, composable patterns rather than complex frameworks or specialized libraries, and recommends starting with the simplest viable solution—often single LLM calls with retrieval and in-context examples—adding complexity only when it demonstrably improves outcomes, since agentic systems trade latency and cost for performance. It also warns that abstraction layers obscure underlying prompts and responses, making debugging harder and tempting unnecessary complexity, and stresses tool and interface design, transparency, and simplicity as core principles.

Kapoor, Stroebl, Siegel, Nadgir, and Narayanan's "AI Agents That Matter" supplies the cost-side evidence: current benchmarks and evaluation practices narrowly focus on accuracy, which makes state-of-the-art agents needlessly complex and costly, misattributes accuracy gains, and conflates model and downstream developer needs. Their proposed joint cost-accuracy optimization shows potential to greatly reduce cost while maintaining accuracy, alongside better holdout sets and standardization to avoid overfitting and fragile agents.

Together, the two sources show that complexity is often an artifact of accuracy-only evaluation rather than a requirement of the task: the Anthropic post gives the design rule (start simple, compose, add complexity only when it pays), while the benchmark paper explains why the field overshoots (accuracy-only scoring rewards needless machinery). No single source makes both points; the combination turns "simple patterns win" from a design preference into a diagnosis of how evaluation incentives produce bloated agents.

## Where it comes from

- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]
- [[notes-on-ai-agents-that-matter-kapoor-stroebl-siegel-nadgir-narayanan|AI Agents That Matter (Kapoor, Stroebl, Siegel, Nadgir, Narayanan)]]

## What this builds on

- None yet.
