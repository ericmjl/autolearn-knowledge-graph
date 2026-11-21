---
type: "evergreen"
title: "Capability evals climb; regression suites hold the line"
created_at: "2026-11-21T13:03:16Z"
updated_at: "2026-11-21T13:03:16Z"
inputs: ["notes-on-demystifying-evals-for-ai-agents", "layered-evals-work-best-split-across-separate-calls"]
provenance_urls: ["https://www.anthropic.com/research/demystifying-evals-for-ai-agents", "https://hamel.dev/blog/posts/evals/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do teams implement layered evals split across separate calls in practice, and what does that look like for eval cadence?"]
---
Agent synthesis

Capability evals and regression evals run as a two-stage stack, where low-pass capability runs climb and high-pass regression suites hold the line. The mechanism is that the same suite passes tasks the agent already handles well: at low pass rates it measures headroom, while at near-100% pass rates it catches backsliding. Once capability tasks saturate, the same tasks graduate into a regression suite run continuously to catch drift, and the failure to separate these two roles produces deceptive scores.

The new source note (Anthropic's eval guide) supplies the two-role structure directly: capability evals start at a low pass rate targeting tasks the agent struggles with, regression evals demand nearly 100% pass rates, and capability evals with high pass rates graduate into a regression suite run continuously. It also shows why saturation hides gains, citing SWE-Bench Verified rising from 30% to above 80% and Qodo, initially unimpressed by one-shot coding evals, building a new agentic eval framework. The existing layered-evals note (Husain's three levels, unit tests, model/human eval, A/B testing, kept as separate calls) supplies the placement of these checks: fast scoped checks on every change, model and human evals on a cadence, A/B testing reserved for significant changes.

Together the two inputs show that eval cadence is a lifecycle decision as much as a cost decision. A layered stack that runs low-pass capability evals continuously and promotes saturated tasks into regression suites keeps each check honest about what it measures, instead of one eval chasing both headroom and guardrail roles. No single input makes this full claim: the layered note describes levels and separate calls but not the capability-to-regression lifecycle, while the new note describes the lifecycle but not the layered placement across cadences. The combination yields a concrete rule for splitting checks across separate calls: put low-pass capability tasks in the cheap frequent layer, and promote them into a near-100% regression layer once they pass consistently, so the stack an agent climbs is never confused with the stack it must maintain.

Start with 20-50 simple tasks drawn from real failures and run both roles side by side on each change. Watch for saturation in the capability layer and graduate tasks before the suite stops climbing, or before the regression layer silently absorbs headroom it no longer measures.

## Where it comes from

- [[notes-on-demystifying-evals-for-ai-agents|Demystifying evals for AI agents]]

## What this builds on

- [[layered-evals-work-best-split-across-separate-calls|Layered evals work best split across separate calls]]
