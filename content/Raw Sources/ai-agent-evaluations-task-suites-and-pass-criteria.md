---
title: "AI Agent Evaluations: Task Suites and Pass Criteria"
type: "raw-source"
url: "https://levystreet.com/engineering/ai-agent-evaluations/"
author: "Levy Street (no individual author named)"
publication: "Levy Street"
published: "2026-10-19"
archived: "2026-11-25T16:01:18Z"
---

> [!quote] Original source
> **Author(s):** Levy Street (no individual author named)  
> **Title:** AI Agent Evaluations: Task Suites and Pass Criteria  
> **Published in:** Levy Street  
> **Date:** 2026-10-19  
> **Original:** <https://levystreet.com/engineering/ai-agent-evaluations/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-ai-agent-evaluations-task-suites-and-pass-criteria|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How do product teams structure holdout sets and task-specific eval suites to avoid agent overfitting, and what cadence keeps them honest?

## Archived text

Short answer

AI agent evaluation means running an agent against a fixed suite of realistic tasks, each with explicit pass and fail criteria checked against the final system state and the steps taken, several times per task. Report task success, consistency across repeats (pass^k), harmful-action rate and cost per successful task, and rerun the suite on every prompt, tool or model change before release.

- Write each task as input, seed state, required outcome, forbidden actions and a step limit.
- Grade the final system state with code first. Use LLM judges only for open-ended text.
- Repeat every task several times. Report pass^k, not just one-run success.
- Penalise bad output explicitly so an agent cannot win by producing more of it.
- Version tasks, fixtures, graders and judge models together, and gate releases on them.

What should an AI agent evaluation measure?

An agent evaluation measures whether the agent reaches the right end state, by an acceptable path, at an acceptable cost, consistently. Measuring only the final answer misses agents that get there by breaking rules, and measuring a single run misses agents that succeed by luck.

With n trials of a task and c successes, an unbiased estimate of that task’s pass^k is C(c, k) divided by C(n, k), the chance that k trials drawn from the n were all successes. The τ-bench paper introduced pass^k because capable function-calling agents were found to be inconsistent across repeated attempts at the same task.

How do you build a task suite with pass and fail criteria?

A task suite is a versioned set of realistic cases, each with an environment to run in and criteria that a program can check. Build it from real work, not from imagination.

- Sample real cases. Pull 50 to 150 cases from tickets, inboxes or logs, stratified by type and difficulty. Deliberately include the awkward ones: missing data, conflicting instructions, requests that should be refused.
- Fix the environment. Give each task a seed state: database fixtures, mock APIs or a snapshot of documents. Live systems change underneath you and make results impossible to compare.
- Write criteria as checks. Required end state, forbidden actions, required approvals and a step limit. If a criterion cannot be checked by code or a calibrated rubric, rewrite it.
- Split the suite. Keep a development set you tune against and a sealed holdout you only run before releases and model upgrades.
- Version everything together. Tasks, fixtures, graders, judge prompts and judge model versions share one version number, so a score always means the same thing.

A task definition and grader can be this small:

TASK = {

    "id": "refund-017",

    "input": "Order 88412 arrived damaged. Customer wants a refund.",

    "seed_state": "fixtures/orders_v3.json",

    "must": [("refund.created", {"order_id": "88412", "amount_lte": 129.00}),

             ("reply.drafted", {"mentions_refund": True})],

    "must_not": ["email.sent_without_approval", "refund.created_other_order"],

    "max_steps": 10,

}

def grade(task, final_state, trace):

    failures = [m for m in task["must"] if not final_state.satisfies(*m)]

    harms = [e for e in trace.events if e.kind in task["must_not"]]

    over = len(trace.steps) > task["max_steps"]

    return {"passed": not failures and not harms and not over,

            "failures": failures, "harms": harms, "steps": len(trace.steps)}

The grader reads final state and the trace. It never asks the agent whether it succeeded.

When should you use an LLM as the judge?

Use deterministic checks wherever the outcome is visible in system state, and an LLM judge only for qualities code cannot read, such as whether a drafted reply is accurate, polite and complete. LLM judges are useful but biased: Zheng et al. documented position, verbosity and self-enhancement biases alongside high agreement with human preferences on their benchmarks.

Rules we apply to judges:

- Rubrics with anchors. A 1 to 5 scale where each level is described, or a set of yes/no questions, never “rate the quality”.
- Evidence required. The judge must quote the passage that justifies each score, which makes disagreements debuggable.
- Calibrate before trusting. Label a sample by hand, measure judge agreement, and recheck it whenever the judge model or rubric changes.
- Pin the judge. A silently upgraded judge moves every score. Treat the judge model as part of the suite version.
- Separate families where possible. Judging with a model from a different provider than the agent reduces shared blind spots.

