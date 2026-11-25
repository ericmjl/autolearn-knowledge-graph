---
title: "Mastering RAG: 8 Failure Modes to Evaluate Before Going to Production | Splunk"
type: "raw-source"
url: "https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html"
author: "Pratik Bhavsar"
publication: "Splunk"
published: "2026-09-07"
archived: "2026-11-25T15:01:12Z"
---

> [!quote] Original source
> **Author(s):** Pratik Bhavsar  
> **Title:** Mastering RAG: 8 Failure Modes to Evaluate Before Going to Production | Splunk  
> **Published in:** Splunk  
> **Date:** 2026-09-07  
> **Original:** <https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-mastering-rag-8-failure-modes-to-evaluate-before-going-to-production-splunk|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: What detection methods exist for models misreading or blending retrieved context, and how do they fit with grounding?

## Archived text

Mastering RAG: 8 Failure Modes to Evaluate Before Going to Production

Artificial Intelligence Pratik Bhavsar

Key Takeaways

- RAG systems require systematic testing across eight distinct failure modes, including retrieval quality, hallucinations, and security, to identify risks that remain invisible during standard development.
- Effective evaluation depends on building a "living" test dataset that combines real user logs with synthetic edge cases, supported by ground truth annotations to track performance regression.
- Automated evaluators such as Context Adherence, PII detection, and Prompt Injection analysis provide quantitative metrics, enabling teams to move from anecdotal debugging to data-driven system reliability.

Retrieval-augmented generation (RAG) works well right up until it meets real users. Combining retrieval with a capable language model introduces failure points that neither component has on its own, and most of them stay invisible until someone asks the question you did not anticipate.

Testing is the last step before deployment and the one most teams compress. This guide covers the eight failure modes worth testing for, the specific scenarios inside each, and how to build a dataset that exercises all of them. Every scenario names the evaluator that catches it, so you can move from "this feels risky" to a number you can track.

1. Retrieval quality

Retrieval quality measures whether your system finds the right documents. When retrieval fails, the model generates a response from incomplete or incorrect information, and nothing downstream can recover it. Five aspects determine whether a retrieved document is actually suitable.

Relevance

Relevance measures how well retrieved documents align with the query. A question about photosynthesis should return documents explaining both the light-dependent and light-independent reactions, not general overviews of plant biology.

In the example above, documents 1 and 2 are highly relevant and give comprehensive information on the process. Context Relevance scores this automatically by comparing query intent against retrieved content, so you do not have to eyeball it case by case.

Diversity

Diversity assesses the variety of information across retrieved documents, making sure they cover different aspects or perspectives rather than restating the same point three times.

Here the retrieved documents are diverse, covering various impacts of climate change across different types of ecosystems.

Top-k document omission

Another failure point is when the definitive answer exists in your document collection but does not rank highly enough to make it into the context passed to the model. Retrieval selects only the top K documents. This fails when K is set too low, or when a highly relevant document gets pushed down the ranking by less essential content.

Format mismatch

This occurs when the user asks for information in a specific structure — a table, a list, JSON — and the model disregards the instruction. Even with perfectly relevant context, a response in the wrong shape is unusable by whatever consumes it next.

Specificity issues

Here the model delivers a response that is either too vague to act on or so detailed it buries the answer. Neither is an apt reply to the question asked. Instruction Adherence measures how closely the model follows prompt instructions on format and specificity, which makes both of these failures countable rather than anecdotal.

Worth doing before you read on: pick five queries your users actually ask, and for each one examine the top three documents your system retrieves.

- Does document 1 directly answer the query?
- Do documents 2 and 3 add new information or repeat document 1?
- If the query specifies a format, can the retrieved documents support that structure?
2. Hallucinations

Hallucinations in RAGare cases where the model generates information not present in the context documents. A RAG system should ground every response in what it retrieved. There are six patterns to watch for.

Noise robustness

Context documents carry a great deal of information, and the model has to work out which piece is relevant. Noise robustness measures its ability to extract what matters from a mixture of relevant and irrelevant documents. In the example below, the model must pull the relevant fact while ignoring surrounding noise; the incorrect response draws from the irrelevant retrieved documents instead.

Chunk Relevance tells you which of the retrieved chunks actually contained useful information for the query, which is how you separate a retrieval problem from a generation problem.

Negative rejection

RAG systems have to know when they do not know. Negative rejection assesses whether the model declines to answer when none of the context provides useful information, rather than producing a confident guess.

Context Adherence is the metric here. It is defined as a measure of closed-domain hallucination — cases where the model said things that were not provided in the context — on a scale from 0 to 1.

Information integration

Rarely does a single document contain everything needed for a comprehensive answer. Information integration evaluates whether the model can answer complex questions that require combining information across multiple documents.

Completeness measures whether responses incorporate all the relevant context available. If Context Adherence is precision, Completeness is recall.

