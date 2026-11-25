---
type: "evergreen"
title: "Claim-level judges need repeated re-validation, not one-time calibration"
created_at: "2026-11-25T04:02:34Z"
updated_at: "2026-11-25T04:02:34Z"
inputs: ["notes-on-reliability-without-validity-a-systematic-large-scale-evaluation-of-llm-as-a-judge-models", "claim-level-faithfulness-is-the-actionable-check-that-a-grounded-model-used-its-context"]
provenance_urls: ["https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How should the claim-level faithfulness judge be kept calibrated as the model, prompt, or retrieved-document distribution drifts over time?"]
---
Agent synthesis

Calibrating a faithfulness judge once and treating it as durable instrumentation is the failure this pair of sources closes. Grounding never removes hallucination, and the claim-level check that measures it inherits the judge's own limits: exact-match agreement overstates chance-corrected agreement by 33-41 percentage points, judge rankings shift by up to 14 positions across benchmarks, and test-retest reliability above 0.95 can coexist with severe position bias. A judge tuned on 20-50 human-labeled answers and reused next quarter is measuring a changed instrument. The fix is a standing validation loop, not a one-time calibration: chance-correct with Cohen's kappa, run paired AB+BA position swaps, replicate at temperature 0 with caching disabled, cross-validate on at least two benchmarks of contrasting label structure, and audit the consistency-bias paradox when test-retest tops 0.95. (see: claim-level faithfulness is the actionable check that a grounded model used its context) Run those checks whenever the model, prompt, or retrieved-document distribution changes, and gate releases on both the faithfulness score and the validation evidence, not on the score alone.

## Where it comes from

- [[notes-on-reliability-without-validity-a-systematic-large-scale-evaluation-of-llm-as-a-judge-models|Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias]]

## What this builds on

- [[claim-level-faithfulness-is-the-actionable-check-that-a-grounded-model-used-its-context|Claim-level faithfulness is the actionable check that a grounded model used its context]]
