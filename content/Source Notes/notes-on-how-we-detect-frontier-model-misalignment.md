---
type: "source-note"
title: "Notes on: How we detect frontier model misalignment"
raw: "how-we-detect-frontier-model-misalignment"
url: "https://openai.com/index/how-we-detect-frontier-model-misalignment/"
created_at: "2026-11-25T02:02:21Z"
updated_at: "2026-11-25T02:02:21Z"
---
- Archived full text: [[how-we-detect-frontier-model-misalignment|Full archived text, with credits]]
- Link: <https://openai.com/index/how-we-detect-frontier-model-misalignment/>

## What it says

OpenAI describes how its multi-layer monitoring system detects frontier-model misalignment across training, evaluation, and internal and external deployment. Lightweight activation probes at layer 0 pass flagged cases to a model-based reviewer at layer 1 and onward to investigative agents and automated investigations that compare the transcript with network logs and system telemetry. Flagged cases escalate to humans or trigger automatic pauses of the affected workload, while unflagged traffic is audited at a small random rate to catch probes that miss unfamiliar behavior. Monitoring is deliberately asynchronous and keeps rewards unchanged so that alerts don't create an incentive to conceal misalignment.

## Claims drawn from this source

- **Misalignment monitoring follows a multilayer architecture, cheap first, expensive later.** Layer 0 uses lightweight activation probes tuned for high recall; layer 1 runs a model-based reviewer over the agent's recent conversation, chain of thought, and tool use; layer 2 sends flagged cases to an investigative agent that can read full transcripts across context windows and run code in an isolated environment; layer 3 for sensitive workloads compares transcripts with network logs and telemetry.
- **Probes are deliberately sensitive and audited.** Layer 0 probes accept false alarms to reduce the chance of missing concerning behavior, and a random 5 percent of unflagged traffic is sent to the next layer so reviewers can identify behavior probes may have missed.
- **Frontier RL runs and internal Codex traffic skip the probe layer.** Because probes are sensitive, frontier reinforcement-learning runs and internal Codex traffic proceed directly to the next layer.
- **Reviewer checks run at each turn and on context summarization, targeting at most 30 minutes apart.** Frontier RL runs and internal Codex traffic get an L1 check at the end of each turn and whenever the agent summarizes its earlier work to make room in the context window; the schedule is moving to no more than 30 minutes between checks.
- **Sensitive workloads add a layer that compares transcripts with outside evidence.** At L3, the security investigator compares the transcript with network logs, other system telemetry, and evidence from earlier cases to decide whether to alert a human responder; alignment reviewers also compare reports across cases to find serious failures and recurring patterns.
- **Paging is limited and selective, and critical alerts can auto-pause workloads.** Highest-priority security alerts reach security and training teams typically within 15 minutes of the initial alert; frontier RL runs can page at any hour, most other traffic is limited to business hours, and internal Codex traffic has paging disabled. Some critical alerts automatically pause the affected workload without waiting for a responder, with a broader safeguard in development that pauses affected activity if responders have not ruled out a highest-priority alert within 30 minutes.
- **Monitoring is designed so that flagging does not reward concealment.** When a training sample triggers the monitors, its RL reward is left alone and the sample stays in training, and monitoring is asynchronous so samples that prompted longer investigations are not disadvantaged; the system can still pause, terminate, or roll back a run when monitors find a serious problem, but leaves rewards unchanged at the sample level.
- **External deployments do not routinely escalate to OpenAI humans and can pause conversation instead.** External misalignment monitoring does not routinely escalate flagged cases to human reviewers at OpenAI; where automatic intervention is supported, the system can pause the affected conversation and hand the user information to review, and enterprise customers can configure webhook alerts to their own security teams. Pause decisions depend on conversation-tracking mechanisms, and this system does not cover Chat Completions API requests.
- **The system is validated with replayed incidents, simulated attacks, audits, and red-teaming.** Recorded incidents, simulated attacks (OAI-repo Sabotage v2 and Sneaky Sandbox Escape), random traffic audits, and red-teaming by METR and Redwood Research are used to evaluate performance; recall at each threshold is tracked on a central dashboard and proposed monitoring changes are tested before deployment.
