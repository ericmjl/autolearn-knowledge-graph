---
type: "source-note"
title: "Notes on: How To Use Decision Models for Evals – Hamel’s Blog"
raw: "how-to-use-decision-models-for-evals-hamel-s-blog"
url: "https://hamel.dev/blog/posts/decision-model-evals/"
created_at: "2026-11-21T07:01:28Z"
updated_at: "2026-11-21T07:01:28Z"
---
- Archived full text: [[how-to-use-decision-models-for-evals-hamel-s-blog|Full archived text, with credits]]
- Link: <https://hamel.dev/blog/posts/decision-model-evals/>

## What it says

Hamel Husain and Antaripa Saha evaluate decision models (TypeSafe Jev, Perplexity Decider, Liquid d1/d1-ultra, Cloudflare Clef Flash, OpenAI Decisions) as low-cost alternatives to LLM judges for automated evals. Using 100 apartment-leasing traces labeled pass/fail, they compare F1 after tuning the decision threshold, calibration of predicted failure probabilities via Platt scaling, and cost, finding OpenAI Decisions highest F1 at ~4.5x cost of Perplexity, with feasibility depending on minimum precision/recall requirements and business goals.

## Claims drawn from this source

- **Decision models are a low-cost alternative to LLM judges for automated evals.** Decision models like TypeSafe's Jev, Perplexity's Decider, Liquid's d1, Cloudflare's Clef, and OpenAI's Decisions API promise fast, inexpensive classification as alternatives to LLM judges for automated evals.
- **The default 0.50 decision threshold often leaves performance on the table.** A model could assign every failure a score of 0.40 and every passing trace a score of 0.10, classifying perfectly at a 0.30 threshold but catching nothing at the default 0.50.
- **Threshold choice trades precision against recall against business goals.** Lowering the threshold catches more failures but raises false alarms; criminal trials emphasize precision while cancer screening emphasizes recall, and the right tradeoff depends on the use case.
- **Threshold tuning with hard minimum precision and recall requirements is the right workflow.** The authors restrict threshold tuning to values meeting at least 80% precision and recall during training, using stratified five-fold cross-validation and reporting that no threshold qualifies if none meets both minimums.
- **Cost vs performance matters more than raw F1 alone.** Perplexity Decider reached F1 0.79 at 0.82 cents per 100 eval runs, while OpenAI Decisions reached F1 0.87 at 3.72 cents per 100 runs, about 4.5 times the cost.
- **Decision models' probabilities are not always calibrated; Platt scaling can fix it.** Perplexity, Liquid d1, and Clef Flash move closer to the diagonal after calibration; one Clef group predicted ~8% failure probability while 60% of traces failed, while Jev and d1-ultra were already well calibrated.
- **Binary pass/fail evals with narrow, per-failure-mode judges beat broad classifiers.** The post recommends binary pass/fail evals and building a separate judge for each failure mode rather than one broad judge prompt.
- **Harder eval tasks may still justify paying for LLM judgments.** OpenAI Decisions uses GPT-6 Luna and delivered the highest F1 at the highest cost, and Randy Olson found decision models match LLMs on classification and routing but LLMs pull ahead on knowledge and reasoning tasks.
