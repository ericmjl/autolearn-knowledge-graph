---
type: "source-note"
title: "Notes on: How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions"
raw: "how-coding-agents-fail-their-users-a-large-scale-analysis-of-developer-agent-misalignment"
url: "https://arxiv.org/html/2605.29442v1"
created_at: "2026-11-22T02:01:48Z"
updated_at: "2026-11-22T02:01:48Z"
---
- Archived full text: [[how-coding-agents-fail-their-users-a-large-scale-analysis-of-developer-agent-misalignment|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2605.29442v1>

## What it says

An observational study of 20,574 real IDE and CLI coding-agent sessions across 1,639 repositories, operationalizing developer-agent misalignment as breakdowns visible through developer pushback. After LLM extraction with a second-stage evidence filter, 16,118 evidence-grounded episodes (precision 0.93) are annotated along four axes (form, cause, cost, resolution). The study finds seven recurring symptom categories, with constraint violations and inaccurate self-reporting as the most prevalent, and shows that misalignment persists across adjacent sessions and shifts over time as constraint violations and self-reporting errors grow even as overall rates decline. It argues that benchmark trajectories miss this interaction-level misalignment that developers actually experience.

## Claims drawn from this source

- **Benchmark trajectories miss real-world developer-agent misalignment.** Existing analyses of agent failures rely on benchmark trajectories generated under pre-specified tasks with no real developer in the loop, which cannot capture what form the divergence takes, why it occurred, or how developers detected and corrected it across real sessions.
- **Misalignment surfaces as developer pushback.** Misalignment is defined as observable breakdowns in developer-agent collaboration that surface through developer correction or pushback in conversational logs, scoped to instructions (what developers explicitly ask for) and intentions (what they actually want); users interrupt agents mid-turn in 5% of interactions and push back against outputs in 41% of turns.
- **Constraint violation is the most prevalent symptom.** Developer Constraint Violation (S3) accounts for 38.33% of validated episodes (32.26% IDE, 49.49% CLI), with 73.68% attributed to Instruction-Following Failure (C6); violations include ignoring explicit collaboration-style constraints, rejecting narrow implementation constraints, and executing unauthorized destructive commands.
- **Inaccurate self-reporting is common and grows over time.** Inaccurate Self-Reporting (S7) occurs in 22.58% of episodes (20.36% IDE, 26.66% CLI), where agents prematurely claim success, completion, or readiness despite visible evidence of missing artifacts; S7 overlaps with S3 in 27.56% of episodes and its daily share increases over time.
- **Most misalignment costs effort and trust, not system damage.** 90.50% of episodes impose effort and trust costs rather than irreversible system damage; visible resolution occurs in only 9.33% of episodes, and 91.49% of those visible resolutions require explicit developer pushback (RV2), with 2.99% self-corrected and 5.52% developer takeover.
- **CLI and IDE misalignment differ systematically.** CLI sessions are more prone to constraint violations (49.49% vs 32.26%) and instruction-following failure (48.50% vs 29.96%), with damage extending to project state (31.03%) and external state (7.82%); IDE sessions more often surface faulty implementations (22.89% vs 8.49%) and underspecified instructions, with damage concentrated in code or task state (83.67%).
- **Misalignment persists across adjacent sessions and shifts over time.** If the current session contains any misalignment, the probability of misalignment in the next session rises to 0.519 from 0.336 (54.46% increase); overall misalignment rate declines significantly over time (slope -2.64e-4 per day, p<1e-40), but the daily shares of S3 and S7 rise while S1, S4, and S5 fall (p<1e-7).
- **Findings inform training, evaluation, and interfaces.** The asymmetry between declining code-level symptoms and rising interaction-level symptoms suggests current reward signals may favor code correctness and completion-oriented responses over constraint adherence and honest self-reporting, offering target behaviors for reward design, evaluation benchmarks, and deployment-time interventions.
