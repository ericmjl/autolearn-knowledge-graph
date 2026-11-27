---
title: "TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents"
type: "raw-source"
url: "https://arxiv.org/html/2610.41216v1"
author: "Kehong Gong"
publication: "arXiv"
published: "2026-10-22"
archived: "2026-11-27T10:01:01Z"
---

> [!quote] Original source
> **Author(s):** Kehong Gong  
> **Title:** TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents  
> **Published in:** arXiv  
> **Date:** 2026-10-22  
> **Original:** <https://arxiv.org/html/2610.41216v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-tinyastral-transferring-self-evolving-harnesses-to-tiny-generalist-manipulation-agents|Source note]]
Themes: [[Loop engineering]]
Why it was archived: How evolved harnesses transfer across models and what the mechanism is (question 1/0)

## Archived text

TinyAstral: Transferring Self-Evolving Harnesses

to Tiny Generalist Manipulation Agents

Abstract

Robot agents built on vision–language models depend on both the planner and its harness: the tools, feedback, memory, and recovery logic around it. Can improvements to a large teacher’s harness be carried into a compact agent with lower inference compute cost? We present TinyAstral, a two-stage approach. We first freeze an open-weight teacher and improve its harness through recursive self-improvement (RSI): frontier LLM agents read the teacher’s trajectories and propose harness edits, and each edit is accepted only if it passes a paired statistical test. We then freeze the final harness, collect teacher trajectories with reasoning and failure recovery, and distill a small student that replaces the teacher in the same harness. On RoboTwin, harness evolution raises the teacher’s success from 33.4% to 63.6%; the final 4B student reaches 62.8%. Across four harness versions, distilled 4B students score close to their corresponding teachers, and later versions yield stronger students, showing that harness evolution gains carry into compact models. The harness gains also transfer to other frozen planners without retraining. On identical episodes, the final 4B student outperforms open 4B agents, the open 27B harness-RSI model SenseNova-RoboRSI, and our own teacher model placed in three competitors’ harnesses. It stays close to its teacher on all three training benchmarks, and on three benchmarks never used for RSI or training it scores close to a 552B planner running the same harness. On the measured deployment episodes, it uses about one fifth of its teacher’s accelerator time.

1 Introduction

Vision–language models (VLMs) can operate robot arms by reading images and calling perception and motion tools [25, 18, 11, 12]. The model chooses the object, action sequence, and stopping point; the surrounding harness grounds these choices, executes them, and reports what happened. Tool interfaces, feedback, task memory, and failure recovery therefore contribute to the agent’s performance alongside the model itself [57, 40, 46, 10].

Two lines of work offer complementary ways to build these agents. Harness evolution improves the system around a frozen planner [40, 46, 10]; agent distillation trains compact models from a stronger agent’s trajectories [27, 24, 56]. We connect these approaches by asking: can we first improve a large teacher’s harness, then transfer the resulting decision-making capability to a small model? This would allow the improved system to run with substantially less inference compute.

We present TinyAstral, a family of 0.8B–4B manipulation agents built in two stages (Fig. 2). First, we freeze the weights of an open-weight teacher, Qwen3.8-Flash-Next [34], and improve its harness through a master-guided recursive self-improvement (RSI) loop. Humans specify the rules and budget in advance. Frontier LLM agents then inspect failures and propose harness edits, which the system automatically accepts or rejects according to pre-registered paired statistical tests. Second, we freeze the final harness and collect teacher trajectories containing reasoning, tool calls, and recovery from injected failures. Together with auxiliary offline real-robot supervision, these trajectories train a compact student to interpret feedback, choose actions, recover from failure, and decide when to finish. At deployment, the student replaces the teacher in the same frozen harness.

We evaluate both stages and the connection between them. Harness evolution raises the frozen teacher’s RoboTwin success from 33.4% to 63.6%, and distillation produces a 4B student at 62.8%. To test whether this connection holds beyond the final endpoint, we distill students at four harness versions. The four students score 36.2%, 49.8%, 60.0%, and 62.8%, each close to its corresponding teacher. The same evolved harness also improves DeepSeek-V4.1-Flash and the untrained 4B initialization, showing that its gains are reusable across planners. On identical episodes the student outperforms every open competitor we ran, including our own teacher model inside three competitors’ harnesses (93.6% vs. 78.9% on Guava; 78.3% vs. 57.3% and 53.0% on LIBERO-PRO), and on unseen benchmarks the small 4B student scores close to a 552B planner in the same harness.

Our contributions are:

- • 

Harness evolution followed by distillation. A two-stage approach first improves a frozen teacher’s manipulation harness, then trains a compact planner from that teacher’s reasoning and recovery trajectories for deployment in the same harness.

- • 

Evidence that evolution gains transfer. The harness improves other frozen planners, and distilled students at four harness versions track the performance of their corresponding teachers, showing that system improvements carry into compact models.

- • 

Compact agents with lower inference compute cost. A single TinyAstral-4B model covers six benchmarks: on identical episodes it outperforms every open competitor we ran, including our own teacher model inside three competitors’ harnesses, scores close to its teacher on the three training benchmarks and close to a 552B planner on unseen ones, and uses about one fifth of the teacher’s accelerator time per episode in our deployment measurement.

2 Related Work

Large models operating robots through a harness.

