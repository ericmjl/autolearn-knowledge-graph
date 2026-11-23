---
type: "evergreen"
title: "Provider patches close the replay path but leave old transcripts behind"
created_at: "2026-11-22T01:06:29Z"
updated_at: "2026-11-22T01:06:29Z"
inputs: ["notes-on-stolen-thoughts-how-encrypted-ai-reasoning-leaked-api-keys-and-passwords", "encrypted-reasoning-traces-replay-as-trusted-state-across-sessions"]
provenance_urls: ["https://profero.io/blog/stolen-thoughts/", "https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/", "https://simonwillison.net/2026/Sep/17/compaction-summaries/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["What concrete mitigations do providers use to stop replayable encrypted reasoning traces from being treated as trusted state?"]
---
Agent synthesis

Provider patches close the replay path but leave credentials in old transcripts: the fix stops the specific sibling-model jailbreak while leaving the shared-key, cross-account replayability and the persistence of credentials inside published traces untouched.

The mechanism is cryptographic portability with stateless client storage: a reasoning block is an authenticated ciphertext returned in the API response JSON under one global key shared across all users and sessions, and the client is expected to store and return the blob on later turns. The patched endpoint refuses the specific replay path that routed a strong model's block into a weaker sibling model, but the keys are still global, and the blocks that already live in the public record keep working as long as decryption works.

The new source note reports that all three providers (Anthropic, OpenAI, Google) shipped mitigations before publication, and counts 315,320 blocks extracted from 6,708 publicly posted trajectories, 704 distinct privacy artifacts recovered from real sessions, and 64 artifacts visible only inside the encrypted reasoning. The sampled evergreen on encrypted reasoning traces argues the trust gap in the other direction, treating the trace as an encrypted-but-replayable instruction channel rather than session-local memory (see: encrypted reasoning traces replay as trusted state across sessions). Together, the two inputs show that a patched endpoint buys time on the demonstrated attack while leaving the retention problem and the design flaw standing.

The structural fix is per-session or per-account key management, and it cannot reach into every repository and delete the encrypted blocks already sitting there. Treat every published agent transcript as a credential slot: keep reasoning transcripts out of public repos, rotate anything that ever touched a reasoning session, and do not replay, reuse, or trust a trace across sessions or models.

## Where it comes from

- [[notes-on-stolen-thoughts-how-encrypted-ai-reasoning-leaked-api-keys-and-passwords|Stolen Thoughts: How Encrypted AI Reasoning Leaked API Keys and Passwords]]

## What this builds on

- [[encrypted-reasoning-traces-replay-as-trusted-state-across-sessions|Encrypted reasoning traces replay as trusted state across sessions]]
