---
type: "source-note"
title: "Notes on: Deeper insights into retrieval augmented generation: The role of sufficient context"
raw: "deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context"
url: "https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/"
created_at: "2026-11-26T05:01:45Z"
updated_at: "2026-11-26T05:01:45Z"
---
- Archived full text: [[deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context|Full archived text, with credits]]
- Link: <https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/>

## What it says

Google Research, building on the ICLR 2025 paper 'Sufficient Context', argues that context relevance is the wrong thing to measure in RAG: the question is whether the context contains enough information to give a definitive answer. They define context as 'sufficient' if it holds all necessary information, and 'insufficient' if it lacks, is incomplete, inconclusive, or contradictory, then build an LLM-based autorater that classifies query-context pairs. The autorater, trained with prompted Gemini 1.5 Pro, matches human gold labels at least 93% of the time, outperforming fine-tuned PaLM-24B (FLAMe) and answer-in-context baselines. Using the autorater, they find that standard benchmark datasets hide many insufficient-context instances, that RAG paradoxically increases hallucination while reducing abstention (Gemma wrong answers rise from 10.2% with no context to 66.1% with insufficient context), and that a 'selective generation' step combining the sufficiency label with model confidence in a logistic regression model buys better accuracy-coverage trade-offs, up to 10% more accurate on the questions answered. Recommendations: add a sufficiency check before generation, retrieve more or re-rank context, and tune abstention thresholds. The chain also launched Vertex AI RAG Engine's LLM Re-Ranker, which re-ranks retrieved snippets for relevance to the query.

## Claims drawn from this source

- **Context relevance is the wrong metric for RAG; sufficiency is the right one.** Prior work only considers how relevant the context is to the user query, but the authors argue the context's relevance alone is the wrong thing to measure; what matters is whether it provides enough information for the LLM to answer.
- **A prompted LLM autorater classifies sufficient vs. insufficient context at over 93% accuracy.** They built an LLM-based autorater evaluating query-context pairs, optimized with chain-of-thought prompting and 1-shot examples; measured against 115 human-expert-labeled examples, it reaches at least 93% agreement, with prompted Gemini 1.5 Pro best and FLAMe slightly worse as a cheaper alternative.
- **The autorater beats ground-truth-answer-based baselines.** Gemini outperforms TRUE-NLI (a fine-tuned entailment model) and a 'Contains GT' method that checks whether the ground truth answer appears in the context, likely because of better language understanding.
- **Standard benchmark datasets contain many insufficient-context instances.** FreshQA, HotPotQA, and MuSiQue all contain such instances; datasets with more sufficient-context instances, like FreshQA, are ones where context is derived from human-curated supporting documents.
- **RAG paradoxically reduces abstention and increases hallucination.** Adding context increases the model's confidence and its propensity to hallucinate rather than abstain; Gemma's incorrect-answer rate on no-context versus insufficient-context questions rises from 10.2% to 66.1%.
- **Selective generation with the sufficiency signal improves accuracy on answered questions.** Combining the sufficient-context label with the model's self-rated confidence in a logistic regression model to predict hallucination, then setting a coverage-accuracy abstention threshold, beats confidence alone and raises accuracy by up to 10% of the time.
- **RAG systems should add a sufficiency check before generation.** Concrete recommendations: add a sufficiency check before generation, retrieve more context or re-rank the retrieved contexts (as the Vertex AI RAG Engine LLM Re-Ranker does, improving nDCG and RAG accuracy), and tune an abstention threshold with confidence and context signals.