Counterfactual robustness

Some context documents contain errors. Counterfactual robustness assesses whether the model can identify known factual errors in retrieved documents and respond appropriately rather than repeating them.

Correctness identifies when responses reproduce errors from their sources, which is the failure that damages trust fastest because the system looks well-grounded while being wrong.

Unclear queries

User queries are often unintentionally vague, particularly when framed as follow-up questions that depend on earlier turns. It is worth evaluating how the model handles them.

Incorrect citations

An incorrect citation occurs when the model references sources that do not exist, or misattributes information to the wrong document. This breaks trust in exactly the domains where users check sources. The entire response must be traceable back to the retrieved documents, with no invented details slipped in between.

Context Adherence catches the ungrounded claim; Chunk Relevance tells you whether the cited chunk was ever useful in the first place.

Three tests worth running now:

- Retrieve five documents where only one contains the answer and ask a specific question, to see whether the model extracts from the right document or blends in the rest.
- Ask a question your documents cannot answer, such as a future quarter's revenue, and see whether it admits the gap or fabricates.
- Request an answer with citations and verify each one references a real retrieved document and quotes it correctly.

Failing any of these means you are shipping ungrounded responses.

3. Privacy breaches

Privacy is a non-negotiable failure mode, especially when the system touches sensitive data. A breach occurs when the model discloses private, sensitive or confidential information that should never have reached the user. RAG makes this particularly dangerous for three reasons.

- PII retrieval: the system retrieves documents containing personally identifiable information — names, addresses, medical records — that was not correctly redacted in the source material.
- Context leakage: the model leaks information from another user's session, or from internal, non-customer-facing documents that ended up in the retrieval corpus.
- Data retention violations: user data that should have been deleted months ago is still sitting in the vector database, ready to surface in someone else's query.

The third one is the quietest and the hardest to catch. When was the last time you audited what is actually in your vector database? Deletion requests that were honored in the source system do not automatically cascade to derived chunks, embeddings and indexes, which means a user who exercised their right to erasure six months ago may still be answerable today.

The PII evaluator detects and flags personally identifiable information in both inputs and outputs, which covers the first two cases. The third needs an audit, not a metric.

4. Malicious use

Models must refuse to help users engage in illegal activities, spread misinformation, or act unethically. Retrieval does not change this obligation — if anything it raises the stakes, because a RAG system speaks with the authority of your document corpus behind it.

Illegal activities

This evaluates the model's response to queries about committing fraud, manufacturing controlled substances, bypassing security systems, or planning other criminal acts.

Harmful content creation

This evaluates responses to queries soliciting toxic language, hate speech, explicit content, bullying material or dangerous self-harm advice.

Toxicity Detection flags whether a response contains hateful or toxic information, and runs on both the input and the output.

Harmful activity assistance

This evaluates the model's response to queries inquiring about harmful activities, distinguishing a proper refusal from guidance that helps the user proceed.

5. Security breaches

Attacks on the model's own security are a separate category from misuse, and gaps here can cause serious harm to the enterprise.

Emotional manipulation

Attackers design prompts to manipulate the model into generating harmful content, crafting them to make it play specific roles, acquire higher privileges, or shift attention in a way that facilitates undesirable outputs.

Prefix injection

Prefix injection inserts specific instructions or phrases at the beginning of a prompt to manipulate the model's behavior.

Refusal suppression

Refusal suppression instructs the model to respond under constraints that eliminate common refusal phrasings, which makes an unsafe response more likely simply by removing the language the model would normally reach for.

Mismatched generalization

Mismatched generalization happens because the model was pretrained on a far larger and more diverse dataset than its safety training covered. That gap leaves capabilities outside the reach of safety training, and it can be exploited for jailbreaks — encoding a request in base64, for instance, so that decoding and answering happen outside the path safety training anticipated.

The Prompt Injection evaluator identifies malicious inputs attempting to override system instructions, covering all four of these patterns.

Three queries to try against your own system:

- A role manipulation attempt that tells the model to disregard retrieved policy documents and assume override permissions.
- A prefix injection in the form of a fake SYSTEM directive disabling safety guidelines.
- An encoded request in base64.

Your system should refuse all three. If it complies with any of them, you have a security gap that needs attention before anything else on this list.

6. Out-of-domain questions

Most RAG systems serve a specific use case — banking customer service, travel planning, internal IT support. They need to handle queries outside that domain gracefully, claiming their actual specialty and referring the user onward rather than answering confidently from adjacent context.

Instruction Adherence is the evaluator here, since staying inside the defined domain is ultimately a question of whether the model followed its system instructions.

7. Completeness

A good user experience requires comprehensive responses. Completeness assesses how well the model recalls and incorporates all relevant information from the retrieved documents without dropping details related to the query.

