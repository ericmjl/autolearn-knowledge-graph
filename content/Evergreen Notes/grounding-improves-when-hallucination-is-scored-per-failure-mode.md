---
type: "evergreen"
title: "Grounding improves when hallucination is scored per failure mode"
created_at: "2026-11-25T15:03:01Z"
updated_at: "2026-11-25T15:03:01Z"
inputs: ["notes-on-mastering-rag-8-failure-modes-to-evaluate-before-going-to-production-splunk", "grounding-reduces-hallucination-but-cannot-eliminate-it"]
provenance_urls: ["https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["What detection methods exist for models misreading or blending retrieved context, and how do they fit with grounding?"]
---
Agent synthesis

Grounding reduces hallucination but only holds up when hallucination is scored against an explicit failure taxonomy rather than trusted as a default. The old view of grounding is binary: retrieval exists, so the answer is grounded. The new evidence replaces that binary with a 0-to-1 Context Adherence score for closed-domain hallucination, plus Chunk Relevance to separate retrieval problems from generation problems, and Completeness as the recall analog for what the response leaves out.

The mechanism: RAG combines two components that each carry their own failure point, and most failures stay invisible until someone asks a question you did not anticipate. The new source names eight modes, from retrieval quality (relevance, diversity, top-k omission, format mismatch, specificity) through hallucination patterns (noise robustness, negative rejection, information integration, counterfactual robustness, unclear queries, incorrect citations) to out-of-domain handling, completeness, and brand tone. Each mode maps to a specific evaluator, so "this feels risky" becomes a number you can track.

The note on grounding makes the tension explicit: retrieval anchors the model to supplied sources and lowers hallucination, but the model can still misinterpret, blend, or ignore that context. The new note adds the missing half: the grounding check itself must be measured, because the same failure that slips through silently at the generation layer is the one a scorer can catch. The three tests in the new source make debugging concrete: retrieve five documents where one holds the answer and check whether the model extracts it or blends the rest, ask a question the documents cannot answer and check whether it admits the gap, and request citations and verify each one references a real retrieved document.

A living test dataset ties it together: 100 to 200 real queries from logs plus synthetic edge cases, ground truth annotations, cases mapped to all eight modes, and production failures swapped into regression tests as they appear. (see: grounding reduces but cannot eliminate hallucination) Start by scoring Context Adherence and Chunk Relevance on the five queries you already run, then build the regression set out of every hallucination that slips through.

## Where it comes from

- [[notes-on-mastering-rag-8-failure-modes-to-evaluate-before-going-to-production-splunk|Mastering RAG: 8 Failure Modes to Evaluate Before Going to Production | Splunk]]

## What this builds on

- [[grounding-reduces-hallucination-but-cannot-eliminate-it|Grounding reduces hallucination but cannot eliminate it]]