Language and vision-language models can operate robots by writing code or issuing tool calls over perception and motion primitives [25, 18, 11, 12], with spatial-reasoning models supplying grounding [32, 50]. Recent work shows that the harness around the model, namely its tool interface, feedback, memory, and recovery logic, is a first-order factor. Harness VLA [57] composes a frozen VLA with memory-guided agents, RoboDawn [14] and MotorMind [22] expose closed-loop interfaces to a general VLM, and PyRUA-Lean [37] cuts token cost with interactive code execution. A growing line also evolves the harness from execution traces: PhysEvo [40] runs recursive self-improvement around a single frozen model, HarnessPAI [46] evolves an executable program, ASPIRE [28] accumulates a skill library, and the two RoboRSI systems [10, 47] refine skills and agent components with validation before release. Concurrent with our work, SenseNova-RoboRSI [10] also trains a 27B VLM on validated interaction experience, and World Action Agent [56] distills the tool-call traces of its skill-evolved harness into a 9B VLM. We share the view that the harness is what improves while model weights stay fixed. TinyAstral differs in three ways: the harness of a locally hosted open-weight teacher evolves continually under paired statistical selection, its gains are measured across planners at successive snapshots, and the evolved teacher is distilled into 0.8B, 2B, and 4B students that stay close to it.

Small manipulation agents and VLAs.

End-to-end VLAs such as OpenVLA [21], \(\pi_{0}\) [3], and \(\pi_{0.5}\) [31] map observations directly to actions and are trained on large robot datasets, which makes them compact at inference but dependent on in-distribution demonstrations; benchmarks such as LIBERO-PRO [58] and RoboTwin 2.0 [8] probe how far they carry under perturbation. A second route trains a small model to be the agent instead. Guava [27] designs a manipulation harness and distills reasoning and recovery trajectories from a frontier VLM into a 4B open model, PyRUA-Lean [37] trains a 4B coder with GRPO on 45 LIBERO-PRO instances, and Robo-Harness K1 [24] and World Action Agent [56] fine-tune small VLM students on harness traces. TinyAstral first evolves the teacher harness and then freezes it for data collection and distillation. Distillation at several frozen snapshots tests whether the preceding harness improvements carry into student performance.

Self-improving agents and agent distillation.

Language agents can improve through stored experience and reflection [44, 36], and recent systems let a model rewrite its own scaffold or code: STOP [51], ADAS [17], Gödel Agent [49], and the Darwin Gödel Machine [54], following the classical notion of recursive self-improvement [13]; GEPA [2] reflects on execution traces to evolve prompts. ADAS also reports transfer of discovered agents across models and domains. TinyAstral evolves the tools, execution feedback, task memory, and recovery logic of a manipulation harness under paired statistical selection, and carries the evolved system into a tiny student. Knowledge distillation [15, 35] and its agent variants, FireAct [6] and AgentTuning [53], transfer trajectories from a strong language agent to a smaller one on text and tool-use tasks; Distilling Step-by-Step [16] uses teacher rationales as extra supervision, and BetterTogether [38] alternates prompt optimization with fine-tuning of the same model. We supervise rationales together with tool calls inside a closed-loop visual interaction history, and distill from a teacher whose harness has already been evolved, into a student of a different size.

3 Method

TinyAstral has two stages (Fig. 2). In the first, a master improves the harness of a frozen teacher through a statistically gated loop (Sec. 3.2). Once evolution ends, we freeze the final harness, collect teacher trajectories through it, and distill the resulting reasoning and recovery behavior into a compact student (Sec. 3.3). At deployment, the student replaces the teacher in the same harness. We first define the agent and its interface (Sec. 3.1).

3.1 Planner, harness, and scoring

Agent and harness.

A planner model \(\pi\) controls a robot through a harness \(H\). At turn \(t\) the harness gives \(\pi\) an observation \(o_{t}\), and \(\pi\) produces a reasoning trace followed by exactly one tool call \(a_{t}\). The harness executes the call and returns a structured result \(r_{t}\). The harness determines how an action is carried out: perception (SAM 3 segmentation [5] lifted to depth point clouds), grasp and placement geometry, collision-free motion planning, and closed-loop corrections. The planner determines what to do: which object, which part of it, which reference and spatial relation, which arm, in what order, and when the task is finished. The model never outputs joint angles or coordinates unless a tool explicitly requests them.

Observations combine camera images, the task instruction, recent tool results, and gripper state. Object-level tools provide grasping, placement, verification, and recovery primitives; the full interface is specified in Appendix G.

Autonomous termination and scoring.

The agent ends an episode itself by calling done with the predicates it believes hold (e.g. on(a,b), upright(a), lifted(a,cm)). The harness checks these predicates with the cameras and gripper sensors; if a check fails, it rejects the call and returns the measurement so the agent can keep working. After two rejections, the next done ends the episode without a check. An episode also ends if the agent calls give_up or exhausts its budget (30 tool calls on RoboTwin; per-benchmark limits in Appendix B). The environment’s success flag never enters the model’s input. Our primary metric, strict success \(S\), counts an episode only if the agent ended it with done and the benchmark’s success predicate holds in the final state. We also report ever success, which counts an episode if the task was achieved after any tool call.

3.2 Stage 1: Evolving the teacher harness

