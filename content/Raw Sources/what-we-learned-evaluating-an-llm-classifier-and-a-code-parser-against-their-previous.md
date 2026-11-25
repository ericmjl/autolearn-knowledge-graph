---
title: "What we learned evaluating an LLM classifier and a code parser against their previous results | Endor Labs"
type: "raw-source"
url: "https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing"
author: "Endor Labs"
publication: "Endor Labs"
published: "2026-11-18"
archived: "2026-11-25T00:00:55Z"
---

> [!quote] Original source
> **Author(s):** Endor Labs  
> **Title:** What we learned evaluating an LLM classifier and a code parser against their previous results | Endor Labs  
> **Published in:** Endor Labs  
> **Date:** 2026-11-18  
> **Original:** <https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-what-we-learned-evaluating-an-llm-classifier-and-a-code-parser-against-their-previous|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How eval graders should avoid false negatives and false positives

## Archived text

There's a common belief that evals are an LLM thing: if your feature has a model in it, you need one, and if it doesn't, your test suite has you covered. I don't think that's right. An eval is a test for quality rather than correctness: it runs your real system on a fixed set of real cases, scores every result, and tells you whether this version is better or worse than the last one you trusted. Nothing in that definition needs a model, and one of the two evals in this post has no model in it at all. A deterministic parser, a search ranker, or a rules engine has a “how well does it work” question too, and that's precisely the question a unit test can't answer. A test is a smoke detector: it beeps, or it doesn't. An eval is a thermometer: it tells you the temperature, and whether it's rising.

Here's what the difference looks like on a normal morning. One of our nightly evals passed every quality bar we'd set for it, and turned red anyway. A case that an LLM-backed classifier used to label strictly was now getting a milder label on every sample we took. The eval isn't allowed to decide whether that's acceptable, so it held the case out of the baseline, turned the run red, and waited for a person. When we looked, the new label was wrong: a decision that has to come back as "block" was now coming back as "ask", and we fixed the classifier rather than accept the new answer.

The stakes aren't abstract. That label decides whether something is blocked or only questioned, so "ask" where "block" belongs means a thing that used to be stopped now goes through after a prompt. Everything on the surface was still working: the code hadn't changed, the tests were green, and the classifier's aggregate numbers were still inside their limits. One decision had gone softer than allowed, and the eval was the only thing that noticed. We built it to go red in exactly this situation, because a regression that gets accepted automatically is one nobody ever sees.

Tests and evals answer different questions

A test asks: does it work? An eval asks: how well does it work, and did that change since the last time we looked?

Every eval we run, with or without a model in it, has the same four parts:

- A dataset. The inputs you care about, in version control, where each case says what a good result looks like and why it's there.
- A runner. It runs the real system on each case, through the real path rather than a mock.
- A grader. It turns each output into a score, whether that's an exact match, a rule, a metric, or another model's opinion.
- A baseline. The scores from the last run a person accepted, so every new run can report what moved.

The output isn't a green check but a set of scores and how far each one moved, and that changes what happens at the end. An eval tolerates some failures, because it's watching a trend rather than a boolean, but it still flags a single case that gets worse. And when a score moves, a person decides whether to fix the system or accept the new result as the baseline. I'll come back to these four parts later, because each one needs a few things to be trustworthy, and that's where our two very different evals turned out to be the same.

Why this matters more now

- Tests were enough for a long time, so it's fair to ask what changed. Three things, and they compound.
- LLMs give different answers to the same input. Run a model-backed feature once, and you've learned almost nothing, because the next run can disagree. An eval needs many cases, and for the unstable ones, several samples of each, before a flip means anything. The classifier eval below does exactly this: a flip that shows once is noise, and a flip that shows on every sample is a change.
- Behavior moves without a commit. A provider updates a model, someone edits a prompt in a config file, a server-side change deploys. Your tests are pinned to your code, so none of that trips them, and a prompt edit rarely gets the review a code change gets. An eval that runs on a schedule, not only on commits, is what notices.
- Every fix is a trade. Whether the system is a model, a parser, or a ranker, the change that fixes the case you were staring at tends to shift a case you weren't looking at. Without an eval, you see the first one and ship the second. The parser case below is exactly this: one change, six codebases better, one worse.

Where does the right answer come from?

There are many ways to classify evals. The one that's served us best is a single question: where does the right answer come from? Answer it for your feature, and the grader mostly designs itself.

Sometimes you know the answer. Then the grader is a comparison, and the only choice is what to compare against.

- A labeled dataset is the plain case: a person wrote the expected output for each input, and the grader checks for a match. Our classifier eval is one of these. Each case carries the label the rubric says it should get.
- Reference facts cover outputs that are too long or too varied to match whole, but that must contain something specific: a CVE identifier, a function name, a version. The grader checks that the fact is present, by exact match or a pattern, and ignores the rest.
- A benchmark has a measured answer rather than a written one. The right value is whatever the last accepted run produced, and the grader compares against that: files parsed, seconds taken, peak memory. Benchmarking is an eval with the same dataset, grader, and baseline, pointed at a number instead of a label.

Sometimes there's no answer key. A generated explanation, a remediation, a summary: no single correct output exists to match against, so the grader has to judge rather than compare.

