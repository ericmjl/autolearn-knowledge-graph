---
title: "Model Routing as an Eval Problem | Mercor Enterprise"
type: "raw-source"
url: "https://www.mercor.com/blog/mercor-model-routing-eval-problem/"
author: "Brandon Lei"
publication: "Mercor"
published: "2026-07-09"
archived: "2026-11-27T07:01:45Z"
---

> [!quote] Original source
> **Author(s):** Brandon Lei  
> **Title:** Model Routing as an Eval Problem | Mercor Enterprise  
> **Published in:** Mercor  
> **Date:** 2026-07-09  
> **Original:** <https://www.mercor.com/blog/mercor-model-routing-eval-problem/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-model-routing-as-an-eval-problem-mercor-enterprise|Source note]]
Themes: [[Agent design patterns]], [[Evals and agent quality]]
Why it was archived: What optimization methods do practitioners use to find the cost-accuracy Pareto frontier for agent workloads?

## Archived text

Model routing is an evaluation problem

With Vaithiyanathan Sundaram, Michael Wang, Biao Zhang, Braden Holstege, Han Pei, Alex Gonzalez, Helen Rhee, Imani Parker-Fong

Frontier models are becoming both more capable and more expensive. As enterprises scale agents into production, token bills can grow quickly, and the most capable model is rarely the right model for every task.

The goal is not to run the best model everywhere. It is to run the least expensive model that still delivers the required level of performance for the work in front of it.

That makes model routing a cost-quality optimization problem, also known as the Pareto optimization problem. Every agent has a frontier of tradeoffs between performance and cost. The job is to operate on that frontier instead of overpaying for capability a task does not need.

Figure 1: Each point represents a model-routing configuration tested against the same evaluation suite. The Pareto frontier contains the configurations that are not dominated by another option on both cost and quality.

How you assign models to work determines where you land, whether the choice is static, query-level, or made dynamically inside the agent. At Mercor, we believe the only reliable way to find that frontier, and keep an agent on it as models change, is rigorous evaluation.

Evaluations are the system of record

In Agent Eval Systems, we argued that an evaluation suite is the decision layer for agent quality. It defines what good means for a specific agent, on its actual workload, inside its actual environment.

That same suite should govern cost optimization. Here, good performance and quality corresponds to higher scores on the verifiers rigorously defined in its evaluation suite. Once quality is measurable, every model swap, routing rule, and harness change can be judged by whether performance held, what tradeoffs appeared, and what it cost.

Without that measurement layer, lower token spend is ambiguous. It may mean the agent got more efficient. It may also mean it started skipping work, mishandling edge cases, or failing in places the cost dashboard cannot see.

This reframes model routing. Public leaderboards can tell you how models perform on shared benchmarks, but they cannot tell you which model your specific agent needs for your tasks in your environment. That is why every agent needs a comprehensive evaluation suite. It is the only way to see the real tradeoffs when a model or harness changes. From there, model routing becomes a harness experimentation question of which architecture and model mix gets closest to the Pareto frontier on your evaluation suite.

Three ways to route models

There are three broad strategies for assigning models to work inside an agent:

1. Static Model Selection

Sweep every candidate model across the full evaluation suite, then pick the single model that delivers the required performance at the lowest cost.

2. Query Classification Routing

Classify each incoming query by difficulty, then route it to a model sized for that difficulty. For example, a lightweight router might send hard queries to Opus and routine ones to Haiku.

3. Dynamic Delegation

Keep a frontier model as the main agent and let it delegate subtasks to subagents running smaller, cheaper models, deciding at runtime, with full context, what it can safely hand off.

These three are the most established patterns, not an exhaustive list. Hybrid approaches exist, and new ones will emerge as agent architectures evolve.

Each of these can be the right answer. Which one is right depends on the shape of the agent’s workload, especially how widely task difficulty varies. That shape is exactly what an evaluation suite reveals.

Workload shape determines routing strategy

Some agents operate on workloads with relatively concentrated difficulty. The tasks vary in topic, but most sit in the same rough band of complexity. For these agents, static model selection can be enough.

