---
type: "evergreen"
title: "Token efficiency comes from removing avoidable work, not from smaller context windows"
created_at: "2026-11-25T13:02:20Z"
updated_at: "2026-11-25T13:02:20Z"
inputs: ["notes-on-improving-token-efficiency-in-github-agentic-workflows", "agentic-workflows-trade-latency-and-cost-for-performance"]
provenance_urls: ["https://github.blog/ai-and-ml/github-copilot/improving-token-efficiency-in-github-agentic-workflows/", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do teams manage the fluctuating token cost burden of agentic workflows once the human costs stay fixed?"]
---
Agent synthesis

Token efficiency comes from removing avoidable work, not from fitting more into a small window. GitHub's Agentic Workflows team instrumented hundreds of production workflows and found that a run spending many turns on deterministic data-gathering (fetching issue metadata, scanning labels, reading diffs) burns LLM turns for work a shell command can do. Migrating that work into pre-agentic CLI setup steps, and pruning MCP registrations the agent never calls, removed that spend from the reasoning loop entirely.

The mechanism has three parts. First, measure: a proxy captures token usage into normalized records so runs are comparable and anomalies surface (a workflow that normally takes four LLM turns taking eighteen). Second, act: a daily auditor flags runs and a daily optimizer proposes fixes, and both are themselves agentic workflows whose own usage appears in the daily reports. Third, normalize: an Effective Tokens metric applies model multipliers (Haiku 0.25x, Sonnet 1.0x, Opus 5.0x) with output tokens at 4x weight and cache-reads at 0.1x, so a 10% ET reduction means a genuine 10% cost reduction across tiers.

Raw token counts mislead. On a live repository, workload drift masquerades as efficiency: the Contribution Check workflow looked worse on tokens while per-turn efficiency improved, because the same runs now handled bigger diffs (9% small pull requests in the post period versus 41% pre). Tracking LLM call counts alongside token counts, and run frequency alongside per-run cost, separates the signal (constant turns-per-run with falling tokens-per-call is genuine improvement) from the workload change. The trade-latency-and-cost note holds: agentic workflows buy latency and tokens for performance, and this post shows the cost side is also manageable, by turning avoidable work into deterministic pre-steps and measuring the residue with ET rather than raw counts. Run frequency compounds: the 62% reduction at Auto-Triage Issues (6.8 runs per day) saved roughly 7.8M ET in aggregate.

The soft spot is quality. Process signals (output tokens per call, turn counts per run, tool-call completion) stay stable while token consumption falls, but nothing observes whether output quality actually held, and there is no agentic-workflow benchmark for ground-truth correctness. Episode-level lineage and portfolio-level dedup of reads are the next lever. The cheapest LLM call is the one you do not make. Start with proxy-level logging in day one, prune the toolset to what the agent actually calls, move deterministic data-gathering out of the reasoning loop, and gate optimizations on ET with call-count normalization, not token counts alone. (see: agentic spend is engineered, not priced by the token)

## Where it comes from

- [[notes-on-improving-token-efficiency-in-github-agentic-workflows|Improving token efficiency in GitHub Agentic Workflows]]

## What this builds on

- [[agentic-workflows-trade-latency-and-cost-for-performance|Agentic workflows trade latency and cost for performance]]
