---
type: "source-note"
title: "Notes on: Introducing the Evaluation Engine: Build High-Accuracy Evaluators and Guardrails Fitted to Your Agents | Splunk"
raw: "introducing-the-evaluation-engine-build-high-accuracy-evaluators-and-guardrails-fitted-to"
url: "https://www.splunk.com/en_us/blog/artificial-intelligence/introducing-evaluation-engine.html"
created_at: "2026-11-23T03:02:03Z"
updated_at: "2026-11-23T03:02:03Z"
---
- Archived full text: [[introducing-the-evaluation-engine-build-high-accuracy-evaluators-and-guardrails-fitted-to|Full archived text, with credits]]
- Link: <https://www.splunk.com/en_us/blog/artificial-intelligence/introducing-evaluation-engine.html>

## What it says

Splunk argues that product-specific evaluation stops being a sampled audit when the judge is cheap enough to run on every transaction. Its Eval-G1 models are small tuned adapters predicting one token per verdict, built from a team's traces and expert labels in an afternoon, and they match or beat frontier LLM judges on PII and toxicity while answering in about a third of a second at up to 98% lower cost. Accuracy is only half the story: at production volume, speed and cost decide how much traffic you can evaluate, and a guardrail is judged by what it lets through.

## Claims drawn from this source

- **Eval-G1 predicts a single token per verdict, in about a third of a second.** Each custom evaluator reads the input once, predicts the label with a calibrated probability, and returns in about 0.34s end to end, up to 14x faster than frontier LLM judges, which took 2.2 to 4.7 seconds per evaluation on PII and toxicity.
- **On PII, the tuned evaluator caught more than any tested model.** The Eval-G1 PII evaluator caught 99.4% of leaked personal data at 0.958 F1 (precision 0.928, recall 0.994), ahead of every model tested; the best LLM judge, GPT 6 Sol, reached 0.902, and Jev reached 0.865.
- **On toxicity, the tuned evaluator trails the best frontier judge on F1 but beats three of five on conciseness.** Toxicity F1: Eval-G1 0.847 vs GPT 6 Sol 0.903 (GPT 6 Luna 0.902, Claude Sonnet 5 0.654). Conciseness on the same 549-word rubric: Eval-G1 0.871, beating three of five frontier judges and within 1.3 points of Claude Opus 5.5 at 0.884.
- **Guardrails are judged by what they let through.** Three frontier judges were precise on toxicity but caught fewer than 60% of toxic messages (Gemini 3.8 Flash recall 0.593, Claude Opus 5.5 recall 0.562, Claude Sonnet 5 recall 0.518), so a guardrail missing more than four in ten violations is not much of a guardrail; on PII the tuned evaluator caught 99.4% of all violations.
- **Speed and cost bound the coverage of evaluation at production volume.** Only GPT 6 Sol matched the tuned evaluator's accuracy on PII and toxicity, at about 16 times the cost per evaluation, and GPT 6 Luna at a similar cost but eight times slower; that makes Eval-G1 cheap enough to score up to 100% of production traffic.
- **A tuned evaluator ships in an afternoon once trustworthy examples exist.** In the worked example, three experts labeled 60 fee conversations (about 2.5 hours), the tuner expanded them to about 5,000 training examples, trained the evaluator in about two hours, and the guardrail went live by 5:00 pm; without a ground truth dataset, plan for two to three days, because agreeing on examples takes longer than tuning.
