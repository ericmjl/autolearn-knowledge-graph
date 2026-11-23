---
type: "source-note"
title: "Notes on: OpenAI’s August fix for theft of reasoning traces was quickly bypassed"
raw: "openai-s-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed"
url: "https://www.csoonline.com/article/4240662/openais-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed.html"
created_at: "2026-11-23T02:01:11Z"
updated_at: "2026-11-23T02:01:11Z"
---
- Archived full text: [[openai-s-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed|Full archived text, with credits]]
- Link: <https://www.csoonline.com/article/4240662/openais-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed.html>

## What it says

Xint published a compaction-smuggling attack that bypassed OpenAI's August fix for reasoning-trace theft: encrypted reasoning is captured, re-encoded with tabs, and replayed inside a compaction item to gpt-4.1 and gpt-4o, which output it verbatim because compaction runs on the same model that produced the reasoning. Analysts argue the fix was narrow (paths instead of properties) and advise enterprises to retest after vendor fixes, build regression notification into contracts, and track researcher disclosures.

## Claims drawn from this source

- **Compaction smuggling bypassed OpenAI's August mitigation.** Xint captured encrypted reasoning, removed the original task, requested the reasoning under a 'solution' key with spaces replaced by tabs, then sent the compaction item to gpt-4.1 and gpt-4o, which echoed it as-is; tabs were converted back to spaces.
- **The August mitigation only blocked cross-model replay.** Compaction runs on the same model that produced the reasoning, so it sailed past the fix that only blocked replaying reasoning into a different model; the attack worked at every reasoning effort tried.
- **Vendor fixes are narrow and incomplete.** AWS fixed a bug in April and had to refix it in September; analysts say vendors fix the specific attack path, not the underlying class of weakness, so fixes keep arriving narrow.
- **Enterprises should not treat a patch as closure.** Advisers advise CISOs to press providers on how exploits were tested across interconnected features, build regression notification into contracts, and retest with their own testing after vendor fixes.
- **AI platform flaws arrive without CVEs or advisories.** CISO operations built on CVE feeds and vendor advisories are blind to these flaws; CISOs should write security notification obligations into contracts and ask whether a fix addressed the report or the class.
- **The feature and the vulnerability are one capability.** Compaction's portability across models exists so agentic tools like Codex let users switch models mid-session, so every new path on a combinatorial feature surface is a fresh route to the same asset.
- **Bounty pricing lags the reported severity.** A $6,000 bounty was paid for a bug enabling industrial-scale distillation the NSA, CISA, and FBI warned about in a September joint advisory.
