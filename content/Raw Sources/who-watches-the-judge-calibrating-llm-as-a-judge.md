---
title: "Who Watches the Judge? Calibrating LLM-as-a-Judge"
type: "raw-source"
url: "https://www.tekstream.com/blog/llm-as-a-judge-calibration-ai-quality/"
author: "Cece Kintner"
publication: "TekStream Solutions, LLC"
published: "2026-09-14"
archived: "2026-11-27T08:01:24Z"
---

> [!quote] Original source
> **Author(s):** Cece Kintner  
> **Title:** Who Watches the Judge? Calibrating LLM-as-a-Judge  
> **Published in:** TekStream Solutions, LLC  
> **Date:** 2026-09-14  
> **Original:** <https://www.tekstream.com/blog/llm-as-a-judge-calibration-ai-quality/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-who-watches-the-judge-calibrating-llm-as-a-judge|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How often does a calibrated judge drift out of agreement in production, and what keeps it honest after re-calibration?

## Archived text

Who Watches the Judge? Calibrating LLM-as-a-Judge

By Brad Bell, Principal Observability Lead

LLM-as-a-judge is the backbone of production AI evaluation, and an uncalibrated judge is a confident hallucination with a decimal point. The discipline that decides whether your quality scores mean anything.

You cannot put a human on every production AI response, so to measure quality at scale you reach for the obvious tool: use another language model to score the first one. LLM-as-a-judge is how almost every team that has gotten serious about AI quality actually measures it, and it works well enough that it has quietly become the backbone of production evaluation.

It also introduces a problem that should make any engineer pause. You have replaced an unmeasurable thing (is the AI right) with a measurable proxy (what score did the judge give), and the proxy is produced by exactly the same kind of system whose unreliability sent you looking for a measurement in the first place. An LLM judge can be confidently wrong in precisely the way the model it grades can be confidently wrong. If you do not watch the judge, you have not solved the measurement problem. You have hidden it behind a number.

The short version: An LLM judge is a measurement instrument, and instruments get calibrated or they lie to you. Calibration is an ongoing loop: build a human-labeled reference set, score the judge against it, fix the disagreements, and re-check on a schedule because judges drift five ways (model updates, traffic shift, rubric rot, known biases, and gaming). An uncalibrated judge does not just give a wrong number; it corrupts every SLO, gate, and postmortem built on top of it.

This is the post about watching the judge. It is the unglamorous discipline that decides whether your quality scores mean anything, and it is the part most teams skip until a calibrated reality collides with their confident dashboard.

Treat the judge as an instrument, because that is what it is

The reframe that makes this tractable: an LLM judge is a measurement instrument, and measurement instruments get calibrated or they lie to you. Nobody trusts a thermometer because it confidently displays a number; they trust it because someone checked it against a known reference and keeps checking. A quality score is a reading off an instrument, and a reading you have never validated against ground truth is not data. It is a guess with a decimal point that looks like data.

Ground truth, in this setting, is human judgment: a sample of real production outputs scored by people against a written rubric. Calibration is the ongoing process of checking your automated judge against that human-scored sample, finding where they disagree, fixing the cause, and re-checking on a schedule because the agreement decays over time. That loop is the whole discipline, and skipping any part of it is how teams end up with a green quality SLO sitting on top of a judge that quietly stopped being right months ago.

The calibration loop, concretely

Figure 1. The calibration loop: build a labeled set, score the judge against it, fix the disagreements, and re-check on a schedule, forever.

Start by building the labeled set. Sample real production outputs (not synthetic examples, not the easy cases) and have humans score them against an explicit rubric. The rubric matters as much as the scores: if your reviewers cannot articulate why an answer earned its grade, the judge has no stable target to match, and you will discover that your humans disagree with each other before you ever get to the model. That inter-rater disagreement is not a setback; it is the rubric telling you it is not specific enough yet, and resolving it is the most valuable hour you will spend.

Then score the judge against that same sample and measure agreement, not output. The mistake here is checking that the judge produced a number, which it always will. The question is whether its numbers track the humans’. Where they diverge, you have found something: a rubric ambiguity, a prompt weakness in the judge, a class of input the judge mishandles. Tighten the rubric, sharpen the judge prompt, add few-shot examples that pin the hard cases, and re-measure. Disagreement is the signal you are mining, not noise to smooth over.

And then re-check on a cadence, forever, because every input to this system drifts. The schedule is the part teams abandon first and regret most, because nothing alerts you that your judge has fallen out of calibration; it keeps emitting confident scores the entire time it is going wrong.

What are the five ways a judge drifts?

Figure 2. Five ways a judge drifts: model updates, traffic shift, rubric rot, known biases, and gaming. Every one is invisible without a periodic human-labeled check.

Drift is not one failure; it is five, and naming them tells you what to watch for. The judge model updates: your provider ships a new version and your scoring shifts under you with no announcement that maps to your rubric. Traffic drifts: new use cases arrive that the rubric never anticipated, and the judge scores them with the same unwarranted confidence it brings to familiar ones. The rubric rots: what your organization means by a good answer changes as the product and the policy evolve, and the written criteria lag behind.