- An LLM as judge reads each output against a rubric and scores it. This is the most flexible grader and the easiest to fool yourself with, because a judge is a model, and models drift. A judge needs its own labeled eval, or one unmeasured system is measuring another.
- Property checks need neither a judge nor an answer. They test things that must hold for every output: valid JSON, no secrets, under a length limit, cites only files that exist. They're cheap and deterministic, and worth running on every eval, whatever else grades it.
- Pairwise or human comparison asks a weaker question, “which of these two is better?”, and gets a more reliable answer. We used it to decide whether a cheaper model could replace a pricier one in one pipeline step: same inputs to both models, and a third model judged each pair blind, with the order swapped to cancel position bias. Over 52 pairs, the cheaper model came out comparable or better, at about 4.6x lower cost and about 40% slower, which was fine for a step off the critical path. The sample was small, so we treat the result as a strong signal rather than proof, and it was enough to make the switch.

Two cases from the evals we run

We run evals across the product on two schedules: a small, fast slice on every pull request that touches the system under test, and the full dataset every night. The PR slice is there to catch the obvious regression before merge, and the nightly run to catch the slow one.

Dataset size is a budget decision. Every case costs money, time, and compute on every run, so each one has to earn its place by covering a category, an edge case, an attack, or a bug that escaped before. When we add a case, we write down why, and a case nobody can explain gets cut.

The two evals below look nothing alike, which is the reason I picked them.

An LLM classifier: red, on purpose

This is the eval from the opening. It measures a classifier backed by an LLM, and each case carries an expected label written from the rubric the classifier is supposed to follow, so it's a labeled-dataset eval.

Because the model can answer the same input differently from one run to the next, the eval sends every case three times and takes the majority; when a case disagrees with its baseline, it samples that case again for five more samples before it believes the flip. A flip that shows once is noise. A flip that shows on every sample is a change.

That morning every quality bar passed: the model answered nearly every case, and false negatives and false positives both stayed inside their limits. One case still flipped on every sample, so the eval held it out of the baseline and turned the run red until a person decided. What surprised me the first time I saw a run like this was how little the aggregate told us: every top-line number was green, and the only signal was one row.

In the same run, several cases improved, and the eval wrote those into the baseline on its own. We built it that way on purpose: gains are cheap to accept, and a loss always needs a person.

A code parser: no LLM, still an eval

The second eval has no model in it. It measures a deterministic code parser on a fixed set of open-source codebases, each pinned to an exact commit, because results from different commits aren't comparable. The baseline stores how many files the parser handles in each codebase, which makes this one a benchmark: the right answer is whatever the last accepted run produced.

After one change to the parser, the nightly run reported more files parsed in six codebases and fewer in a seventh codebase. The gains were a handful of files each, one to five; the loss was six files out of roughly 860 in a large compiler codebase. The unit tests were green, because unit tests cover the cases someone thought to write, and nobody had thought to write that one. The eval was the only thing that measured the trade. As with the classifier, the gains went into the baseline by themselves, and the loss waited for a person.

The eval also records time per file and peak memory, so it doubles as a performance benchmark. A run that hangs or blows its memory limit gets an error result, and an error result never reaches the baseline. That rule matters more than it sounds, and it's the first of the three principles further down.

What every eval needs

This is where the two evals—one with a model and one without—turned out to be the same. Earlier I said every eval has four parts: a dataset, a runner, a grader, and a baseline. Having each part isn't the same as being able to trust it. A dataset you can't version is one you can't compare against. A runner that calls a mock measures the mock. A grader that counts a timeout as a pass hides the exact failure you built the eval to catch. A baseline nobody owns goes red and stays red.

When we laid the two evals side by side, the things that made each part trustworthy came to twelve, and they fall into four groups that follow the four parts. Inputs are what the dataset needs. Execution is what the runner needs. Judgment is what the grader and the baseline need. Operations is the part the four-part list leaves out: the report, the schedule, and the person who acts on red.

If you take one thing from the diagram, take the baseline rule: write gains automatically, hold losses for a person, and keep absolute floors so that a dozen small accepted losses can't add up to a decay nobody approved.

Three principles we learned

The diagram says what to build. These three are about what to do when the eval runs and the answer isn't clean, and each one changes how we score.

- A missing result is never a pass. Many systems fall back to a default answer when a model doesn't respond in time, and from the outside a test can't tell “safe” from “never checked”. Count an unanswered check as inconclusive, keep it out of every score, and treat a run with no results at all as a failure rather than a quiet green.
- Only stable cases belong in a pull-request check. A case that flips between runs fails pull requests at random, and within a week people stop reading the check. Keep unstable cases in the nightly run, where the eval can afford to sample them more, and promote a case to the PR slice only once it has held steady.
- Some labels are honestly a range. When two reviewers would reasonably disagree on a label, say between two adjacent severity levels, let the case accept either, instead of forcing a coin flip into the answer key and then “fixing” the model every time the coin lands the other way.

Start small today

None of this needs a platform, and you don't need all twelve things on day one. Any team can get started with this just with these four things:

- Twenty to thirty real cases, each one there for a reason you can write down.
- A script that runs the real system on those cases and scores the output.
- A baseline file in version control.
- A nightly job that compares each run with the baseline and tells a person what moved.

Then make one habit stick: every bug that escapes becomes a new case. After a few months, that dataset is the best description of your feature's edges you'll own.

If anyone can ask “how good is it?” about your feature, it needs an eval, with or without an LLM.

What's next?

When you're ready to take the next step in securing your software supply chain, here are 3 ways Endor Labs can help:
