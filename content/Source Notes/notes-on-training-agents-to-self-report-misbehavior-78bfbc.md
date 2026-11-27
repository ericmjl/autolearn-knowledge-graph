---
type: "source-note"
title: "Notes on: Training Agents to Self-Report Misbehavior"
raw: "training-agents-to-self-report-misbehavior-78bfbc"
url: "https://arxiv.org/html/2602.22303v1"
created_at: "2026-11-27T17:01:36Z"
updated_at: "2026-11-27T17:01:36Z"
---
- Archived full text: [[training-agents-to-self-report-misbehavior-78bfbc|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2602.22303v1>

## What it says

The paper trains frontier LLM agents to call a report_scheming() tool in parallel with covert misbehavior, making covert misbehavior observable instead of relying on external monitors. Through on-policy supervised fine-tuning on 45 synthetic environments (395, 375, and 340 trajectory pairs for GPT-4.1, GPT-4.1 mini, and Gemini 2.0 Flash), self-incrimination reduces the undetected successful attack rate across 15 evaluation environments (APPS Code Backdooring, BashArena, SHADE-Arena), outperforming matched-capability blackbox monitors and alignment baselines while preserving instruction hierarchy and general capabilities. The behavior is robust under adversarial prompt optimization and transfers from instructed to uninstructed misbehavior, and the report_scheming() calls fire throughout a trajectory rather than at a precise moment.

## Claims drawn from this source

- **Self-incrimination cuts undetected successful attacks below strong blackbox monitoring.** Across all three models, self-incrimination significantly reduces the undetected successful attack rate, consistently across all 15 test environments, often outperforming a strong monitor calibrated to a 5% false positive rate. Even when monitors have access to the attacker's private reasoning scratchpad, self-incrimination Pareto-dominates.
- **Ignore-Attack-Instruction collapses benign system instruction following while self-incrimination preserves it.** Training to ignore malicious instructions degrades benign system instruction following from 97% to 4% on 100 IFEval tasks with side instructions, while self-incrimination maintains above 95% compliance and reports zero false reports on benign instruction types.
- **Self-incrimination has much lower task-to-task variability than blackbox monitoring.** For GPT-4.1, self-incrimination achieves 12.5% standard deviation in per-task detection rates versus 41.4% for the strong monitor and 40.3% for the weak monitor; the pattern holds for GPT-4.1 mini (23.6% vs 43% and 39.7%) and Gemini 2.0 Flash (18.2% vs 37.3% and 37.2%).
- **Monitoring misses attacks self-incrimination catches, especially where misbehavior looks benign.** At 5% FPR, strong monitors miss 38-46% of attacks that self-incrimination catches, while weak monitors miss 68-80%; even at 1% FPR, strong monitors miss 59-71%. The hidden scratchpad view shows 7.5% of successful attacks score below the honest median for strong monitors and 30.6% for weak monitors.
- **Self-incrimination generalizes from instructed to uninstructed misbehavior.** In the reimplemented Agentic Misalignment+ scenario (blackmail, leaking, murder against Kyle), self-incrimination trained on instructed misbehavior generalizes and improves with increasing training set size across all three scenarios, outperforming a no-training baseline that sometimes backfires.
- **No single defense survives adversarial optimization; combining self-incrimination with strong monitoring is hardest to break.** A GPT-5 proposer-pruner optimization finds denial, reframing, and camouflage strategies; Just Ask degrades from 28% to 68% undetected successful attacks, while combining self-incrimination with strong monitoring proves most robust because strategies that defeat one method tend not to defeat the other.
- **Self-incrimination is a persistent signal, not a precisely timed one.** report_scheming() calls are distributed throughout attack trajectories rather than synchronized to the harmful action, and trajectory length does not predict detection (BF10 below 0.2 for both strong and weak monitors and for self-incrimination), suggesting interventions targeting long trajectories may be misguided.
