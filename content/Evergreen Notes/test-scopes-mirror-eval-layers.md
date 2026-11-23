---
type: "evergreen"
title: "Test scopes mirror eval layers"
created_at: "2026-11-23T09:06:58Z"
updated_at: "2026-11-23T09:06:58Z"
inputs: ["notes-on-test-wikipedia", "layered-evals-work-best-split-across-separate-calls"]
provenance_urls: ["https://en.wikipedia.org/wiki/Test", "https://hamel.dev/blog/posts/evals/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How should layered evals be automated in CI for agentic loops, and what do they miss when they run only at the end?"]
---
Agent synthesis

Testing is not one activity but a family of scoped judgments, and agent eval stacks should inherit that structure. The source note supplies the taxonomy: test as assessment measures the respondent's knowledge, software testing covers computing and systems tests, engineering testing splits into metal, mechanical, proof, product, stress, and system testing, and statistical hypothesis testing is a separate branch. The layered-evals evergreen supplies the cadence: fast unit tests on every change, model and human eval on a set cadence, and A/B testing reserved for significant changes, each layer run as its own call.

The synthesis is that scope and cost rise together. A unit-scope check scopes the claim to a small function and costs almost nothing; a stress or system test scopes the claim to the whole structure and costs more; an A/B test scopes the claim to a cohort and costs the most. Mapping the two taxonomies shows that a CI pipeline which runs only a final eval after the agent ships collapses every scope into one check, exactly the single-test mistake the taxonomy warns against. The evaluation belongs at each level of the loop, not only at the end.

An agent loop benefits the same way: a unit-scope check inside the loop, a structural check at the task boundary, and a cohort check on significant changes. This keeps each layer honest about what it measures, because flatter checks hide the failures the higher-cost scopes catch (see: layered evals work best split across separate calls). Start by enumerating the product's test scopes, then assign each to an eval layer with its own cadence, and wire each layer into CI as a separate step.

## Where it comes from

- [[notes-on-test-wikipedia|Test - Wikipedia]]

## What this builds on

- [[layered-evals-work-best-split-across-separate-calls|Layered evals work best split across separate calls]]
