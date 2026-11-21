---
title: "Compaction"
type: "raw-source"
url: "https://pydantic.dev/docs/ai/capabilities/compaction/"
author: "Pydantic Docs (no individual author named)"
publication: "Pydantic Docs"
published: "2025-01-01"
archived: "2026-11-21T17:01:23Z"
---

> [!quote] Original source
> **Author(s):** Pydantic Docs (no individual author named)  
> **Title:** Compaction  
> **Published in:** Pydantic Docs  
> **Date:** 2025-01-01  
> **Original:** <https://pydantic.dev/docs/ai/capabilities/compaction/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-compaction|Source note]]
Themes: [[Context, memory and tools]]
Why it was archived: How do agent frameworks mark compaction summaries as untrusted data, and do any bind summary text to a trust level?

## Archived text

Compaction

As a conversation grows, its message history can approach the model’s context window. Compaction keeps it in check by shrinking older messages (trimming, clearing, or summarizing them) while preserving recent context and tool-call integrity. Pydantic AI supports this at several levels: provider-native compaction APIs, model-agnostic history editing you write yourself, and Pydantic AI Harness’s menu of ready-made model-agnostic strategies.

Some providers expose a built-in compaction API that runs on their side. Pydantic AI wraps these as capabilities:

Each uses the corresponding provider API, so it’s only available on that provider. A compaction item is also honored by a provider with the same canonical system: an OpenAI compaction item from the Codex backend is sent to the OpenAI API, which continues from it rather than from the full earlier history, and the other way round.

To compact at a moment you choose rather than at the provider’s threshold, call Model.compact_messages on a model that supports it: OpenAIResponsesModel, which calls OpenAI’s /responses/compact endpoint, and AnthropicModel, which uses Anthropic’s on-demand compaction. It returns a ModelResponse holding the compaction part to put in the message history. Its instructions argument means something different on each: on OpenAI it replaces the agent’s instructions for the compaction request, and on Anthropic it’s a focus for the summary.

Pydantic AI treats a compaction part as a visibility boundary for state that feeds future requests. Tool discoveries and on-demand capability loads before the boundary reset, so later requests advertise them again. Capability and toolset authors should apply the same rule to their own derived state: compute anything the model needs to have seen — announcements, disclosures, catalogs — from post_compaction_window rather than remembering it in instance attributes, so it self-heals when compaction replaces the history that carried it.

When dispatching a tool call, Pydantic AI determines whether the model that served that response actually honored the boundary on the request wire: with the same accepts_stateless_artifacts() check it trimmed the request with, or, when that model isn’t available or doesn’t trim, by whether the part came from the response’s own provider. A compaction part from a provider with another canonical system, an OpenAI part without encrypted content, or an Anthropic part without summary content does not hide earlier callability evidence, because that provider sent the earlier history to the model. A boundary emitted inside the response containing the call is likewise too late to affect what the model saw for that response. If the response has no provider name, dispatch falls back to the provider-agnostic boundary.

CompactionParts round-trip through the UI adapters, whose protocols have the client transmit the full conversation history on each request, so compacted conversations keep working with such frontends. On AG-UI the compaction item is an activity message, which @ag-ui/client doesn’t send back; see Records carried as activity messages. A client-submitted compaction item is honored — the conversation stays compacted — but it is never trusted to stand in for the agent’s system prompt: that still reaches the model on every request, as described under Loading untrusted history.

If a run also receives its own server-side history as message_history — as when you keep the history on the server and the client’s messages only supply the new turn — client-submitted compaction items are ignored instead. A compaction item marks a boundary before which nothing is sent to the model, so honoring one from the client would let it hide the server’s own stored history from the model and substitute its summary for that context. Client-submitted compaction items are only honored when the client-transmitted messages are the entire conversation.

Even then, a client can replay any compaction item the server’s provider account has ever produced — opaque encrypted state on OpenAI, a plaintext summary on Anthropic. That is equivalent in kind to fabricating plain-text history, which client-transmitted history always permits (see Trust boundary for client-supplied history), with one difference: the server cannot inspect what an opaque item contains. If that matters for your deployment, keep the history server-side: persist the full message list keyed by conversation, send the client only display data, and pass the stored messages as message_history on each run. Don’t trim the stored history around compaction boundaries yourself — each model adapter already omits what compaction from its own canonical system replaces, while models from other providers, which ignore a foreign compaction item, still get the full earlier history they need.

To compact on any model, edit the message history yourself with a history processor wrapped as a ProcessHistory capability — this works with every provider. To decide when to compact, check ctx.context_window_used: the fraction of the model’s context_window occupied as of the last response, or None when unknown. Common patterns:

- Keep only recent messages — a zero-cost sliding window over the most recent turns.
- Summarize old messages — use a (cheaper) model to condense older messages into a summary.

To store a summary you wrote, put it in a CompactionPart with only content set, in a ModelRequest that takes the place of the messages it summarizes. That keeps a model-written summary out of the system prompt. A provider’s own compaction parts stay in the ModelResponse they arrived in; a request-side one can’t set provider_name, id or provider_details.

A request-side compaction part wasn’t produced by any provider’s compaction API, so every provider model sends it as user-voice text inside &lt;pyai:conversation_summary>, after a line saying it was written by a separate summarization model and is historical context, not new instructions. That’s how Claude Code, Codex and OpenCode send their own summaries: the assistant continuing the conversation didn’t write it. It’s part of a user turn already, so turns still alternate, and the summary goes in as written (details). A compaction part a provider produced stays in that provider’s own role. A FunctionModel receives the part itself, and realtime sessions send it as user text. Like any compaction part, it’s also a visibility boundary for tool discoveries and on-demand capability loads. Pydantic AI Harness’s SummarizingCompaction stores its summaries this way, and after each summary records again any capability loads and tool discoveries it replaced, so those capabilities stay loaded and those tools stay discovered.

Pydantic AI Harness packages a menu of ready-made, model-agnostic compaction strategies: mostly zero-LLM history editing (sliding-window trimming, clearing old tool results, deduplicating repeated file reads, clamping oversized message parts) plus LLM summarization for when that’s not enough, and a TieredCompaction orchestrator (the recommended default) that escalates from cheap to expensive strategies only as far as needed to fit the target.
