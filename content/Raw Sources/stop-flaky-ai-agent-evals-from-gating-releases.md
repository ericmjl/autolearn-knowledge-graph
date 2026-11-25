---
title: "Stop Flaky AI Agent Evals From Gating Releases"
type: "raw-source"
url: "https://makeyouragent.ai/blog/stop-flaky-ai-agent-evals-release-gates"
author: "Make Your Agent (no individual author named)"
publication: "Make Your Agent"
published: "2026-11-09"
archived: "2026-11-25T01:00:47Z"
---

> [!quote] Original source
> **Author(s):** Make Your Agent (no individual author named)  
> **Title:** Stop Flaky AI Agent Evals From Gating Releases  
> **Published in:** Make Your Agent  
> **Date:** 2026-11-09  
> **Original:** <https://makeyouragent.ai/blog/stop-flaky-ai-agent-evals-release-gates>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-stop-flaky-ai-agent-evals-from-gating-releases|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How flaky evals should behave under repeat sampling for release gates

## Archived text

Blog · · 10 min read

AI agent eval flakiness: stop flaky evals from making release decisions

AI agent eval flakiness can make an unchanged system pass on Monday and fail on Tuesday. If CI treats one stochastic attempt as a stable measurement, the gate can approve a regression, block a safe release, or invite engineers to rerun the suite until it turns green. The fix is not to hide variance behind a wider threshold.

Build the release decision around paired repeated trials. Separate statistical repetitions from infrastructure retries, compare the candidate and baseline on the same cases and fixtures, measure uncertainty by risk slice, and allow an inconclusive result. This article defines the records, execution sequence, decision rules, failure handling, and tests needed to make that gate trustworthy.

Why one eval run cannot support a release verdict

An agent evaluation has more moving parts than a deterministic unit test. The model can choose a different tool or trajectory. A model-based grader can vary. Retrieved data can change. A rate limit can interrupt one attempt. Even if the final aggregate score looks precise, it may be one draw from several distributions.

Anthropic's guide to agent eval design recommends multiple trials per task and distinguishes pass@k, where any attempt may succeed, from pass^k, where every attempt must succeed. Those metrics answer different questions. A best-of-several capability score should not become a reliability claim for a workflow that users expect to succeed on its first production attempt.

LangSmith exposes evaluation repetitions because both the application and evaluator can be non-deterministic. Repetition gives the gate a more stable estimate.

The common CI pattern still discards that fact:

- Run the baseline suite once.
- Run the candidate suite once.
- Average all task scores.
- Block if the candidate is lower by a fixed amount.

That comparison confounds release effect, trial variance, case mix, grader variance, and operational errors. It also lets frequent easy cases hide a serious decline in a small high-risk slice.

Define the decision before choosing a repeat count

For each metric and risk slice, declare:

- the baseline release and candidate release being compared
- the task set, fixture versions, tool doubles, grader, and grading rubric
- the unit of analysis, such as task, conversation, or full product workflow
- the minimum regression worth blocking
- the minimum improvement worth promoting for an experimental feature
- the maximum trial and token budget
- the behavior when evidence remains inconclusive

The minimum regression matters because statistical significance alone does not establish practical importance. A large suite may detect a tiny score change that has no product consequence. A small suite may miss a material decline because the result is noisy. The release contract needs both an uncertainty rule and an effect-size rule.

A useful three-way decision is:

Do not convert inconclusive into pass. That simply restores the one-shot failure under a more elaborate name.

Store an immutable eval manifest

A release gate must be reproducible after the models, prompts, datasets, and tools have changed. Put every behavior-affecting input into an immutable manifest.

{

  "eval_id": "eval_2041",

  "baseline_release": "support-agent@184",

  "candidate_release": "support-agent@185",

  "dataset_version": "support-regressions@92",

  "fixture_snapshot": "fixtures@2026-09-09T08:00Z",

  "grader_release": "support-judge@31",

  "rubric_version": "grounded-resolution@12",

  "slices": ["refund", "delivery", "account-access"],

  "regression_margin": {"task_success": 0.02},

  "initial_trials_per_case": 3,

  "max_trials_per_case": 12,

  "max_total_trials": 2400,

  "decision_policy": "paired-lower-bound@4"

}

