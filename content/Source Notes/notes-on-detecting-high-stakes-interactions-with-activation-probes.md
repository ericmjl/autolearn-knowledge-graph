---
type: "source-note"
title: "Notes on: Detecting High-Stakes Interactions with Activation Probes"
raw: "detecting-high-stakes-interactions-with-activation-probes"
url: "https://arxiv.org/html/2506.10805v1"
created_at: "2026-11-27T16:02:11Z"
updated_at: "2026-11-27T16:02:11Z"
---
- Archived full text: [[detecting-high-stakes-interactions-with-activation-probes|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2506.10805v1>

## What it says

The paper evaluates activation probes for detecting high-stakes LLM interactions (contexts where outputs could cause significant real-world harm), comparing probes with prompted and fine-tuned LLM monitors. Probes trained on a synthetic dataset generalize robustly to out-of-distribution real-world datasets, matching medium-sized LLM baselines at ~6 orders of magnitude lower compute. The paper shows probes are not standalone user-facing monitors (at 1% FPR, TPR is only ~43%, vs ~55% for the best baseline) but are strong as a cheap initial filter in a two-stage cascade that routes uncertain cases to expensive classifiers, and that small amounts of deployment-context samples markedly improve probe performance.

## Claims drawn from this source

- **Probes trained on synthetic data generalize to diverse real-world datasets.** Best probes (Attention, Softmax, Mean) reach mean AUROC over 0.95 on development datasets and over 0.91 on held-out test datasets, comparable to prompted or fine-tuned medium-sized Llama-3 and Gemma-3 LLMs.
- **Probes cost roughly six orders of magnitude less and match medium-sized LLM monitors.** Probes achieve performance competitive with baselines that are up to six orders of magnitude more expensive (Llama-1B-scale fine-tunes and prompted medium LLMs).
- **At 1% false-positive rate, probes catch far less than the best LLM baseline.** The best probe detects only ~43% of high-stakes cases at 1% FPR, compared to ~55% for the best LLM baseline, indicating neither probes nor most baselines are safe as standalone monitors where false positives directly impact users; at 20-40% FPR probes reach substantially better TPR.
- **A two-stage cascade beats either method alone at fixed compute.** Probes continuously monitor all interactions and route the k% most uncertain (median-distance) samples to a more expensive classifier; averaging probe and baseline scores on routed samples consistently outperforms probes or the LLM alone across compute budgets, and even beats a weak baseline combined with a probe.
- **Training on deployment samples lifts probes past prompted baselines.** Even with 256 deployment-context samples added to synthetic training data, probes can exceed the prompted Llama-70B baseline, so on-policy sample data meaningfully shrinks the synthetic-to-real generalization gap.
- **Humor, signaling words, and coded language mislead probes.** The probe misfires on low-stakes contexts triggered by words like 'emergency', can under-fire on ethically coded unethical prompts such as 'responsible money laundering', and scores lower when a high-stakes prompt is embedded in a low-stakes context.
- **Linear probes are vulnerable to targeted adversarial attack.** Linear probes are known to be sensitive to targeted adversarial attacks, so relying on a single probe for critical safety decisions is risky and reinforcement of probes' role as one component in a multi-layered defense.
