---
title: "Continuous LLM Evaluation: A Practical Guide for Production Teams | MLflow"
type: "raw-source"
url: "https://mlflow.org/articles/continuous-llm-evaluation/"
author: "MLflow AI Platform (no individual author named)"
publication: "MLflow AI Platform"
published: "2026-11-05"
archived: "2026-11-26T03:00:58Z"
---

> [!quote] Original source
> **Author(s):** MLflow AI Platform (no individual author named)  
> **Title:** Continuous LLM Evaluation: A Practical Guide for Production Teams | MLflow  
> **Published in:** MLflow AI Platform  
> **Date:** 2026-11-05  
> **Original:** <https://mlflow.org/articles/continuous-llm-evaluation/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: Question 0: how calibration loops for eval judges degrade over time and what maintenance cadence production teams use

## Archived text

Continuous LLM Evaluation: A Practical Guide for Production Teams

Continuous LLM evaluation means scoring your application's behavior on every change and on live traffic, not once before launch. In practice you combine four pieces: a versioned dataset of real cases, automated scorers (code checks and LLM judges), a CI gate that blocks regressions, and sampled evaluation of production traces. This guide shows how to build each piece, in the order we would build them.

TL;DR

- Treat evaluation as an ongoing function of development and operations, not a release gate. Agents and prompts change too often for a one-time test to stay valid.
- Start with a small golden dataset built from real traces, include bad examples, and stratify it by intent, difficulty and failure mode.
- Run the offline suite in CI on every pull request and fail the build when scores drop below your thresholds.
- Sample production traffic, score it with the same scorers, and feed every new failure back into the dataset.
- Calibrate your LLM judges against human labels, and cache model calls so your measurements are not noisy.

Table of Contents

What continuous LLM evaluation actually is

A traditional software test suite answers a binary question: does the function return the expected value? LLM applications fail differently. Outputs vary run to run, quality is a matter of degree, and an agent can reach the right answer through a wrong or dangerous path. A model provider update, a prompt edit or a new tool can shift behavior without a single line of application code failing.

Researchers working on agent engineering argue for the same shift. A CSIRO-led paper on evaluation-driven development and operations of LLM agents proposes that evaluation should be a continuous, governing function across development and operations, rather than a terminal gate, so autonomous agents can evolve safely.

In day-to-day terms, continuous evaluation has three loops:

- Pre-merge loop. Every change to a prompt, model, tool or retrieval step runs against an offline dataset in CI.
- Post-deploy loop. A sample of live traffic is scored automatically, and low-scoring traces are flagged.
- Learning loop. Failures from production become new test cases, so the suite grows with your real failure modes.

The rest of this guide builds these loops in order. If you want the broader picture of how the pieces fit, our overview of LLM and agent evaluation in MLflow covers the building blocks.

Why a release-time check is not enough

Three things make one-time evaluation brittle.

Your system is more than a model. Behavior depends on the prompt, the retrieved context, the tools and the model version. Any of them can change independently.

Users drift. The queries you imagined during development are not the queries you receive after three months in production. A dataset frozen at launch slowly stops representing reality.

Agents have trajectories. A multi-step agent can produce a correct final answer while calling the wrong tool, leaking data into a sub-call or burning ten times the tokens. Outcome-only checks miss this. You need to evaluate the path, which is why tracing is the foundation of everything below.

Step 1: Instrument your app so every run leaves a trace

Continuous evaluation without traces is guesswork. A trace records each step of a run: the prompt, retrieved documents, tool calls, intermediate reasoning, latency and token counts. That record is what you score, replay and mine for new test cases.

In MLflow, tracing is enabled with an autolog call for supported frameworks, or with a decorator for your own functions:

import mlflow

mlflow.set_experiment('support-agent')

@mlflow.trace

def answer(question: str) -> str:

context = retrieve(question)

return call_llm(question, context)

Because MLflow tracing builds on OpenTelemetry, the traces fit into the observability tooling you may already run. Our page on LLM and agent observability explains what gets captured and how to inspect it.

Step 2: Build a golden dataset from real behavior

The dataset is the part of your evaluation program that no tool can do for you. Frameworks are interchangeable; the examples you choose are what make your scores meaningful.

A few rules that hold up in practice:

- Start small and include failures. Airbnb's engineering team recommends a golden dataset of 50 to 100 examples that includes bad examples, so your scorers prove they can tell good from bad.
- Prefer real traces to synthetic ones. Pull examples from production or staging traces. Synthetic data is useful to fill gaps, but it reflects what you imagine, not what users do.
- Stratify. Label examples by intent, difficulty and observed failure mode. Random sampling under-represents the rare failures that cause the most damage.
- Version it. Treat the dataset like code. A score is only comparable across commits if you know which dataset produced it.
- Write expectations, not just inputs. For each case record an expected fact, a required tool call, or a guideline the answer must follow.

To turn traces into rows, search them and select the ones worth keeping:

traces = mlflow.search_traces(max_results=200)

# review, label, then store the chosen cases as your versioned dataset

A good first target is a couple dozen cases per major intent. Grow it every time production surprises you.

Step 3: Pick scorers that match your failure modes