Pin provider model identifiers where the provider supports it. Record the actual model response metadata and every resolved dependency even when a configured alias cannot be pinned. Store tool responses or use versioned, production-faithful fixtures so the baseline and candidate see equivalent product state.

The manifest is also the boundary between this problem and judge calibration. A calibrated judge may still produce variable scores. Pinning its release tells you which measurement instrument ran. Separate calibration data should prove that the instrument agrees sufficiently with qualified humans.

Separate a trial from a retry

A statistical trial is a deliberate independent observation. A retry is an operational attempt to complete that observation after a classified transient failure. Mixing them biases the result.

Suppose a task times out twice and succeeds on its third execution. Counting only the success makes the agent look reliable. Counting all three as independent task trials exaggerates the sample size. Hiding the timeouts loses production-relevant evidence.

Use separate identifiers and outcomes:

logical_trial_id = hash(eval_id, case_id, release_id, repetition_index)

attempt_id = unique_id(logical_trial_id, retry_index)

if attempt completes:

    persist trial outcome and stop retrying

elif failure is retryable and deadline remains:

    persist failed attempt, then retry same logical trial

else:

    persist trial as operational_failure

Keep operational failure rate as its own release metric. Decide in advance whether a terminal timeout, provider error, or tool failure counts as task failure for the product journey. Do not ask the statistical layer to erase it.

An NVIDIA NeMo request asks for native per-task repeats. Keep your internal schema explicit even if an evaluation vendor uses one overloaded runs field.

Pair baseline and candidate trials

Run the baseline and candidate against the same case IDs, fixture snapshot, rubric, and comparable execution conditions. Preserve the pair at case and repetition level.

Pairing reduces noise caused by differences in case difficulty. If the candidate receives a different random sample of tasks, the comparison may measure the sample rather than the release. For expensive suites, randomize execution order within each pair so provider load or fixture drift does not always favor one release.

A paired record can contain:

{

  "case_id": "refund-044",

  "repetition": 3,

  "baseline_trial": "trial_b_044_3",

  "candidate_trial": "trial_c_044_3",

  "baseline_score": 1,

  "candidate_score": 0,

  "difference": -1,

  "slice": "refund",

  "fixture_version": "invoice_883@17"

}

FutureAGI's overview of statistical significance in LLM evaluations describes variance, confidence intervals, paired tests, and sample-size planning. Choose the statistical method with someone who understands the metric and sampling design. Binary task success, bounded rubric scores, and latency distributions do not automatically share the same test.

The pipeline can support more than one statistical method. It must record the method, assumptions, interval, effect estimate, sample size, and decision boundary so a reviewer can reconstruct the verdict.

Measure slices before the aggregate

An aggregate can stay flat while one critical workflow becomes worse. Calculate effect and uncertainty for declared slices before calculating the portfolio result.

Useful slices come from product risk and behavior, not whichever tags are easiest to query:

- irreversible versus reversible actions
- write workflows versus read workflows
- tenant or policy class
- tool family and trajectory length
- routine cases versus known production failures
- language, locale, or accessibility path
- first attempt versus recovery path

Set a minimum sample policy for each release-blocking slice. If a critical slice has too few valid paired trials, mark it inconclusive. Do not let thousands of low-risk FAQ cases overrule ten payment or access-control cases.

NVIDIA's evaluation guidance emphasizes multi-run and trajectory-aware evaluation. A final-answer score can miss a dangerous path that happened to end well. Preserve deterministic policy checks, tool-call assertions, and verified product outcomes alongside probabilistic quality scores.

Spend repetitions where uncertainty remains

A fixed large repeat count wastes budget on obvious results. A fixed small count leaves borderline results unresolved. Use a bounded sequential policy.

Start every case with the manifest's minimum trial count. At each checkpoint:

- Recompute paired effects and uncertainty for each release-blocking slice.
- Stop a slice when its result clearly satisfies pass or fail rules.
- Allocate the next batch of trials to unresolved slices or influential cases.
- Stop when the global trial, token, cost, or time budget is reached.
- Return inconclusive for any required slice that still crosses a boundary.

The allocation rule must be deterministic and versioned. Otherwise, two operators can spend the same budget on different cases and get incomparable decisions. Record why each additional trial was selected.

