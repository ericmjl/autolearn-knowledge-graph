---
type: "source-note"
title: "Notes on: Context engineering: memory, compaction, and tool clearing | Claude Cookbook"
raw: "context-engineering-memory-compaction-and-tool-clearing-claude-cookbook"
url: "https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools"
created_at: "2026-11-25T08:03:54Z"
updated_at: "2026-11-25T08:03:54Z"
---
- Archived full text: [[context-engineering-memory-compaction-and-tool-clearing-claude-cookbook|Full archived text, with credits]]
- Link: <https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools>

## What it says

The Claude cookbook argues that long-running agents fail two ways: a 200K window hard-stops mid-task, and a 1M window keeps running while context rot and prefill latency degrade recall. It presents three first-party primitives that target different slices of the problem: compaction (a whole-transcript operation that distills the conversation into a summary), tool-result clearing (a sub-transcript operation that drops old, re-fetchable tool results while keeping the record the call happened), and a memory tool (structured note-taking into persistent storage that survives across sessions). The primitives compose rather than compete; the right choice is driven by which part of the context problem the workload actually has, and lossiness runs a spectrum from lossless (clearing, memory on what is saved) to lossy (compaction).

## Claims drawn from this source

- **Context rot degrades recall before the window fills.** Needle-in-a-haystack studies show that as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases, across all models.
- **A 1M window does not save an unmanaged trajectory.** On a 1M window the research agent completed with peak context 335,279 tokens (96.3% file-read results) but sat on stale content, while on a 200K window the same run stopped after 3 turns at 168,242 tokens.
- **Compaction is a whole-transcript operation with prompt-dependent fidelity.** Compaction distills user messages, assistant messages, tool calls, and tool results into a summary (e.g. a ~2,783-token summary replacing prior turns); a probe kept 3/3 high-level facts but dropped 3/3 obscure specifics, and custom instructions replace the default summarization prompt entirely.
- **Clearing is a sub-transcript edit that is lossless but requires re-fetching.** Clearing surgically replaces old tool_result blocks with a placeholder while keeping the tool_use record; in the cookbook's run, 4 clearing events freed ~163K tokens each and the peak stayed at 173,137, with 7 of 8 file reads gone from context.
- **Memory moves information out of the window across sessions.** Session 2 with memory read 4 file reads at peak ctx 172,623 versus 8 reads at 333,977 without memory; memory is just-in-time retrieval in practice and solves cross-session persistence that clearing and compaction cannot.
- **The three primitives compose, and layering needs config.** With all three active the agent peaked at 169,938 tokens (vs 335,279 baseline) with a final context of 13,749; clearing excludes the memory tool via exclude_tools ["memory"] so saved files are not cleared.
- **Lossiness runs a spectrum, not a binary.** Clearing is lossless as long as the tool is re-callable; compaction is lossy and controlled by the summarization prompt; memory is lossless on what the agent saves but is only as good as the agent's judgment about what to save.
- **Each workload has its own primitive, not 'use all three'.** Skip memory for fresh-session chatbots, skip compaction when sessions stay under the limit, skip clearing when the agent needs to compare past tool results in full; the diagnostic question is which part of the context problem the workload actually has.