What does GTM-Bench teach about scoring agents?

Score bad output as harmful, or agents will learn to flood you with it. GTM-Bench, published by Blackpearl Group in June 2026 and co-authored by Levy Street team members, makes this explicit. It contains 72 tasks drawn from a taxonomy of 59,881 real prospecting queries. Each agent produces an inferred offer, an inferred ideal customer profile and a ranked list of buyer records (paper, section 2.5).

Every returned record is graded by LLM match and audit judges and scores plus one if A-grade, zero if B-grade and minus one below that. The task score multiplies offer and profile quality by the sum of those record scores. In the paper’s words, “this design deliberately treats low-quality records as harmful.” The effect shows in the results: several general-purpose agents finished with negative net scores, and the paper records one agent returning 6,342 rows on a single task.

Three lessons transfer to business agents. Penalise false positives in proportion to the work they create for a person. Score intermediate artifacts (here, the inferred offer) as well as the final list, because a wrong early inference poisons everything after it. And state reproducibility limits honestly: the paper notes that its production environment uses Blackpearl’s own data, which limits reproduction outside the benchmark operator. Our write-up of AI agents for go-to-market research covers the domain findings.

How do you run evaluations so the numbers mean something?

Run each task several times at production settings, report intervals rather than single numbers, and budget for the cost. Small suites have wide uncertainty: 40 passes out of 50 tasks gives a 95% Wilson interval of roughly 67% to 89%, so a two-point change between releases is noise.

Cost is easy to estimate. Illustrative example: 60 tasks, 5 trials each, at an average of US\$0.40 per agent run is 300 runs and US\$120 per full suite, plus judge calls. That is cheap next to a production incident, and it is why we keep a smaller smoke suite for every change.

Keep the suite in your own repository and runner. Hosted evaluation products come and go: OpenAI’s deprecations page lists its Evals platform becoming read-only on 31 October 2026 and shutting down on 30 November 2026, as listed on 19 October 2026. Portable task files and graders survive that kind of change.

Versioning prompts and evaluations covers how to tie these runs to releases, and monitoring AI quality covers the production side.

Where do agent evaluations go wrong?

Most broken evaluations fail quietly by measuring something easier than the real task.

- Grading the claim, not the state. A grader that reads the agent’s final message will pass agents that say “done” without doing it.
- Leakage. Few-shot examples copied from the test set inflate scores. Keep the holdout sealed and out of every prompt.
- Environment drift. Tasks that hit live websites or shared databases give different answers each week. Snapshot what you can and record what you cannot.
- Overfitting. After months of tuning against the same 50 tasks, the suite measures memory of those tasks. Refresh it with new production cases.
- Synthetic-only suites. Generated tasks are useful for coverage, but they miss the mess of real inputs. See testing AI with synthetic data for where they help.

The NIST AI RMF core puts the principle plainly: AI systems should be tested before deployment and regularly while in operation. For agents built with retrieval, pair this guide with RAG retrieval evaluation. If you want a second pair of eyes on an existing suite, that is the core of our LLM evaluation services, and the AI agent acceptance checklist is a useful sign-off document. The architecture these tests assume is set out in designing reliable AI agents.

- Tasks come from real cases, stratified by type, with hard and refusal cases included
- Every task has a seed state, required outcomes, forbidden actions and a step limit
- Graders check system state and the trace, never the agent’s own claim
- LLM judges use anchored rubrics, quote evidence, are calibrated and are pinned
- Bad or unsupported output is penalised, not just ignored
- Each task runs several times and results report pass^k and intervals
- Tasks, fixtures, graders and judge versions share one suite version
- A sealed holdout runs before releases and model upgrades
- Release gates are written down and enforced in CI
- Production samples are graded weekly and new failures join the suite

Sources

- GTM-Bench: Evaluating Agentic AI Systems for Buyer/Seller Coherence in Go-to-Market Workflows, Blackpearl Group Limited, June 2026
- GTM-Bench leaderboard, Blackpearl Group, accessed 19 October 2026
- τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains, arXiv (Yao et al.), 2024
- Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena, arXiv (Zheng et al.), 2023
- Deprecations, OpenAI API documentation, accessed 19 October 2026
- AI RMF Core, National Institute of Standards and Technology, 2023

Written by the Levy Street team in Wellington. Last updated 19 October 2026.