Then there are the systematic biases that LLM judges are known to carry regardless of drift. They tend to prefer longer answers over better ones, to favor the first option in a comparison, to rate their own model’s outputs more generously, and to reward agreeable, confident phrasing over correct content. You do not eliminate these; you measure them, account for them in the rubric, and watch them. And finally, if the judge gates releases, the system under test will, over time, learn to satisfy the judge rather than the user, which is the AI-evaluation version of teaching to the test. A judge that is never re-examined is a target waiting to be gamed.

Practical moves that make calibration cheaper

None of this requires a research team, and a few practices keep the cost sane. Sample intelligently rather than scoring everything: a well-chosen few hundred labeled examples per cycle, weighted toward the hard and high-stakes cases, beats ten thousand random ones. Keep a frozen reference set so you can detect judge drift independently of traffic drift; if the judge’s scores on a fixed set move, the judge moved. Use multiple judges or an ensemble for high-stakes scoring, since their disagreement is itself a useful uncertainty signal. And write the rubric as if onboarding a new human reviewer, because in effect you are onboarding the model the same way; a rubric a person can apply consistently is a rubric a judge can apply consistently.

The throughline is that calibration is not a one-time setup task you complete and file away. It is a low-grade, permanent operational practice, like keeping any instrument trustworthy, and budgeting for it from the start is the difference between a quality program that holds and one that silently rots.

Why this is the load-bearing wall under your AI SLO

If you have stood up a correctness SLO for your AI (and the case for doing so is strong), then the LLM judge is the instrument that produces the SLI underneath it. Which means an uncalibrated judge does not just give you a wrong number; it corrupts the entire apparatus built on top of it. Your error budget burns against a fiction. Your release gates pass or fail on a misreading. Your postmortems cite a metric that was lying. The SLO discipline you carefully adopted is only as trustworthy as the judge calibration nobody wanted to own.

That is the uncomfortable dependency worth ending on: the most sophisticated AI quality program in the world rests on whether someone is quietly checking the judge against human reality on a schedule. It is the least glamorous task in the entire stack, and it is load-bearing. Teams that treat it as optional are not running an AI quality program; they are running a very convincing simulation of one.

Calibration is one piece of the evaluation signal, which is one of the five signals that make an AI system observable at all. If you are not sure whether your quality scores rest on a calibrated judge or an unexamined one, that is worth finding out before you trust the SLO they feed. Our three-minute self-assessment scores where your evaluation practice stands alongside the other four signals; it is a reasonable place to learn whether your next move is building the judge or auditing the one you already trust.

Frequently asked questions

What is LLM-as-a-judge?

LLM-as-a-judge is the practice of using one language model to score the outputs of another against a rubric, so that AI quality can be measured at production volume without a human on every response. It is the backbone of most production AI evaluation, and it is only trustworthy if the judge is calibrated against human-labeled ground truth.

How do you calibrate an LLM judge?

Run a loop: build a reference set of real production outputs scored by humans against an explicit rubric, score the judge against the same set and measure agreement rather than output, fix the disagreements (rubric ambiguity, judge-prompt weakness, mishandled input classes), and re-check on a fixed schedule because agreement decays over time.

What are the known biases of LLM judges?

LLM judges tend to prefer longer answers over better ones, favor the first option in a comparison, rate their own model’s outputs more generously, and reward agreeable, confident phrasing over correct content. You do not eliminate these biases; you measure them, account for them in the rubric, and watch them.

Why does an uncalibrated judge matter?

Because everything downstream rests on the judge’s score. If it is uncalibrated, your error budget burns against a fiction, your release gates pass or fail on a misreading, and your postmortems cite a metric that was lying. An uncalibrated judge does not just give a wrong number; it corrupts the entire SLO apparatus built on top of it.

Reach out to our experts!

About the Author

Brad Bell is the Principal Observability Lead at TekStream Solutions, a Digital Resilience partner that helps organizations operate, recover, and adapt with confidence by modernizing, securing, and optimizing their digital environments. His 29 years of experience spans large-scale telecommunications infrastructure, enterprise cloud strategy, and operational transformation across industries ranging from financial services to quick-service restaurants — work that included scaling monitoring platforms to 12,000+ nodes, architecting next-generation networks, and turning reactive ops teams into reliability engineering organizations. A Grafana Certified Solutions Architect and PreSales Solution Architect, he teaches SRE immersion courses at major financial institutions and consults on observability strategy at the enterprise level, helping clients navigate the convergence of cost pressure, tool sprawl, and AI-driven operations that is reshaping how enterprises think about reliability. His perspective isn’t theoretical — it comes from having been the person on the other end of a 2 AM page, and from watching organizations make expensive, avoidable mistakes with their observability investments. At TekStream, his focus is helping enterprises build platforms that solve today’s problems and hold up against where the industry is headed.
