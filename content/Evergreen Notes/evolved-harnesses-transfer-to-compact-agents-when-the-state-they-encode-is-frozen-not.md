---
type: "evergreen"
title: "Evolved harnesses transfer to compact agents when the state they encode is frozen, not just the model"
created_at: "2026-11-27T10:02:22Z"
updated_at: "2026-11-27T10:02:22Z"
inputs: ["notes-on-tinyastral-transferring-self-evolving-harnesses-to-tiny-generalist-manipulation-agents", "harness-evolution-pays-off-only-with-a-dense-held-out-oracle"]
provenance_urls: ["https://arxiv.org/html/2610.41216v1", "https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent", "https://arxiv.org/html/2607.08124v3"]
refutation_status: "untested"
answers_questions: ["How do evolved harnesses transfer across models, and what is the mechanism behind that transfer?"]
---
Agent synthesis

Harness evolution produces gains that survive distillation and planner swaps because the harness encodes how an action is executed, not what a step does. TinyAstral freezes an open-weight teacher, evolves its tools, feedback, memory, and recovery logic through a master-guided loop with pre-registered paired statistical tests (33.4% to 63.6% strict success on RoboTwin, with only the harness changing), then distills teacher reasoning and injected-failure recovery into a 4B student that runs the same frozen harness. The student reaches 62.8%, stays within 2.4 pp of a 552B planner on never-trained benchmarks, and uses about one fifth of the teacher's accelerator time.

The transfer is mechanical, not incidental. Students trained at each of four harness versions track their corresponding teacher (36.2%, 49.8%, 60.0%, 62.8%), and the same evolved harness lifts the untrained 4B planner from 14.6% to 41.2% and a 552B planner not used during evolution by 30.6 pp. Harness evolution gains are reusable across planners because the improved system lives in the frozen scaffold: the student re-executes the same feedback and recovery logic, and keeps the teacher's stated rationale in the training target (dropping that text costs 19.3 pp on LIBERO-PRO). Distilling the student from evolved-harness trajectories is thus a way to move the evolved system's decision-making capability into a compact model, not a way to re-grade the model.

The held-out oracle note holds for grading evolved harnesses, but the new evidence shows what the adaptation loop consumes: the harness state. Evolved harness code is inspectable and reusable across planners, which is why a batch-specific evolved harness that improves one model can carry into another without re-evolution. The parallel is the harness-evolution note's advice that adaptation runs on dense execution traces while the oracle stays outside as a post-selection gate: here, the frozen harness itself is the asset that crosses models. What this does not settle is whether explicit oracle-over-candidates comparisons still pay off once the harness state is frozen and reused.

Run evolution on harness code, freeze it, and measure transfer by distilling into a compact student and swapping frozen planners before trusting an evolved harness for a new deployment.

## Where it comes from

- [[notes-on-tinyastral-transferring-self-evolving-harnesses-to-tiny-generalist-manipulation-agents|TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents]]

## What this builds on

- [[harness-evolution-pays-off-only-with-a-dense-held-out-oracle|Harness evolution adapts on dense execution traces, gated by held-out oracles]]
