---
type: "source-note"
title: "Notes on: Introducing advanced tool use for Claude"
raw: "introducing-advanced-tool-use-for-claude"
url: "https://www.anthropic.com/research/advanced-tool-use"
created_at: "2026-11-26T15:01:29Z"
updated_at: "2026-11-26T15:01:29Z"
---
- Archived full text: [[introducing-advanced-tool-use-for-claude|Full archived text, with credits]]
- Link: <https://www.anthropic.com/research/advanced-tool-use>

## What it says

Anthropic describes three features that let agents work with hundreds or thousands of tools: the Tool Search Tool (on-demand discovery of tool definitions, with defer_loading), Programmatic Tool Calling (orchestration through code instead of natural-language round-trips), and Tool Use Examples (sample calls that show usage patterns JSON schemas cannot express). The post reports that tool definitions can consume 50,000+ to 134,000 tokens before an agent reads a request, that Tool Search Tool cuts token usage by 85% while improving MCP evaluation accuracy (Opus 4: 49% to 74%; Opus 4.5: 79.5% to 88.1%), and that Programmatic Tool Calling cuts average token use 37% (43,588 to 27,297) while improving internal knowledge retrieval and GIA benchmarks by a few points. Tool Use Examples improve accuracy from 72% to 90% on complex parameter handling.

## Claims drawn from this source

- **Tool definitions can consume 50K+ tokens and reach 134K before any work begins.** A five-server MCP setup with GitHub (35 tools, ~26K tokens), Slack (11 tools, ~21K), Sentry (~3K), Grafana (~3K), and Splunk (~2K) totals 58 tools using approximately 55K tokens, and at Anthropic, tool definitions have been seen consuming 134K tokens before optimization.
- **Tool Search Tool cuts token usage by 85% and improves MCP accuracy.** With defer_loading, only the Tool Search Tool itself (~500 tokens) and a few critical tools load upfront; total context consumption drops from ~77K tokens to ~8.7K tokens, preserving 95% of the context window. Internal testing showed Opus 4 improving from 49% to 74% and Opus 4.5 from 79.5% to 88.1% with Tool Search Tool enabled.
- **Deferred tools do not break prompt caching.** Because deferred tools are excluded from the initial prompt entirely and only added after Claude searches, the system prompt and core tool definitions remain cacheable.
- **Most tool-use failures are wrong selection and incorrect parameters, not schema validity.** The most common failures are wrong tool selection and incorrect parameters, especially when tools have similar names like notification-send-user vs. notification-send-channel.
- **Programmatic Tool Calling keeps intermediate results out of context and cuts tokens 37%.** Claude writes Python orchestration code and a sandboxed Code Execution tool processes results, so only the final output enters context. Average usage dropped from 43,588 to 27,297 tokens on complex research tasks, and internal knowledge retrieval improved from 25.6% to 28.5% while GIA benchmarks improved from 46.5% to 51.2%.
- **Tool Use Examples fix parameter accuracy that JSON schemas cannot express.** Schemas define structure but not conventions: date formats like YYYY-MM-DD vs 2024-11-06T00:00:00Z, ID conventions, nested structure usage, and parameter correlations. Internal testing showed tool use examples improved accuracy from 72% to 90% on complex parameter handling.
- **Layer features by bottleneck rather than all at once.** Start with the biggest constraint: context bloat from definitions goes to Tool Search Tool, large intermediate results to Programmatic Tool Calling, and parameter errors to Tool Use Examples.
