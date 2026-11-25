---
type: "evergreen"
title: "Clearing, compaction, and memory divide context management by failure mode"
created_at: "2026-11-25T08:05:01Z"
updated_at: "2026-11-25T08:05:44Z"
inputs: ["notes-on-context-engineering-memory-compaction-and-tool-clearing-claude-cookbook", "context-signals-outrank-context-size"]
provenance_urls: ["https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools", "https://www.anthropic.com/research/effective-context-engineering-for-ai-agents", "https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How should long-horizon agents combine compaction, structured note-taking, and just-in-time retrieval as context grows?"]
---
Agent synthesis

Long-horizon agents fail two ways: a hard wall on smaller windows, or silent recall decay on large ones, and neither is cured by a bigger window. Clearing drops stale re-fetchable tool results without inference cost, compaction distills the whole transcript into a summary, and structured note-taking moves findings out of the window so they survive across sessions; each keeps the working set small enough that neither failure mode bites.

The evidence is concrete. The Claude cookbook's research agent read eight ~40K-token documents; 96.3% of the final 335,279-token context was file-read results, and on a 200K window the same run stopped after three turns at 168,242 tokens. Clearing (trigger 30K, keep 4) freed ~163K tokens per event across four events, holding the peak at 173,137, though seven of eight reads vanished from context. Compaction (trigger 180K) held the peak at 169,164 with a ~2,783-token summary that kept all three high-level facts and lost all three obscure specifics. Memory saved a follow-up session four file reads (172,623 peak vs 333,977 without). Run together, the three held the peak at 169,938 against a 335,279 baseline, ending at 13,749 tokens.

Read against the sampled note on context signals, this sharpens it: which tokens you select outranks how many you fit, and the three primitives are the instruments that deliver that selection at scale (see: context signals outrank context size). The note argues for minimal prompts, bare tool sets, just-in-time retrieval, compaction, and structured note-taking. The cookbook adds the division of labor that makes that concrete. Compaction serves the conversation that cannot be re-fetched. Clearing serves the bulky output that can. Memory serves the knowledge that must outlive the session. It also adds the tuning details the note does not: exclude_tools ["memory"] so saved notes are never cleared, per-workload trigger and keep thresholds, and prompts that preserve the details the probe shows are at risk of being lost. Lossiness runs a spectrum, not a binary: clearing is lossless while tools stay re-callable, compaction is lossy by design, and memory is lossless on what the agent chooses to save and only as good as that judgment.

Diagnose which slice of context growth your workload actually has before adding any tool: dialogue, tool output, or cross-session knowledge. Add only the matching primitive first, then layer the others once the workload proves it hits both problems, and keep the per-primitive knobs tuned to the workload rather than to the default.

## Where it comes from

- [[notes-on-context-engineering-memory-compaction-and-tool-clearing-claude-cookbook|Context engineering: memory, compaction, and tool clearing | Claude Cookbook]]

## What this builds on

- [[context-signals-outrank-context-size|Context signals outrank context size]]
