---
type: "source-note"
title: "Notes on: Stealing Reasoning Traces from Proprietary LLM APIs"
raw: "stealing-reasoning-traces-from-proprietary-llm-apis"
url: "https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/"
created_at: "2026-11-21T10:01:16Z"
updated_at: "2026-11-21T10:01:16Z"
---

# Notes on: Stealing Reasoning Traces from Proprietary LLM APIs

- Archived full text: [[stealing-reasoning-traces-from-proprietary-llm-apis|Full archived text, with credits]]
- Link: <https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/>

## What it says

Simon Willison links a paper showing that Anthropic, OpenAI, and Google return encrypted chain-of-thought blocks to clients, which can be replayed across sessions, users, and models. The attackers feed a trace from a frontier model into a weaker sibling and jailbreak it into outputting the stronger model's hidden reasoning in plaintext. The authors report that every model in a family used the same encryption key, that Claude Haiku 4.5 was the easiest to attack, and that providers fixed the issue after the report.

## Claims drawn from this source

- **Encrypted reasoning blocks can be replayed across sessions, users, and models.** Anthropic, OpenAI, and Google return encrypted chain-of-thought blocks to clients that can be replayed across sessions, users, and models.
- **Same-family models share an encryption key.** The paper's authors found that every model under the same family used the same encryption key, so blocks from a frontier model could be fed into the weakest members of the family.
- **Weak siblings unlocked the stronger model's reasoning.** Attackers replayed the frontier model's trace into a weaker sibling, jailbroke it, and recovered the stronger model's hidden reasoning in plaintext.
- **Claude Haiku 4.5 was the easiest to attack.** They used a prompt asking the model to transcribe the reasoning verbatim inside thinking-copy tags, plus an assistant turn prefix of <thinking-copy>; the prefix feature was removed in the 4.6 models but still worked in Haiku 4.5.
- **Revealed traces were never intended for human consumption.** The GPT-5.5 reasoning tokens revealed were clearly never intended for human consumption, showing terse internal planning like 'Need app.css truncated... Need create components.'
- **Reasoning traces are treated as sacrosanct and unlock prompt injection.** Tricking a model into thinking about exfiltrating data, then replaying that encrypted thinking track into another model, works because models appear to treat their own reasoning traces as sacrosanct and are much more likely to follow instructions inside those chunks.
- **Providers acknowledged the report and closed the attacks.** All model providers acknowledged the receipt of the report and subsequently the authors were unable to launch the same attacks.
