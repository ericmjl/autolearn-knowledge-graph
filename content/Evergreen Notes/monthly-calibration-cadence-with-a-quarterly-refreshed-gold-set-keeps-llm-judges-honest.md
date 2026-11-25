---
type: "evergreen"
title: "Monthly calibration cadence with a quarterly-refreshed gold-set keeps LLM judges honest"
created_at: "2026-11-25T11:01:49Z"
updated_at: "2026-11-25T11:01:49Z"
inputs: ["notes-on-llm-as-judge-best-practices-in-2026-calibration-bias-and-cost", "claim-level-judges-need-repeated-re-validation-not-one-time-calibration"]
provenance_urls: ["https://futureagi.com/blog/llm-as-judge-best-practices-2026/", "https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How often should claim-level faithfulness judges be re-validated, and what does the literature say about re-validation cadence?"]
---
Agent synthesis

Monthly calibration cadence with a quarterly-refreshed gold-set keeps LLM judges honest. An LLM judge is a measuring instrument that degrades. Future AGI's 2026 guide shows the failure mode concretely: a GPT-4 judge that scored GPT-4 production outputs looked green for three months while its agreement with a human expert sat at kappa 0.31, over-rewarding same-family outputs and under-penalizing fluent hallucinations. The guide prescribes a monthly calibration run over a 200-500-trace human gold-set, with Cohen's kappa tracked and alerted against (0.6 as a common bar), and a quarterly refresh that replaces the staler 100-200 entries with fresh production traces.

This is the operational shape of the claim-level re-validation evergreen. The claim-level note adds the judge-quality floor (chance-corrected kappa, AB+BA position swaps, temperature-0 replication, cross-benchmark replication, the consistency-bias paradox) and the drift argument (a judge tuned once and reused next quarter measures a changed instrument). The Future AGI guide adds the operating cadence: monthly kappa checks against the gold-set, quarterly gold-set refresh, drift in 60-90 days, different-family judge selection, an explicit versioned rubric, length and position bias mitigation, 5-20% sampling with async execution, and judge cost kept under 10-15% of production. Neither source alone gives the full operating rhythm.

The synthesis: gate on a cadence, not a score. Run the judge over the gold-set every month, refresh the gold-set quarterly, and treat launch-day calibration as a low water mark, not a certificate. Instrument judge cost as its own line, and stop trusting the score the moment a cadence check or a bias control breaks.

## Where it comes from

- [[notes-on-llm-as-judge-best-practices-in-2026-calibration-bias-and-cost|LLM-as-Judge Best Practices in 2026: Calibration, Bias, and Cost]]

## What this builds on

- [[claim-level-judges-need-repeated-re-validation-not-one-time-calibration|Claim-level judges need repeated re-validation, not one-time calibration]]
