---
type: "evergreen"
title: "Golden sets built from production traffic beat benchmarks built from imagined edge cases"
created_at: "2026-11-28T04:01:45Z"
updated_at: "2026-11-28T04:01:45Z"
inputs: ["notes-on-building-a-golden-eval-dataset-from-production-traffic", "product-specific-evals-beat-generic-benchmarks"]
provenance_urls: ["https://openrouter.ai/blog/tutorials/building-a-golden-eval-dataset-from-production-traffic/", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["How do teams build and maintain product-specific eval sets when labeled data is scarce, and what does overfitting to a benchmark cost in production?"]
---
Agent synthesis

Golden sets built from production traffic beat benchmarks built from imagined edge cases. A golden dataset is a curated collection of real production inputs paired with reviewed expected outputs, versioned in Git and run before every deploy, so a change to the prompt or model is checked against the traffic the user actually sends, not general capability.

The mechanism is distribution match. The product-specific evals note argues that accuracy-only evaluation misleads and that tasks must be tailored to users' actual work; the new source shows the operational recipe: pull a sample of production traffic (a few hundred raw items), deduplicate and cluster so paraphrases do not dominate, weight the set toward failure modes that are hard to afford, and write expected outputs as binary or analytic rubrics that two reviewers grade the same way. Synthetic examples remain a minority fill for known coverage gaps, never a foundation.

The evidence runs one way. The evals evergreen holds that overfitting to a benchmark masks cost and complexity; the new source supplies the fix: freeze the set, record the commit hash, and compare models through one API on the same frozen set rather than trusting a public benchmark, while watching cost per call because a two-percentage-point accuracy gain can mean thirty times the cost. The set itself needs a lifecycle: a quarterly refresh of aged items (monthly if the product changes fast), no retirement of passing items, and a Git-diff-visible rubric so a pass-rate move is always attributable.

Neither input alone covers the whole path from raw traffic to a trustworthy release gate; together they say a product-specific eval set is a continuously maintained regression suite for behavior, not a one-time benchmark score. Pull production traffic, cluster it toward failures users hit, review expected outputs with binary rubrics, wire it into CI, refresh it on schedule, and run every deployment candidate against the frozen set before any A/B test.

## Where it comes from

- [[notes-on-building-a-golden-eval-dataset-from-production-traffic|Building a Golden Eval Dataset from Production Traffic]]

## What this builds on

- [[product-specific-evals-beat-generic-benchmarks|Product-Specific Evals Beat Generic Benchmarks]]