Do not stop early merely because the candidate currently looks good. Early stopping rules must be symmetric enough to avoid promoting lucky candidates while demanding more evidence from unlucky ones.

Decide from an evidence receipt

The decision service should consume a completed evidence receipt, not scrape a dashboard. A receipt should include:

- manifest digest and resolved release identities
- complete and excluded trial counts with reason codes
- retry and operational-failure counts
- per-slice baseline, candidate, effect, and uncertainty
- decision margin and statistical method
- repeat budget consumed and stopping reason
- deterministic safety assertion results
- grader release and calibration receipt reference
- final pass, fail, or inconclusive outcome

Sign or otherwise make the receipt tamper-evident if it crosses systems. Attach it to the deployment record so incident responders can see which evidence authorized the release.

A release may pass statistical quality checks and still fail a deterministic security invariant. Combine outcomes conservatively. A forbidden cross-tenant read, unauthorized write, or missing approval should block immediately rather than wait for a confidence interval.

Handle failures without biasing the gate

Several failure modes need explicit policy.

Missing pairs: If either baseline or candidate is missing, do not treat the surviving score as a pair. Retry under the declared attempt policy or exclude both sides with a reason. Too many missing pairs should make the slice inconclusive.

Fixture drift: If an authoritative record changes between paired executions, invalidate the pair. Refresh the fixture snapshot and rerun both releases.

Grader failure: Retry the same grading operation under a bounded policy. Record grader instability separately. If the grader remains unavailable, use a predeclared deterministic fallback or stop as inconclusive.

Provider or tool outage: Preserve the failure as operational evidence. If the goal is behavior quality under healthy dependencies, rerun later but do not delete the outage record. If the journey promises recovery from that outage, count it in the task result.

Budget exhaustion: Return the unresolved slices and the evidence already collected. Never relax the regression margin after seeing the data.

Engineers rerunning a failed gate: A rerun needs a new eval ID linked to the prior receipt. The release system should not accept whichever run produced the most favorable result. Define whether evidence combines across runs or why the earlier run was invalidated.

Verify the gate before trusting it

Test the measurement system with controlled defects and controlled noise.

- Run the same pinned release as both baseline and candidate. The gate should usually pass as equivalent or return inconclusive, not manufacture a stable improvement.
- Inject a known regression into one high-risk slice. The gate must fail even if the global average remains flat.
- Add random score noise without changing behavior. The repeat allocator should spend more evidence and avoid a confident false verdict.
- Force one transient attempt failure. The retry must retain the same logical trial ID and must not increase the statistical repetition count.
- Change a fixture between paired trials. The system must invalidate the pair.
- Exhaust the repeat budget around the decision margin. The result must be inconclusive.
- Make the grader unavailable. The pipeline must follow its declared fallback or stop, not assign a default passing score.
- Submit an evidence receipt with a changed manifest digest. Deployment must reject it.
- Rerun a failed eval unchanged. The audit trail must retain both outcomes and prevent cherry-picking.

Track the gate itself over time: false blocks, regressions missed before production, inconclusive rate, repeat cost by slice, grader disagreement, and operational failure rate. A rising inconclusive rate may mean the suite lacks power, the system became more variable, or the decision margin is tighter than the available budget can support.

Common mistakes

Do not use pass@k as a first-attempt reliability promise. It measures whether at least one of several attempts can succeed.

Do not widen a threshold until flakes disappear. That hides both measurement noise and real small regressions.

Do not compare unpaired task samples when paired fixtures are available. Case-mix variance can dominate the release effect.

Do not report only the mean. Keep the interval, slice results, sample count, exclusions, and operational failures.

Do not let easy cases compensate for a deterministic safety failure or a material decline in a critical slice.

Do not make “rerun CI” the recovery path. A release verdict needs one evidence policy, not a contest between random outcomes.

Next action

Choose one release-blocking eval suite and run the current production release against itself with three paired trials per case. Preserve every attempt, repetition, fixture version, and slice. Measure how often the one-shot verdict disagrees with the repeated result, then set a practical regression margin and a bounded inconclusive policy before the next prompt or model change. That self-comparison will show how much of your current AI agent eval flakiness belongs to the agent, the grader, the fixtures, or the gate.
