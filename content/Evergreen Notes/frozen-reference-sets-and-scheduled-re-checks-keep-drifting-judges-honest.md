---
type: "evergreen"
title: "Frozen reference sets and scheduled re-checks keep drifting judges honest"
created_at: "2026-11-27T08:03:02Z"
updated_at: "2026-11-27T08:03:02Z"
inputs: ["notes-on-who-watches-the-judge-calibrating-llm-as-a-judge", "calibrated-judges-not-trusted-ones-keep-evaluation-honest"]
provenance_urls: ["https://www.tekstream.com/blog/llm-as-a-judge-calibration-ai-quality/", "https://builder.aws.com/content/3H8qTeKHyPXyLX8Nf8HTElUBZJR/a-practitioners-guide-to-llm-as-a-judge-calibration-on-amazon-bedrock", "https://arxiv.org/html/2605.29442v1", "https://arxiv.org/abs/2401.07339", "https://addyosmani.com/blog/ai-coding-workflow/", "https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/"]
refutation_status: "untested"
answers_questions: ["How often does a calibrated judge drift out of agreement in production, and what keeps it honest after re-calibration?"]
---
Agent synthesis

A calibrated judge stays honest only through scheduled re-checks, because agreement decays through five distinct drift modes rather than a single slow slope.

The mechanism is instrument drift. The sampled evergreen treats the judge as a measurement instrument selected and validated on a seed dataset before it is allowed to grade, with chance-corrected agreement and structured bias probes. The new source supplies what happens after selection: the judge's numbers track humans imperfectly and stop tracking them as the world moves. Its five drift modes are model updates (the provider ships a new version and the scoring shifts with no announcement tied to your rubric), traffic shift (new use cases arrive that the rubric never anticipated), rubric rot (what good means changes as the product and policy evolve), known biases (length preference, first-position preference, self-enhancement, agreeable phrasing), and gaming (a judge that gates releases becomes a target the system learns to satisfy rather than the user). None of the five alerts you; the judge keeps emitting confident scores while it is going wrong, which is exactly why the schedule is the part teams abandon first.

The evidence runs one way, not another. The picked note says to re-run calibration when the generator model, prompt distribution, or catalog changes; the new source says the same thing and adds the cheapest version of it: a few hundred well-weighted labeled examples per cycle beats ten thousand random ones, a frozen reference set makes drift detectable independently of traffic shift (if the judge's scores on a fixed set move, the judge moved), ensemble judges turn disagreement into an uncertainty signal for high-stakes scoring, and the rubric should read like an onboarding guide for a new human reviewer because the judge is being onboarded the same way.

Together the two inputs say that calibration is not a gate you pass once but a permanent, low-grade operational practice. The sampled note builds the initial check; the new source shows why that check must keep running and what a cheap, reliable cadence looks like. A green quality SLO on top of an unwatched judge is a convincing simulation of an AI quality program, not one (see: calibrated judges, not trusted ones, keep evaluation honest).

Keep a frozen reference set, score the judge on a schedule weighted toward hard and high-stakes cases, and treat any movement on the frozen set as a drift event that reopens calibration.

## Where it comes from

- [[notes-on-who-watches-the-judge-calibrating-llm-as-a-judge|Who Watches the Judge? Calibrating LLM-as-a-Judge]]

## What this builds on

- [[calibrated-judges-not-trusted-ones-keep-evaluation-honest|Calibrated judges, not trusted ones, keep evaluation honest]]
