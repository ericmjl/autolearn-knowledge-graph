---
type: "evergreen"
title: "Grounding alone cannot show which source controlled the answer"
created_at: "2026-11-26T10:02:35Z"
updated_at: "2026-11-26T10:02:35Z"
inputs: ["notes-on-does-rag-know-when-retrieval-is-wrong-diagnosing-context-compliance-under-knowledge", "grounding-reduces-hallucination-but-cannot-eliminate-it"]
provenance_urls: ["https://arxiv.org/html/2605.14473v4", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How can a system detect that a model misread retrieved context after grounding?"]
---
Agent synthesis

Grounding reduces hallucination, yet the final answer cannot show which source controlled it. A RAG model that answers "yes" to a misconception injected into the retrieved context may be faithfully following the context, or it may have detected the conflict and ignored retrieval; the answer alone cannot tell the two apart. The mechanism is implicit arbitration: standard RAG conditions generation directly on retrieved evidence, so under conflict the posterior can dominate the parametric prior.

Context-Driven Decomposition exposes that arbitration. The probe asks the model to elicit the answer implied by the context, elicit its parametric answer, compare the two, isolate the conflicting premise, and resolve the conflict, then perturbs the resolution trace with mistake-injection and truncation tests to ask whether the trace actually changes the answer. Under worst-case misconception injection (TruthfulQA top misconception as context, N=500), Standard RAG scores 15.0% while CDD scores 62.0%. On the Epi-Scale synthetic stress test (2,250 adversarial records), CDD reaches 78.1% macro versus 63.0% for Standard RAG, with the largest margins on Entity Swap (88.0% vs 79.3% for a conflict-aware instruction baseline) and Logical Contradiction (83.2% vs 75.4%); a length-matched sham decomposition scores only 40.1%, so the structure matters, not the number of steps. The caveat is just as diagnostic: mistake injection drops Gemini-2.5-Flash accuracy from 78.1% to 28.0% (64.1% causal sensitivity), while Claude-family sensitivities fall in [-3%, +7%], so accuracy gains transfer across models while the causal footprint of the trace does not.

Set beside grounding's known limits (see: grounding reduces hallucination but cannot eliminate it), the source note shows that faithfulness scoring is necessary but incomplete. A faithfulness check measures whether the answer stayed inside the retrieved context; decomposition measures which source controlled the answer, and trace perturbation tests whether the resolution was load-bearing. The pair turns a blind spot into two separate audits: one for staying inside the context, one for trusting what the context actually drove.

Use CDD-style decomposition as a diagnostic layer alongside faithfulness scoring, per model family, before trusting any grounded answer under suspected knowledge conflict. Do not read the trace as a verdict: on the Claude family the same trace improves accuracy without a measurable causal footprint, so the intervention reports a risk, not a guarantee.

## Where it comes from

- [[notes-on-does-rag-know-when-retrieval-is-wrong-diagnosing-context-compliance-under-knowledge|Does RAG Know When Retrieval Is Wrong? Diagnosing Context Compliance under Knowledge Conflict]]

## What this builds on

- [[grounding-reduces-hallucination-but-cannot-eliminate-it|Grounding reduces hallucination but cannot eliminate it]]