The self-improving system consists of the frozen teacher \(\pi_{T}\), the harness \(H\), and the master \(M\). Only \(H\) changes. The weights of \(\pi_{T}\) stay fixed throughout, and \(M\) does not act in the environment. Humans specify the rules (including the pre-registered acceptance criteria) and budget before the loop begins. The master is a set of frontier LLM agents that read trajectories, propose edits, implement them, and audit one another’s code. The system applies the pre-registered paired statistical tests to determine acceptance. Each round runs the current teacher, analyzes its failures, proposes edits, and tests a candidate against the current harness.

1. Read trajectories.

The current accepted harness \(H_{k}\) is run on development seeds. The master inspects the logged images, tool calls, tool results, and teacher reasoning, and assigns each failure to one of ten failure classes, such as off-target placement, false completion (done accepted but the final state fails), missing primitives, task-memory errors, and instance misidentification.

2. Propose edits.

For a target cluster of failing tasks, the master writes candidate components: new tools or primitives, more honest tool returns, perception fixes, failure handling, or local corrections to the task memory. Edits must be general. Code may not branch on the task name. In the final integration phase, the system prompt and existing tool descriptions must remain byte-identical to the parent. Memory may change only for the targeted tasks. In addition, every new component must fire through an explicit trigger that writes a component-specific marker to the log. A separate code audit verifies that, whenever the trigger does not fire, the candidate behaves step-for-step like the parent.

3. Test and accept edits.

Candidates are compared with the current harness on the same task/seed pairs. Training, selection, and evaluation seeds occupy disjoint ranges. The pre-registered gate requires positive evidence of improvement on targeted or triggered pairs and checks for regressions elsewhere; unsuccessful candidates are rejected or stopped early. The final integration phase accepted three of seven candidates. Evaluation seeds are excluded from acceptance tests. The acceptance rules and capability ledger are in Appendix E.

Task memory.

RoboTwin instructions often leave the success condition implicit (e.g. “lift” requires holding the object at least 10 cm up). For RoboTwin only, the harness therefore reads one short end-state note per task; the notes contain no actions or trajectories, are refined during RSI on development seeds, and are frozen and read-only at evaluation. The other five benchmarks, including all zero-shot ones, use no task memory.

From evolution to a frozen teacher system.

We number accepted main-line snapshots chronologically from the starting harness \(H_{0}\); the lineage proceeds through \(H_{16}\) to the final \(H^{*}\) (Tab. 8). These accepted versions are distinct from the 296 candidate capabilities and the seven integration cycles in the final phase. We freeze \(H^{*}\) before collecting the final teacher trajectories for distillation.

3.3 Stage 2: Collecting supervision from the frozen system

The teacher \(\pi_{T}\) collects trajectories through the frozen \(H^{*}\). These trajectories supervise a student \(\pi_{S}\) to reason about observations and feedback and choose the next tool call. The teacher weights and harness remain fixed during data collection and student training. The distillation recipe combines reasoning targets, recovery branches, strict-success filtering, and training samples exported from the exact harness interactions.

Keep the teacher’s reasoning.

Each training target supervises the teacher’s stated rationale together with its next tool call, i.e. \(\ldots\) and then the call. Emptying the reasoning text while keeping all samples identical lowers success by 19.3 pp on LIBERO-PRO, 11.2 pp on SimplerEnv Google VM, and 10.0 pp on VLABench (Sec. 4.4).

Recovery branches.

Successful episodes rarely show how to recover from failure, so we add recovery branches. Starting from a successful teacher episode, we replay its first \(k\) calls in a fresh simulator with the same seed, using the recorded results and without querying the model. At the branch point we inject a perturbation: on RoboTwin, the grasped object slips, or the target object is moved by 6–10 cm before the next grasp; on Guava and LIBERO, a grasp misses, a push falls short, or a placed object is displaced. The teacher then continues online. A branch is kept only if the perturbation took effect, the replay reproduced every recorded result code, and the teacher still reached strict success. Its samples begin at the first decision after the perturbation. On RoboTwin, branches are subsampled to 20% of the RoboTwin samples (3,471 branch and 13,857 main-episode samples).

Strict successes only.

Main episodes run at temperature \(0\), as in evaluation. A training seed on which the teacher fails is retried up to twice at temperature \(0.7\) with an unchanged prompt. We keep only episodes that the teacher ended with done and that the benchmark judges successful in the final state. Episodes that succeeded at some point but were later undone are discarded. Success labels are used offline for this selection and never appear in the training messages.

Offline real-robot supervision.

To expose the student to real images, we add offline data from public real-robot datasets (AgiBot World [1]; Fractal [4], BridgeData V2 [43], DROID [19], and Berkeley UR5 [7] from Open X-Embodiment [29]), cast as three auxiliary tasks in the harness format: state and failure judgment (27,918 samples), sub-goal planning (4,187), and next tool call (9,771). For next-call samples, we convert each recorded action sequence into a tool-call trajectory: gripper events and segment boundaries place the calls, and dataset annotations name the objects and spatial relations. Each step is rendered with the final harness’s observation and history format, so the student sees real scenes through the same interface it uses in simulation. The teacher then supplies the reasoning. It first predicts the call without seeing the reference; if the two match, its reasoning is kept. Otherwise, as in the rationalization step of STaR [52], it is given the reference call and asked to explain it, and the explanation is kept only if it passes consistency and quality checks. In both cases the dataset-derived call is the action target (details in Appendix F).

