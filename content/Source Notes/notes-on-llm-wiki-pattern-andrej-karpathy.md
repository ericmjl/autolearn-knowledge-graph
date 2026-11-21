---
type: "source-note"
title: "Notes on: LLM Wiki pattern (Andrej Karpathy)"
raw: "llm-wiki-pattern-andrej-karpathy"
url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---

# Notes on: LLM Wiki pattern (Andrej Karpathy)

- Archived full text: [[llm-wiki-pattern-andrej-karpathy|Full archived text, with credits]]
- Link: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

## What it says

The source describes an "LLM Wiki" pattern for building personal knowledge bases: rather than retrieving raw documents at query time (RAG), the LLM incrementally reads, extracts, and integrates sources into a persistent, interlinked markdown wiki that is compiled once and kept current. It defines three layers — immutable raw sources, an LLM-owned wiki of markdown pages, and a schema document that configures the LLM's behavior — plus three workflows: ingest, query, and lint. The human curates sources and asks questions while the LLM handles summarizing, cross-referencing, filing, and bookkeeping, with index.md and log.md aiding navigation and history. The wiki is a git repo of markdown files, and optional tooling (search engines, Obsidian, slide decks, frontmatter queries) can be layered on.

## Claims drawn from this source

- **Wiki compiles knowledge once instead of re-deriving it per query.** Unlike RAG, which rediscovers knowledge from scratch on every question, the wiki is a persistent, compounding artifact with cross-references and contradictions already flagged.
- **Three layers: raw sources, wiki, schema.** Raw sources are immutable and serve as the source of truth; the wiki is LLM-owned markdown (summaries, entity/concept pages, synthesis); the schema (e.g. CLAUDE.md, AGENTS.md) tells the LLM how the wiki is structured and what workflows to follow.
- **Ingest integrates one source across many pages.** Processing a source writes a summary page, updates the index, updates entity/concept pages, and appends a log entry; a single source may touch 10-15 wiki pages.
- **Query answers can be filed back into the wiki.** Good answers — comparisons, analyses, discovered connections — should be saved as new wiki pages rather than disappearing into chat history.
- **Lint periodically health-checks the wiki.** Lint looks for contradictions, stale claims, orphan pages, missing concept pages, missing cross-references, and data gaps, and can suggest new questions and sources.
- **index.md avoids embedding-based RAG at moderate scale.** A content-oriented catalog of pages with one-line summaries lets the LLM read the index first and drill in, working well around ~100 sources and hundreds of pages.
- **log.md is an append-only, parseable timeline.** Chronological entries with a consistent prefix (e.g. '## [2026-04-02] ingest | Title') make the log parseable with simple unix tools like grep and tail.
- **LLM maintenance cost is near zero, unlike human-maintained wikis.** Humans abandon wikis because bookkeeping grows faster than value; LLMs don't get bored, don't forget cross-references, and can touch ~15 files in one pass.
