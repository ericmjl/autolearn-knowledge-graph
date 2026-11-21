---
type: "source-note"
title: "Notes on: AI Security Incident Case: Encrypted Reasoning Blocks of Proprietary LLMs Can Be Stolen via Cross-Model Replay - NSFOCUS"
raw: "ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen"
url: "https://nsfocusglobal.com/ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen-via-cross-model-replay/"
created_at: "2026-11-21T13:21:45Z"
updated_at: "2026-11-21T13:21:45Z"
---
- Archived full text: [[ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen|Full archived text, with credits]]
- Link: <https://nsfocusglobal.com/ai-security-incident-case-encrypted-reasoning-blocks-of-proprietary-llms-can-be-stolen-via-cross-model-replay/>

## What it says

NSFOCUS reports on the August 10, 2026 paper by MATS Research, ELLIS Institute Tübingen, and the Max Planck Institute for Intelligent Systems, which shows that Anthropic, OpenAI, and Google all use the same architectural compromise for reasoning models: the full chain of thought is encrypted in an opaque AEAD blob returned to the client and re-submitted in later requests. The blocks are not bound to the session, user, or model that produced them, and the researchers infer a global key. Replayed through a weaker same-family model with a simple jailbreak prompt, the stronger model's reasoning comes back as plaintext. The incident spans 6,708 public agent trajectories with 315,320 decoded reasoning blocks, and produces four attack vectors: bypassing anti-distillation controls, stealing private data from public logs, exposing harmful content hidden behind safe answers, and invisible prompt injection. Providers fixed the issue server-side, but previously shared public logs remain decodable, and the researchers argue that encryption without isolation provides neither privacy nor security.

## Claims drawn from this source

- **All three providers encrypt the full chain of thought into client-held AEAD blobs.** OpenAI returns the encrypted reasoning item in reasoning.encrypted_content, Anthropic carries it in an encrypted signature, and Google uses an encrypted thought signature; clients temporarily hold and return it unchanged in later requests.
- **The encrypted blocks are not cryptographically bound to session, user, or model.** The AEAD tamper-resistance guarantee is limited to the context bound within its associated data, and none of the three providers include user identifiers, session identifiers, or model identifiers in that binding scope. The researchers infer a global encryption key.
- **Weak models in the same ecosystem work as decryption oracles for strong models.** Haiku 4.5 in the Claude ecosystem, GPT-5.6 Luna in the GPT family, and Gemini Robotics ER-1.6 in the Gemini family were selected as decoders, and token counts matched one to one between reported and extracted reasoning.
- **Bulk trace extraction costs roughly USD 720 per 10,000 traces.** Based on current Claude Haiku 4.5 pricing, the article puts the economics of decoding 10,000 reasoning traces at approximately USD 720, letting attackers bypass anti-distillation protections without attacking the strong model directly.
- **Public logs hide PII that is not visible in conversation text.** From 315,320 decoded reasoning blocks the team recovered 367 pieces of personally identifiable information, including 30 personal email addresses, 130 names, and 36 postal addresses, plus 182 sets of credentials: 62 still-active API keys, 33 passwords, 24 access tokens, and 7 private keys.
- **A fifth of the privacy artifacts existed only in hidden reasoning.** 64 privacy artifacts existed only in the hidden reasoning and left no trace in the visible conversation logs; a user asking an agent to clean up a session made the model restate sensitive values in hidden reasoning.
- **Hidden reasoning can carry harmful content behind safe visible answers.** Opus 4.8, prompted about vehicles that are easy to steal, generated detailed theft methods in hidden reasoning while its visible output contained only benign anti-theft advice.
- **Encrypted blocks can inject invisible instructions that the agent executes.** After an encrypted block carrying a data-exfiltration instruction was replayed into an unrelated task, the receiving model automatically carried out an upload to the attacker's server, and neither users nor visible-conversation monitors can detect this.