3.4 Student training and deployment

Teacher data comes from training seeds of all 50 RoboTwin tasks, the 7 seen Guava tasks, and LIBERO-90 [26]; the final set has 83,753 decision samples, half of them simulated (composition and hyper-parameters in Appendix F). We fine-tune all language-model parameters of Qwen3.5-4B [33] for 2 epochs; at deployment the student replaces the teacher inside the frozen harness, served in bf16 on one accelerator.

4 Experiments

We first show how harness evolution improves frozen planners and how distillation transfers these gains to compact students. We then compare the final student with its teacher and other agents, and test its generalization to unseen benchmarks. Finally, we analyze training ingredients, recovery behavior, and inference compute cost.

4.1 Setup

Benchmarks.

We report six benchmarks. Three belong to benchmark families that supply training data: RoboTwin 2.0 [8] with all 50 tasks \(\times\) 10 evaluation seeds (500 episodes), Guava [27] with 15 tasks \(\times\) 30 official seeds (450 episodes; 7 tasks seen in training, 8 unseen), and LIBERO-PRO [58] with 300 episodes (three LIBERO [26] suites, original and four perturbation types, 2 seeds each). Three are never touched by RSI or training and test zero-shot transfer: SimplerEnv [23] (Visual Matching, 960 episodes on the Google Robot and WidowX), VLABench [55] (the first 500 episodes of the official list over five tracks), and EB-Manipulation [48] (228 episodes). RoboTwin is also the RSI development benchmark. Acceptance decisions use only selection seeds; evaluation seeds (\(\geq 100{,}000\)) are disjoint from selection and training seeds (Sec. 3.2). Guava evaluation seeds are disjoint from our Guava training seeds, and LIBERO-PRO training data comes only from LIBERO-90.

Evaluation protocol.

We report strict success \(S\) (Sec. 3.1) on the three training benchmarks and each benchmark’s official success measure on the zero-shot benchmarks (Tab. 2). VLABench stops at the official success event and EB-Manipulation latches success; neither defines a final-state predicate after done. All rates use fixed denominators. Episodes with undetermined outcomes count as failures; upper bounds counting them as successes and ever success are reported in Tab. 5. Comparisons between systems we run are paired on identical (task, seed) episodes; published results are listed separately. We report success rates and paired differences in percentage points. Within our harness, all evaluated planners decode at temperature 0 and share perception and motion-planning services. Competitor implementations and benchmark-specific configurations are detailed in Appendix B.

4.2 Harness evolution and transfer to compact students

Experimental design.

We evaluate four harness versions, \(H_{1}\), \(H_{7}\), \(H_{16}\), and \(H^{*}\), on the same 500 RoboTwin episodes (Tab. 1). The teacher, DeepSeek-V4.1-Flash, and the untrained 4B planner keep their weights fixed across versions. For each version, we collect teacher trajectories under the same collection-budget constraints and independently train a student from the same Qwen3.5-4B checkpoint on successful episodes, using the same training recipe (Appendix F). Each student runs in its corresponding harness.

Harness evolution.

With teacher weights fixed, success rises from 33.4% under \(H_{1}\) to 63.6% under \(H^{*}\) (full lineage in Tab. 8). The gains also transfer to other planners: DeepSeek-V4.1-Flash [9], which was not the planner used during harness evolution, improves by 30.6 pp without model-specific harness changes. The untrained 4B planner improves from 14.6% to 41.2%. All three improve across the four measured versions.

Distilling evolution gains.

We train a separate 4B student for each harness version. Student success increases from 36.2% at \(H_{1}\) to 62.8% at \(H^{*}\), with each student scoring close to its corresponding teacher (Tab. 1). Thus, improvements to the teacher’s harness carry into the distilled students. Within the final harness \(H^{*}\), the distilled student also outperforms the untrained 4B model by 21.6 percentage points (62.8% vs. 41.2%), showing the additional benefit of distillation.

4.3 Performance and generalization

Student versus teacher.

TinyAstral-4B stays close to its teacher on all three training benchmarks: 62.8% vs. 63.6% on RoboTwin, 93.6% vs. 94.7% on Guava, and 78.3% vs. 80.0% on LIBERO-PRO (Tab. 2). In the same harness, it also improves over the untrained 4B model by 18.4 pp on Guava and 42.0 pp on LIBERO-PRO; counting all undetermined outcomes as successes raises the untrained model’s LIBERO-PRO score to at most 57.3%.

Comparison with other agents.

On the same evaluation episodes, TinyAstral-4B outperforms the tested open agents, including Guava-4B, PyRUA-Lean-4B, and SenseNova-RoboRSI-27B (Tab. 2). It also exceeds systems using our teacher model, Qwen3.8-Flash-Next, in other harnesses: 93.6% vs. 78.9% for the Guava harness, and 78.3% vs. 57.3% and 53.0% for MotorMind and PyRUA-Lean on LIBERO-PRO. PyRUA-Lean-4B is trained and self-evaluated with a per-step environment success signal; without this signal, which our protocol withholds, it often declares success prematurely. These results highlight the contribution of the evolved harness and distilled policy to the final system’s performance. Competitor-specific execution and scoring protocols are detailed in Appendix B.

Generalization to unseen benchmarks.

