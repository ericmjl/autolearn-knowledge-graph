---
type: "evergreen"
title: "Per-call judges need risk-calibrated guardrails, not just cheap evals"
created_at: "2026-11-23T05:03:43Z"
updated_at: "2026-11-23T05:03:43Z"
inputs: ["notes-on-task-specific-llm-evals-that-do-don-t-work", "purpose-built-small-evaluators-make-product-specific-evals-run-on-every-transaction"]
provenance_urls: ["https://eugeneyan.com/writing/evals/", "https://galileo.ai/blog/llm-evaluation-step-by-step-guide", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["Does per-transaction product-specific evaluation hold up in high-stakes deployments where a false negative matters more than cost?"]
---
Agent synthesis

Per-call product-specific evaluation does not hold up in high-stakes deployments on cheap judges alone: even 100%-of-traffic evaluation misses the 5-10% factual inconsistency that inheres in RAG and prompt-engineered systems, so it must be paired with a risk-calibrated guardrail layer. The mechanism that makes per-transaction evals affordable is the purpose-built small evaluator: a judge that is cheap enough to run on every call turns evaluation from a periodic audit into a per-call control, which is the economic precondition for the holdout-and-cost-accuracy discipline. The Eugene Yan source adds the calibrated-bar half: off-the-shelf evals barely correlate with application-specific performance, accuracy is too coarse (recall and precision across thresholds, ROC-AUC, PR-AUC, and distribution separation are the right metrics), and typical factual inconsistency is 5-10% even after grounding, with below 2% prohibitively hard. In high-stakes, external-facing deployments (medical, financial) the false negative on a miss matters more than the judge cost, so the bar must be set high and a guardrail must catch the residual low-margin failures. Internal-facing deployments accept a lower bar and can start small, per the a16z internal-vs-external split.

The two sampled inputs do not say this together: the Splunk-small-evaluator evergreen argues that cost no longer forces sampling, but it stops at the economic precondition and never states what the per-call judge misses; the Yan source argues that the bar must be risk-calibrated, but it predates per-call judges and says nothing about 100%-traffic evaluation. The synthesis is that cheap per-call evaluation and risk-calibrated guardrails are complements: the judge catches the cheap, high-volume slice, while the guardrail catches the residual 5-10% that a single-threshold judge will miss, especially when a false negative is costly. The evidence is concrete: Voiceflow's harness caught a 10% intent-classification drop on a model upgrade; NLI consistency evals finish a few hundred samples past the point of obvious inconsistency; the survival rule is to measure judge cost per interaction before choosing an eval stack, and to refuse to treat a per-call pass as proof of correctness.

When false negatives matter more than cost, run the cheap judge on every call and still keep a risk-calibrated guardrail, an active-learning label loop, and a hard case review; do not treat a per-call pass rate as proof the system is safe (see: product-specific evals beat generic benchmarks).

## Where it comes from

- [[notes-on-task-specific-llm-evals-that-do-don-t-work|Task-Specific LLM Evals that Do & Don't Work]]

## What this builds on

- [[purpose-built-small-evaluators-make-product-specific-evals-run-on-every-transaction|Purpose-built small evaluators make product-specific evals run on every transaction]]
