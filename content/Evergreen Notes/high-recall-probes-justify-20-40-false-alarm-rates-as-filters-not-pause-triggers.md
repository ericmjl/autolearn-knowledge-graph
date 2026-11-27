---
type: "evergreen"
title: "High-recall probes justify 20-40% false-alarm rates as filters, not pause triggers"
created_at: "2026-11-27T16:03:16Z"
updated_at: "2026-11-27T16:03:16Z"
inputs: ["notes-on-detecting-high-stakes-interactions-with-activation-probes", "probe-flags-trigger-pauses-and-escalations-in-production-not-just-logs"]
provenance_urls: ["https://arxiv.org/html/2506.10805v1", "https://openai.com/index/how-we-detect-frontier-model-misalignment/", "https://arxiv.org/html/2609.19101v2", "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://www.goodfire.com/research/reward-hacking-activation-monitors"]
refutation_status: "untested"
answers_questions: ["What false-alarm rates and responder bandwidth justify auto-pausing a workload on an activation-probe flag?"]
---
Agent synthesis

High-recall activation probes belong in the filter stage of a monitoring cascade, not at the user-facing pause gate. Probes read residual-stream activations, cost orders of magnitude less than prompted LLM monitors, and generalize to out-of-distribution real-world datasets, but their true-positive rate at 1% false-positive rate is only ~43% (vs ~55% for the best LLM baseline), so treating a probe flag as ground truth would pause workloads on false alarms. At 20-40% FPR, probes reach substantially higher TPR, and in a tiered system a false positive costs a rerun through the expensive classifier or a reviewer, not a stalled workload or a harmed user.

The new source quantifies the shape of that trade. Probes trained on synthetic data generalize out of distribution (mean AUROC above 0.95 on development datasets and above 0.91 on held-out test sets), match medium-sized LLM monitors (prompted or fine-tuned) at roughly six orders of magnitude lower compute, and form the efficient front of a two-stage cascade that routes only the k% most uncertain (median-distance from the median probe score) samples to a costlier classifier. Small doses of deployment-context samples change a lot: probes trained on synthetic plus even ~256 deployment samples outperform the prompted Llama-70B baseline. The failure modes are specific and repeatable, too: humor, signaling words like "emergency", ethically coded language like "responsible money laundering", and high-stakes prompts embedded in low-stakes contexts all push the probe in the wrong direction, and linear probes remain vulnerable to targeted adversarial attack.

Read against the production-escalation note, the division of labor becomes precise. The pipeline there runs activation probes under a model-based reviewer, an investigative agent, and (for sensitive workloads) telemetry comparison, then lets humans or an automatic pause act; a random 5% audit sample keeps the cascade honest. The probe supplies the cheap, continuous first-stage screen and defines the band of alert intensity that must earn a human look; the reviewers and the high-priority pauses decide what happens. A probe flag alone is an input to that decision, not the verdict. Activation probes detect proxy-signal hacks before gold outcomes degrade; the new evidence is that the same telemetry becomes an enforceable intervention only at the cascade boundary, with the pause reserved for the highest-priority flags and only when review does not clear them in time.

Run probes tuned for high recall as an 80-90%-of-traffic filter at a deliberate 20-40% false-positive band, keep flagged samples in the LLM/reviewer tier, and reserve automatic pause for high-priority failures that survive review and persist past the clearance window. Do not let a probe flag alone halt a workload; treat the probe as a cost-efficient gate to deeper inspection, and keep the audit sample honest.

## Where it comes from

- [[notes-on-detecting-high-stakes-interactions-with-activation-probes|Detecting High-Stakes Interactions with Activation Probes]]

## What this builds on

- [[probe-flags-trigger-pauses-and-escalations-in-production-not-just-logs|Probe flags trigger pauses and escalations in production, not just logs]]
