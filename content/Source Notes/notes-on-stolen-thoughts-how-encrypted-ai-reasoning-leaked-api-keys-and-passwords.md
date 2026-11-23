---
type: "source-note"
title: "Notes on: Stolen Thoughts: How Encrypted AI Reasoning Leaked API Keys and Passwords"
raw: "stolen-thoughts-how-encrypted-ai-reasoning-leaked-api-keys-and-passwords"
url: "https://profero.io/blog/stolen-thoughts/"
created_at: "2026-11-22T01:02:57Z"
updated_at: "2026-11-22T01:02:57Z"
---
- Archived full text: [[stolen-thoughts-how-encrypted-ai-reasoning-leaked-api-keys-and-passwords|Full archived text, with credits]]
- Link: <https://profero.io/blog/stolen-thoughts/>

## What it says

The post covers a published, coordinated-with-providers vulnerability: reasoning blocks returned by frontier LLM APIs use authenticated encryption with a single global key shared across all users and sessions, so blocks from one session can be replayed into a weaker sibling model that decrypts and prints the original model's hidden chain-of-thought. The researchers collected 315,320 blocks from 6,708 public agent trajectories and recovered 704 privacy artifacts, 64 of them visible only inside the encrypted blocks. All three providers mitigated the specific replay path before publication, but the shared-key, replayable-across-accounts design flaw, and the persistence of credentials inside already-published transcripts, remain unfixed.

## Claims drawn from this source

- **Encrypted reasoning blocks use one global key across all users and sessions.** Matthew Green found in May 2026 that the blocks use authenticated encryption with a single global key shared across all users and sessions, and could be replayed across sessions, accounts, and (for OpenAI) models without triggering errors.
- **Replay across models is the core extraction primitive.** Panfilov et al. operationalized Green's finding by replaying each intact encrypted block into the same provider's API routed to a weaker sibling model, jailbreaking it to transcribe the reasoning verbatim, which decrypts the block with the shared key and outputs the stronger model's hidden reasoning in plaintext.
- **315,320 blocks from 6,708 public agent trajectories yielded 704 privacy artifacts.** The researchers collected public transcripts from GitHub and Hugging Face, extracted 315,320 signed blocks, and found 704 distinct privacy artifacts from genuine user sessions: 62 API keys, 33 passwords, 24 access tokens, and 30 personal email addresses, plus other PII and technical identifiers.
- **64 artifacts appeared only inside the encrypted reasoning.** Sixty-four of the 704 artifacts appeared exclusively inside the reasoning blocks, never visible in the chat window, meaning the user who generated them did not see them either.
- **Providers blocked the specific replay path before publication.** All three providers implemented mitigations before publication, blocking the specific replay path demonstrated in the paper, though the broader architectural question of a shared global key replayable across accounts remains.
- **No per-session or per-account key management exists.** If encrypted reasoning is worth protecting with a shared global key, why is it replayable across accounts at all? Proper per-session or per-account key management would eliminate the entire class of replay-based extraction.
- **Published transcripts carry undetectable credentials.** Any team that posted an agent transcript to a public repository or support ticket may have shipped live credentials embedded inside encrypted reasoning blocks, invisible to the user and to standard secret-scanning tools, and those credentials persist until rotated with no way to count or remove them.
