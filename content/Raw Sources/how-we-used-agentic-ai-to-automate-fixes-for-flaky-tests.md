---
title: "How We Used Agentic AI to Automate Fixes for Flaky Tests"
type: "raw-source"
url: "https://konghq.com/blog/engineering/how-we-used-agentic-ai-to-fix-kong-gateways-flakiest-tests"
author: "Datong Sun"
publication: "Kong Inc."
published: "2026-06-10"
archived: "2026-11-21T16:01:19Z"
---

> [!quote] Original source
> **Author(s):** Datong Sun  
> **Title:** How We Used Agentic AI to Automate Fixes for Flaky Tests  
> **Published in:** Kong Inc.  
> **Date:** 2026-06-10  
> **Original:** <https://konghq.com/blog/engineering/how-we-used-agentic-ai-to-fix-kong-gateways-flakiest-tests>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-how-we-used-agentic-ai-to-automate-fixes-for-flaky-tests|Source note]]
Themes: [[Loop engineering]]
Why it was archived: How do self-verifying agents handle flaky tests and oracle rot in fast feedback loops?

## Archived text

# How We Used Agentic AI to Fix Kong Gateway's Flakiest Tests

Datong Sun

Each change to Kong Gateway's codebase triggers a comprehensive test suite that runs more than 17,000 * 2 = 34,000 test cases among the two primary architectures (x86 and ARM) we support. This process takes about 23.5 hours on a single machine. But we don't wait that long. A large fleet of machines runs the suite in parallel, and we shard the work aggressively so each commit finishes in a fraction of that time. That setup works well, right up until flaky tests get involved.

On the Kong engineering team, we've been exploring how an agentic AI workflow can make developing Kong Gateway more efficient. Fixing flaky tests turned out to be the ideal place to start.

## The problem

Quality is at the core of every product we build. To move fast without compromising on quality, we rely on an extensive set of test suites that tell us quickly whether a change has caused a regression. Those suites are large enough that a single full run takes about 23.5 hours with a single machine, which is why we spread the work across a large fleet of machines.

But as we ship more features, the suite keeps growing, and more flaky tests start showing up.

For the uninitiated, flaky tests are tests that fail sometimes but usually pass on a rerun. They're unavailable on large projects and a constant drain on engineers: after a flaky failure, you have to rerun the job, which costs both engineering time and machine time. Worse, as the flaky rate climbs, engineers trying to merge PRs start stepping on each other during reruns, creating a feedback loop that can consume the entire CI fleet’s capacity. Once that happens, queueing time spikes — sometimes engineers wait more than 30 minutes to an hour before a test even starts.

## Flaky tests are hard to fix

The obvious question is: **why not just ask engineers to fix the flaky tests?**

We did. It never worked well. And we realized there are two main reasons behind this:

- First,** the reason a test is flaky is not always obvious.** Finding it often takes a deep understanding of both the feature under test and its implementation. Even the test's original author usually can't spot the real cause — if they could, they wouldn't have written a flaky test in the first place.
- Second, even once an engineer identifies the cause, **fixing it properly takes extensive validation**. Because the failure is intermittent, running the fixed test once proves nothing. Engineers end up babysitting a PR for hours, rerunning it many times to confirm the flakiness is actually gone.

All of this makes fixing flaky tests an expensive investment. It often takes one experienced engineer a full day to fix two of them. It's also a battle we can't win outright. As we build more features, we have to keep pouring engineering time into keeping CI flakiness at an acceptable level, or risk blocking new development entirely and rendering CI unusable.

## Can we use AI to fix flaky tests?

By now you can probably see why flaky tests are expensive for any large engineering project, and expensive for humans to fix. When agentic coding went mainstream, this was one of the first use cases we considered for, because:

- Agents can scan far more of the codebase and logs than a human can, and quickly — a better shot at finding a flaky test's root cause.
- Agents can babysit the validation of a fix for hours without intervention, which humans are terrible at.

So we ran an experiment attempting to use Claude Code to fix the flaky tests in Kong Gateway.

## The identify-fix-verify loop

The first thing we needed was a way to identify which tests were flaky and how often they failed. Luckily, the team had already built a dashboard on top of Datadog's CI Visibility feature that gives us a clear picture of the flakiest tests and their failure rates.

We used that dashboard as the benchmark for our fixes, and used its list to seed the agents.

Here's the agentic workflow we settled on after a few rounds:

