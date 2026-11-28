---
type: "source-note"
title: "Notes on: Verifier–Harness Co-Evolution for Training-Free Self-Improvement on Open-Ended Tasks"
raw: "verifier-harness-co-evolution-for-training-free-self-improvement-on-open-ended-tasks"
url: "https://arxiv.org/html/2610.17609v1"
created_at: "2026-11-28T05:01:44Z"
updated_at: "2026-11-28T05:01:44Z"
---
- Archived full text: [[verifier-harness-co-evolution-for-training-free-self-improvement-on-open-ended-tasks|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2610.17609v1>

## What it says

Unified Co-Evolution (UCoE) keeps an executable verifier program and the agent's harness state evolving together on open-ended tasks, with all model parameters fixed. It synthesizes candidate verifier programs, tests them on response contrasts (pairs of responses that differ in one declared property with a known preferred side), and picks the candidate whose discrimination on its weakest contrast family, driving capacity, is highest. During deployment the verifier diagnoses one weakness, guides a single local repair, decides which response is served, and decides whether the accepted repair enters the harness state. At checkpoints it is re-evolved from task diagnostics, with an adoption gate requiring a worst-family gain on the selection split, a held-out win, and no regression beyond tolerance on existing families.

## Claims drawn from this source

- **A fixed verifier goes stale as responses improve and task demands shift.** The draft and revision pairs the actor produces drift away from the contrasts on which the initial verifier was selected, and its criteria or aggregation can go stale.
- **Driving capacity is discrimination on the weakest contrast family.** Candidates are ranked by their signed discrimination on the family where they are weakest, so strength on easy properties cannot mask a blind spot.
- **Verifier program keeps every criterion explicit and is executable.** The verifier maps a task and a response to a vector of criterion scores and a scalar reward, and its diagnosis procedure, program interpreter, and verifier-model parameters never change.
- **Deployment serves the revision only on a margin.** The revision is served only when its reward lead exceeds a margin, and a rejected revision may update metadata only, with at most one accepted generalized trigger-action procedure added per accepted repair.
- **Verifier adoption is gated on the same contrasts.** A candidate replaces the current verifier only if it improves worst-family discrimination on the selection split, wins more held-out contrasts than it loses, and stays within a fixed regression tolerance on every existing family.
- **UCoE beats direct generation across open-ended and verifiable tasks.** It averages 59.00% preference against matched direct generation with Qwen3-8B and 57.19% with Qwen3.8-27B, and lifts the three-benchmark verifiable mean from 36.06% to 38.48% without a loss on any benchmark.
- **Current-task repair contributes most of the gain.** Removing the verifier-guided repair drops Arena-Hard preference from 58.30% to 50.80%, while freezing the verifier or random initial selection each cost between 56.60% and 56.70%.
