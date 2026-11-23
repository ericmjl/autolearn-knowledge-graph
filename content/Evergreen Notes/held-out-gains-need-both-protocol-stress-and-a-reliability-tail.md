---
type: "evergreen"
title: "Held-out gains need both protocol stress and a reliability tail"
created_at: "2026-11-23T13:03:34Z"
updated_at: "2026-11-23T13:03:34Z"
inputs: ["notes-on-beyond-prompts-measuring-and-optimizing-llm-tool-agent-harnesses", "held-out-tasks-still-share-one-protocol-so-harness-gains-need-protocol-stress-tests"]
provenance_urls: ["https://arxiv.org/html/2609.05736v2", "https://arxiv.org/abs/2609.18366", "https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How do harness-evolution methods like CHASE systematically generate protocol perturbations that preserve task semantics, and does the approach help when a benchmark has no known shortcuts?"]
---
Agent synthesis

Held-out harness gains need both a protocol stress-test and a reliability tail, because held-out scoring alone hides gains that live in the protocol and rewards optimizers that occasionally stumble onto a strong harness. The protocol from the new source note reports mean held-out lift, worst-condition lift, repeatability, logged search cost, and a budgeted reliable-lift estimator RelLift95(B) under repair/gate/scorecard splits with the scorecard touched once. Mean lift is a discovery statistic, not a deployment promise: BetterHarness found the best individual harnesses on both tau^2 domains yet returned a selected tail of WorstLift -13.5 pp with negative RelLift95, while PRISM gave up some peak and kept a positive selected tail on all three benchmarks.

The two blind spots have different mechanisms. CHASE names the protocol-side one: a harness whose gain comes from formatting conventions survives held-out scoring unchanged, so a Challenger searches for a protocol change that preserves the tasks but cuts the updated harness's gain over the initial harness, with executable checks confirming the transformation before the loss is trusted; on SWE-Bench Pro V2, changing issue formatting and tool-output field order drops HarnessEvolve's gain from 8.57 to 3.81 points, while CHASE keeps 10.48 of its 11.43-point gain. The PRISM protocol names the selection-side one: under budget B, the deployer picks the run with the best pre-scorecard statistic, and RelLift95(B) is the 5th-percentile selected held-out lift over repeated uses, so a harness that is often good-only-on-lucky-draws never clears the gate.

The synthesis is a two-axis gate for harness claims. First, perturb the protocol and report retained gain next to the held-out score. Second, repeat the protocol and report the lower tail of the selected harness (WorstLift, repeatability, budgeted RelLift95) next to the mean. A defensible harness gain is one that holds up on both axes, the dense-oracle rule with the protocol stress-test added and the selection lottery made visible (see: held-out tasks still share one protocol, so harness gains need protocol stress-tests). Before crediting any evolved harness, ask the two questions: does it survive a protocol change, and does the optimizer reliably select it rather than occasionally find it?

## Where it comes from

- [[notes-on-beyond-prompts-measuring-and-optimizing-llm-tool-agent-harnesses|Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses]]

## What this builds on

- [[held-out-tasks-still-share-one-protocol-so-harness-gains-need-protocol-stress-tests|Held-out tasks still share one protocol, so harness gains need protocol stress-tests]]
