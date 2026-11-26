---
type: "evergreen"
title: "Passage-level sufficiency gates under-detect in multi-hop retrieval"
created_at: "2026-11-26T18:06:54Z"
updated_at: "2026-11-26T18:06:54Z"
inputs: ["notes-on-rag-wikipedia", "sufficiency-gates-not-relevance-scores-keep-grounded-agents-from-hallucinating"]
provenance_urls: ["https://en.wikipedia.org/wiki/Rag", "https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How well do sufficiency gates hold up on multi-hop retrieval, where no single passage contains the full answer?"]
---
Agent synthesis

Passage-level sufficiency gates under-detect in multi-hop retrieval: the answer lives in the union of passages, not in any single one. Relevance measures whether a passage matches the query; sufficiency measures whether the context contains everything needed for a definitive answer. That distinction, validated at roughly 93% accuracy against human gold labels on 115 examples, holds an atomic relationship between one question and one context. In multi-hop retrieval the decomposition matters: each hop returns a passage that is fully relevant, yet the union can still miss the second or third hop, so the gate passes context whose information is incomplete. The mechanism is a mismatch between what the gate certifies (one context against one question) and where the information actually sits (across hops). The rag-wikipedia source contributes one provenance line: retrieval-augmented generation is generative artificial intelligence with the addition of information retrieval capabilities, with no argumentation about multi-hop design. That is exactly the gap, because standard RAG evaluation keeps the question atomic and squashes the composite evidence into a single atomic question.

The evidence cuts both ways. The sufficiency-gates note reports that Gemma's incorrect-answer rate jumps from 10.2% with no context to 66.1% with insufficient context, and that a selective generation step beats confidence alone and lifts accuracy on answered questions by up to 10%. Both assume the context is either complete or useless. Multi-hop context is usually partially complete, which is precisely the regime where a gate false-passes the union or fails to signal enough to fetch the next hop. Selective generation cannot recover a union no single hop contains.

Build the gate at the union level: label, for each retrieved set, whether the full set supports a definitive answer, and validate the autorater against human-built multi-hop gold labels rather than atomic-question benchmarks. Report a false-pass rate next to the accuracy the gate claims, treat retrieval of a full-hop set as a separate control from passage relevance, and re-rank or re-fetch when the union gate fails. Gate on whether the set supports the conclusion, not whether each passage is a match.

## Where it comes from

- [[notes-on-rag-wikipedia|Rag - Wikipedia]]

## What this builds on

- [[sufficiency-gates-not-relevance-scores-keep-grounded-agents-from-hallucinating|Sufficiency gates, not relevance scores, keep grounded agents from hallucinating]]
