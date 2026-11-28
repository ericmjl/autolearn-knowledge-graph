---
type: "source-note"
title: "Notes on: Detecting Intent Drift in AI Agents With Runtime Behavioral Data - ARMO"
raw: "detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data-armo"
url: "https://www.armosec.io/blog/detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data/"
created_at: "2026-11-28T07:01:25Z"
updated_at: "2026-11-28T07:01:25Z"
---
- Archived full text: [[detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data-armo|Full archived text, with credits]]
- Link: <https://www.armosec.io/blog/detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data/>

## What it says

ARMO argues that behavioral baselines structurally fail for AI agents on Kubernetes and that intent drift must be detected at runtime. The four prerequisites baselines need (stable identity, stable topology, consistent workload shape, predictable patterns) are architecturally impossible for ephemeral agent pods: a 24-hour learning window against pods living minutes to hours leaves the tool perpetually in learning mode, and attacks hide in that window. Drift is distinguished from anomaly: a behavioral anomaly is a statistical outlier on a single event, while intent drift is a change in the agent's goals, visible only in correlated action chains (tool invocation -> data access -> external egress). ARMO's response combines eBPF kernel-layer observation (immediate, 1-2.5% CPU, 1% memory), Deployment-level baselines (Application Profile DNA) that persist across pod churn, application-layer context (prompts, tool parameters), runtime-derived AI-BOM, and attack story generation that assembles signals across the full stack into a narrative chain, cutting investigation time by over 90%.

## Claims drawn from this source

- **Per-pod behavioral baselines are perpetually in learning mode in production Kubernetes.** Classic baselines require ~24 hours of stable observation to converge, while median pod lifetime during active operations is minutes to a few hours, so the window where detection is strong is a fraction of total runtime.
- **Intent drift is a change in goals, visible only in action chains across layers.** An agent reading customer_pii and POSTing to an unknown endpoint performs both steps within baseline bounds; the shift appears in the combination and direction of events, not in any individual score.
- **Four mechanisms produce intent drift in production AI agents.** Prompt injection (fastest, often under thirty seconds), compromised dependencies, memory poisoning (gradual conditioning across sessions, zero alerts until final payload), and emergent behavior after model updates or prompt changes.
- **Deployment-level identity beats pod-level baselines.** Application Profile DNA attaches behavioral profiles to Kubernetes Deployments and ServiceAccounts so a new pod inherits the baseline immediately, with no learning window.
- **Kernel-level eBPF observation gives detection from the first syscall.** eBPF captures the syscall chain from the first moment the pod executes at 1-2.5% CPU and 1% memory overhead, independent of baseline convergence.
- **Runtime-derived AI-BOM turns CI/CD changes into observable events.** Instead of flagging every behavioral shift as an anomaly, ARMO's AI workload discovery tracks which model version, tools, and dependencies actually executed versus what was declared.
- **Attack story generation correlates full-stack signals into a single narrative.** Cloud, container, Kubernetes, and application events assemble into an investigation-ready story that reduces investigation and triage time by over 90%.
- **Kernel-level alone catches symptoms, not root cause.** Kernel-level signals miss prompt content, tool invocation parameters, and agent state; L7 application-layer context captures the why behind syscall activity.
