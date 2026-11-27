---
type: "source-note"
title: "Notes on: TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents"
raw: "tinyastral-transferring-self-evolving-harnesses-to-tiny-generalist-manipulation-agents"
url: "https://arxiv.org/html/2610.41216v1"
created_at: "2026-11-27T10:01:29Z"
updated_at: "2026-11-27T10:01:29Z"
---
- Archived full text: [[tinyastral-transferring-self-evolving-harnesses-to-tiny-generalist-manipulation-agents|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2610.41216v1>

## What it says

TinyAstral shows that a robot harness evolved around a frozen teacher can carry its gains into a tiny distilled student. A frontier master loop rewrites an open-weight teacher's harness (tools, feedback, task memory, recovery logic) under pre-registered paired statistical tests; the frozen final harness then collects teacher trajectories (reasoning, tool calls, injected-failure recovery), which train a 0.8B-4B student deployed in the same harness. Evolution lifts the teacher from 33.4% to 63.6% strict success on RoboTwin, the 4B student reaches 62.8%, students at four harness versions track their teachers, harness gains transfer to other frozen planners, and the deployed student uses about one fifth of its teacher's accelerator time.

## Claims drawn from this source

- **Harness evolution lifts a frozen teacher without touching model weights.** Only the harness H changes: the teacher weights (Qwen3.8-Flash-Next) stay fixed, humans pre-register rules and acceptance criteria, and frontier LLM agents inspect failures, classify them into ten failure classes, and propose tool/perception/memory edits accepted only by paired statistical tests on disjoint training/selection/evaluation seeds.
- **The evolved 4B student reaches near-teacher performance and uses about a fifth of its accelerator time.** Evolution raises the teacher from 33.4% (H1) to 63.6% (H*) strict success on RoboTwin; the 4B student reaches 62.8%, stays close on the training benchmarks (93.6% vs 94.7% Guava; 78.3% vs 80.0% LIBERO-PRO), and runs at 25.3 accelerator-seconds vs 123.8 for the teacher in deployment.
- **Harness evolution gains transfer to other frozen planners without retraining.** The same evolved harness improves DeepSeek-V4.1-Flash (not used during evolution) by 30.6 pp and the untrained 4B planner from 14.6% to 41.2%; the final student also outperforms the teacher inside competitors' harnesses (93.6% vs 78.9% on Guava; 78.3% vs 57.3% and 53.0% on LIBERO-PRO).
- **Students trained at later harness versions score higher, tracking their teacher.** Four independently trained 4B students (H1, H7, H16, H*) score 36.2%, 49.8%, 60.0%, and 62.8% on RoboTwin, each close to its corresponding teacher, showing system improvements carry into compact models.
- **Keeping the teacher's reasoning text is the largest single ablation effect.** Removing the reasoning text while keeping all training samples otherwise unchanged lowers success by 19.3 pp on LIBERO-PRO (49 of 300 episodes hit the call limit without reasoning versus 7 with it), 11.2 pp on SimplerEnv Google VM, and 10.0 pp on VLABench.
- **Recovery branches teach failure recovery without model queries at replay.** From a successful episode the teacher's first k calls are replayed in a fresh simulator using recorded results without querying the model; a perturbation (object slip, 6-10 cm displacement, missed grasp) is injected, and the branch is kept only if the perturbation took effect, the replay reproduced every recorded result code, and the teacher still reached strict success.
