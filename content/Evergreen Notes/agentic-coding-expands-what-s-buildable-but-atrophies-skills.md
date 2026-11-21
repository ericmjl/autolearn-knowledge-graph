---
type: "evergreen"
title: "Agentic coding expands what's buildable but atrophies skills"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-agentic-coding-is-a-trap-lars-faye", "notes-on-karpathy-on-coding-with-claude-and-leverage-x-post"]
provenance_urls: ["https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://x.com/karpathy/status/2015883857489522876"]
refutation_status: "untested"
---

# Agentic coding expands what's buildable but atrophies skills

Agent synthesis

Agent-driven coding expands what can be built and increases stamina, but overuse atrophies manual skills and supervision quality. The mechanism is a shift in the developer's role: from writing code to orchestrating agents, generating specs, and reviewing output. Karpathy reports moving from roughly 80% manual coding to 80% agent coding in a month, describing programming increasingly as "programming in English," and argues the main gain is expansion rather than speedup—doing things not previously worth coding and approaching code blocked by knowledge or skill gaps. Agents also never get tired or demoralized, dramatically increasing stamina for long stretches of work.

The cost is skill atrophy and a supervision paradox. Karpathy notes that manual coding ability is atrophying—generation and discrimination are different brain capabilities, so he can still review code even as writing it manually declines—and Lars Faye's essay reports skills dissipating within months, citing an Anthropic study with a 47% drop-off in debugging skills. Faye argues this inverts the priority list away from understanding, conciseness, and standards toward raw speed, and that juniors lose learning friction when reviewing generated code replaces direct code work (review is at best half the learning process). The paradox is that effective supervision requires the very coding skills that overuse degrades.

Both sources also flag that agents are not self-sufficient: Karpathy warns that models make subtle conceptual mistakes, wrong assumptions, overcomplication, and dead code, and need close supervision in a large IDE; Faye adds that spec-driven orchestration burns tokens, adds surrounding complexity, and distances humans from the code. The combination shows what no single source says alone: the expansion of what can be built is real and stamina-increasing, but it is purchased with degraded manual skill and supervision quality, so the workflow works best with agents as secondary processes—specs, planning, pseudo-code, ad-hoc delegation—while humans stay engaged in implementation and review.

## Where it comes from

- [[notes-on-agentic-coding-is-a-trap-lars-faye|Agentic Coding is a Trap (Lars Faye)]]
- [[notes-on-karpathy-on-coding-with-claude-and-leverage-x-post|Karpathy on coding with Claude and leverage (X post)]]

## What this builds on

- None yet.
