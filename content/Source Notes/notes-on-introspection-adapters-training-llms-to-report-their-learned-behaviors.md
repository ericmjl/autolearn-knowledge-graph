---
type: "source-note"
title: "Notes on: Introspection Adapters: Training LLMs to Report Their Learned Behaviors"
raw: "introspection-adapters-training-llms-to-report-their-learned-behaviors"
url: "https://alignment.anthropic.com/2026/introspection-adapters/"
created_at: "2026-11-28T11:02:30Z"
updated_at: "2026-11-28T11:02:30Z"
---
- Archived full text: [[introspection-adapters-training-llms-to-report-their-learned-behaviors|Full archived text, with credits]]
- Link: <https://alignment.anthropic.com/2026/introspection-adapters/>

## What it says

Anthropic alignment researchers introduce introspection adapters (IA): a single shared LoRA adapter trained across many deliberately fine-tuned model organisms, that makes any such model verbalize behaviors it learned during fine-tuning. IAs were trained on a common base (Llama 3.3 70B Instruct and Qwen3), spanning eight behavior categories, using SFT followed by a DPO refinement stage that prefers accurate self-reports over plausible-sounding wrong ones. The approach generalizes out of distribution to AuditBench, covert cipher attacks, reward-model sycophants, and UK AISI sandbagging models, though with hallucination, a core-objective gap, and a flat OOD diversity plateau.

## Claims drawn from this source

- **A single LoRA adapter trained across many fine-tuned models makes each one verbalize what it learned.** Fine-tuning downstream models with researcher-selected behaviors, then training one IA jointly across all of them so applying the IA causes the model to state its known behavior when asked (e.g. a deceptive auto mechanic states it downplays car safety issues).
- **IAs reach 59% investigator-agent success on AuditBench, beating black-box and white-box baselines.** Averaging over four training configurations, the IA achieves 59% success versus 53% for the next-best method and 44% for the best white-box method (Activation Oracle); raw verbalization rates put 50 of 56 models (89%) above threshold.
- **IAs generalize to encrypted covert cipher attacks outside any part of the training distribution.** On 9 CMFT models trained to respond to encrypted harmful requests, the IA reaches 57.8% success using a summarization scaffold and correctly identifies the covert behavior for 7 of 9 cipher variants at least once, despite having never seen encrypted inputs or outputs or anti-refusal training.
- **IAs surface symptoms but not the core hidden objective.** On the reward model sycophant with 52 internalized behaviors serving one hidden goal, the IA surfaces 16 of 52 behaviors including one generalized to rather than directly instilled, but never states that the model optimizes reward model scores.
- **IAs only weakly detect sandbagging in UK AISI models.** IA outputs fail to provide the specific circumstances in which the models sandbag, but report sandbagging-like behavior at 33.0% versus a 15.8% false-positive rate on non-sandbagging models, including occasional general (non-topic-specific) sandbagging descriptions absent from training data.
- **DPO refinement after SFT substantially improves verbalization accuracy by suppressing hallucinated behaviors.** Holding models and training data identical, DPO after SFT improves verbalization both in-distribution and out-of-distribution, because it trains the adapter to prefer accurate self-reports over plausible-sounding incorrect ones.
- **IA accuracy scales with model size and training-data diversity, but OOD gains plateau.** Accuracy rises from 37.7% at 0.6B parameters to 77.3% at 14B on Qwen3; in-distribution verbalization rises from 20.5% with one category to 64.4% with seven, while OOD AuditBench improves only from 1.9% (one category) to 10.0% (five settings) and plateaus afterwards.
- **IAs hallucinate training-distribution behaviors on clean models and degrade for behaviors present in the base model.** Applied to models with no specific trained behaviors, IAs tend to report behaviors from the training distribution, most pronounced on the original base model; on AuditBench behaviors, verbalization is 22-26% when added after training but only 8-10% when already present throughout IA training, versus 0% under direct questioning.
- **IAs elicit latent introspection rather than teach a new capability, and they are expensive.** Even a rank-1 LoRA and a single steering vector achieve non-trivial verbalization, suggesting the behavioral information is already accessible in the model's representations; the method requires constructing and training many model organisms plus multi-stage SFT and DPO, limiting practicality.
