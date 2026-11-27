---
type: "source-note"
title: "Notes on: Evaluating LLMs in production: From drift detection to continuous monitoring"
raw: "evaluating-llms-in-production-from-drift-detection-to-continuous-monitoring"
url: "https://wandb.ai/site/articles/evaluating-llms-in-production/"
created_at: "2026-11-27T03:01:40Z"
updated_at: "2026-11-27T03:01:40Z"
---
- Archived full text: [[evaluating-llms-in-production-from-drift-detection-to-continuous-monitoring|Full archived text, with credits]]
- Link: <https://wandb.ai/site/articles/evaluating-llms-in-production/>

## What it says

The article lays out a continuous LLM evaluation framework for production systems: four drift types (data, model, retrieval, behavioral), a living evaluation set split into a dev set and a test set, temperature 0 for judge and target, strategic manual sampling for judge drift, a controlled RAG drift experiment showing a 40% quality drop from one outdated document, component-level trace visibility via W&B Weave dashboards that surface token/cost drift before quality drift, and a continuous evaluation loop that scores recent production traffic through an Evaluation API. It argues that aggregate metrics tell you something is wrong while component-level traces tell you what is wrong and where.

## Claims drawn from this source

- **Four distinct drift types occur in production LLM systems.** Data drift (inputs shift from the trained distribution), model drift (provider updates shift intrinsic quality), retrieval drift (vector DB returns irrelevant or stale context), and behavioral drift (external APIs or user expectations change). Each requires a different monitoring approach.
- **Static offline evaluation sets are invalidated by production realities.** The evaluation set must be a living artifact refreshed with representative production examples, split into a dev set used during rapid iteration and a rarely-touched test set that provides an unbiased ground truth.
- **Judges and targets run at temperature 0 and keep prompts identical.** Prompts must be identical across comparisons and both the judge and the target model run at temperature 0 to eliminate sampling variance; otherwise genuine improvements are indistinguishable from random fluctuation.
- **Judge drift is caught by strategic manual sampling.** LLM judges occasionally drift and give uneven ratings after provider model updates or edge-case inputs; regular strategic sampling of judged outputs surfaces scoring bugs and strange edge cases that automated methods miss.
- **A single outdated document can drop RAG quality 40%.** In the controlled experiment, adding one outdated LangChain v0.0.200 page to the healthy document pool dropped the judge score from 5.0 to 3.0 (40%), while average relevance increased (0.418 to 0.471) because the stale page scored 0.631, higher than current docs.
- **Cost and efficiency drift precede quality drift.** In the three-day simulation, average quality held at 4.0 while total tokens rose 12% (696 to 782) and average retrieval relevance dropped 3% (0.413 to 0.399), with traces showing the retrieval context growing from roughly 350-450 prompt tokens to 450-470.
- **Aggregate metrics say something is wrong; component-level traces say what is wrong.** Token/cost alerts trigger only after thousands of degraded queries, and average quality drops appear only in user complaints; the retrieval trace is the first anomaly, showing the stale document with the anomalously high relevance score in the first degraded query.
- **A unified platform connects monitoring, evaluation, and traces.** W&B Weave (and equivalents like LangSmith, Langfuse, or Arize Phoenix) ties structured logging, @weave.op-style trace capture, time-series dashboards, and an Evaluation API over recent production traffic into one loop, scoring up to 100 recent queries and triggering investigation on anomalies.
