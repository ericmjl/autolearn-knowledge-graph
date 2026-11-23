---
type: "source-note"
title: "Notes on: Token-Level Truth: Real-Time Hallucination Detection for Production LLMs"
raw: "token-level-truth-real-time-hallucination-detection-for-production-llms"
url: "https://vllm.ai/blog/2025-12-14-halugate"
created_at: "2026-11-23T16:01:14Z"
updated_at: "2026-11-23T16:01:14Z"
---
- Archived full text: [[token-level-truth-real-time-hallucination-detection-for-production-llms|Full archived text, with credits]]
- Link: <https://vllm.ai/blog/2025-12-14-halugate>

## What it says

HaluGate is a conditional, two-stage, token-level hallucination detection pipeline for production LLM deployments, built for the vLLM Semantic Router. It reuses the function-calling tool results as ground truth instead of calling another LLM as a judge. Stage 1 (HaluGate Sentinel, a ModernBERT classifier) decides whether a prompt is fact-seeking, achieving 96.4% validation accuracy in ~12ms and skipping detection for the ~35% of queries that are creative, coding, or opinion based. Stage 2 runs a token-level detector (ModernBERT) over answer tokens, ~125ms for a 4K-token context and ~365ms for 16K, then an NLI explainer that classifies each span as ENTAILMENT/NEUTRAL/CONTRADICTION with severity mapping (0/2/4). Total overhead is 76-162ms P50/P99, negligible against 5-30s generation times. The authors stress that token-level detection is recall-biased (59% F1 on the hallucinated class, nearly half of hallucinations missed, one-third of flags false positives) and that NLI provides precision and explainability rather than detection alone, and that intrinsic hallucinations have no tool context to verify against.

## Claims drawn from this source

- **Tool results are ground truth, not another LLM judge.** The source says function-calling APIs already provide grounding context: tool results are semantically equivalent to retrieved documents in RAG, so context, question, and answer can be extracted from the existing API flow without separate retrieval infrastructure.
- **Pre-classification skips detection for ~35% of queries.** Running token-level detection on creative writing or code review is wasteful and potentially produces false positives; the Sentinel classifier achieves a 72.2% efficiency gain by skipping detection for non-factual queries.
- **Sentinel is a 96.4%-accurate ModernBERT prompt classifier at ~12ms latency.** HaluGate Sentinel is a ModernBERT-base + LoRA adapter (rank 16, alpha 32, 2.2% of parameters) trained on 50,000 samples from 14 datasets, with ~12ms inference latency via native Rust/Candle integration.
- **Token-level detection scales linearly with context length.** For a 4K token RAG context, detection takes ~125ms; for 16K tokens, ~365ms.
- **LLM-as-judge has production flaws HaluGate replaces.** GPT-4 as judge costs 2-5 seconds and $0.01-0.03 per request with low explainability, plus position bias, verbosity bias, self-preference, and inconsistency; HaluGate runs 76-162ms on CPU with high explainability.
- **Token-level detection alone is recall-biased and needs NLI for precision.** Token-level detection achieves only 59% F1 on the hallucinated class, missing nearly half of hallucinations with one-third false positives; a unified 5-class model scored only 21.7% F1, so the two-stage approach lets recall come from token-level detection while NLI filters false positives and explains why each span is wrong.
- **Detection results ship as HTTP headers for downstream policy.** Headers such as x-vsr-fact-check-needed, x-vsr-hallucination-detected, and x-vsr-max-severity enable UI disclaimers, human review queues, audit logging, and conditional blocking of high-severity contradictions.
- **HaluGate cannot detect intrinsic hallucinations and stays open about missing context.** The pipeline targets extrinsic hallucinations where tool/RAG context provides grounding for verification; model-stated facts with no tool call, or factual questions with no tools defined, cannot be verified, and responses lacking tool context are explicitly flagged as unverified rather than silently passed through.
