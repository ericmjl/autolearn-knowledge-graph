---
type: "source-note"
title: "Notes on: Compaction"
raw: "compaction"
url: "https://pydantic.dev/docs/ai/capabilities/compaction/"
created_at: "2026-11-21T17:02:18Z"
updated_at: "2026-11-21T17:02:18Z"
---
- Archived full text: [[compaction|Full archived text, with credits]]
- Link: <https://pydantic.dev/docs/ai/capabilities/compaction/>

## What it says

Pydantic AI documents compaction, the step that keeps a long conversation's history inside the model's context window by trimming, clearing, or summarizing older messages while preserving recent context and tool-call integrity. It separates provider-native compaction APIs (OpenAI /responses/compact, Anthropic on-demand) from model-agnostic history editing, and specifies how a model-written summary is transmitted: as user-voice text inside a <pyai:conversation_summary> block, preceded by a line saying it was written by a separate summarization model and is historical context, not new instructions. Client-submitted compaction items are honored to keep the conversation compacted, but never trusted to stand in for the agent's system prompt, and are ignored entirely when the run also receives its own server-side history, so a client cannot hide stored history and substitute its own summary.

## Claims drawn from this source

- **Compaction keeps history inside the context window.** Compaction shrinks older messages (trimming, clearing, or summarizing them) while preserving recent context and tool-call integrity.
- **Provider-native compaction APIs are exposed as capabilities.** OpenAIResponsesModel calls OpenAI's /responses/compact endpoint, and AnthropicModel uses Anthropic's on-demand compaction; each returns a ModelResponse holding the compaction part.
- **Request-side summaries are sent as untrusted user-voice text.** A request-side compaction part was not produced by any provider's compaction API, so every provider model sends it as user-voice text inside <pyai:conversation_summary>, after a line saying it was written by a separate summarization model and is historical context, not new instructions.
- **Compaction parts act as a visibility boundary.** Tool discoveries and on-demand capability loads before the boundary reset, so later requests advertise them again; capability and toolset authors should recompute from post_compaction_window rather than remembering derived state in instance attributes.
- **Client-submitted compaction items are never trusted as system prompt.** A client-submitted compaction item is honored so the conversation stays compacted, but it is never trusted to stand in for the agent's system prompt, which still reaches the model on every request.
- **Client-submitted items are ignored when server-side history is present.** If a run also receives its own server-side history as message_history, client-submitted compaction items are ignored instead, because a compaction item marks a boundary before which nothing is sent to the model, and honoring one would let a client hide the server's own stored history and substitute its summary.
- **Opaque compaction state is uninspectable and replayable.** A client can replay any compaction item the server's provider account has ever produced, opaque encrypted state on OpenAI or a plaintext summary on Anthropic, with the difference that the server cannot inspect what an opaque item contains.
- **Harness offers cheap-to-expensive compaction strategies.** Pydantic AI Harness packages mostly zero-LLM strategies (sliding-window trimming, clearing old tool results, deduplicating repeated file reads, clamping oversized message parts) plus LLM summarization, with a TieredCompaction orchestrator that escalates only as far as needed to fit the target.
