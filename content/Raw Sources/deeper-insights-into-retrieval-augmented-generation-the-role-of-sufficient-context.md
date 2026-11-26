---
title: "Deeper insights into retrieval augmented generation: The role of sufficient context"
type: "raw-source"
url: "https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/"
author: "Cyrus Rashtchian, Da-Cheng Juan"
publication: "research.google"
published: "2025-05-14"
archived: "2026-11-26T05:01:08Z"
---

> [!quote] Original source
> **Author(s):** Cyrus Rashtchian, Da-Cheng Juan  
> **Title:** Deeper insights into retrieval augmented generation: The role of sufficient context  
> **Published in:** research.google  
> **Date:** 2025-05-14  
> **Original:** <https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context|Source note]]
Themes: [[Retrieval and agentic data science]]
Why it was archived: How can grounded agents detect when retrieved context is insufficient or misleading?

## Archived text

May 14, 2025

Cyrus Rashtchian, Research Lead, and Da-Cheng Juan, Software Engineering Manager, Google Research

We introduce a new notion of sufficient context to examine retrieval augmented generation (RAG) systems, developing a method to classify instances, analyzing failures of RAG systems, and proposing a way to reduce hallucinations.

Retrieval augmented generation (RAG) enhances large language models (LLMs) by providing them with relevant external context. For example, when using a RAG system for a question-answer (QA) task, the LLM receives a context that may be a combination of information from multiple sources, such as public webpages, private document corpora, or knowledge graphs. Ideally, the LLM either produces the correct answer or responds with “I don’t know” if certain key information is lacking.

A main challenge with RAG systems is that they may mislead the user with hallucinated (and therefore incorrect) information. Another challenge is that most prior work only considers how relevant the context is to the user query. But we believe that the context’s relevance alone is the wrong thing to measure — we really want to know whether it provides enough information for the LLM to answer the question or not.

In “Sufficient Context: A New Lens on Retrieval Augmented Generation Systems”, which appeared at ICLR 2025, we study the idea of "sufficient context” in RAG systems. We show that it’s possible to know when an LLM has enough information to provide a correct answer to a question. We study the role that context (or lack thereof) plays in factual accuracy, and develop a way to quantify context sufficiency for LLMs. Our approach allows us to investigate the factors that influence the performance of RAG systems and to analyze when and why they succeed or fail.

Moreover, we have used these ideas to launch the LLM Re-Ranker in the Vertex AI RAG Engine. Our feature allows users to re-rank retrieved snippets based on their relevance to the query, leading to better retrieval metrics (e.g., nDCG) and better RAG system accuracy.

We define context as “sufficient” if it contains all the necessary information to provide a definitive answer to the query and “insufficient” if it lacks the necessary information, is incomplete, inconclusive, or contains contradictory information. For example:

Input query: The error code for “Page Not Found” is named after room 404, which had stored the central database of error messages in what famous laboratory?

The second context is very relevant to the user’s query, but it does not answer the question, and hence it is insufficient.

With this definition, we first develop an LLM-based automatic rater (“autorater”) that evaluates query-context pairs. To evaluate the autorater, we first had human experts analyze 115 question-and-context examples to determine if the context was sufficient to answer the question. This became the “gold standard” to which we compared the LLM’s judgements. Then, we had the LLM evaluate the same questions and contexts, where it outputs either “true” for sufficient context or “false” for insufficient context.

To optimize the model’s ability to solve this task, we also improved the prompt with various prompting strategies, such as chain-of-thought prompting and providing a 1-shot example. We then measured classification performance based on how often the LLM’s true/false labels matched the gold standard labels.

Using our optimized prompt, we show that we can classify sufficient context with very high accuracy (at least 93% of the time). It also turns out that the best performing method we tried is a prompted Gemini 1.5 Pro, without any fine-tuning. As baselines, we show that FLAMe (fine-tuned PaLM 24B) is slightly worse than Gemini but could be a more computationally efficient alternative. We also compare our approach to methods that rely on ground truth answers, such as TRUE-NLI (a fine-tuned entailment model), and a method that checks if the ground truth answer appears in the context ("Contains GT"). Gemini outperforms the alternatives, likely because it has better language understanding abilities.

This autorater enables us to scalably label instances and analyze model responses based on sufficient vs. insufficient context.

Using our sufficient context autorater, we analyzed the performance of various LLMs and datasets, leading to several key findings:

Actionable insights: Based on our findings, we now have recommendations for how to improve RAG systems. For example, it could be beneficial to (i) add a sufficiency check before generation, (ii) retrieve more context or re-rank the retrieved contexts, or (iii) tune an abstention threshold with confidence and context signals.

Our analysis reveals that several standard benchmark datasets contain many instances with insufficient context. We consider three datasets: FreshQA, HotPotQA, and MuSiQue. Datasets with a higher percentage of sufficient context instances, such as FreshQA, tend to be those where the context is derived from human-curated supporting documents.

Example 182 from FreshQA is the question “How many food allergens with mandatory labeling are there in the United States?” This is a tricky question because the answer is nine, after sesame was added in 2023. The supporting document in the dataset is the Wikipedia article on Food Allergies, where the table under “Regulation of labeling” provides the list of the nine allergens with mandatory labeling.

A surprising observation is that while RAG generally improves overall performance, it paradoxically reduces the model's ability to abstain from answering when appropriate. The introduction of additional context seems to increase the model's confidence, leading to a higher propensity for hallucination rather than abstention.

To understand this, we use Gemini to rate each model response by comparing it to the set of possible ground truth answers. We classify each response as “Correct”, “Hallucinate” (i.e., incorrect answer), or ”Abstain” (e.g., saying “I don’t know”). With this approach we find, for example, that Gemma goes from providing incorrect answers on 10.2% of questions with no context up to 66.1% when using insufficient context.

As another contribution, we develop a “selective generation” framework that leverages sufficient context information to guide abstention. We consider the following metrics: selective accuracy measures the model’s fraction of correct answers among the ones it answers, and coverage is the fraction of answered questions (non-abstentions).

Our selective generation approach combines the sufficient context signal with the model's self-rated confidence scores to make informed decisions about when to abstain. This is more nuanced than simply abstaining whenever the context is insufficient, as models can sometimes provide correct answers even with limited context. We use these signals to train a logistic regression model to predict hallucinations. We then set a coverage-accuracy trade-off threshold, determining when the model should abstain from answering.

We use two main signals for abstention:

Our results demonstrate that this approach leads to a better selective accuracy-coverage trade-off compared to using model confidence alone. By using the sufficient context label, we can increase the accuracy on the questions that the model answers, sometimes by up to 10% of the time.

Our work provides new insights into the behavior of LLMs within RAG systems. By introducing and utilizing the concept of sufficient context, we have developed a valuable tool for analyzing and enhancing these systems. We showed that hallucinations in RAG systems may be due to insufficient context, and we demonstrated that selective generation can mitigate this issue. Future work will analyze how different retrieval methods influence context sufficiency and explore how signals about retrieval quality can be used to improve model post-training.

This work is in collaboration with Hailey Joren (lead student author), Jianyi Zhang, Chun-Sung Ferng, and Ankur Taly. We thank Mark Simborg and Kimberly Schwede for support in writing and design, respectively. We also thank Alyshia Olsen for help in designing the graphics.