Figure 2: Static model selection works best when task difficulty is concentrated. Routing and delegation become more useful when task difficulty varies widely across tasks or subtasks.

An internal support triage agent is the canonical example. If most tasks involve classifying issues, retrieving known policy, or drafting bounded responses, a full model sweep may reveal a clear knee in the cost-performance curve. Here, the best model is selected against the criterion the deployment actually needs, whether that means the strongest quality-to-cost ratio, the lowest cost above a quality floor, the highest quality under a cost ceiling, or the model that performs best on the quality gates that matter most. In agents with bounded complexity, past a certain capability tier, we have found that additional model quality buys little additional task performance, and the routing problem is mostly solved with static model selection.

Figure 3: A full model sweep for one agent on Mercor Enterprise Platform. Several mid-tier models score within a few points of the most expensive option at a fraction of the cost per task. When the curve looks like this, the knee is easy to find and static selection is enough.

Other enterprise agents face workloads with much wider difficulty variance. A due diligence agent might draft a voice of customer summary based on several interviews or be asked to create an end to end diligence deck based on a comprehensive dataroom. A software engineering agent might make a one-line configuration fix in one task and debug a failing distributed deployment in another.

For these agents, any single fixed model is likely to be inefficient on part of the workload. A smaller model may be enough for the easy tasks, while a frontier model is still needed for the hardest ones.

The intuitive fix is query-classification routing, where each incoming request is scored for difficulty before being routed to the right model. That only works when the request contains enough information to predict how hard the task will actually be.

Often, it does not. The complexity of a task is not always visible in the query. "Fix the failing login flow" might be a one-line change or a three-hour investigation across logs, services and deployment state. Nothing in the query text distinguishes the two. A classifier that only sees the query is guessing about the part of the problem that actually determines difficulty. From our internal testing and benchmarking, model routing classifiers tend to over-fit to the tasks they were tuned on rather than capturing generalized judgement of what tasks are truly easy or difficult. When the classifier is wrong, cheap models are handed tasks they cannot finish, or expensive models are handed queries a weaker model could already fulfill. The result is lower accuracy and higher cost - the worst of both.

This is where dynamic delegation becomes useful. Instead of making the routing decision before the agent has context, the system moves the decision inside the agent. The main agent inspects the environment, breaks down the task, and decides what to hand off. It keeps the work that determines correctness, including the plan, the ambiguous calls, and the final review, while a cheaper model handles the token-heavy middle of the trajectory, such as exploration, test runs, and mechanical edits. Because that middle is where most of the tokens go, moving it to a smaller model can lower cost meaningfully while keeping quality largely intact.

Delegation is not free. It pays for reliability by running a frontier model as the orchestrator on every task, including the easy ones. That can be wasteful for very simple workloads, but when difficulty is uneven and hard to predict up front, delegation can win if the cost of misrouting hard tasks outweighs the orchestration overhead. That is an empirical question for the evaluation suite to answer.

The eval suite is the hard part

Everything above assumes the existence of an evaluation suite that faithfully represents the agent's real workload, but building that suite is harder than building the infrastructure around it.

Logging, tracing, and scoring harnesses are commodity capabilities at this point. What is not a commodity is knowing what to measure. A routing decision is only as good as the verifiers behind it, and those verifiers need deep company context. They need to know which tasks actually show up in production, how often they occur, which failures carry real business cost, which ones are cosmetic, what the environment looks like when the agent inspects it, and what a domain expert would consider acceptable for each task type.

None of that context lives in a dashboard. It lives with the people who do the work today. An eval suite built without them measures a workload that does not exist, and every routing decision optimized against it lands somewhere other than the real frontier. Teams that buy observability tooling and stop there end up with excellent visibility into the wrong questions.

Mercor Enterprise builds the evaluation layer behind these decisions. Our FDEs work with the customer’s domain experts to turn production context into a domain-specific eval suite, then use it to test model and harness changes against the same quality bar. The output is not a generic router, but is instead a measured cost-quality strategy that can adapt as the workload and model landscape change.
