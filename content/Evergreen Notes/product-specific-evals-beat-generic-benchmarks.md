---
type: "evergreen"
title: "Product-Specific Evals Beat Generic Benchmarks"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-your-ai-product-needs-evals-hamel-husain", "notes-on-ai-agents-that-matter-kapoor-stroebl-siegel-nadgir-narayanan"]
provenance_urls: ["https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
---

# Product-Specific Evals Beat Generic Benchmarks

Agent synthesis

Product-specific evals beat generic benchmarks because accuracy-only evaluation misleads and produces agents that fail beyond the benchmark. Hamel Husain argues that unsuccessful AI products almost always share a root cause: weak evaluation systems, and that evals must be tailored to users' tasks rather than relying on general model benchmarks or vibe checks. The Kapoor et al. paper makes the complementary point that current agent benchmarks narrowly focus on accuracy, leaving agents needlessly complex and costly, and that this focus leads to mistaken conclusions about where accuracy gains come from.

The mechanism is a shift from one-dimensional scoring to task-aligned, held-out evaluation. Husain describes a three-level stack—unit tests, model/human eval, and A/B testing—with rising cost and cadence, plus fast, scoped assertions that run on every change and are updated from observed failures. Kapoor et al. show that inadequate or absent holdout sets cause agents to overfit and take shortcuts, and that jointly optimizing cost and accuracy can greatly reduce cost while maintaining accuracy.

Together, the sources show that product-specific evals with holdouts and cost-accuracy optimization produce agents that work beyond benchmarks. Husain's Rechat Lucy case shows plateauing performance broken by systematic evaluation rather than more prompt engineering, while Kapoor et al. argue for principled holdout design and standardized evaluation to avoid overfitting and improve reproducibility. No single source alone connects task-tailored evals, holdout discipline, and cost-accuracy tradeoffs into one path to agents that generalize past the benchmark.

## Where it comes from

- [[notes-on-your-ai-product-needs-evals-hamel-husain|Your AI Product Needs Evals (Hamel Husain)]]
- [[notes-on-ai-agents-that-matter-kapoor-stroebl-siegel-nadgir-narayanan|AI Agents That Matter (Kapoor, Stroebl, Siegel, Nadgir, Narayanan)]]

## What this builds on

- None yet.