TinyAstral-4B also generalizes to three benchmarks never used for RSI or training: SimplerEnv, VLABench, and EB-Manipulation. Its success rates are within 5.0 pp of its teacher and within 2.4 pp of the 552B DeepSeek-V4.1-Flash, all using the same harness (Tab. 2). Compared with the untrained 4B model, distillation improves performance across all four evaluation settings, with gains of 10.0 pp on SimplerEnv Google VM and 13.6 pp on VLABench. Despite receiving no training on these benchmarks, the student also exceeds published results from \(\pi_{0}\)-FAST [30] on both SimplerEnv robots and \(\pi_{0}\) [3] on VLABench, although these baselines were fine-tuned on in-domain data (protocol details in Appendix C).

Smaller students.

TinyAstral-0.8B reaches 61.8% on RoboTwin and 93.8% on Guava, close to the 4B student, but falls to 54.7% on LIBERO-PRO compared with 78.3%. On the zero-shot benchmarks, both the 0.8B and 2B students remain within 3.0 pp of the 4B model across all four settings. The effect of model size is therefore most pronounced on LIBERO-PRO among the evaluated benchmarks (Tab. 2).

4.4 Ablations and recovery behavior

Teacher reasoning.

Keeping the teacher’s reasoning has the largest measured effect among our ablations (Tab. 3). Removing the reasoning text while keeping all training samples otherwise unchanged lowers success by 19.3 pp on LIBERO-PRO, 11.2 pp on SimplerEnv Google VM, and 10.0 pp on VLABench. On LIBERO-PRO, 49 of 300 episodes end at the call limit without reasoning, compared with 7 under the full recipe.

Auxiliary real-robot supervision.

Adding real-robot data raises next-call accuracy on held-out real-robot episodes from 0.235 to 0.923, with no statistically detectable change in success across the seven simulated settings (Tab. 3). Its measured benefit is in offline decisions on real observations.

Behavior under failure.

The student responds to failures by re-describing target objects, correcting placements, and changing grasp points, in both training and unseen benchmarks (Figs. 3, 4 and 5). The same student also runs in closed loop on a real SO-ARM101 arm, sorting two balls into matching boxes and stacking three tape rolls (Fig. 3, top). Of the 271 zero-shot episodes solved by the student but not by the untrained 4B model in the same harness, 171 (63%) end with the untrained model exhausting its call budget. Additional examples, including a failure, are shown in Figs. 4 and 5.

4.5 Inference compute cost

We measure inference compute cost as planner accelerators multiplied by median episode duration, using the same 20 SimplerEnv episodes for each system. In their deployed configurations, the student uses 25.3 accelerator\(\cdot\)s against 123.8 for the teacher (4.9\(\times\)) and 249.6 for DeepSeek-V4.1-Flash (9.9\(\times\)), and its median episode is also the shortest (25.3 s vs. 31.0 and 31.2 s; Tab. 4). The 4B student is served in bf16 on one accelerator without quantization or speculative decoding; the teacher uses four accelerators with FP8 weights and tensor parallelism, and DeepSeek-V4.1-Flash uses eight.

5 Conclusion

TinyAstral first improves a frozen teacher through harness evolution, then distills its reasoning and recovery behavior into a compact student deployed in the final harness. Across four harness versions, students trained from later versions perform better and stay close to their corresponding teachers, showing that harness improvements carry into compact agents. The harness gains also transfer to other frozen planners. The final 4B student outperforms every open competitor we ran on identical episodes, stays close to its teacher on three training benchmarks, scores close to a 552B planner on unseen benchmarks, and uses about one fifth of the teacher’s accelerator time in our deployment measurement. These results support harness evolution followed by distillation as a route to capable robot agents with lower inference compute cost. Future work will extend the approach to more RSI environments.

References