At the top level is the **fix-flakes** skill, the orchestrating agent, which runs on Opus. It takes a seed file — a flaky test's Datadog CSV export — and reads it to download all the CI logs from that test's recent failures. This step matters: failure logs usually contain vital clues about what's going wrong (as an example, a test failure after running for exactly 20 seconds could signal agents to look closely at timeout conditions), and they keep the agent grounded instead of guessing and hallucinating.

Once the failing test is identified and its logs are downloaded, **fix-flakes** spawns an Opus **flake-fixer** subagent to investigate and produce a fix. This is usually the most expensive step in token terms, but it generally runs in under 10 minutes — the **flake-fixer** often has to sift through multiple log files and dozens of source and test files to form a hypothesis and write a fix.

When **flake-fixer** is satisfied, it creates a branch, commits the fix, and pushes it to the repository. It then reports a summary of its theory and reports back to the orchestrator and exits.

The orchestrator then launches a **flake-verifier** subagent to check the fix. **flake-verifier** is a smaller Haiku agent, because each rerun produces more than one failure — there are other flaky tests in the suite — and the agent has to decide whether the test in question is fixed while filtering out the rest as noise. The CI output is scattered across many unstructured log files, and we found Haiku to be the easiest and most reliable way to judge whether a rerun succeeded. flake-verifier polls the run periodically until it can call success or failure, then reports back.

The orchestrator keeps spawning **flake-verifier** subagents to match the "rerun streak" configured when the skill is invoked. If no failure shows up across the full streak, **fix-flakes** open a PR for review. If a **flake-verifier** reports a recurrence at any point, the orchestrator downloads and combines the new failure logs with the previous **flake-fixer** summaries, spawns a fresh **flake-fixer**, and repeats — until the test is fixed and verified, or a maximum attempt count is reached, at which point it reports the failure.

Finally, the verified PR goes through normal human code review, same as any PR a person opens, and gets merged.

## The need to preserve context

Why design the loop this way? Mostly for context management. Keeping a model's context concise helps it hold attention, and it sharply reduces the cost of running a long agentic task like this.

**flake-fixer** is the most context-heavy agent in the system: it has to read through large log files and source code to build a solid theory of the flakiness. Carrying every previous fix along wouldn't help the next investigation much, but it would fill the context window fast. So we ask each **flake-fixer** to produce exactly one analysis and one fix, and to hand a summary back to the orchestrator — that way the next **flake-fixer** knows what's already been tried and can reach for new theories.

Subagents also let us use smaller, cheaper models like Haiku for steps that don't need heavy reasoning, like verifying a result, which cuts costs further.

With this workflow, one flaky test can generally be fixed and verified in 4–5 hours — most of that spent in the verification loop, since CI itself takes a while — using an average of 100–200k tokens start to finish. The process is highly automated and needs no human intervention while the agents run. Fixing several tests at once is just a matter of running multiple instances of Claude Code with different seed files, all running concurrently and not interfering with each other.

## How well does this work?

Over a week and a half, we ran this harness against the **15** flakiest tests on our dashboard. It fixed **12** of them and gave up on **3**. That result is striking, given the same work would often take an experienced engineer multiple weeks, often with less success.

It also did something we didn't ask for: while investigating the failures, the workflow surfaced two genuine bugs in our codebase.

**The **`**conf_loader**`** sorting bug**

One test compares the output of our `conf_loader `against an expected table, and it had been failing at random for years. Engineers had tried to fix it before, but it never stayed fixed. The failure looked like this (trimmed for length):

Rather than just reorder the output, the harness investigated the codebase and the `conf_loader` source and realized the loader wasn't sorting duplicate directives by their value. Combined with the nondeterministic ordering of hash-table enumeration, that left the ordering of duplicate `lua_shared_dict` directives unstable. The fix it produced:

Our reviewer agreed this was the root cause, and our monitoring dashboard confirmed it: after the change, this five-year-old flaky test never recurred. All of it came out of the agentic loop — no human ever gave Claude any guidance.

### The concurrent auth race condition

The workflow turned up another genuine bug — two, actually. The test in question spawns 10 clients that hit our Admin auth endpoint at once. Occasionally, one of the requests fails, returning no session when it should.

Claude first suspected our `cluster_mutex` module, and it did find a small bug there: the mutex didn't return quickly when it was already held by a local request. But that fix did **not** pass the verification streak, so **flake-fixer** was spawned again to dig deeper. This time it identified a subtle data race in the session plugin the test relies on, and produced a fix that, once merged, made the flakiness disappear entirely.

