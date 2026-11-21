---
title: "Your eval suite has a variance problem before it has a score problem"
type: "raw-source"
url: "https://vectoryai.com/blog/eval-variance-pass-at-k-and-suite-saturation/"
author: "Vectory (no individual author named)"
publication: "Vectory"
published: "2026-09-07"
archived: "2026-11-21T23:02:56Z"
---

> [!quote] Original source
> **Author(s):** Vectory (no individual author named)  
> **Title:** Your eval suite has a variance problem before it has a score problem  
> **Published in:** Vectory  
> **Date:** 2026-09-07  
> **Original:** <https://vectoryai.com/blog/eval-variance-pass-at-k-and-suite-saturation/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-your-eval-suite-has-a-variance-problem-before-it-has-a-score-problem|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: Saturation-graduation rule: when and how to move capability evals into regression suites

## Archived text

One run is a sample, not a score

If you cannot tell whether last night's drop from 0.88 to 0.79 is a regression or noise, the answer is that you do not have enough trials and you have not said which metric the number represents. Run each task multiple times, report pass^k when the agent has to succeed on every attempt and pass@k when one success out of k attempts is enough, and treat a suite whose scores no longer separate two candidate versions as a broken suite rather than a finished one.

The arithmetic makes the problem concrete. Anthropic's agent-evals guidance defines a trial as each attempt at a task, and works an example where a 75 percent per-trial success rate produces roughly 42 percent pass^3, meaning all three trials succeed less than half the time.[1] Nothing about the agent changed between those runs. The reported number changed because sampling changed.

So the first fix is not a better grader or a bigger suite. It is a run manifest that records how many trials you took and under which conditions, so two reports can be compared at all. The values in the examples below are illustrations of the record shape, not measured Vectory results.

- task_id and suite_version, so the case is identifiable across releases.
- trials: 5 and metric: pass^5, stated before results are read.
- model_id, temperature, and seed, because sampling settings move variance.
- harness_version, since the harness is part of the system under test.[1]

Pick the metric that matches the product promise

pass@k measures the chance of at least one success in k attempts, so it rises as k grows. pass^k measures the chance that all k trials succeed, so it falls as k grows. At k equal to 1 the two are the same number, which is exactly why a single-run report hides the distinction. With the 75 percent per-trial rate from the example above, increasing k widens the gap: pass@k rises while pass^k falls.[1]

The choice follows the product, not the dashboard. If a user can retry cheaply and a failed attempt costs a few seconds, pass@k describes the experience honestly. If a single failure writes a bad record, sends a wrong message, or merges a broken patch, then the promise is that every attempt works, and pass^k is the number that belongs in the gate.

Reporting both at once is often the most useful line in a release review. A results row reading pass@5: 1.00, pass^5: 0.24, variance_flag: high, decision: block says something a single average cannot: the capability exists, and the reliability does not.

- Retry is free and invisible to the user: gate on pass@k.
- A single failure is user-visible or writes state: gate on pass^k.
- Publish both numbers so reviewers can see the spread.
- Never compare a pass@k figure from one release against a pass^k figure from another.

A 0 percent pass rate is usually a broken task

The most expensive misreading in eval work is treating a floor score as a capability gap. Anthropic's guidance states the diagnostic plainly: a 0 percent pass rate across many trials, such as 0 percent pass@100, is most often a signal of a broken task.[1] A hard task produces a low, noisy rate. A broken task produces a clean zero.

Grading precision is a frequent cause. The same guidance reports a CORE-Bench case where an answer of 96.12 was marked wrong because the expected value was 96.124991.[1] No prompt change and no model upgrade will move that score, because the agent was right and the comparison was wrong.

The cheap check is to read transcripts before filing anything. Anthropic's framing is that eval scores should not be taken at face value until someone digs into the details, and that failures should seem fair.[1] Start with three transcripts, then expand the sample if the failure mode is still unclear.

- Trigger: pass@100 at 0.00 on a task the team believes is achievable.
- Action: read three transcripts end to end before opening a model ticket.
- Common finding: grader compared a formatted string instead of a tolerance.
- Resolution: fix the grader, rerun, and record the task as amended in the suite changelog.

Ambiguity shows up as variance, not as an error

Underspecified tasks rarely fail loudly. They fail sometimes, which reads as flakiness. Anthropic offers a usable quality bar: a good task is one where two domain experts would independently reach the same pass or fail verdict, because ambiguity in task specifications becomes noise in metrics.[1]