- [1] (2025) AgiBot World Colosseo: a large-scale manipulation platform for scalable and intelligent embodied systems. In 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), Note: arXiv:2503.06669 External Links: Document Cited by: §3.3.
- [2] (2026) GEPA: reflective prompt evolution can outperform reinforcement learning. In International Conference on Learning Representations (ICLR), Note: arXiv:2507.19457 Cited by: §2.
- [3] (2025) \(\pi_{0}\): A vision-language-action flow model for general robot control. In Robotics: Science and Systems (RSS), Note: arXiv:2410.24164 Cited by: Table 7, Table 7, Table 7, §2, §4.3.
- [4] (2023) RT-1: robotics transformer for real-world control at scale. In Robotics: Science and Systems (RSS), Note: arXiv:2212.06817 External Links: Document Cited by: §3.3.
- [5] (2026) SAM 3: segment anything with concepts. In International Conference on Learning Representations (ICLR), Note: arXiv:2511.16719 Cited by: §3.1.
- [6] (2023) FireAct: toward language agent fine-tuning. arXiv preprint arXiv:2310.05915. External Links: 2310.05915 Cited by: §2.
- [7] (2023) Berkeley UR5 demonstration dataset. Note: https://sites.google.com/view/berkeley-ur5/home Cited by: §3.3.
- [8] (2025) RoboTwin 2.0: a scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. arXiv preprint arXiv:2506.18088. External Links: 2506.18088 Cited by: §2, §4.1.
- [9] (2026) DeepSeek-V4.1-Flash: pushing the limits of KV cache compression. External Links: Link Cited by: §4.2.
- [10] (2026) SenseNova-RoboRSI: recursive self-improvement for embodied agents. Note: GitHub repository External Links: Link Cited by: §1, §1, §2, Table 2.
- [11] (2024) MOKA: Open-World robotic manipulation through Mark-Based visual prompting. In Robotics: Science and Systems (RSS), Note: arXiv:2403.03174 External Links: Document Cited by: §1, §2.
- [12] (2026) CaP-X: a framework for benchmarking and improving coding agents for robot manipulation. arXiv preprint arXiv:2603.22435. External Links: 2603.22435 Cited by: Table 7, §1, §2.
- [13] (1966) Speculations concerning the first ultraintelligent machine. In Advances in Computers, Vol. 6, pp. 31–88. External Links: Document Cited by: §2.
- [14] (2026) Transferring the intelligence of VLMs to robotic control. arXiv preprint arXiv:2609.22966. External Links: 2609.22966 Cited by: Table 7, Table 7, Table 7, Table 7, §2, Table 2, Table 2.
- [15] (2015) Distilling the knowledge in a neural network. arXiv preprint arXiv:1503.02531. External Links: 1503.02531 Cited by: §2.
- [16] (2023) Distilling Step-by-Step! outperforming larger language models with less training data and smaller model sizes. In Findings of the Association for Computational Linguistics: ACL 2023, pp. 8003–8017. Note: arXiv:2305.02301 External Links: Document Cited by: §2.
- [17] (2025) Automated design of agentic systems. In International Conference on Learning Representations (ICLR), Note: arXiv:2408.08435 Cited by: §2.
- [18] (2023) VoxPoser: composable 3D value maps for robotic manipulation with language models. In Conference on Robot Learning (CoRL), Note: arXiv:2307.05973 Cited by: §1, §2.
- [19] (2024) DROID: a large-scale in-the-wild robot manipulation dataset. In Robotics: Science and Systems (RSS), Note: arXiv:2403.12945 External Links: Document Cited by: §3.3.
- [20] (2025) Robot-R1: reinforcement learning for enhanced embodied reasoning in robotics. In Advances in Neural Information Processing Systems (NeurIPS), Note: arXiv:2506.00070 Cited by: Table 7.
- [21] (2024) OpenVLA: an Open-Source Vision-Language-Action model. In Conference on Robot Learning (CoRL), Note: arXiv:2406.09246 Cited by: §2.
- [22] (2026) MotorMind: scaffolding general vision language models for Zero-Shot robot manipulation. arXiv preprint arXiv:2609.38078. External Links: 2609.38078 Cited by: Table 7, Table 7, Table 7, §2, Table 2, Table 2.
- [23] (2024) Evaluating Real-World robot manipulation policies in simulation. In Conference on Robot Learning (CoRL), Note: arXiv:2405.05941 Cited by: §4.1.
- [24] (2026) Robo-Harness K1: harnessing Robot-Use agents via perception augmentation. arXiv preprint arXiv:2609.29389. External Links: 2609.29389 Cited by: Table 7, §1, §2.
- [25] (2023) Code as policies: language model programs for embodied control. In 2023 IEEE International Conference on Robotics and Automation (ICRA), Note: arXiv:2209.07753 External Links: Document Cited by: §1, §2.
- [26] (2023) LIBERO: benchmarking knowledge transfer for lifelong robot learning. In Advances in Neural Information Processing Systems (NeurIPS), Note: arXiv:2306.03310 Cited by: §3.4, §4.1.
- [27] (2026) Guava: distilling frontier VLMs into a compact agent through a robotic manipulation harness. arXiv preprint arXiv:2606.18363. External Links: 2606.18363 Cited by: Appendix B, Table 6, Table 7, Table 7, Table 7, §1, §2, §4.1, Table 2, Table 2, Table 2.
- [28] (2026) ASPIRE: agentic /Skills discovery for robotics. arXiv preprint arXiv:2607.00272. External Links: 2607.00272 Cited by: Table 7, §2.
- [29] (2024) Open X-Embodiment: robotic learning datasets and RT-X models. In 2024 IEEE International Conference on Robotics and Automation (ICRA), Note: arXiv:2310.08864 External Links: Document Cited by: §3.3.
- [30] (2025) FAST: efficient action tokenization for vision-language-action models. In Robotics: Science and Systems (RSS), Note: arXiv:2501.09747 External Links: Document Cited by: Table 7, Table 7, Table 7, §4.3, Table 2.
- [31] (2025) \(\pi_{0.5}\): A vision-language-action model with open-world generalization. In Conference on Robot Learning (CoRL), Note: arXiv:2504.16054 Cited by: §2.
- [32] (2025) SoFar: Language-Grounded orientation bridges spatial reasoning and object manipulation. In Advances in Neural Information Processing Systems (NeurIPS), Note: arXiv:2502.13143 External Links: Document Cited by: Table 7, §2, Table 2.
- [33] (2026) Qwen3.5: towards native multimodal agents. External Links: Link Cited by: §3.4.
- [34] (2026) Qwen3.8-Flash-Next: a new architecture, towards ultimate cost-efficiency. Note: Hugging Face model card, https://huggingface.co/Qwen/Qwen3.8-Flash-Next External Links: Link Cited by: §1.
- [35] (2019) DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. arXiv preprint arXiv:1910.01108. External Links: 1910.01108 Cited by: §2.
- [36] (2023) Reflexion: language agents with verbal reinforcement learning. In Advances in Neural Information Processing Systems (NeurIPS), Note: arXiv:2303.11366 External Links: Document Cited by: §2.
- [37] (2026) Fewer tokens, better action: GPT-6 Astra robot agents with 14% higher success rate but 65% fewer tokens. arXiv preprint arXiv:2610.01939. External Links: 2610.01939 Cited by: Appendix B, Table 7, Table 7, Table 7, §2, §2, Table 2, Table 2, Table 2.
- [38] (2024) Fine-Tuning and prompt optimization: two great steps that work better together. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP), Note: arXiv:2407.10930 External Links: Document Cited by: §2.
- [39] (2026) StarVLA: a Lego-like codebase for Vision-Language-Action model developing. arXiv preprint arXiv:2604.05014. External Links: 2604.05014 Cited by: Table 7, Table 7, Table 7.
- [40] (2026) PhysEvo: astra can act, let it. arXiv preprint arXiv:2610.08995. External Links: 2610.08995 Cited by: §1, §1, §2.
- [41] (2025) VLABench/pi0-fast-ft-primitive-10task-deltachunk: \(\pi_{0}\)-FAST fine-tuned on VLABench primitive tasks. Note: Hugging Face model card, https://huggingface.co/VLABench/pi0-fast-ft-primitive-10task-deltachunkAccessed 2026-10-22 Cited by: Table 7.
- [42] (2025) VLABench/pi0-primitive-10task: \(\pi_{0}\) fine-tuned on VLABench primitive tasks. Note: Hugging Face model card, https://huggingface.co/VLABench/pi0-primitive-10taskAccessed 2026-10-22 Cited by: Table 7.
- [43] (2023) BridgeData V2: a dataset for robot learning at scale. In Conference on Robot Learning (CoRL), Note: arXiv:2308.12952 Cited by: §3.3.
- [44] (2024) Voyager: an Open-Ended embodied agent with large language models. Transactions on Machine Learning Research (TMLR). Note: arXiv:2305.16291 Cited by: §2.
- [45] (2026) Self-evolving embodied agents via Skill-Harness evolution. arXiv preprint arXiv:2608.11350. External Links: 2608.11350 Cited by: Table 7.
- [46] (2026) HarnessPAI: an evolving harness for physical AI. arXiv preprint arXiv:2609.29166. External Links: 2609.29166 Cited by: §1, §1, §2.
- [47] (2026) RoboRSI: stable, efficient, and reusable robot self-evolution in complex real-world environments. arXiv preprint arXiv:2610.12424. External Links: 2610.12424 Cited by: §2.
- [48] (2025) EmbodiedBench: comprehensive benchmarking multi-modal large language models for Vision-Driven embodied agents. In International Conference on Machine Learning (ICML), Note: arXiv:2502.09560 Cited by: Table 7, Table 7, §4.1, Table 2.
- [49] (2025) Gödel agent: a self-referential agent framework for recursive self-improvement. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL), Note: arXiv:2410.04444 Cited by: §2.
- [50] (2026) Embodied-R1: reinforced embodied reasoning for general robotic manipulation. In International Conference on Learning Representations (ICLR), Note: arXiv:2508.13998 Cited by: §2.
- [51] (2024) Self-Taught optimizer (STOP): recursively Self-Improving code generation. In Conference on Language Modeling (COLM), Note: arXiv:2310.02304 Cited by: §2.
- [52] (2022) STaR: bootstrapping reasoning with reasoning. In Advances in Neural Information Processing Systems (NeurIPS), Cited by: §3.3.
- [53] (2024) AgentTuning: enabling generalized agent abilities for LLMs. In Findings of the Association for Computational Linguistics: ACL 2024, Note: arXiv:2310.12823 External Links: Document Cited by: §2.
- [54] (2026) Darwin Gödel Machine: open-ended evolution of self-improving agents. In International Conference on Learning Representations (ICLR), Note: arXiv:2505.22954 Cited by: §2.
- [55] (2025) VLABench: a Large-Scale benchmark for Language-Conditioned robotics manipulation with Long-Horizon reasoning tasks. In 2025 IEEE/CVF International Conference on Computer Vision (ICCV), Note: arXiv:2412.18194 External Links: Document Cited by: §4.1.
- [56] (2026) World action agent: harnessing VLMs for robot manipulation via world action rehearsal. arXiv preprint arXiv:2609.29964. External Links: 2609.29964 Cited by: Table 7, Table 7, §1, §2, §2, Table 2, Table 2.
- [57] (2026) Harness VLA: steering frozen VLAs into reliable manipulation primitives via Memory-Guided agents. arXiv preprint arXiv:2607.08448. External Links: 2607.08448 Cited by: Table 7, Table 7, §1, §2.
- [58] (2025) LIBERO-PRO: towards robust and fair evaluation of Vision-Language-Action models beyond memorization. arXiv preprint arXiv:2510.03827. External Links: 2510.03827 Cited by: §2, §4.1.

