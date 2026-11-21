---
type: "evergreen"
title: "Context signals outrank context size"
created_at: "2026-11-21T18:02:57Z"
updated_at: "2026-11-21T18:02:57Z"
inputs: ["notes-on-effective-context-engineering-for-ai-agents", "context-packing-and-tailored-interfaces-rival-model-choice"]
provenance_urls: ["https://www.anthropic.com/research/effective-context-engineering-for-ai-agents", "https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do you decide what context to pack for an agent: what signals should drive selection once the model sees all of a repo?"]
---
Agent synthesis

The leverage in context comes from which tokens you select, not how many you fit. Anthropic's context engineering evidence says context rot degrades recall as window size grows, so every token depletes a finite attention budget: the smallest set of high-signal tokens maximizes the desired outcome. The selection signals are structural. Folder hierarchy, naming conventions, timestamps, and file sizes carry purpose before any content loads, a file named test_utils.py in a tests folder means something different from the same name in src/core_logic/. An agent should carry lightweight identifiers and pull data just-in-time with tools rather than memorize a corpus, turning the repo into a set of cues rather than a pile to stuff.

The context-packing evergreen says packing context is co-equal with model choice; the same evidence says the real unit of packing is the signal, not the document. Minimal prompts at the Goldilocks altitude (not brittle if-elses, not vagueness), a minimal tool set where a human can say which tool fits, and diverse canonical examples rather than edge-case lists all push the window toward signal. The hybrid Claude Code pattern drops CLAUDE.md up front and uses glob and grep to retrieve just-in-time, which pairs the packing strategy with just-in-time exploration and bypasses stale indexing. For long-horizon work the same discipline holds: compaction, structured note-taking, and sub-agents with 1,000-2,000-token summaries keep working memory clean (see: the harness is the product, not the model).

Concretely, start with a minimal prompt and a bare set of tools, measure, then add signals where failure modes appear. Let the agent explore just-in-time with metadata as the cue, and only grow the context when the evaluator says the task needs it. Sizing the window is the wrong question; choosing which tokens deserve attention is the one that pays.

## Where it comes from

- [[notes-on-effective-context-engineering-for-ai-agents|Effective context engineering for AI agents]]

## What this builds on

- [[context-packing-and-tailored-interfaces-rival-model-choice|Context packing and tailored interfaces rival model choice]]
