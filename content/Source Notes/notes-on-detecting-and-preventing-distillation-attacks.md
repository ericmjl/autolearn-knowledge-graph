---
type: "source-note"
title: "Notes on: Detecting and preventing distillation attacks"
raw: "detecting-and-preventing-distillation-attacks"
url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks"
created_at: "2026-11-22T16:02:18Z"
updated_at: "2026-11-22T16:02:18Z"
---
- Archived full text: [[detecting-and-preventing-distillation-attacks|Full archived text, with credits]]
- Link: <https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks>

## What it says

Anthropic's February 2026 report describes industrial-scale distillation campaigns by DeepSeek, Moonshot, and MiniMax against Claude: over 16 million exchanges through roughly 24,000 fraudulent accounts, targeting agentic reasoning, tool use, and coding. The report traces how these campaigns work (fraudulent accounts, proxy services with hydra-cluster architectures, synchronized traffic, rubric-based grading, and chain-of-thought elicitation) and what Anthropic does about it: classifiers and behavioral fingerprinting for attack patterns, intelligence sharing with other labs and authorities, tightened access controls on educational and startup pathways, and countermeasures that reduce the efficacy of outputs for illicit distillation.

## Claims drawn from this source

- **DeepSeek targeted reasoning, rubric-based grading, and censorship-safe alternatives.** The DeepSeek campaign generated over 150,000 exchanges aimed at reasoning capabilities across diverse tasks, rubric-based grading tasks that made Claude function as a reward model for reinforcement learning, and creating censorship-safe alternatives to policy-sensitive queries such as questions about dissidents or authoritarianism.
- **Moonshot used varied account types and later targeted reasoning-trace reconstruction.** Moonshot (Kimi models) employed hundreds of fraudulent accounts across multiple access pathways, and in a later phase attempted to extract and reconstruct Claude's reasoning traces. Attribution used request metadata matching public profiles of senior Moonshot staff.
- **MiniMax was detected mid-campaign and pivoted within 24 hours of a model launch.** MiniMax generated over 13 million exchanges targeting agentic coding, tool use, and orchestration. Anthropic detected the campaign while still active, before MiniMax released the model it was training; when Anthropic released a new model during the campaign, MiniMax redirected nearly half its traffic within 24 hours.
- **Distillation attacks use hydra-cluster proxies and coordinated traffic.** Labs use commercial proxy services to resell access at scale; these run hydra-cluster architectures, sprawling networks of fraudulent accounts that distribute traffic across the API and third-party platforms, with no single point of failure. In one case a single proxy network managed more than 20,000 fraudulent accounts simultaneously, mixing distillation traffic with unrelated customer requests.
- **The attack pattern is mass volume concentrated in narrow capabilities.** A prompt that seems benign on its own, such as asking for data-driven analysis grounded in transparent reasoning, becomes a distillation signal when variations arrive tens of thousands of times across hundreds of coordinated accounts targeting the same narrow capability. Massive volume, repetitive structures, and content mapping to training value are the hallmarks.
- **Anthropic's server-side defenses combine detection, intelligence sharing, access controls, and countermeasures.** Anthropic builds classifiers and behavioral fingerprinting systems to identify distillation patterns in API traffic, including chain-of-thought elicitation and coordinated activity across large numbers of accounts. It shares technical indicators with other labs, cloud providers, and authorities; strengthens verification for educational accounts, security research programs, and startup organizations; and develops product, API, and model-level safeguards that reduce distillation efficacy without degrading legitimate customers.
- **Illicit distillation undermines export-control rationale.** Models built through illicit distillation lack the safeguards American labs build in, so dangerous capabilities can proliferate into military, intelligence, and surveillance systems. Without visibility, advancements look like export-control failures, but they depend on extracted American capabilities; restricted chip access limits both direct training and the scale of illicit distillation.
