---
type: "evergreen"
title: "Small tuned evaluators carry the per-call layer; tolerance is a recall number"
created_at: "2026-11-23T03:03:00Z"
updated_at: "2026-11-23T03:03:00Z"
inputs: ["notes-on-introducing-the-evaluation-engine-build-high-accuracy-evaluators-and-guardrails-fitted-to", "purpose-built-small-evaluators-make-product-specific-evals-run-on-every-transaction"]
provenance_urls: ["https://www.splunk.com/en_us/blog/artificial-intelligence/introducing-evaluation-engine.html", "https://galileo.ai/blog/llm-evaluation-step-by-step-guide", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["How accurate are purpose-built small evaluators versus frontier judges on every transaction, and what accuracy can teams tolerate at the per-call layer?"]
---
Agent synthesis

A small tuned evaluator can carry the per-call layer of production evaluation, and the tolerance to set on it is a recall number, not an accuracy number. Splunk's Evaluation Engine tunes Eval-G1 models from a team's own traces and expert labels, predicts one token per verdict in about 0.34 seconds, and matches or beats frontier judges where the miss costs the most: it caught 99.4% of leaked personal data at 0.958 F1, ahead of every model tested, while the best frontier judge reached 0.902. The mechanism is that a one-token adapter on a shared base model costs about 98% less per evaluation than a frontier judge, so coverage stops being a sample and becomes every transaction.

The evidence cuts both ways. On PII, recall is 0.994 and the tuned evaluator wins outright. On toxicity, precision rivals frontier judges but recall does not: three frontier judges were precise yet caught fewer than 60% of toxic messages, and the tuned evaluator's F1 (0.847) trails GPT 6 Sol's 0.903. On conciseness, the tuned evaluator scores 0.871, beating three of five frontier judges and coming within 1.3 points of Claude Opus 5.5. The gap is therefore not "small models are weaker," it is "small models are weaker on categories where every miss is a leak, and roughly matched on judgment calls that need an explicit rubric."

Read next to the sampled evergreen on purpose-built small evaluators, the earlier note set the economics: once a judge is cheap enough to run per interaction, evaluation becomes a per-call control instead of a periodic audit. The Splunk source adds the accuracy numbers and the per-call metric that decides whether that claim holds. The sampled note stops at the cost side; the new source shows the accuracy side is mostly a recall story. Teams should set the tolerance for the per-call layer by the cost of a miss: near-zero false negatives for PII-style categories, and judged-by-recall for guardrails, while holding a frontier judge for the categories where it still leads.

Run the tuned evaluator on 100% of traffic for the categories where a miss is irreversible, keep a frontier judge for judgment calls and for the residual categories, and report the recall of whichever judge is live as a release metric rather than just F1.

## Where it comes from

- [[notes-on-introducing-the-evaluation-engine-build-high-accuracy-evaluators-and-guardrails-fitted-to|Introducing the Evaluation Engine: Build High-Accuracy Evaluators and Guardrails Fitted to Your Agents | Splunk]]

## What this builds on

- [[purpose-built-small-evaluators-make-product-specific-evals-run-on-every-transaction|Purpose-built small evaluators make product-specific evals run on every transaction]]
