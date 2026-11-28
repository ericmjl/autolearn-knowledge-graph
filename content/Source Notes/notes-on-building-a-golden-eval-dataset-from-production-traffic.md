---
type: "source-note"
title: "Notes on: Building a Golden Eval Dataset from Production Traffic"
raw: "building-a-golden-eval-dataset-from-production-traffic"
url: "https://openrouter.ai/blog/tutorials/building-a-golden-eval-dataset-from-production-traffic/"
created_at: "2026-11-28T04:01:19Z"
updated_at: "2026-11-28T04:01:19Z"
---
- Archived full text: [[building-a-golden-eval-dataset-from-production-traffic|Full archived text, with credits]]
- Link: <https://openrouter.ai/blog/tutorials/building-a-golden-eval-dataset-from-production-traffic/>

## What it says

OpenRouter's guide argues that a golden eval dataset - reviewed production inputs paired with expected outputs, versioned in Git and run on every deploy - closes the gap between public benchmarks and the traffic a product actually serves. It walks through pulling a sample of production traffic, deduplicating and clustering it, writing human-reviewed binary or analytic rubrics, running a first evaluation to sort failures into real failures, rubric problems, and ungradeable ambiguities, and wiring the set into CI with a refresh cadence and per-PR subsets. It also shows how to run the same frozen set across model candidates through one OpenAI-compatible API, with calibration and judge-reliability caveats.

## Claims drawn from this source

- **A golden dataset is a regression test for behavior, not a benchmark.** It is a curated collection of production inputs paired with reviewed expected outputs, held out from training and evaluated on every release candidate; it runs in CI with known-good expected outputs to catch drift between deploys.
- **Production traffic is the better foundation than synthetic data.** Production examples preserve the observed distribution of intents, contain the failure modes users actually hit, and track product drift, while synthetic examples - useful only as a minority minority of the set - are marked as synthetic in metadata.
- **Size should match the job.** Roughly 10 items to explore a single issue, 20-50 reviewed items for coverage of key failure modes, and 100 to 1,000 items for a full regression set, with a smaller tens-to-low-hundreds subset kept for pull request gates.
- **Coverage of failure modes matters more than volume.** The set should weight toward the failure modes you cannot afford; under-represented intents that fail badly cost more than well-represented intents that fail gracefully.
- **Two-annotator review exposes rubric problems.** Have two people annotate a subset independently and fix the rubric until two reviewers grade the same output the same way; two rubric choices improve consistency, binary criteria and analytic rubrics over holistic ones.
- **The first evaluation pass is where the set is hardened.** Run the current production model against the set and sort failures into real failures (kept), rubric problems (expected output fixed), and ambiguous items (cut); skipping this pass hides false regressions during real deploys.
- **Version the set, rubric, and baseline together.** A dataset.jsonl, rubric.md, run harness, and baseline.json committed to Git and wired into CI with a pass-rate drop threshold plus written acknowledgment for smaller drops; refresh the set quarterly or monthly for fast-moving products, and retire items only when the behavior no longer exists.
- **LLM judges need calibration and seed robustness.** Binary criteria and a no-prose instruction keep judge output parseable; one study found inter-rater reliability between judges ranging from 0.167 to 1.00 across random-seed replications, so calibrate the judge against human-labeled examples, use a different model as judge than the model under test, and do not treat a single judge run as ground truth on high-stakes decisions.
