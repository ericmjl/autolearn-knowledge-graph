---
title: "AI Security Incident Case: Encrypted Reasoning Blocks of Proprietary LLMs Can Be Stolen via Cross-Model Replay - NSFOCUS"
type: "raw-source"
url: "https://nsfocusglobal.com/ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen-via-cross-model-replay/"
author: "NSFOCUS (no individual author named)"
publication: "NSFOCUS"
published: "2026-08-20"
archived: "2026-11-21T13:20:48Z"
---

> [!quote] Original source
> **Author(s):** NSFOCUS (no individual author named)  
> **Title:** AI Security Incident Case: Encrypted Reasoning Blocks of Proprietary LLMs Can Be Stolen via Cross-Model Replay - NSFOCUS  
> **Published in:** NSFOCUS  
> **Date:** 2026-08-20  
> **Original:** <https://nsfocusglobal.com/ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen-via-cross-model-replay/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen|Source note]]
Themes: [[Agent security]]
Why it was archived: How do shared-key reasoning traces change the attack surface when an agent's trace crosses model families?

## Archived text

Overview

On August 10, 2026, MATS Research, the ELLIS Institute Tübingen, the Max Planck Institute for Intelligent Systems, and other institutions jointly published the paper Stealing Reasoning Traces from Proprietary LLM APIs. The research reveals a common architectural flaw in the reasoning model APIs of three major AI providers, Anthropic, OpenAI, and Google, which allows attackers to extract complete plaintext chains of thought from the encrypted reasoning blocks of their flagship models. The research team further conducted a large-scale analysis of 6,708 agent trajectories publicly available on GitHub and Hugging Face, decoding 315,320 reasoning blocks. This is the most systematic and largest security study of LLM reasoning traces publicly documented to date.

Vulnerability Background

Before generating a final answer, frontier reasoning models first produce an internal chain of thought. To protect intellectual property and prevent competitors from stealing their reasoning capability through distillation, Anthropic, OpenAI, and Google choose not to return the chain of thought in plaintext to clients, protecting it through encryption instead. However, in stateless interaction scenarios such as multi-turn conversations and tool calls, the server does not persist the complete state of every turn. If an application wants the model to continue from where it left off, it must resubmit the prior reasoning context in the next request.

To solve this storage problem, the three providers adopted the same architectural compromise: they encrypt the full reasoning process into an opaque string returned to the client, which the client temporarily holds and returns unchanged in the next request. OpenAI returns the encrypted reasoning item through the reasoning.encrypted_content field, Anthropic carries the full reasoning inside an encrypted signature, and Google uses an encrypted thought signature. These encrypted blocks are implemented with AEAD (Authenticated Encryption with Associated Data) schemes, which provide confidentiality and integrity protection at the cryptographic level.

However, although these encrypted blocks are authenticated-encrypted, they are not strictly bound to the specific session, user, or model that produced them. Through experiments, the research infers that the three providers may use a global encryption key. This means an encrypted reasoning block generated in one session can be replayed into another session, another user, or even another model. The tamper-resistance guarantee of AEAD is limited to the context bound within its associated data, and none of the three providers include user identifiers, session identifiers, or model identifiers within that binding scope.

Attack Flow

The entire attack chain is not complicated. In the first API call, the attacker submits a math problem, coding problem, or other task to a strong model. The strong model completes its reasoning, and the API returns the visible answer, a reasoning summary, and the encrypted reasoning block. In the second call, the attacker inserts this ciphertext into the context of a compatible model and appends a simple jailbreak prompt asking it to repeat the prior thinking word for word. The server first validates and parses the ciphertext; the weaker model then receives the restored reasoning state and, guided by the jailbreak prompt, outputs it in plaintext.

For different providers, the researchers selected compatible models with weaker protections within each ecosystem to serve as decoders: Haiku 4.5 in the Claude ecosystem, GPT-5.6 Luna in the GPT family, and Gemini Robotics ER-1.6 in the Gemini family. The paper verifies extraction fidelity by comparing the number of reasoning tokens reported by the API with the number of extracted reasoning tokens, and the two match essentially one to one. The economics of this attack are highly significant. Based on current Claude Haiku 4.5 pricing, decoding 10,000 reasoning traces costs approximately USD 720. Attackers do not need to directly break the safety alignment of the strong model itself; by using a weaker model as a “decryption oracle,” they can extract reasoning at scale and low cost.

Four Attack Vectors

This flaw gives rise to four distinct attack vectors:

Bypassing anti-distillation protections

