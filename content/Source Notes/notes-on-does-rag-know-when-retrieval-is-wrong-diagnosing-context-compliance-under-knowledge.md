---
type: "source-note"
title: "Notes on: Does RAG Know When Retrieval Is Wrong? Diagnosing Context Compliance under Knowledge Conflict"
raw: "does-rag-know-when-retrieval-is-wrong-diagnosing-context-compliance-under-knowledge"
url: "https://arxiv.org/html/2605.14473v4"
created_at: "2026-11-26T10:02:06Z"
updated_at: "2026-11-26T10:02:06Z"
---
- Archived full text: [[does-rag-know-when-retrieval-is-wrong-diagnosing-context-compliance-under-knowledge|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2605.14473v4>

## What it says

The paper asks whether a RAG model follows retrieved evidence or its parametric prior when the two conflict, and argues that final-answer accuracy cannot tell the difference. It introduces Context-Driven Decomposition (CDD), a five-step inference-time diagnostic: elicit the answer implied by the retrieved context, elicit the model's parametric answer, compare them, isolate the conflicting premise, and resolve the conflict. The resolution trace is then perturbed with mistake-injection and truncation tests to measure whether the trace causally drives the final answer. Across an Epi-Scale synthetic stress test (2,250 clean + 2,250 adversarial records), TruthfulQA misconception injection, and Claude-family reruns, CDD shows that standard RAG enters a measurable context-compliance regime (15.0% worst-case accuracy), that explicit decomposition improves controlled-conflict robustness (78.1% vs 63.0% macro), and that accuracy gains transfer across model families even when trace-perturbation sensitivity does not.

## Claims drawn from this source

- **Under worst-case misconception injection, Standard RAG reaches only 15.0% accuracy.** Using the top human misconception as retrieved context (TruthfulQA, N=500 scored examples, ±3.1%), Standard RAG reaches 15.0%; CDD reaches 62.0% (±4.3%) under the same probe.
- **CDD improves controlled-conflict robustness over Standard RAG.** On 2,250 Epi-Scale adversarial records (Gemini-2.5-Flash), CDD scores 78.1% macro average versus 63.0% for Standard RAG.
- **The largest gains concentrate on localized factual-conflict families.** CDD reaches 88.0% on Entity Swap and 83.2% on Logical Contradiction, versus conflict-aware instruction baselines of 79.3% and 75.4%.
- **The decomposition structure matters, not just the number of steps.** A length-matched sham decomposition with vacuous steps scores only 40.1% adversarial macro, far below full CDD (78.1%); removing Premise Isolation (Step 4) or the Divergence Check (Step 3) drops the macro average to 65.1% and 66.0%.
- **Accuracy gains transfer across model families while causal sensitivity does not.** On Gemini-2.5-Flash, mistake injection drops CDD accuracy from 78.1% to 28.0% (64.1% sensitivity), but all three Claude CDD sensitivities fall within [-3%, +7%] at N=2,250, despite positive adversarial accuracy gains.
- **CDD trades clean-context accuracy for adversarial robustness.** CDD scores 67.2% clean / 78.1% adversarial (72.23% harmonic mean) versus Standard RAG's 84.9% clean / 63.0% adversarial (72.33% harmonic mean), statistically tied overall.
- **CDD-alpha routes only high-conflict samples to deep decomposition.** With a prompted contradiction gate at tau=0.7, 30.0% of samples route to deep CDD and 70% to Standard RAG, yielding 68.5% adversarial accuracy, only about 1.0 point above the analytical random-routing expectation of 67.5%.
