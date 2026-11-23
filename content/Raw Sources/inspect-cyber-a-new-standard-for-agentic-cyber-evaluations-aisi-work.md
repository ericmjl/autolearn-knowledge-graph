---
title: "Inspect Cyber: A New Standard for Agentic Cyber Evaluations | AISI Work"
type: "raw-source"
url: "https://www.aisi.gov.uk/blog/inspect-cyber"
author: "AI Security Institute (no individual author named)"
publication: "AI Security Institute"
published: "2025-06-26"
archived: "2026-11-23T23:01:05Z"
---

> [!quote] Original source
> **Author(s):** AI Security Institute (no individual author named)  
> **Title:** Inspect Cyber: A New Standard for Agentic Cyber Evaluations | AISI Work  
> **Published in:** AI Security Institute  
> **Date:** 2025-06-26  
> **Original:** <https://www.aisi.gov.uk/blog/inspect-cyber>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-inspect-cyber-a-new-standard-for-agentic-cyber-evaluations-aisi-work|Source note]]
Themes: [[Evals and agent quality]], [[Agent security]]
Why it was archived: What do sandboxed cyber eval designs look like in practice, and how does the grader distinguish a contained attack from a live one?

## Archived text

AI systems are growing more powerful in the cyber domain. This means they can increasingly be used to defend against cyber threats – but can also be exploited to create them. As capabilities advance, there is an escalating need for more rigorous, realistic, and reproducible evaluations.

The current process for building these cyber evaluations, however, is inefficient, with teams often rewriting extensive setup code each time they design a new benchmark. These inefficiencies slow the pace of research, hinder collaboration, and complicate reliability. Today, we’re releasing Inspect Cyber to standardise and streamline the process of creating and running agentic cyber evaluations – tasks that assess AI agents' abilities to autonomously complete cybersecurity objectives across diverse environments.

Where Current Practices Fall Short

The existing process for creating and running agentic cyber evaluations is needlessly complex. Every new evaluation or benchmark requires the same repetitive setup, including creating sandboxed infrastructure, connecting agents to models, and developing run scripts. The lack of standardisation causes several critical issues:

- Development time balloons as creators write setup code rather than focus on the core component of their evaluations – the environments in which the agent is placed
- Collaboration suffers due to differences in implementation making it hard for teams to share, understand, and build upon each other’s work
- Reliability diminishes because experimental results are hard to reproduce and verify

Inspect Cyber: A Standardised Solution

We’ve developed Inspect Cyber to address these inefficiencies. Built on our robust Inspect evaluation platform, Inspect Cyber provides an intuitive, standardised framework for creating and running agentic cyber evaluations. This allows developers to work faster, focus on the most important aspects of their evaluations, and collaborate more effectively. In a nutshell, the open-source Python package:

- Provides a clear, consistent process for creating agentic cyber evaluations using just two configuration files – one for the evaluation and another for its required infrastructure
- Empowers researchers to easily produce multiple variants of an evaluation, such as with different agent prompts or affordances
- Promotes AI evaluation best practices, such as verifying solvability
- Enhances legibility through a recommended project structure

Additionally, since Inspect Cyber is built on top of Inspect, it inherits all of Inspect's powerful functionalities, including support for easily running evaluations on diverse models using custom agents, scoring mechanisms, sandbox environments, and policies for human oversight or baselining.

Join Our Community

We have been using Inspect Cyber internally for several months across a spectrum of evaluation scenarios, from foundational Capture the Flag challenges to increasingly sophisticated cyber ranges simulating Active Directory services, enterprise networks, and critical national infrastructure. It has proven remarkably straightforward, robust, and powerful.

However, we appreciate that Inspect Cyber may not yet adequately serve all user workflows. By open sourcing the package, we invite feedback and contributions from the community. Our goal is to continue lowering the barriers to creating agentic cyber evaluations, enabling researchers to more seamlessly bring their evaluation ideas to life.

Getting Started

We recommend beginning by reviewing the package’s documentation. There you will also find examples demonstrating how to use Inspect Cyber to build Capture the Flag and cyber range evaluations.

We encourage you to share your ideas and contributions through the GitHub repository. If Inspect Cyber doesn’t fit your workflow or if you have ideas for new features, please open an issue or submit a pull request.

Together, we can develop the cyber evaluations our field needs to keep pace with rapidly advancing AI systems. We're excited to see what you build!
