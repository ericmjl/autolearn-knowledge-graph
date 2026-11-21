---
type: "evergreen"
title: "Workflows encode fixed paths; agents need declarative criteria"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-building-effective-agents-anthropic", "notes-on-karpathy-on-coding-with-claude-and-leverage-x-post"]
provenance_urls: ["https://blog.anthropic.com/building-effective-agents", "https://x.com/karpathy/status/2015883857489522876"]
refutation_status: "untested"
---

# Workflows encode fixed paths; agents need declarative criteria

Agent synthesis

Workflows encode predefined code paths, while agents leverage declarative success criteria rather than imperative instructions. In the Anthropic post "Building effective agents," workflows are defined as LLMs orchestrated through predefined code paths, whereas agents let LLMs dynamically direct their own processes and tool use in a feedback loop. Karpathy's X post "Karpathy on coding with Claude and leverage" supplies the complementary half: leverage comes from giving agents goals and success criteria—write tests first, use a browser MCP, write a naive correct algorithm then optimize it—rather than imperative instructions. The mechanism is a shift in what is specified: a workflow fixes the sequence of steps in code, while an agent is handed a target and is left to choose how to reach it, with the human supplying criteria and guardrails rather than a script. The evidence is split across the two sources: Anthropic draws the architectural line between predefined paths and dynamic control, and Karpathy shows what that dynamic control requires in practice—declarative criteria, close supervision, and sandboxed or verified feedback rather than step-by-step commands. Together they show that the workflow/agent distinction is not only architectural but also a change in the developer's job: from encoding paths to specifying outcomes, with the agent's freedom bounded by criteria, tests, and review rather than by fixed instructions.

## Where it comes from

- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]
- [[notes-on-karpathy-on-coding-with-claude-and-leverage-x-post|Karpathy on coding with Claude and leverage (X post)]]

## What this builds on

- None yet.