Metric selection is a translation exercise. Product owners say what good looks like ("trustworthy," "on-brand," "doesn't promise refunds we can't give"), and engineers map those goals to something measurable. Use three kinds of scorers, cheapest first.

Run code checks everywhere, because they are free and exact. Use LLM judges for qualities that code cannot express. Reserve humans for calibrating the judges and for the cases the judges flag.

A minimal offline evaluation in MLflow looks like this:

import mlflow

from mlflow.genai.scorers import Correctness, Guidelines

results = mlflow.genai.evaluate(

data=golden_dataset,

predict_fn=answer,

scorers=[

Correctness(),

Guidelines(name='tone', guidelines='Be polite and never promise refunds.'),

],

)

print(results.metrics)

The Agent and LLM evaluation page lists the built-in judges and how to write custom scorers.

Calibrate your judges before you trust them

An uncalibrated judge is a second black box stacked on the first. Airbnb describes running its virtual judges against a golden dataset, measuring agreement with human labels, and refining judge prompts until agreement reaches a target in the high 80s to 90s percent. Perfect agreement is not realistic, since humans disagree with each other too.

The workflow is simple: have domain experts label 100 or so cases, run the judge on the same cases, look at disagreements, tighten the judge's instructions, and repeat. Ask the judge to return its reasoning with every score, so you can inspect bias and spot misreadings. We go deeper in our guide to LLM judge calibration: measure, correct and report.

Step 4: Put evaluation in CI/CD

This is the step that turns evaluation from a report into a safeguard. The idea: any pull request that touches prompts, model settings, tools or retrieval triggers the offline suite, and the job fails if quality falls below your thresholds.

A workable pipeline:

- Trigger on relevant paths. Run on changes to prompt files, agent code, tool definitions and config. Skip it for README edits.
- Run the suite against the PR build. Point predict_fn at the code in the branch.
- Compare to a baseline. Store the main branch's scores and compare per scorer, not just on average. An average can hide a collapse in one intent.
- Fail with a clear message. Print which scorer dropped, on which cases, with links to the traces.
- Post a summary to the PR. Reviewers should see score deltas without opening a dashboard.

A gate script can be as plain as this:

import sys

THRESHOLDS = {'correctness/mean': 0.85, 'tone/mean': 0.90}

failed = [k for k, v in THRESHOLDS.items() if results.metrics.get(k, 0) &lt; v]

if failed:

print('Evaluation gate failed:', failed)

sys.exit(1)

Check the exact metric names your scorers emit before hard-coding thresholds. Run the script as a normal CI step, and failures block the merge like any other failing test. Teams at other companies describe the same pattern: evaluation runs in CI integrations and failures block merges, while preview deployments can host end-to-end tests against preview URLs.

Keep the gate fast and stable

CI gates that take an hour or flake randomly get disabled. Airbnb's engineers report that much of the apparent noise in LLM evaluation comes from the testing process itself, for example from re-running evaluations, and that caching model calls makes measurement deterministic, efficient and diagnostic.

Practical consequences for your pipeline:

- Cache LLM and tool responses keyed on the full input, so unchanged parts of the pipeline cost nothing on reruns.
- Run a small smoke subset on every commit and the full suite on merge or nightly.
- Set thresholds with a margin based on observed run-to-run variance, not on a number you wish for.
- Run independent cases in parallel.

Step 5: Trace-based regression testing

A regression suite built from traces answers a sharper question than a generic benchmark: did this change break something that used to work for our users?

The loop looks like this:

- A production trace is flagged, by a low judge score, a thumbs-down or a support ticket.
- An engineer reviews it, writes the expected behavior, and adds it to the dataset with a failure-mode label.
- The fix ships, and the case now guards against the same failure forever.
- Each new PR runs the whole accumulated suite.

Over months the suite becomes an institutional memory of every way your system has failed. Compare traces between versions too: when a score moves, look at which spans changed. Did retrieval return different documents? Did the agent add a tool call? Did latency or token usage jump? The trace turns "the score dropped" into "the planner now calls search twice before answering."

This is also how an agent regression suite differs from a prompt test set. For agents, assertions should cover the trajectory: which tools were called, in what order, with which arguments, and how many steps it took.

Step 6: Agent replay testing

Replay uses a captured trace to create a repeatable test. Instead of hoping the live model repeats a behavior, you re-run the agent's logic against the recorded inputs and tool outputs, then check what it does.

What to capture so replays are useful:

- The full input and context, including the system prompt version and model identifier.
- Tool calls and their results, so the replay can serve recorded responses and avoid hitting live APIs or causing side effects.
- Configuration, such as temperature, retrieval parameters and feature flags.
- Timing and token counts, for cost and latency assertions.

What to check in a replay:

- Deterministic assertions on the trajectory: the right tool was called, the forbidden one was not, arguments had the correct shape.
- Outcome scorers on the final answer.
- Budget assertions: steps, tokens and latency within limits.

Handle sensitive content before a trace becomes a test fixture. Redact or replace personal data, secrets and customer content at capture time, and keep stored traces under the same access rules as production logs. Airbnb's live-traffic sampling, described below, uses de-identified traffic for the same reason.

