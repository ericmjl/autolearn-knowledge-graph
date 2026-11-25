---
type: "evergreen"
title: "Binding and fingerprinting together close replayable reasoning attacks"
created_at: "2026-11-21T22:03:11Z"
updated_at: "2026-11-25T14:03:37Z"
inputs: ["notes-on-disrupting-a-coordinated-model-distillation-campaign", "shared-key-reasoning-blocks-turn-weak-siblings-into-decryption-oracles", "notes-on-detecting-and-preventing-distillation-attacks", "notes-on-combatting-adversarial-distillation"]
provenance_urls: ["https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/", "https://nsfocusglobal.com/ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen-via-cross-model-replay/", "https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/", "https://simonwillison.net/2026/Sep/17/compaction-summaries/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent", "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks", "https://openai.com/index/combatting-adversarial-distillation/"]
refutation_status: "untested"
answers_questions: ["What server-side mitigations did AI providers deploy after the shared-key reasoning block replay attack?", "What server-side controls close replayable encrypted-reasoning attacks, and what do partner-hosted deployments need to replicate them?", "How do providers intend to stop encrypted reasoning traces from being replayed across sessions and models, and is the fix architectural or protocol-level?"]
---
Agent synthesis

Binding and fingerprinting together close replayable reasoning attacks, and the new OpenAI report pushes the binding to the weakest point: the conversation that produced the trace. The 2026-11 source ties GPT-6.2 Astra and Sol reasoning to the conversation history that produced it. As new messages are added, the model can build on its earlier reasoning, and if an earlier message is rewritten, the API drops the reasoning that followed it. Older model families with weaker safeguards are blocked from reading the stronger model's protected reasoning, and API-level protections now span user, workspace, organization, and model-family boundaries, including a closed pathway that could expose another user's reasoning.

The request-level stack around binding is layered end to end. Input classifiers detect attempts to extract protected reasoning; output classifiers scan assistant messages and tool-call arguments for leaks, because a model can expose protected reasoning in a tool's arguments without including it in its final answer. Adversarial training teaches the model to refuse disclosure while still answering legitimate requests, and successful attack logs become regression tests, replayed statically and through adaptive red-teamers. Adaptive black-box evaluation against GPT-6.2 Astra put the average attack success rate below 1% for each attack type, down from 54.0% against GPT-6 Astra with original safeguards. The campaign-level layer still matters: investigations of coordinated extraction campaigns produce enforcement actions across networks of accounts, with weekly actions ranging from thousands to tens of thousands of accounts, and indicators shared with other providers.

That new evidence sharpens the sampled note's two halves. The client-side framing from the sampled evergreen treats replayed traces as trusted state that is really an unverified instruction channel, and the distillation half shows the value being extracted: exact reasoning traces transfer more cyber capability to a student model than reasoning summaries, even after reinforcement learning, which is why the block cannot be protected by the model refusing to speak. Fingerprinting and binding close the same threat surface from opposite layers, and the new report adds the request-level half: even with binding, the trace can leak through tool-call arguments, and must be scanned before it reaches the caller.

Treat reasoning blocks and extraction traffic as one threat surface: bind each block to the conversation that produced it, scan assistant messages and tool-call arguments for leaks, replay past attacks as regression tests, fingerprint the coordinated-account patterns, and share indicators across providers (see: encrypted reasoning traces replay as trusted state across sessions).

## Where it comes from

- [[notes-on-disrupting-a-coordinated-model-distillation-campaign|Disrupting a coordinated model-distillation campaign]]
- [[notes-on-detecting-and-preventing-distillation-attacks|Detecting and preventing distillation attacks]]
- [[notes-on-combatting-adversarial-distillation|Combatting adversarial distillation]]

## What this builds on

- [[shared-key-reasoning-blocks-turn-weak-siblings-into-decryption-oracles|Shared-key reasoning blocks turn weak siblings into decryption oracles]]