The published example is worth copying into your own review. A Terminal-Bench audit found that unspecified script filepaths caused undeserved failures, since the agent had no way to know where the grader would look.[1] The agent solved the problem and then lost on a detail the task never stated.

Run the two-expert test on any task whose trial results scatter. If two reviewers disagree about whether a transcript passed, the task specification is the defect, and tightening it removes variance that no amount of extra trials will average away.

- Symptom: trial results scatter while the transcripts look reasonable.
- Test: two reviewers grade the same transcript blind and compare verdicts.
- Fix the specification first: required output location, format, and stop condition.
- Prefer grading what the agent produced over the path it took.[1]

Contamination looks exactly like improvement

Scores that rise for the wrong reason are harder to catch than scores that fall. Shared state between trials is a documented source. Anthropic describes a case where a Claude run gained an advantage by reading git history left behind by earlier trials, which means the second trial was an easier task than the first.[1]

Version drift produces the same illusion at the harness layer. The SWE-bench Verified page states that results from mini-SWE-agent release 1.x and 2.x are not necessarily comparable to each other, because 1.x parses actions from output strings while 2.x uses tool calling, and temperature was pinned at 0.0 for 1.x and left unset from 2.x onward.[3] Two numbers from the same named benchmark can therefore describe different experiments.

That page also shows what a controlled comparison costs: SWE-bench Verified is a human-validated subset of 500 SWE-bench instances, built with OpenAI, where annotators checked that problem statements were understandable, test patches valid, and tasks achievable.[3] Isolation and validation are the work, not overhead on top of it.

- Reset the workspace, caches, and version control state between trials.
- Assert a clean environment as a precondition rather than assuming it.
- Pin harness_version and sampling settings on every reported score.
- Treat any unexplained score jump as a contamination hypothesis first.

Saturation is a suite failure, not a milestone

Two suites should carry opposite expectations. Anthropic's guidance is that capability evals should start at a low pass rate, while regression evals should sit at a nearly 100 percent pass rate, and that a saturated capability eval can graduate into the regression suite.[1] A single threshold applied to both suites will either block every release or none of them.

The number to watch is discrimination, not the mean. A capability suite reporting pass_rate: 0.98 with 0.01 separation between candidate and baseline has stopped answering the release question, whatever the headline says. The action is to graduate those tasks into regression, where a near-perfect rate is the point, and author harder capability tasks.

New tasks should come from the same place the first ones did. Anthropic suggests 20 to 50 simple tasks drawn from real failures as a strong start, and argues that maintaining evals should be as routine as maintaining unit tests.[1] A suite with no additions this quarter is drifting away from the product it is supposed to guard.

- capability_suite.pass_rate: 0.98 with discrimination 0.01 means graduate, not celebrate.
- regression_suite target: near 1.00, with the release threshold set by the consequence of failure.
- Source new tasks from incidents, escalations, and expensive successes.
- Retire a task only when the product behavior it covers no longer exists.

The reporting contract that lets a reader separate signal from noise

Public benchmarks already model the format. Terminal-Bench publishes cost and tokens beside resolution rate, and states that the whiskers on its chart span the 95 percent confidence interval, so readers see a range instead of a point.[2] METR fits success probability against human task length per model and draws 95 percent confidence bands from hierarchical bootstrapping over task families, tasks, and attempts.[4] Its reported trend, a 50 percent time horizon doubling roughly every 7 months with stated uncertainty of about 1 to 4 doublings per year, comes with a caveat the page states itself: some of the text and figures in that post are out of date, only the interactive chart is maintained, and Time Horizon 1.1 was announced on 29 January 2026.[4] Cite the caveat with the number.

Thresholds need the same specificity. Anthropic's evaluation guidance contrasts a vague criterion like safe outputs against a measurable one: less than 0.1 percent of outputs out of 10,000 trials flagged for toxicity by the content filter.[5] The second version states a population, a trial count, and a detector, so two teams reading it would run the same test.

Finally, report your own misses. Anthropic extended its evaluation cadence from three months to six in version 2.0 of its Responsible Scaling Policy to avoid lower-quality, rushed elicitation, and its self-review disclosed shortfalls including evaluations finished three days late and missing elicitation techniques such as best-of-N and chain-of-thought.[6] A gate that never reports where it fell short gives a reader no way to judge how much the passing runs are worth.

- Trial count and the metric name beside every score.
- An interval or spread, not only a point estimate.
- Cost and token usage next to quality, since a win you cannot afford is a product decision.
- Suite, harness, model, and grader versions, plus known gaps in this run.
