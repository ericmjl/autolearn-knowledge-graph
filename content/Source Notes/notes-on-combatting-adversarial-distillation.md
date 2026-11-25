---
type: "source-note"
title: "Notes on: Combatting adversarial distillation"
raw: "combatting-adversarial-distillation"
url: "https://openai.com/index/combatting-adversarial-distillation/"
created_at: "2026-11-25T14:01:27Z"
updated_at: "2026-11-25T14:01:27Z"
---
- Archived full text: [[combatting-adversarial-distillation|Full archived text, with credits]]
- Link: <https://openai.com/index/combatting-adversarial-distillation/>

## What it says

OpenAI reports its defense against adversarial distillation: request-level safeguards (model behavior, classifiers, API controls) plus campaign-level investigation and enforcement. Stronger protections for GPT-6.2 Astra and Sol cut the average adaptive red-team attack success rate from 54.0% to 0.2%, tie protected reasoning to the conversation history that produced it, block older weaker model families from reading it, and scan assistant messages and tool-call arguments for leaks. An internal study showed exact reasoning traces transfer more cyber capability to a student model than reasoning summaries, even after reinforcement learning.

## Claims drawn from this source

- **Distillation defenses combine request-level and campaign-level safeguards.** At the request level, model behavior, classifier checks, and API controls limit reasoning trace extraction; at the campaign level, OpenAI looks for patterns in request and account signals that reveal coordinated attempts to extract model capabilities.
- **Updated safeguards cut adaptive red-team attack success from 54.0% to 0.2%.** In an internal adaptive evaluation, attack success rate fell from 54.0% against GPT-6 Astra with its original safeguards to 0.2% against GPT-6.2 Astra with updated safeguards; in the adaptive black-box evaluation, ASR was below 1% for each attack type.
- **Protected reasoning is tied to the conversation history that produced it.** With GPT-6.2 Astra and Sol, the API ties protected reasoning to the conversation history, dropping the reasoning when an earlier message is rewritten, and prevents older model families with weaker safeguards from reading it.
- **Output classifiers scan tool-call arguments for leaks.** A model can expose protected reasoning in a tool's arguments without including it in its final answer; output classifiers block suspected leaks before that content reaches the caller, for both streaming and non-streaming responses.
- **Exact reasoning traces transfer more capability than reasoning summaries.** In an internal study of cyber capability transfer, the student trained on exact reasoning traces generally outperformed the student trained on reasoning summaries after supervised fine-tuning, and still scored higher at the largest inference budget after reinforcement learning.
- **Campaign-level findings become regression tests for defenses.** Attack logs from red-teaming, production monitoring, responsible disclosure, and investigations become regression tests, and adaptive red-teamers are used to test whether original attacks still expose protected reasoning.
