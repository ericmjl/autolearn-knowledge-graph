---
type: "source-note"
title: "Notes on: Harness Engineering for Self-Improvement"
raw: "harness-engineering-for-self-improvement"
url: "https://lilianweng.github.io/posts/2026-07-04-harness/"
created_at: "2026-11-21T08:02:00Z"
updated_at: "2026-11-21T08:02:00Z"
---
- Archived full text: [[harness-engineering-for-self-improvement|Full archived text, with credits]]
- Link: <https://lilianweng.github.io/posts/2026-07-04-harness/>

## What it says

Lilian Weng maps harness engineering as the substrate for recursive self-improvement: the layer between the raw model and the real world becomes a first-class, optimizable system. Harnesses orchestrate planning, tool use, context management, state, and evaluation; much recent auto-research and self-improving-agent work is organized around how to optimize that layer, from context scaffolds (ACE, MCE, Meta-Harness) to code-level evolution (ADAS, AFlow, DGM, SIA), with recurring cautions about evaluator weakness, reward hacking, and permission boundaries.

## Claims drawn from this source

- **The harness is as important as raw model intelligence.** The layer between the raw model and the real-world context seems to be as important as the model's raw intelligence, i.e. the evals right after pretraining. A harness is the system surrounding a base model that orchestrates execution and decides how the model thinks and plans, calls tools and acts, perceives and manages context, stores artifacts, and evaluates results.
- **Harness optimization progresses from prompts to optimizer code.** The progression in what is being optimized is roughly: instruction prompts, structured context, workflow, harness code, optimizer code. As the model becomes more intelligent and powerful, we move toward more complex targets and generic methods.
- **Context engineering treats context as an evolving playbook.** Agentic Context Engineering (ACE) has three components to maintain one context playbook of bullet points, each with an identifier and a description: a generator produces trajectories referencing bullets, a reflector distills insights from successful and failed trajectories, and a curator merges structured, itemized entries rather than rewriting the full prompt blob, preventing context collapse and brevity bias.
- **Meta-Harness optimizes harness code, not prompts.** Meta-Harness moves another level deeper: the optimized object is the code that determines and optimizes what information should be stored, retrieved, and presented to the model. The proposer is a coding agent and the final output is a collection of harness candidates on the Pareto frontier, with execution history accessible via a file system.
- **Self-improving harnesses run a propose-evaluate-accept loop.** Self-Harness clusters failures into verifier-grounded failure patterns, proposes bounded harness edits with a preserved-passes record, and accepts candidates only if they have no regression on held-in and held-out splits. It learns model-specific harness instructions that target different weaknesses of different base models and improves held-out pass rates.
- **Harness evolution needs observability and edits outside the loop.** Agentic Harness Engineering (AHE) creates a closed loop with three observability pillars: component observability (7 editable components, each failure mapped to one), experience observability (traces analyzed into a hierarchy of evidence), and decision observability (every edit paired with a falsifiable prediction). Edits live only in the harness workspace while runs, tracer, verifier, and LLM configuration are read-only, disabling a set of reward hacking.
- **Self-improvement is bounded by base-model capability.** STOP improved mean downstream performance with GPT-4 but degraded with weaker models like GPT-3.5 and Mixtral. Lin et al. found harness-updating capability is broad: a 9B harness proposer can write a skill procedurally isomorphic to Opus, but utilizing the updated harness requires correct, timely tool invocation and long-horizon instruction following.
- **Recursive self-improvement remains bounded by evaluators and permission boundaries.** The evaluator and permission control should likely sit outside the loop that evolves the harness, with held-out tests, trace audits, and human review at decision points. AI scientists can write plausible manuscripts with fabricated citations and implementation drift, and research taste, negative results, diversity collapse, and long-term success remain open bottlenecks.
