---
type: "evergreen"
title: "Vendor reasoning-trace fixes leave the weakness class open"
created_at: "2026-11-23T02:01:43Z"
updated_at: "2026-11-23T02:01:43Z"
inputs: ["notes-on-openai-s-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed", "encrypted-reasoning-traces-replay-as-trusted-state-across-sessions"]
provenance_urls: ["https://www.csoonline.com/article/4240662/openais-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed.html", "https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/", "https://simonwillison.net/2026/Sep/17/compaction-summaries/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["What concrete mitigations do providers and clients adopt after replayable encrypted reasoning traces are shown to cross models and sessions?"]
---
Agent synthesis

Vendor fixes for encrypted reasoning traces patch the reported path while the underlying class of weakness survives. A fix that blocks replaying a trace into a different model does nothing for an attack that replays it through a same-model compaction, and neither OpenAI's August fix nor AWS's April fix addressed the property that makes any encrypted blob readable. The mechanism is whack-a-mole on a combinatorial feature surface: every new feature (compaction, session portability, model switching) is a fresh path to the same asset, and point fixes on that surface keep losing. The source documents the bypass itself: tab substitution slips past usage-policy classifiers, compaction items stay portable, and gpt-4.1 and gpt-4o echoed the replay verbatim. Interviewed analysts say a vendor's "fixed" should never be treated as closure; enterprises should retest with their own testing, build regression notification into contracts, track researcher disclosures, and ask whether a fix addressed the report or the class. The reasoning-trace evergreen already argues traces are replayable across sessions and models, and mitigations that only block cross-model replay leave the clerk-readable-letter case untouched (see: encrypted reasoning traces replay as trusted state across sessions). Treat every vendor security fix as a narrow path closure; verify the class with independent testing before trusting any patch notice.

## Where it comes from

- [[notes-on-openai-s-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed|OpenAI’s August fix for theft of reasoning traces was quickly bypassed]]

## What this builds on

- [[encrypted-reasoning-traces-replay-as-trusted-state-across-sessions|Encrypted reasoning traces replay as trusted state across sessions]]
