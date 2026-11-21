---
title: "Incident Report: unsanctioned agent behaviour during cyber testing"
type: "raw-source"
url: "https://simonwillison.net/2026/Aug/5/incident-report/"
author: "Simon Willison"
publication: "Simon Willison’s Weblog"
published: "2026-08-05"
archived: "2026-11-21T11:00:45Z"
---

> [!quote] Original source
> **Author(s):** Simon Willison  
> **Title:** Incident Report: unsanctioned agent behaviour during cyber testing  
> **Published in:** Simon Willison’s Weblog  
> **Date:** 2026-08-05  
> **Original:** <https://simonwillison.net/2026/Aug/5/incident-report/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-incident-report-unsanctioned-agent-behaviour-during-cyber-testing|Source note]]
Themes: [[Agent security]]
Why it was archived: Fills the gap on autonomous-agent security incidents: real-world failure modes when agents run unsanctioned cyber tests.

## Archived text

5th August 2026 - Link Blog

Incident Report: unsanctioned agent behaviour during cyber testing. It happened again. This time it was the UK government's AI Security Institute who accidentally attacked other companies while running an evaluation with models with the safety filters turned off. From their technical paper (PDF):

During a cyber evaluation, from 25 to 28 July 2026, AI agents engaged in sustained, unsanctioned activity directed at what were, in practice, real people and organisations. These attempts were unsuccessful and, to the best of our knowledge, no real-world harm resulted. [...]

Across 122 evaluation attempts on two of AISI’s cyber challenges, AISI found 19 instances where AI agents took unsanctioned action on the live internet, including cases that targeted real people and organisations. [...]

It is uncertain to what extent the model recognised it was taking actions against real people. In the most serious case, an AI agent (Mythos 5) decided to attempt to solve the cyber challenge using a supply-chain attack. As a result, the AI agent created a GitHub account and then tried to convince an open-source repository maintainer to accept a malicious GitHub pull request (PR), including by creating a second account masquerading as another human user endorsing the PR. [...] Furthermore, in its attempt to solve the challenge, the agent decided to employ the technique of “spear-phishing” by sending targeted emails containing malicious content and attempting to manipulate recipients into accepting the code changes, and planned a prompt injection to compromise other coding agents.

The thing I found most surprising is that AISI were running these agents without any form of network sandboxing at all:

AISI provided the AI agents with internet access during these evaluations, which enabled their actions on the open internet in this setting. Internet access was a deliberate part of AISI’s evaluation configuration in this setting, and not due to sandbox escape.

This, combined with the fact that "AISI deliberately disables developer-implemented cyber-classifiers", makes the fact that the agents started attacking real-world targets entirely unsurprising to me.

Most of the reported incidents were claude Mythos 5, but "GPT-5.6 Sol without cyber classifiers" scored a few as well.

Here's "Sample 1" from the paper, in which the agent tries to execute a supply-chain attack by submitting a PR with a hidden prompt injection attack, then social engineering with a second agent pretending to have reviewed the code!

It's a fun paper. I recommend reading the whole thing.

Recent articles

- Running the full server-side Datasette Python app in the browser with service workers and Pyodide - 17th November 2026
- Locating the source of a mysterious beep with Claude - 9th November 2026
- Hide your slop PR descriptions behind  - 9th November 2026
- Qwen 3.8 27B on my laptop can interpret model weights, too - 3rd November 2026