Step 7: Evaluate live traffic

Offline suites only cover what you thought of. Production evaluation covers everything else. Airbnb describes sampling 5% of live, de-identified traffic daily, running programmatic checks and virtual judges on it, and surfacing flagged outputs for human review.

A sensible production setup:

- Sample, don't score everything. A fixed percentage, plus 100% of traces with explicit negative feedback or errors.
- Score asynchronously. Run judges off the request path so users never wait on evaluation.
- Reuse your scorers. The same definitions in CI and production mean scores are comparable.
- Watch trends, not single scores. Alert on a sustained drop in a scorer's rolling mean, or a shift in the mix of intents.
- Route flags to people. A queue of low-scoring traces, reviewed weekly, is the cheapest source of new test cases you will ever have.

Our AI monitoring for LLMs and agents page covers how to track these signals alongside latency, cost and errors.

Operational risks and how to manage them

A few things go wrong in nearly every continuous evaluation program. Each has a straightforward fix.

- Judge cost grows quietly. Use code checks first, sample production, and cache.
- Goodhart effects. If you tune a prompt only against the golden set, scores rise while real quality stalls. Refresh the set with new production cases regularly and hold out a slice you never tune against.
- Stale labels. Policies change. Review the human-labeled calibration set on a schedule, quarterly is a common cadence in layered evaluation guidance, and re-check judge agreement afterward.
- Judge model changes. If the model behind your judge is updated, re-run calibration before trusting trend lines.
- Data exposure. Evaluation touches real user content. De-identify, restrict access and set retention limits.

And a reminder that evaluation is a lifecycle concern, not a final inspection. Writing on self-learning algorithms and autonomous AI chatbots makes a related point: systems that adapt over time need ongoing oversight rather than one release-time sign-off.

Our perspective: evaluation belongs in the platform, not beside it

We build MLflow on a simple belief: the teams that ship reliable agents are the ones that close the loop between what happens in production and what gets tested before the next release. That loop breaks when tracing lives in one tool, evaluation in another, prompts in a spreadsheet and gateway rules in a third.

So we put the pieces together. Traces capture agent reasoning. Evaluation uses those traces and LLM judges to score them. Prompts are versioned in a registry so you can tie a score to the exact prompt that produced it. The AI Gateway governs access across providers. Everything is open source under Linux Foundation governance, with no enterprise feature paywalls, and tracing builds on OpenTelemetry so you are not locked into one framework.

Our advice if you are starting: do not wait for a perfect dataset. Instrument one app, collect fifty real traces, label them, and wire a gate into CI this week. The first regression it catches will pay for the effort.

Kevin

Putting it together: a 30-day rollout

Week 1. Turn on tracing in your main app. Review twenty traces by hand to see how it really behaves.

Week 2. Build the first golden set of 50 to 100 cases, including known bad ones. Add deterministic checks and one or two judges. Get a baseline score.

Week 3. Calibrate judges against human labels. Add the CI job with a smoke subset and a gate on the scorers you trust.

Week 4. Start sampling production traces, route low scores to a review queue, and promote the first reviewed failures into the dataset. Version your prompts in the MLflow Prompt Registry so every score ties to a prompt version.

After that, the work is maintenance: add cases, retire obsolete ones, recalibrate on a schedule and tighten thresholds as quality improves.

Start with MLflow

MLflow is an open-source platform for GenAI and LLM lifecycle management, covering deep tracing of agent reasoning, automated LLM-as-a-Judge evaluation, prompt management and versioning, and a cross-provider AI Gateway. Every feature is available in the open-source project, so you can build the whole loop in this guide without a license.

Begin with MLflow and add tracing to one application, then explore AI observability for LLMs and agents to see what your traces reveal. Teams that need enterprise support or integration help can find out more from the project site.

FAQ

How is continuous LLM evaluation different from running a benchmark?

A benchmark measures a model on generic tasks at one moment. Continuous evaluation measures your application, with your prompts, tools and data, on every change and on live traffic. It is built from your own traces and failures, so it catches the regressions your users would actually notice.

How big should the evaluation dataset be?

Start with 50 to 100 examples that include bad cases, as Airbnb's engineers suggest, and grow it from production failures. Quality and coverage matter more than count. Label examples by intent, difficulty and failure mode so you can see which slice regressed.

Can I use an LLM judge as the only evaluator?

It is safer not to. Use deterministic checks for anything code can verify, LLM judges for subjective qualities, and human labels to calibrate the judges. Re-check judge agreement with humans whenever you change the judge prompt or the judge model.

What should block a merge in CI?

Block on scorers you have calibrated and that map to real user harm: correctness on core intents, policy and safety guidelines, required tool usage. Compare per scorer against the main branch baseline, with a margin for run-to-run variance, rather than relying on a single average.

Sources

- Evaluation-Driven Development and Operations of LLM Agents (arXiv)
- Eval-driven development: Lessons from evaluating GenAI at scale (Airbnb Engineering)
- From weeks to a day: how we made LLM evaluation fast enough to iterate on (Airbnb Engineering)
- AI agent evaluation frameworks in production