Supplementary Material 

Appendix A All runs

Appendix B Competitor protocols

Our budgets.

Every planner run in our harness uses the same per-episode tool-call limit on a given benchmark (Tab. 6). Guava uses its official per-task round limits; the other limits were set by us before evaluation.

Competitors.

All competitors run from their released code and weights on our accelerators; no closed-source API is used. Guava-4B [27] runs in the official Guava harness (weights at revision 19a8c77, official prompt and parser, temperature 0) on our 450 Guava episodes, with the same per-task round limits; its result is re-scored with our unified metric (380/450). PyRUA-Lean-4B [37] runs in its official harness on all 500 RoboTwin episodes, whose task/seed pairs match ours one to one, and is scored with the same strict metric (64/500; it calls finish in 478 episodes; 20 episodes with undetermined outcomes count as failures).

Same teacher in alternative systems.

Guava harness with Qwen3.8-Flash-Next uses the official prompt and parser with medium reasoning effort and default sampling, whereas our teacher uses its default xhigh reasoning and temperature 0. Both allow 25/30 calls per task. MotorMind with this planner uses its official stop-on-success protocol and uncapped calls (median 77, compared with 8 for our student on LIBERO-PRO). PyRUA-Lean with this planner uses benchmark-trained VLA executors and allows 30/40 calls on RoboTwin/LIBERO-PRO; it runs on all 500 RoboTwin episodes (91/500) and our 300 LIBERO-PRO episodes, and its reported success requires finish(success) and final-state success.

