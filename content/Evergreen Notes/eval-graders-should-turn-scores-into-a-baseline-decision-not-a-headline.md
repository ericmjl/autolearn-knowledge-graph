---
type: "evergreen"
title: "Eval graders should turn scores into a baseline decision, not a headline"
created_at: "2026-11-25T00:01:57Z"
updated_at: "2026-11-25T00:01:57Z"
inputs: ["notes-on-what-we-learned-evaluating-an-llm-classifier-and-a-code-parser-against-their-previous", "public-eval-headlines-hide-reliability-grader-noise-and-single-shot-limits"]
provenance_urls: ["https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["How should eval graders be designed to avoid failing correct work and passing wrong work at scale?"]
---
Agent synthesis

A public eval score is not a verdict on capability; it is a measurement whose design decides whether the truth surfaces. Average pass rate hides the gap between a model that solves a task every time and one that solves it one time in three, and a grader that fails correct work or passes wrong work corrupts every number downstream of it.

The new source shows how to fix the grader itself. It asks one question first: where does the right answer come from? Labeled datasets, reference facts, and benchmarks support comparison-style graders; cases with no answer key need a judge, a property check, or a pairwise comparison. The eval runs the real system, not a mock, keeps the dataset versioned in git with one reason per case, and samples unreliable cases three times and takes a majority, re-sampling five more times when a case disagrees with its baseline. A flip that shows once is noise; a flip that shows on every sample is a change.

The baseline rule is the sharpest piece: gains write themselves into the baseline, losses wait for a person, and absolute floors stop a dozen small accepted losses from adding up to unapproved decay. Only stable cases belong in the pull-request check, unstable cases stay in nightly, and a missing result is never a pass. Ambiguous labels become ranges: accept either adjacent severity instead of forcing a coin flip in the answer key.

Read together with the public-eval-headlines note, the two sources show that grader design and aggregate design are the same problem: both hide the mismatch between the metric and the task. The headlines note names the three errors (wrong aggregate, flawed grader, single-shot task); the new source names the operational fix (repeat sampling, person-gated losses, stability gating, missing results kept out of scoring). The synthesis is that a grader earns trust by surfacing what moved, not by printing a number that summarizes away the movement.

Start with twenty to thirty real cases, each with a reason, a baseline file in version control, and a nightly job that tells a person what moved. Treat every headline score as a shortlist input, then run the final gate in your own harness where gains and losses are separated.

## Where it comes from

- [[notes-on-what-we-learned-evaluating-an-llm-classifier-and-a-code-parser-against-their-previous|What we learned evaluating an LLM classifier and a code parser against their previous results | Endor Labs]]

## What this builds on

- [[public-eval-headlines-hide-reliability-grader-noise-and-single-shot-limits|Public eval headlines hide reliability, grader noise, and single-shot limits]]
