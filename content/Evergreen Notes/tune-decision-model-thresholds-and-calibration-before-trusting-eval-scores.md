---
type: "evergreen"
title: "Tune decision-model thresholds and calibration before trusting eval scores"
created_at: "2026-11-21T07:02:12Z"
updated_at: "2026-11-21T07:02:12Z"
inputs: ["notes-on-how-to-use-decision-models-for-evals-hamel-s-blog", "product-specific-evals-beat-generic-benchmarks"]
provenance_urls: ["https://hamel.dev/blog/posts/decision-model-evals/", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
---
Agent synthesis

Decision model scores are useless as-is: the default 0.50 threshold silently discards most of the signal, so eval judges built on decision models must tune the threshold against labeled data and check calibration before they earn trust. A model that assigns every failure a score of 0.40 and every pass a score of 0.10 separates classes perfectly at 0.30 while flagging nothing at the default. The fix is a concrete loop: set minimum precision and recall requirements tied to the business (80% on both for an alerting system), tune thresholds with stratified cross-validation on saved scores, rule out models that cannot meet the minimums, then check whether predicted failure probabilities match observed rates and apply Platt scaling only if calibration is poor.

The cost-versus-accuracy tradeoff follows the same shape as the joint cost and accuracy discipline that product-specific evals demand: Perplexity Decider reached F1 0.79 at 0.82 cents per 100 eval runs, while OpenAI Decisions hit F1 0.87 at 3.72 cents, roughly 4.5x the cost. Calibration is a separate axis from F1: Perplexity, Liquid d1, and Clef Flash moved closer to the diagonal after Platt scaling (one Clef group predicted ~8% failure probability while 60% of traces failed), while Jev and d1-ultra were already well calibrated and need little adjustment. Evaluating decision models looks like evaluating any classifier, but the eval loop adds a second filter: narrow, per-failure-mode binary judges beat one broad judge, and harder tasks may still justify paying for an LLM.

Combined with the product-specific evals discipline, the new source supplies the operating mechanics that generic benchmarks hide: threshold tuning against real traces, explicit precision-recall minimums, calibration checks, and cost vs performance accounting, all per model and per task. No single source alone makes this connection: the eval-discipline source says to build evals for your own product, while the new source shows exactly how to operationalize that discipline with fast, cheap classifiers.

Start by writing the binary criteria, saving model scores and labels, then tune and calibrate before comparing models or trusting any score.

## Where it comes from

- [[notes-on-how-to-use-decision-models-for-evals-hamel-s-blog|How To Use Decision Models for Evals – Hamel’s Blog]]

## What this builds on

- [[product-specific-evals-beat-generic-benchmarks|Product-Specific Evals Beat Generic Benchmarks]]
