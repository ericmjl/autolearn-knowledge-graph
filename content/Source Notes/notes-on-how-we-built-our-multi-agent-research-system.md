---
type: "source-note"
title: "Notes on: How we built our multi-agent research system"
raw: "how-we-built-our-multi-agent-research-system"
url: "https://www.anthropic.com/research/multi-agent-research-system"
created_at: "2026-11-21T14:01:56Z"
updated_at: "2026-11-21T14:01:56Z"
---
- Archived full text: [[how-we-built-our-multi-agent-research-system|Full archived text, with credits]]
- Link: <https://www.anthropic.com/research/multi-agent-research-system>

## What it says

Anthropic describes building Research: a lead orchestrator spawns parallel subagents that act as intelligent filters over their own context windows, returning condensed findings. They report multi-agent gains (90.2% over single-agent Opus 4 on an internal eval), 4x/15x token overheads, failure modes in early versions (over-spawning, over-verbose queries), prompt-engineering heuristics, production tracing and high-level observability, stateful-error handling, rainbow deployments, and an appendix on filesystem-backed subagent outputs, end-state evaluation, and long-horizon context management.

## Claims drawn from this source

- **Orchestrator-worker pattern with parallel subagents beats single-agent performance.** A multi-agent system with Claude Opus 4 as lead and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on Anthropic's internal research eval, decomposing breadth-first queries into subtasks.
- **Token usage explains 80% of performance variance on BrowseComp.** Of three factors explaining 95% of variance in the BrowseComp evaluation, token usage by itself explains 80%, with number of tool calls and model choice the other two. Multi-agent systems buy additional capacity for parallel reasoning by giving each subagent its own context window.
- **Multi-agent systems burn tokens fast (~15x chat).** Agents typically use about 4x more tokens than chat interactions and multi-agent systems about 15x more, so multi-agent use is economically viable only for high-value tasks.
- **Tracing plus high-level observability beats raw conversation logging.** Full production tracing diagnosed why agents failed (bad search queries, poor sources, tool failures). Beyond standard observability, the team monitors agent decision patterns and interaction structures without monitoring individual conversation contents to maintain user privacy.
- **Filesystem-backed subagent outputs minimize the game of telephone.** Subagents call tools to store work in external systems and pass lightweight references back to the coordinator, preventing information loss during multi-stage processing and reducing token overhead from copying large outputs through conversation history.
- **Errors compound in long-running agents.** Agents maintain state across many tool calls and minor failures can be catastrophic; Anthropic combines graceful adaptation (telling the agent a tool is failing) with deterministic safeguards like retry logic, regular checkpoints, and resume-from-error instead of restarts.
- **Small evals first, then LLM-as-judge and human review.** Starting with ~20 real-usage queries caught dramatic early effects (30% to 80% prompt-tweak gains); an LLM judge with a rubric (factual accuracy, citation accuracy, completeness, source quality, tool efficiency) scaled to hundreds of outputs, and human testers still caught edge cases like SEO content-farm bias.