The Completeness evaluator verifies that the response covered the relevant information available in the context provided. When it runs low, there are three usual fixes: tell the model explicitly to include all relevant information it finds, refine retrieval so the most relevant chunks come back, and watch that you are not encouraging padding just to raise the score.

8. Brand damage

Brand damage assesses whether the model's tone, style and phrasing align with your organization's values and public expectations. The goal is a system that communicates respectfully and clearly, and never in language that costs you trust.

Tone and toxicity

Maintaining appropriate tone and eliminating toxicity matters for any production RAG application. This assesses whether responses stay respectful and neutral, as against dismissive, opinionated or politically charged statements offered without evidence.

Non-compliance

Non-compliant keywords are worth screening so responses stay inside your guidelines and ethical standards. This evaluates the model's ability to avoid inappropriate or prohibited terms and keep a compliant conversational tone — refusing to help exploit a loophole rather than obligingly explaining how.

How to build a test dataset

Testing against all eight modes requires a dataset that mirrors real usage while systematically covering the ways things break. Three components have to work together.

Document corpus

Start with documents that represent your current knowledge base, in the formats you actually hold: technical documentation, FAQs, policy documents, user guides, historical data.

Deliberately include documents with overlapping information to test deduplication, contradictory information to test conflict resolution, and varying quality levels to test noise filtering. A financial services system might use 500 policy documents, 2,000 FAQ entries, 10,000 transaction summaries and 100 regulatory compliance documents.

Query set

Develop queries that reflect actual user behavior. Extract 100 to 200 real queries from your logs. Where logs are unavailable, create synthetic queries covering factual lookups, multi-hop questions that require combining two facts, follow-up questions that depend on prior context, and edge cases with typos or ambiguous phrasing.

Ground truth annotations

Define correct responses for each query: expected document IDs, required facts, acceptable formats, and unacceptable hallucinations. Without ground truth you cannot tell whether a change improved the system or degraded it, which makes every subsequent experiment guesswork.

Synthetic test cases

Where real data is thin, build synthetic cases that target specific failure modes:

- Security tests: instruction-override attempts and fake SYSTEM directives disabling safety guidelines.
- Privacy tests: insert fake SSNs and test email addresses into documents, then write queries that should never surface them, such as asking for examples of customer records.
- Domain boundary tests: ask a financial bot for medical advice, a customer service system for legal counsel, or a historical data system to predict the future.
- Error injection: introduce typos, remove context so the query is unanswerable as written, and add internal contradictions such as wanting a refund while keeping the product.

Dataset augmentation

Expand each core query into three to five variations. "How do I reset my password?" becomes a formal version, an informal version, and a verbose version. Add temporal variations to test time-based reasoning: what the policy is, what it was last year, what changed in the recent update, and what the current version says.

Validation checklist

Before deploying the dataset, verify coverage and balance in three steps. Map test cases to all eight failure modes — if retrieval quality has 40 test cases and privacy has three, you will miss privacy failures in production. Check the complexity distribution, counting simple, medium and complex queries, and positive cases against negative ones, aiming for roughly half real user logs and half synthetic. Then run 30 test queries past domain experts to verify ground truth, assess whether synthetic queries look realistic, and confirm the difficulty matches production.

An example of balanced coverage across the eight failure modes.

Dataset maintenance

Your test dataset is a living artifact. Version it alongside your model versions, and regenerate affected test cases whenever you update document chunks. Add production failures to the dataset immediately: a hallucination in production becomes a regression test, a missed privacy violation becomes a new privacy case. Expect the dataset to grow 10 to 20 percent quarterly through this alone.

Audit quarterly for outdated annotations, deprecated document references and missing query patterns, and check whether new regulations require additional cases. One audit worth running today: pull a random sample of 100 documents from your vector database and check creation dates and deletion flags. User data marked for deletion six months ago may still answer queries.

On cost, do the arithmetic before committing to synthetic generation. A thousand synthetic queries at three LLM calls each is 3,000 API calls — cheap in dollars, but the human validation behind it is not. For most teams, 100 real user queries plus 50 synthetic variations gives better return than generating everything from scratch.

Every failure mode and its evaluator

Building a reliable RAG system is more than plugging retrieval into a model. You must know where things go wrong before real users find out for you. The table below maps each failure mode to the evaluator that measures it — use it as a reference when you set up testing.

Learn more about our suite of RAG evaluators here

Conclusion

Each of these eight modes points at the same three things holding a RAG system together: clean retrieval, safe model behavior, and guardrails that hold under pressure. The scenarios here are not exhaustive — no list is — but they cover the failures that actually show up in production, and they give you somewhere concrete to start.

The teams that ship reliable RAG are not the ones that avoided these failures. They are the ones that found them first, turned each one into a test case, and kept the dataset growing as the system changed.

Understanding your RAG system at work is key to trusting AI systems. Learn about Splunk Agent Observability and get hands-on with the Splunk Observability Cloud Free Edition today