In both cases, the agent fixed the flaky test without touching the test files at all. Through log and code analysis, it concluded the tests were written correctly, and the problems lay elsewhere. That's something humans tend to miss — we assume flakiness comes from "bad tests" and stop investigating the code path under test.

The whole Gateway team is feeling the difference. For the first time, CI stability is improving fast enough to be obvious. Merging a PR has gotten noticeably easier because far fewer reruns are needed — which saves a lot of engineering time and meaningfully cuts both the utilization and the queueing of our CI fleet.

## Lessons learned

**Try it on your flaky tests.** If you're still unsure whether agentic coding is a good idea, point it at your flaky test suite and see for yourself. You can't really make things worse — however badly it goes, it won't touch the product. It's about as risk-free as an experiment gets.

**Build a good feedback loop for your agent.** The only reason our flake fixer worked so well is that we told it exactly how to gather failure logs, understand the code path, and run verifications. Without those steps, even the most advanced model will hallucinate — convinced it fixed the issue while the test stays flaky. Agents are smart and will do their best with what you give them. What they're not good at is asking for the things you should be providing but aren't. That, more than anything, is why our flake fixer is effective enough to surface bugs nobody had noticed.

**Help the agent keep its context small.** When there's no reason to carry full context between tasks — like between **flake-fixer** spawns — start fresh and pass along only what the next step needs. It saves substantial time and tokens, and it lets the agent focus on the new investigation and produce a better analysis and fix.

**Use the right agent for the job.** Advanced reasoning models like Opus are worth it for complex code and flakiness analysis; for verification, a smaller model like Haiku does the job just as well.

**Don't over-engineer your harness.** It's tempting to invest heavily up front — a comprehensive harness, a library of polished, general-purpose scripts and skills meant to cover every scenario the agent might encounter. We found the opposite works better. Let the agent write throwaway scripts and one-off tools for the task in front of it; the models are more than capable of building the right thing on the spot, and a tool shaped for one specific job usually beats a generic one trying to handle them all. It also lifts the success rate — an agent running a script it just wrote for a particular task at hand results in far less troubleshooting than one trying to understand and run a general-purpose script built ahead of time, and often results in less token usage overall. Spend your effort where it actually pays off: on the methodology for identifying and verifying flaky tests, and on where to get the data that backs those decisions. That's a far better investment than prescribing the exact script an agent must use to achieve a certain task like rerunning a workflow or parsing the job output.

Overall, we've been pleasantly surprised by this experiment, and it already became part of our development workflow. It has meaningfully improved our productivity and our confidence in the test suite, and also significantly cut our engineering and CI costs.

kongctl was built with the modern development stack in mind. Developers working in a terminal want the ability to query systems quickly to verify state, behaviors, and capabilities. Coding harnesses need well defined tools and accurate schemas for

Rick Spurgeon

# Local Previews and Agent-Driven Authoring for Your Konnect Dev Portal

What it is

The Konnect Dev Portal Toolkit is a free extension published by Kong Inc. on the Visual Studio Code Marketplace (ID konghq.vscode-konnect-dev-portal-toolkit) and on Open VSX.

Konnect Developer Portals are how teams publish API document

Adam DeHaven

# What is an AI Registry? Governing Discovery for AI Agents and MCP Servers

AI agents need access to everything. That doesn't mean they should get it. Introducing Kong AI Registry: Governed discovery for enterprise AI models, MCP servers, and agents.

Most AI agents today operate with a predefined set of connections. Devel

Alex Drag

# How to Test Gateway APIs Directly from Kong Konnect with Insomnia

What You'll Build

To explore the new integration, I'll build a realistic API platform workflow using Konnect, Kong Gateway, and Insomnia.

By the end of this tutorial, I'll have:

A Konnect Control Plane (KongAir Dev)

A local Kong Gateway Data Pl

Juhi Singh

# Agentic AI Governance: The Complete Guide to Frameworks and Controls

Agentic AI governance is the structured management of the authority an organization hands to autonomous AI systems that plan and take action on its behalf. It covers what an AI agent is allowed to do, which systems it can touch, and how those permis

Standing up a production agent means taking it through six stages: React : the agent must be able to react to events as they occur internal or external to the business Discover : Once running, can the agent find what it needs? This means MCP Servers

