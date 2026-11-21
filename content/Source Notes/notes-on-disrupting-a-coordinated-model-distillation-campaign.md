---
type: "source-note"
title: "Notes on: Disrupting a coordinated model-distillation campaign"
raw: "disrupting-a-coordinated-model-distillation-campaign"
url: "https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/"
created_at: "2026-11-21T22:01:32Z"
updated_at: "2026-11-21T22:03:48Z"
---
- Archived full text: [[disrupting-a-coordinated-model-distillation-campaign|Full archived text, with credits]]
- Link: <https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/>

## What it says

OpenAI describes a coordinated adversarial-distillation campaign that extracted protected reasoning from its models, plus the server-side mitigations it deployed: closing the replay pathway, holding streamed output that might expose reasoning, and account enforcement.

## Claims drawn from this source

- **Adversarial distillation is the systematic, unauthorized use of one model's outputs or reasoning to train, reproduce, or improve another model.** Protected reasoning is the model's internal record for working through a task; extracting it can reveal information withheld from the final answer and help others reproduce the model's capabilities.
- **Operators copied encrypted reasoning from one conversation and asked a model in another conversation to decrypt and transcribe the hidden reasoning content.** The operator manipulation involved replaying encrypted reasoning across conversations rather than breaking encryption, compromising a database, or gaining direct access to user conversations.
- **Spikes of 16,000 requests from over 4,000 users on July 24-25 used a relevant extraction pattern, and related prompt-pattern activity spanned a cluster of more than 15,000 users, fully disrupted by July 28.** The activity began July 1 at low volume before the high-volume spikes; a core cluster is attributed to individuals associated with Moonshot AI, the developer of Kimi.
- **OpenAI closed a pathway that let someone who already possessed another user's encrypted reasoning replay it and recover its contents.** It also added checks to detect and hold streamed output that might expose reasoning.
- **OpenAI strengthened protections for hidden reasoning across users, workspaces, organizations, and model families.** The response combined account enforcement, technical controls, and partner coordination: banning or restricting fraudulent accounts, strengthening signup and infrastructure controls, and expanding monitoring.
- **Systems that support portable or replayable reasoning artifacts may face related risks.** OpenAI shared findings through the Frontier Model Forum and government information-sharing channels so other frontier developers and public-sector partners could look for similar activity.
- **Partner-hosted deployments need the same protections as first-party services.** Tool-output attacks require protections that examine more than ordinary visible text; OpenAI is continuing to improve tool defenses, classifier coverage, model refusals, and propagating controls across cloud partners.
