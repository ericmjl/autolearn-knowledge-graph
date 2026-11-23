---
type: "source-note"
title: "Notes on: Task-Specific LLM Evals that Do & Don't Work"
raw: "task-specific-llm-evals-that-do-don-t-work"
url: "https://eugeneyan.com/writing/evals/"
created_at: "2026-11-23T05:02:32Z"
updated_at: "2026-11-23T05:02:32Z"
---
- Archived full text: [[task-specific-llm-evals-that-do-don-t-work|Full archived text, with credits]]
- Link: <https://eugeneyan.com/writing/evals/>

## What it says

Eugene Yan argues that off-the-shelf evals barely correlate with application-specific performance and are not discriminative enough for production, so teams need task-specific evals calibrated to the level of risk. For classification and extraction he recommends recall and precision (not accuracy), ROC-AUC and PR-AUC, and a check of probability-distribution separation; accuracy is too coarse. For summarization he rejects n-gram, similarity, and LLM-based evals, and instead recommends finetuning an NLI model on task-specific data: a few hundred samples catches obvious factual inconsistencies, a thousand or more makes it a solid guardrail (ROC-AUC rose from 0.56 to 0.85 after finetuning on USB and FIB). For translation he notes BLEU sits at the bottom of WMT leaderboards while chrF, BLEURT, COMET, and COMETKiwi do better, with COMETKiwi top reference-free in WMT22 and WMT23. He also treats copyright regurgitation (longest common subsequence under 0.1 for most models) and toxicity (Perspective API threshold p >= 0.5, adversarial prompts from RealToxicityPrompts and BOLD) as evals worth running. Human evaluation stays the gold standard for complex tasks, and most automated evals still depend on human labels. The closing point: calibrate the evaluation bar to the risk level, since the typical factual inconsistency/irrelevance rate is 5-10% even after RAG and good prompt engineering, may be hard to push below 2%, and high-stakes external applications (medical, financial) need a higher bar than internal-facing ones, without letting the urge for perfection strangle iteration.

## Claims drawn from this source

- **Off-the-shelf evals do not correlate with application-specific performance.** Most off-the-shelf evals barely correlate with application-specific performance and aren't discriminative enough to use in production, so teams may spend weeks without evals that reliably measure how they are doing.
- **Accuracy is too coarse; split into recall and precision.** Accuracy should be separated into recall and precision at minimum, ideally across thresholds; ROC-AUC is robust to class imbalance and doesn't require picking a threshold, while PR-AUC summarizes precision-recall trade-off.
- **Distribution separation matters more than AUC for threshold choice.** A model can have high ROC-AUC and PR-AUC yet still be unsuitable for production if probabilities between 0.4 and 0.6 overlap; getting the threshold wrong by 0.05 can cause a big drop in precision or recall, which is why n-gram and vector similarity evals fail.
- **NLI finetuned on task data is the most reliable factual-consistency eval.** Treating the source document as premise and the summary as hypothesis, a few hundred task-specific samples identify obvious inconsistencies and a thousand or more make it a solid eval and hallucination guardrail; finetuning on USB and FIB raised ROC-AUC from 0.56 to 0.85.
- **BLEU is bottom of the leaderboard; chrF, BLEURT, COMET, COMETKiwi do better.** COMETKiwi was the top reference-free metric in WMT22 and the top baseline alongside COMET and BLEURT in WMT23; in WMT23 four of seven top metrics were reference-free.
- **Voiceflow caught a 10% intent-classification regression with a task-specific harness.** Voiceflow's eval harness for intent classification caught a 10% performance drop when upgrading from the deprecating gpt-3.5-turbo-0301 to gpt-3.5-turbo-1106.
- **Typical factual inconsistency rate is 5-10%, and below 2% is prohibitively hard.** Even after grounding via RAG and good prompt engineering, the typical factual inconsistency/irrelevance rate is 5-10%, and LLM providers may make it prohibitively hard to go below 2%, which is why factual inconsistency guardrails on LLM output are needed.
- **Calibrate the evaluation bar to the level of risk.** High-stakes external applications like medical diagnosis or financial advice want a high bar and err on the side of caution, while internal-facing applications (e.g. product classification, document summarization) face lower risk; internal use cases deploy faster per a16z, and teams should start with a minimum lovable product rather than be paralyzed by the need for perfection (Innovator's Dilemma).
