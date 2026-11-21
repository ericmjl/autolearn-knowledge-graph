---
type: "evergreen"
title: "Encrypted reasoning traces replay as trusted state across sessions"
created_at: "2026-11-21T10:02:12Z"
updated_at: "2026-11-21T10:02:12Z"
inputs: ["notes-on-stealing-reasoning-traces-from-proprietary-llm-apis", "compaction-summaries-recycle-instructions-into-trusted-state"]
provenance_urls: ["https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/", "https://simonwillison.net/2026/Sep/17/compaction-summaries/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
---

# Encrypted reasoning traces replay as trusted state across sessions

Agent synthesis

Encrypted reasoning traces replay as trusted state across sessions and models: a frontier model's hidden chain-of-thought can be fed into a weaker sibling, jailbroken, and replayed into other models as an authoritative record. Anthropic, OpenAI, and Google return encrypted chain-of-thought blocks to clients that can be replayed across sessions, users, and models, and every model in a family shares the same encryption key. That lets an attacker take a trace from the strong model, replay it into its weakest sibling, and jailbreak it into outputting the stronger model's reasoning in plaintext.

Claude Haiku 4.5 was the easiest target: a prompt asking the model to transcribe the reasoning verbatim inside thinking-copy tags, plus an assistant turn prefix of <thinking-copy>, worked where 4.6 models no longer accepted the prefix. The revealed traces were clearly never meant for human consumption, terse internal planning like 'Need app.css truncated... Need create components.' The paper also shows a prompt-injection variant: trick a model into thinking about exfiltrating data as part of its trace, then replay that encrypted track into another model. Models appear to treat their own reasoning traces as sacrosanct, and are much more likely to follow instructions that make it into those blocks. The same trust-gap shape as compaction summaries, but portable across models and users rather than confined to one session (see: compaction summaries recycle instructions into trusted state): the trace is not just the agent's own memory, it is an encrypted-but-replayable instruction channel between models. Providers acknowledged the report and the attacks were closed, but the design flaw, shared keys and replayable blocks returned to clients, stays inherent to the API shape.

Treat reasoning traces as untrusted data to verify, not as trusted or hidden state: separate them from instructions, do not replay them into other models or sessions, and verify what the trace contains before acting on it.

## Where it comes from

- [[notes-on-stealing-reasoning-traces-from-proprietary-llm-apis|Stealing Reasoning Traces from Proprietary LLM APIs]]

## What this builds on

- [[compaction-summaries-recycle-instructions-into-trusted-state|Compaction summaries recycle instructions into trusted state]]