Additional competitor metrics.

For PyRUA-Lean-4B on LIBERO-PRO, we report its final-state success, 53/300 (17.7%), marked separately in Tab. 2; 38 of these episodes also end with finish(success). SenseNova-RoboRSI-27B runs with its official stop-on-success rule, 40 policy calls, and an empty task-memory package, and reaches 211/300.

Appendix C Published comparisons

Table 7 lists published results on our six benchmarks together with the advantages each system uses over our setting.

Appendix D More qualitative examples

Appendix E RSI details

Table 8 lists the accepted snapshots of the main lineage. Their acceptance rules and the capability ledger follow.

Direction screen.

Candidates first pass a cheap direction screen on small seed blocks. A candidate is discarded if the task-averaged 95% upper bound of its gain on the target cluster falls below \(+2\) pp. Surviving components are merged into one candidate \(H^{\prime}\). \(H^{\prime}\) and its parent \(H_{k}\) then run concurrently, interleaved on the same \(\sim\)1,150 pre-registered (task, seed) pairs, so that the two arms share load and infrastructure conditions.

Statistical verdict.

Let \(J\) denote the pairs in the target cluster together with the non-target pairs in which a candidate marker fired, and let \(U\) denote the remaining pairs. \(H^{\prime}\) is accepted if (i) the one-sided 97.5% lower bound of the paired gain on \(J\), computed by a task-clustered bootstrap, is positive, and (ii) the net number of wins on the target cluster is positive. \(H^{\prime}\) is vetoed if the untriggered set \(U\) regresses by at least 2 pp with a two-sided 95% upper bound below zero. At the halfway point, the test stops for futility if the net gain on \(J\) is non-positive or the conditional power falls below 10%. The number of pairs is fixed in advance.

Capability ledger.

Every candidate is recorded in a ledger with the failure that triggered it, its proposer, its acceptance evidence, and its fate. Over the whole run, the master proposed 296 candidate capabilities. Of these, 121 were adopted, 16 were adopted and later superseded, 142 were rejected, and 17 remained undecided. The final harness contains 101 capabilities, 87 verbatim and 14 in a successor form; almost all adopted capabilities missing from it were accepted on side branches that were never merged into the main line.

Appendix F Training details

The 41,877 simulated samples comprise 13,857 RoboTwin, 9,054 Guava, and 11,159 LIBERO main-episode samples, plus 3,471, 2,048, and 2,288 recovery-branch samples, respectively. Each sample is one decision, with the loss applied only to the final assistant turn. The vision encoder and projector stay frozen. Training uses learning rate \(10^{-5}\) with cosine decay and 5% warm-up, a global batch of 32, and a maximum length of 12,288 tokens. The 2B and 0.8B students are trained on the same data with the same recipe.

Real-robot next-call pool.

Explanations given the reference call are rejected if they refer to the supplied answer, claim unmeasured success, omit the target object or required reference, or violate the length and format constraints. Next-call relabeling retained 19,598 of 23,070 candidate steps: 4,509 whose reasoning comes from a matching first prediction and 15,089 explained given the reference call. The 9,771 next-call training samples are drawn from this pool.

Appendix G Harness interface details

Observations.

On RoboTwin, \(o_{t}\) contains RGB images from the head camera and both wrist cameras, the task instruction together with the names of scene objects, a proprioceptive line with the measured gripper state of each arm, the result \(r_{t-1}\) of the previous call, and a counter of calls used. Images are kept for the two most recent turns only. Earlier turns retain their text, and earlier assistant messages retain only the tool call, without reasoning. On RoboTwin the first turn also includes the task note (Sec. 3.2). Guava and LIBERO-PRO use the same planner loop and tool semantics through benchmark adapters, keeping the three most recent single-view images.

Tools.

The RoboTwin harness exposes object-level tools: locate, grasp (with an optional part such as handle, rim, or end), place and carry (relative to a reference object, with optional facing or turning), handover, lift, articulate, press, push, pour, move, release, home, bimanual (two calls executed in parallel), verify, done, and give_up. Tools report what they measured rather than what they intended. For example, place re-measures the object after release and returns OFF_TARGET with the offset if the object missed its target. A check whose value cannot be measured reliably is returned as unknown (ok=null) rather than as a pass.
