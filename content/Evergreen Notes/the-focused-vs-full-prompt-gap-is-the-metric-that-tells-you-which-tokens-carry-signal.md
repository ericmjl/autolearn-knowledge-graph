---
type: "evergreen"
title: "The focused-vs-full prompt gap is the metric that tells you which tokens carry signal"
created_at: "2026-11-21T20:03:57Z"
updated_at: "2026-11-21T20:03:57Z"
inputs: ["notes-on-context-rot-how-increasing-input-tokens-impacts-llm-performance", "context-signals-outrank-context-size"]
provenance_urls: ["https://www.trychroma.com/research/context-rot", "https://www.anthropic.com/research/effective-context-engineering-for-ai-agents", "https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do you measure and verify 'context signal' so selection can be automated, not hand-curated?"]
---
Agent synthesis

The focused-vs-full prompt gap is the metric that tells you which tokens carry signal. The context-signals note names the selection cues: folder hierarchy, naming conventions, timestamps, and file sizes carry purpose before content loads, and dropping a file into a window is not the same as giving a model signal. What it leaves undone is measurement: how an agent or a human knows that a candidate token earns its place. Chroma's context-rot report supplies the measurement instrument. It holds task complexity constant and varies only input length, finding that the same task, near-perfectly solved on focused inputs of about 300 tokens, collapses on full inputs of roughly 113k tokens across Claude, GPT, Gemini, and Qwen families even with thinking modes enabled. Where the gap is wide, the extra context is not carrying signal; where it is flat, the window must be full of useful content.

The report gives the fine-grained cues an agent can read off the same experiment. Cosine similarity of question and needle, averaged across five embedding models, steepens the degradation curve: lower similarity compounds length. Distractors compound it non-uniformly: one distractor already costs performance, four cost more, and particular distractors cost more than others; Claude abstains under ambiguity while GPT hallucinates confidently. Structural coherence consistently hurts, so logical flow in the haystack is not a free good, and needle position does not matter. The same experiments show the cost of forcing retrieval plus reasoning into a single call: full conversational history pays a marked tax that a focused prompt avoids.

Together, the two notes turn the selection problem into a checkable quantity. The selection cues from the signals note say which metadata to inspect; the focused-full gap says whether the inspection paid off. That is the difference between a window sized by intuition and a window verified by measurement. The novel part of the composition is neither the cue list nor the failures; it is that both are outputs of one instrument, a held-constant task run at several input lengths, and the delta across lengths is the signal itself.

Measure each candidate context set with the focused-vs-full gap before you let it into the window; tokens whose inclusion collapses that gap are the ones to keep and to retrieve just-in-time.

## Where it comes from

- [[notes-on-context-rot-how-increasing-input-tokens-impacts-llm-performance|Context Rot: How Increasing Input Tokens Impacts LLM Performance]]

## What this builds on

- [[context-signals-outrank-context-size|Context signals outrank context size]]
