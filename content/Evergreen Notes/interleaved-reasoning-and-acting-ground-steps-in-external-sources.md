---
type: "evergreen"
title: "Interleaved reasoning and acting ground steps in external sources"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-react-synergizing-reasoning-and-acting-in-language-models-yao-et-al-iclr-2023", "notes-on-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks"]
provenance_urls: ["https://arxiv.org/abs/2210.03629", "https://arxiv.org/abs/2005.11401"]
refutation_status: "untested"
---

# Interleaved reasoning and acting ground steps in external sources

Agent synthesis

Interleaving reasoning traces with retrieval actions grounds steps in external sources and reduces hallucination and error propagation. Reasoning traces help the model induce, track, update, and recover from action plans, while actions let it query external knowledge bases or environments for additional information rather than relying only on parametric memory.

In "ReAct: Synergizing Reasoning and Acting in Language Models," this interleaving improves over strong baselines across question answering, fact verification, and interactive decision-making, produces more interpretable human-like trajectories, and on HotpotQA and Fever helps overcome hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API. It also outperforms imitation and reinforcement learning on ALFWorld and WebShop with only one or two in-context examples.

"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" supplies the external-memory side: large pre-trained models store factual knowledge but access it poorly, and pairing a parametric seq2seq model with a dense Wikipedia index accessed by a neural retriever yields more specific, diverse, and factual generation. The combination shows that interleaving is a way to operationalize external grounding during reasoning, not just retrieval at the end; neither source alone proves that provenance and world-knowledge updating are solved, which RAG still treats as open problems.

## Where it comes from

- [[notes-on-react-synergizing-reasoning-and-acting-in-language-models-yao-et-al-iclr-2023|ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)]]
- [[notes-on-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks|Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks]]

## What this builds on

- None yet.
