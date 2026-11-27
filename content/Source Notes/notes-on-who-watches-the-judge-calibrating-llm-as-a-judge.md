---
type: "source-note"
title: "Notes on: Who Watches the Judge? Calibrating LLM-as-a-Judge"
raw: "who-watches-the-judge-calibrating-llm-as-a-judge"
url: "https://www.tekstream.com/blog/llm-as-a-judge-calibration-ai-quality/"
created_at: "2026-11-27T08:01:54Z"
updated_at: "2026-11-27T08:01:54Z"
---
- Archived full text: [[who-watches-the-judge-calibrating-llm-as-a-judge|Full archived text, with credits]]
- Link: <https://www.tekstream.com/blog/llm-as-a-judge-calibration-ai-quality/>

## What it says

The source argues that an LLM judge is a measurement instrument, not a reliable oracle, and must be calibrated against human-labeled ground truth and kept calibrated over time. It describes a calibration loop (build a labeled reference set from real production outputs, score the judge and measure agreement, fix disagreements, re-check on a schedule), five drift modes (model updates, traffic shift, rubric rot, known biases, and gaming), and the practical moves that keep calibration cheap: a few hundred weighted labeled examples per cycle, a frozen reference set to detect drift independently of traffic drift, ensemble judges for high-stakes scoring, and a rubric written like onboarding a new human reviewer. Uncalibrated judges corrupt the SLOs, gates, and postmortems built on top of them.

## Claims drawn from this source

- **An LLM judge is a measurement instrument that needs calibration.** An LLM judge is a measurement instrument, and instruments get calibrated or they lie to you. A quality score is a reading off an instrument, and a reading you have never validated against ground truth is not data. It is a guess with a decimal point that looks like data.
- **Calibration is an ongoing loop, not a one-time setup.** Calibration is the ongoing process of checking your automated judge against that human-scored sample, finding where they disagree, fixing the cause, and re-checking on a schedule because the agreement decays over time. That loop is the whole discipline.
- **Judges drift five ways, all invisible without periodic human-labeled checks.** Drift is not one failure; it is five: model updates (provider ships a new version and scoring shifts under you), traffic drift (new use cases the rubric never anticipated), rubric rot (what good means changes), known biases, and gaming (the system learns to satisfy the judge rather than the user). Every one is invisible without a periodic human-labeled check.
- **Known biases of LLM judges require measurement, not elimination.** LLM judges tend to prefer longer answers over better ones, to favor the first option in a comparison, to rate their own model's outputs more generously, and to reward agreeable, confident phrasing over correct content. You do not eliminate these; you measure them, account for them in the rubric, and watch them.
- **A frozen reference set detects judge drift independently of traffic drift.** Keep a frozen reference set so you can detect judge drift independently of traffic drift; if the judge's scores on a fixed set move, the judge moved.
- **A few hundred weighted labeled examples per cycle beat thousands of random ones.** Sample intelligently rather than scoring everything: a well-chosen few hundred labeled examples per cycle, weighted toward the hard and high-stakes cases, beats ten thousand random ones.
- **An uncalibrated judge corrupts the SLO apparatus built on top of it.** If the judge is uncalibrated, your error budget burns against a fiction, your release gates pass or fail on a misreading, and your postmortems cite a metric that was lying.
- **Ensemble judges provide a useful uncertainty signal.** Use multiple judges or an ensemble for high-stakes scoring, since their disagreement is itself a useful uncertainty signal.