Alex Drag

# Introducing Kong AI Registry: Self-Service Discovery for Agents

API management solved a similar problem for developers. Instead of asking a platform team every time they needed an API, developers could go to a Developer Portal, discover what was available to them, and start building — within the governance bound

Alex Drag

# kongctl 1.0: A Declarative, AI-Native CLI for Kong Konnect

kongctl was built with the modern development stack in mind. Developers working in a terminal want the ability to query systems quickly to verify state, behaviors, and capabilities. Coding harnesses need well defined tools and accurate schemas for

Rick Spurgeon

# Local Previews and Agent-Driven Authoring for Your Konnect Dev Portal

What it is

The Konnect Dev Portal Toolkit is a free extension published by Kong Inc. on the Visual Studio Code Marketplace (ID konghq.vscode-konnect-dev-portal-toolkit) and on Open VSX.

Konnect Developer Portals are how teams publish API document

Adam DeHaven

# What is an AI Registry? Governing Discovery for AI Agents and MCP Servers

AI agents need access to everything. That doesn't mean they should get it. Introducing Kong AI Registry: Governed discovery for enterprise AI models, MCP servers, and agents.

Most AI agents today operate with a predefined set of connections. Devel

Alex Drag

# How to Test Gateway APIs Directly from Kong Konnect with Insomnia

What You'll Build

To explore the new integration, I'll build a realistic API platform workflow using Konnect, Kong Gateway, and Insomnia.

By the end of this tutorial, I'll have:

A Konnect Control Plane (KongAir Dev)

A local Kong Gateway Data Pl

Juhi Singh

# Agentic AI Governance: The Complete Guide to Frameworks and Controls

Agentic AI governance is the structured management of the authority an organization hands to autonomous AI systems that plan and take action on its behalf. It covers what an AI agent is allowed to do, which systems it can touch, and how those permis

Standing up a production agent means taking it through six stages: React : the agent must be able to react to events as they occur internal or external to the business Discover : Once running, can the agent find what it needs? This means MCP Servers

Alex Drag

# Introducing Kong AI Registry: Self-Service Discovery for Agents

API management solved a similar problem for developers. Instead of asking a platform team every time they needed an API, developers could go to a Developer Portal, discover what was available to them, and start building — within the governance bound

Alex Drag

# kongctl 1.0: A Declarative, AI-Native CLI for Kong Konnect

kongctl was built with the modern development stack in mind. Developers working in a terminal want the ability to query systems quickly to verify state, behaviors, and capabilities. Coding harnesses need well defined tools and accurate schemas for

Rick Spurgeon

# Local Previews and Agent-Driven Authoring for Your Konnect Dev Portal

What it is

The Konnect Dev Portal Toolkit is a free extension published by Kong Inc. on the Visual Studio Code Marketplace (ID konghq.vscode-konnect-dev-portal-toolkit) and on Open VSX.

Konnect Developer Portals are how teams publish API document

Adam DeHaven

# What is an AI Registry? Governing Discovery for AI Agents and MCP Servers

AI agents need access to everything. That doesn't mean they should get it. Introducing Kong AI Registry: Governed discovery for enterprise AI models, MCP servers, and agents.

Most AI agents today operate with a predefined set of connections. Devel

Alex Drag

# How to Test Gateway APIs Directly from Kong Konnect with Insomnia

What You'll Build

To explore the new integration, I'll build a realistic API platform workflow using Konnect, Kong Gateway, and Insomnia.

By the end of this tutorial, I'll have:

A Konnect Control Plane (KongAir Dev)

A local Kong Gateway Data Pl

Juhi Singh

# Agentic AI Governance: The Complete Guide to Frameworks and Controls

Agentic AI governance is the structured management of the authority an organization hands to autonomous AI systems that plan and take action on its behalf. It covers what an AI agent is allowed to do, which systems it can touch, and how those permis

Standing up a production agent means taking it through six stages: React : the agent must be able to react to events as they occur internal or external to the business Discover : Once running, can the agent find what it needs? This means MCP Servers

Alex Drag

# Introducing Kong AI Registry: Self-Service Discovery for Agents

API management solved a similar problem for developers. Instead of asking a platform team every time they needed an API, developers could go to a Developer Portal, discover what was available to them, and start building — within the governance bound

Alex Drag

## Ready to see Kong in action?

Get a personalized walkthrough of Kong's platform tailored to your architecture, use cases, and scale requirements.
