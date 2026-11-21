---
type: "evergreen"
title: "Layered evals work best split across separate calls"
created_at: "2026-11-21T03:02:25Z"
updated_at: "2026-11-21T03:02:25Z"
inputs: ["notes-on-your-ai-product-needs-evals-hamel-husain", "notes-on-building-effective-agents-anthropic"]
provenance_urls: ["https://hamel.dev/blog/posts/evals/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
---
Agent synthesis

Evals work best as a layered stack of unit tests, model/human eval, and A/B testing, with guardrails and evals split across separate LLM calls rather than embedded in a single prompt. The mechanism is that each layer has different cost and cadence: fast, scoped unit tests run on every change, model and human eval runs on a set cadence, and A/B testing is reserved for significant changes. Keeping evaluation as its own layer, and separating guardrails and evals from the main generation call, lets each check do its job without being diluted inside one prompt.

Hamel Husain's "Your AI Product Needs Evals" supplies the layered stack: Level 1 unit tests, Level 2 model and human eval, Level 3 A/B testing, with rising cost and cadence, plus product-specific evals rather than generic benchmarks, and eval infrastructure reused for debugging, data curation, and fine-tuning. Anthropic's "Building effective agents" supplies the call-separation principle: guardrails and evals work better when split across separate LLM calls, and parallelization across independent subtasks with voting improves complex tasks. Anthropic also stresses simple, composable patterns over complex frameworks, and careful testing in sandboxed environments for agents.

Together, the two sources show that evaluation is not a bolt-on checklist but an architectural layer: a stack of progressively costlier checks, each run as its own step rather than folded into the generation prompt. No single source alone makes this full claim—Husain describes the layers but not the separate-call mechanism, while Anthropic describes separate calls but not the three-level stack. The combination yields the stronger design rule: build the layered eval stack, and implement each layer as its own LLM call or check, so evals stay cheap, frequent, and honest about what they measure.

## Where it comes from

- [[notes-on-your-ai-product-needs-evals-hamel-husain|Your AI Product Needs Evals (Hamel Husain)]]
- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]

## What this builds on

- None yet.
