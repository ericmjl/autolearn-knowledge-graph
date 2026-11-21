---
type: "source-note"
title: "Notes on: Effective context engineering for AI agents"
raw: "effective-context-engineering-for-ai-agents"
url: "https://www.anthropic.com/research/effective-context-engineering-for-ai-agents"
created_at: "2026-11-21T18:02:08Z"
updated_at: "2026-11-21T18:02:08Z"
---
- Archived full text: [[effective-context-engineering-for-ai-agents|Full archived text, with credits]]
- Link: <https://www.anthropic.com/research/effective-context-engineering-for-ai-agents>

## What it says

Anthropic argues that context engineering, the curation of the token set an LLM sees at inference, is the natural progression of prompt engineering for long-running agents. Context rot and a finite attention budget make it a finite resource; effective agents use the smallest set of high-signal tokens. For runtime retrieval, agents should keep lightweight identifiers and load data just-in-time, using hierarchy, names, and sizes as signals. For long-horizon tasks, agents use compaction, structured note-taking, and multi-agent architectures instead of relying on a bigger window.

## Claims drawn from this source

- **Context engineering is the progression of prompt engineering.** Context engineering is the set of strategies for curating and maintaining the optimal set of tokens during LLM inference, including everything outside the prompt: system instructions, tools, MCP, external data, and message history.
- **Context rot shrinks recall as tokens grow.** Needle-in-a-haystack studies show that as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases, across all models, though some degrade more gently.
- **Every token depletes a finite attention budget.** LLMs draw on an attention budget when parsing context; every new token introduced depletes it, creating diminishing marginal returns for context size.
- **System prompts should sit at a Goldilocks altitude.** Prompts hardcoded with brittle if-then logic fail, and vague high-level guidance fails too; the sweet spot is specific enough to guide behavior yet flexible enough to give strong heuristics.
- **Tools should be minimal, self-contained, and token-efficient.** Bloated tool sets covering too much functionality or forcing ambiguous tool choice fail; if a human engineer cannot say which tool fits a situation, an agent cannot either.
- **Diverse canonical examples beat edge-case lists.** Teams often stuff a laundry list of edge cases into a prompt; Anthropic recommends curating diverse, canonical examples instead, because examples are the pictures worth a thousand words.
- **Just-in-time retrieval beats pre-loading everything.** Agents should maintain lightweight identifiers (file paths, stored queries, web links) and dynamically load data at runtime with tools, mirroring human cognition of not memorizing a corpus.
- **Metadata is a behavior-shaping signal.** Folder hierarchies, naming conventions, timestamps, and file sizes help agents understand how and when to use information: a file named test_utils.py in tests/ implies a different purpose than the same name in src/core_logic/.
- **Progressive disclosure and layer-by-layer understanding.** Each interaction yields context that informs the next decision; agents assemble understanding layer by layer while keeping only what is necessary in working memory.
- **The hybrid strategy: load some up front, explore just-in-time.** Claude Code drops CLAUDE.md into context up front while glob and grep allow just-in-time retrieval, bypassing stale indexing and complex syntax trees; runtime exploration is slower than pre-computed retrieval.
- **Long-horizon coherence comes from compaction, note-taking, and sub-agents.** For tasks exceeding the window, Anthropic enumerates compaction (summarize and reinitiate), structured note-taking (persistent notes pulled back in later), and multi-agent architectures (sub-agents explore with tens of thousands of tokens and return 1,000-2,000-token summaries).
- **Compaction should maximize recall, then precision.** The art of compaction is selection of what to keep versus discard; start by maximizing recall on complex traces, then iterate to eliminate superfluous content, and prefer tool result clearing as the lightest safe cut.