Standard black-box model extraction and distillation attacks typically obtain only the model’s final output. For reasoning models, stronger attackers try to recover the model’s proprietary chain of thought. Directly asking the target model for its reasoning content works in some cases, but is increasingly constrained by model-level refusal behavior and system-level anti-distillation measures. Attackers exploit cross-model portability, capture the encrypted payload, and replay it into a smaller, more economical decoder model, thereby bypassing these barriers. The researchers successfully verified this capability on models from all three providers: Anthropic, OpenAI, and Google.

Stealing private data from public logs

Developers often share their session logs and encrypted thought traces publicly online, unaware that the encrypted blocks conceal sensitive data. From the 315,320 decoded reasoning blocks, the research team recovered 367 pieces of personally identifiable information, including 30 personal email addresses, 130 names, and 36 postal addresses; 182 sets of credentials included 62 still-active API keys, 33 passwords, 24 access tokens, and 7 private keys. Of these, 64 privacy artifacts existed only in the hidden reasoning and left no trace in the visible conversation logs. This means that even when developers redact visible text, sensitive information may still remain in the encrypted reasoning blocks. A typical triggering scenario is a user asking an agent to clean up a session, and the model rereading the full history in hidden reasoning while restating the sensitive values that need to be deleted.

The decoded reasoning contains private information. The illustration shows two examples of privacy-sensitive content decoded from encrypted reasoning blocks published publicly online. Left: GPT-5.2 Codex restates an API key that needs to be removed before publishing a GitHub repository. Right: Claude Sonnet 4.6 reasons over the private data of the synthetic identity “Alex Green” while handling a flight booking task in ClawBench.

Exposing harmful content hidden behind safe answers

Models are trained to suppress harmful information in visible output, but they do not necessarily avoid harmful topics in their chain of thought. Attackers can steer a model to explore a harmful topic in depth during reasoning while generating a safe, low-information final answer that passes output filters, then recover the harmful content from the extracted reasoning traces. The paper’s proof of concept shows that Opus 4.8, after receiving a query about vehicles that are easy to steal, generated detailed theft methods in hidden reasoning, while its visible output contained only benign advice on anti-theft measures.

Invisible prompt injection

Attackers can embed a malicious payload entirely inside an encrypted text block, thereby poisoning the deployment environment of a public-facing agent system without triggering any visible anomaly. Unlike traditional prompt injection, the payload is hidden in the reasoning rather than in visible text, so neither users nor external monitors that only inspect visible conversations can detect it. Once injected, the signed reasoning block is treated by the model as its own prior reasoning, which can materially influence subsequent actions. The paper’s proof of concept shows that after an encrypted block carrying a data exfiltration instruction was replayed into an unrelated task, the receiving model automatically carried out an upload to the attacker’s server. Models tend to treat their own reasoning traces as unquestionable content, which gives instructions embedded in encrypted blocks an unusually high execution priority.

Impact and Implications

All three providers have deployed server-side fixes after receiving the responsible disclosure. As of the paper’s publication in August 2026, the researchers confirmed that their original proof-of-concept attacks could no longer be reproduced on current API versions. However, historical working logs that were publicly shared before the fix still face the risk of being decoded.

This incident reveals a key limitation of encryption in real-world deployment: encryption does not equal isolation. Encrypted reasoning blocks provide confidentiality in the mathematical sense, but not isolation in the operational sense. Attackers do not need to break the encryption algorithm; they only need to exploit how the system processes decrypted content afterward. The design decision to share encryption keys between weaker and stronger models means the security of the entire system is determined by its weakest link. Attackers can bypass the strict refusal mechanisms of the strong model itself and complete reasoning extraction through the weaker model.

The portability of encrypted blocks was originally designed to support legitimate features such as model switching, session compression, and fault tolerance. However, that same convenience also opens up room for attackers. As the paper puts it, Ultimately, an architectural design that hides a user’s own data from them – yet leaves it entirely vulnerable to third-party extraction – provides neither privacy nor security.

References

[1] Panfilov A, Schmotz D, Shumailov I, et al. Stealing Reasoning Traces from Proprietary LLM APIs. arXiv:2608.09867, 2026. https://arxiv.org/abs/2608.09867

[2] Willison S. Stealing Reasoning Traces from Proprietary LLM APIs. Simon Willison’s Weblog, 2026-08-11. https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/

[3] The Hacker News. OpenAI, Anthropic, Google API Flaw Let Weaker AI Models Decode Stronger Models’ Reasoning. 2026-08-12. https://thehackernews.com/2026/08/openai-anthropic-google-api-flaw-let.html

[4] Cloud Security Alliance AI Safety Initiative. Encrypted Reasoning Traces Let Attackers Steal Hidden Chain-of-Thought. 2026-08-12. https://labs.cloudsecurityalliance.org/research/csa-research-note-reasoning-trace-theft-llm-apis-20260812-cs/
