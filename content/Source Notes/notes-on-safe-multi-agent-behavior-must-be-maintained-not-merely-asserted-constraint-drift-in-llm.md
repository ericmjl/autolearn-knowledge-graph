---
type: "source-note"
title: "Notes on: Safe Multi-Agent Behavior Must Be Maintained, Not Merely Asserted: Constraint Drift in LLM-Based Multi-Agent Systems"
raw: "safe-multi-agent-behavior-must-be-maintained-not-merely-asserted-constraint-drift-in-llm"
url: "https://arxiv.org/html/2605.10481v1"
created_at: "2026-11-23T19:01:54Z"
updated_at: "2026-11-23T19:01:54Z"
---
- Archived full text: [[safe-multi-agent-behavior-must-be-maintained-not-merely-asserted-constraint-drift-in-llm|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2605.10481v1>

## What it says

The paper argues that many failures in LLM-based multi-agent systems share a common structure: safety-critical constraints lose their operational force as they pass through memory, delegation, communication, tool use, audit, and optimization. It names this 'constraint drift' and distinguishes it from reward hacking and goal misgeneralization, which concern flawed objectives rather than preservation failures. It proposes Constraint State Governance (CSG): constraints as signed, versioned tokens with identity, scope, predicate, priority, and expiry, checked against the current signed state digest before critical actions, recorded for audit, and supplied to learning. An AgentLeak replay of 4,979 traces shows output-only filtering leaves internal exposure almost unchanged while transition-level governance catches it.

## Claims drawn from this source

- **Constraint drift is a preservation failure, not a flawed objective.** The paper defines constraint drift as the loss of operational force of safety-critical constraints across an LLM-based multi-agent trajectory, distinct from reward hacking, specification gaming, goal misgeneralization, and prompt injection, which concern flawed objectives, proxy exploitation, unintended learned goals, or adversarial context manipulation.
- **Five diagnostic modes mark where a constraint stops governing.** The modes are memory drift, authority drift, information-flow drift, accountability drift, and utility-induced drift, derived from the recurring interfaces: state and memory, delegation and authority, communication and tool I/O, execution and audit, and optimization.
- **Output-only safety leaves internal channels exposed.** In the AgentLeak replay (4,979 traces), output-only filtering reduced final-output exposure to 2.9% but left inter-agent messages at 68.8% and shared memory writes at 46.7%, whereas no defense showed 27.2% final, 68.8% inter-agent, and 46.7% memory exposure.
- **Transition-level governance exposes and catches violations.** CSG Lite, a minimal replay implementation checking each observed transition, reduced hidden exposure to 3.3% (inter-agent) and 2.7% (memory), 4.6% (internal total) and 5.7% (total), and recorded 19,916 audit events versus 1,556 under output-only filtering and zero under no defense.
- **Balanced governance keeps utility while staying admissible.** In offline policy search over the same replay, output-only control was not admissible (0.328 forbidden exposure), strict CSG was admissible but lost utility to over-redaction (0% retention), and balanced CSG stayed admissible (0.017 forbidden exposure, 0.983 admissible rate) while preserving 0.980 utility.
- **Governance should bind critical transitions, not every token.** Strong admission checks matter most for external disclosure, delegation, file deletion, production configuration changes, shell commands, memory writes, sensitive tool calls, and irreversible actions; low-risk local reasoning can use lighter checks, giving proportional control rather than maximal control.
- **Drift needs benchmarks, instrumentation, and constraint compilation.** The research agenda calls for benchmarks with multi-step tasks, explicit constraints, and full trajectory records; reusable instrumentation exposing standard records for proposed actions, semantic effects, active constraint state, delegated authority, admission decisions, and audit roots; and practical constraint compilation from user instructions, tool schemas, repository metadata, organizational policy, and runtime context.
