---
title: "Detecting Intent Drift in AI Agents With Runtime Behavioral Data - ARMO"
type: "raw-source"
url: "https://www.armosec.io/blog/detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data/"
author: "Yossi Ben Naim"
publication: "ARMO"
published: "2026-04-01"
archived: "2026-11-28T07:01:00Z"
---

> [!quote] Original source
> **Author(s):** Yossi Ben Naim  
> **Title:** Detecting Intent Drift in AI Agents With Runtime Behavioral Data - ARMO  
> **Published in:** ARMO  
> **Date:** 2026-04-01  
> **Original:** <https://www.armosec.io/blog/detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data-armo|Source note]]
Themes: [[Agent design patterns]], [[Loop engineering]]
Why it was archived: Q0: how multi-agent systems detect and attribute drift mid-run without halting execution

## Archived text

PHP2Shell: What Security Teams Need to Know About CVE-2026-109618 and CVE-2026-109619

On October 21, 2026, the PHP project shipped emergency releases for two critical memory-safety bugs...

Apr 1, 2026

Your behavioral anomaly detection tool just flagged 47 alerts from this morning’s AI agent deployment—but half are from normal autoscaling, a quarter are learning-mode noise from pod restarts, and you have no way to tell which ones actually matter. You start triaging from the top. By the time you reach alert number twelve, a rolling deployment fires and the baseline resets again. Another round of learning-mode alerts floods the queue. Somewhere in that noise, an agent that received a crafted prompt twenty minutes ago has already queried a sensitive database table and exfiltrated the results to an external endpoint. The alert for that event? It’s sitting at position thirty-one, tagged low-confidence because the pod was too new for the baseline to trust its own detection.

This is not a tuning problem. It is a category error. Traditional behavioral baselines depend on four prerequisites—stable entity identity, stable network topology, consistent workload shape, and predictable behavioral patterns—and AI agents running on ephemeral Kubernetes infrastructure violate every single one. Pods recycle faster than baselines can converge. Agent behavior changes with every prompt. CI/CD pushes new models constantly. The baseline tool spends the majority of its time in learning mode, and real attacks hide in that permanent blind spot.

Behavioral baselines structurally fail for AI agents in Kubernetes — not because they need better tuning, but because the prerequisites they depend on are architecturally impossible in ephemeral environments. This article shows how that structural gap creates the opening for intent drift, why anomaly scores miss it, and what a runtime-first detection architecture looks like when it needs to work from the first syscall. We have previously broken down four AI-specific attack chains and mapped what each detection layer catches across them; the baseline failures explored here are the structural reason those detection gaps exist in the first place.

A behavioral baseline is a model of “normal” activity for a workload. The idea is straightforward: observe a system long enough, learn what it usually does, then alert when it deviates. This works when identities are stable, behavior is predictable, and workloads live long enough for the observation to converge into a reliable model.

AI agents in Kubernetes break every one of those assumptions. Not because the baselines are poorly calibrated, but because the four prerequisites they depend on are architecturally impossible in this environment.

Stable entity identity. Baselines need a persistent entity to observe. In Kubernetes, the entity is a pod—and pods are designed to be disposable. A Deployment rollout replaces every pod in the ReplicaSet. The Horizontal Pod Autoscaler creates and destroys pods based on load. Spot or preemptible node reclamation forces pod rescheduling to different nodes. Each time a pod is recreated, the baseline tool must start over. The entity it was learning about no longer exists.

Stable network topology. Network baselines depend on identifying “normal” connections to a fixed set of destinations. Kubernetes Services abstract over dynamic pod IPs—the same Service name resolves to different backend pods every minute. Service meshes add proxy hops that mask direct connections. AI agents compound this by calling external APIs via RAG pipelines and MCP tool runtimes, where destinations vary by prompt. A static “known good destinations” list becomes meaningless within hours. Network baselines either become too loose and miss attacks, or too tight and raise constant false positives—a problem the progressive enforcement methodology addresses on the enforcement side.

Consistent workload shape. Cloud-native teams push changes constantly. For AI agents, that means new model versions, new tools and plugins, updated prompts and policies, feature flags, and canary deployments—each of which shifts what “normal” looks like. A canary deployment means two different “normals” running simultaneously in the same namespace. From the baseline tool’s perspective, every deployment cycle triggers a relearning period where detection confidence drops to near zero.

Predictable behavioral patterns. AI agents are intentionally variable. One prompt triggers a simple database lookup. The next chains three external API calls, writes a temporary file, and spawns a subprocess. A baseline tool sees all of this as noise it needs to “learn.” But the agent is working correctly—its behavior is non-deterministic by design, shaped by whatever input it receives and whatever reasoning path the model takes.

Here is where the math makes the problem concrete. A typical baseline tool requires a sustained observation period to converge—Kubescape’s default learning phase is 24 hours, and commercial tools describe similar windows for building behavioral fingerprints. In a production cluster with rolling deployments, HPA scaling, and spot node reclamation, median pod lifetime during active operations can be minutes to a few hours—not days.

If your baseline needs 24 hours of stable observation and your pods average four hours of lifetime with frequent restarts, the baseline never converges. It is perpetually in learning mode. There is no parameter you can adjust to close the gap between “how long I need to observe” and “how long the thing I’m observing exists.”

This is where the architectural response matters. Instead of building per-pod baselines that reset on every restart, ARMO’s Application Profile DNA attaches behavioral profiles to Kubernetes objects at the Deployment and ServiceAccount level. The baseline persists across pod churn because the identity unit is the Deployment, not the transient pod. When a new pod starts as part of the same Deployment, it inherits the behavioral profile immediately—no learning window, no detection gap. The observe-to-enforce workflow builds on this foundation: once the Deployment-level profile stabilizes, it becomes the basis for enforcement policies that survive any number of pod restarts.

Most content on behavioral detection treats “drift” and “anomaly” as interchangeable terms. They are not. The distinction determines what instrumentation you need, what data plane you operate on, and whether your detection tool can catch the most dangerous class of AI agent compromise.

A behavioral anomaly is a statistical outlier—something the system has not seen before. An agent calling an API endpoint for the first time. A process spawning an unexpected child. A network connection to an unfamiliar domain. Anomaly detection asks one question: Is this different from what I have observed before? It assigns a deviation score to individual events. If the score exceeds a threshold, it fires an alert.

Intent drift is a change in what the agent is trying to accomplish. The agent’s goals have shifted—from helpful assistant to data exfiltrator, from code reviewer to credential harvester. Intent drift is visible not in individual signals but in action chains: tool invocation → data access → external egress → credential use. Each individual step in that chain may fall within “normal” bounds. The agent has called that API before. It has made outbound connections before. An anomaly score on any single event returns low. The shift is in the combination and direction of those events—which requires correlation across syscalls, network flows, tool invocations, and identity context, not per-event scoring.

Consider a concrete scenario. An AI support agent processes customer tickets. Normal behavior includes database reads from a support_tickets table and outbound POSTs to an internal dashboard. Intent drift from a prompt injection changes which table the agent reads and where it POSTs. The individual actions (database read, outbound POST) are within baseline. The targets have shifted.

An anomaly detection system scoring “database read” returns low—the agent reads from databases constantly. Scoring “outbound POST” also returns low—the agent POSTs results every time it processes a ticket. But an action-chain correlation catches what the individual scores miss: this agent has never read from customer_pii AND posted to an unknown external domain in the same execution window. That sequence—not any individual event—reveals the intent shift.

Four mechanisms produce intent drift in production AI agents, each cataloged across the OWASP Top 10 for LLM Applications and the MITRE ATLAS framework:

Prompt injection (direct and indirect). Malicious instructions embedded in user input or external data override the agent’s intended behavior. The agent follows the injected instruction because it cannot distinguish it from a legitimate system prompt. This is the most common attack vector—and the fastest, often executing in under thirty seconds.

Compromised dependencies. A poisoned tool or plugin shifts the agent’s behavior through its instruction set, not through code exploitation. This is tool chain abuse—the agent does exactly what the malicious tool tells it to do.

Memory poisoning. Gradual conditioning across sessions corrupts the agent’s persistent state until a normal request triggers a malicious action. No single interaction is anomalous. The attack unfolds over days or weeks—with zero alerts until the final payload executes. The full attack chain analysis demonstrates how detection stacks go completely blind during the conditioning phase.

Emergent behavior. The agent develops unexpected action patterns from legitimate inputs, especially after model updates or prompt changes. This is not an attack—but the detection challenge is identical: the agent’s goals have shifted without any external signal to explain why.

If you are hunting behavioral anomalies, you build better baselines. If you are hunting intent drift, you correlate action chains across kernel events, container signals, Kubernetes metadata, and application-layer context. Different problem, different instrumentation.

This is where ARMO’s attack story generation is specifically designed for intent drift detection. Instead of assigning anomaly scores to individual events, it assembles signals across the full stack—cloud events, container events, Kubernetes events, and application events—into a single narrative that reveals the sequence, not just the deviation. When the support agent reads from customer_pii and POSTs to an external domain, the output is not two low-confidence alerts. It is one attack story with the complete chain: prompt injection detected → unauthorized tool invocation → sensitive data access → exfiltration to external endpoint. That story-level correlation is what reduces investigation and triage time by over 90%.

The four prerequisites from Section 1 are not abstract limitations—they produce specific, observable failure modes in production clusters. Here is what each one looks like when your AI agents are running on real Kubernetes infrastructure.

Consider a typical AI agent deployment during a release cycle. You roll out a new model version. The Deployment controller terminates old pods and creates new ones. The HPA adjusts replicas based on incoming request volume. Spot nodes are reclaimed, forcing pods to reschedule.

Your baseline tool sees a cascade of new pod identities. Each one enters “learning mode.” During this window, detection confidence is low—all events from new pods are tagged as unverified. Now imagine a compromised model version ships in this rollout. The agent begins exfiltrating data during the first few minutes of operation. The baseline tool sees “new behavior from a new pod”—indistinguishable from the normal behavioral variance of a fresh deployment. The exfiltration alert, if it fires at all, carries the same low-confidence tag as every other learning-mode event.

The compounding effect is severe. In a cluster with rolling deployments, HPA scaling, and spot node reclamation, a baseline tool may spend the majority of its operational time in learning mode. The window where detection is strong—after the baseline converges but before the next disruption—is a fraction of the total runtime. Real attacks target precisely this permanent learning window.

Kubernetes Services resolve to different pod IPs on every request. Service mesh sidecars add proxy hops that mask direct connections. Egress through NAT gateways obscures source identity. AI agents add another layer of variability: RAG pipeline sources that depend on query content, MCP tool endpoints that appear and disappear as integrations are added, and external API destinations that shift based on which tools the agent invokes.

A network baseline built on “known good destinations” degrades to uselessness within days. Either it becomes so loose that any destination is “normal”—and exfiltration to an attacker-controlled endpoint passes through—or it stays tight and raises alerts on every legitimate new tool integration. Security teams, facing this choice, typically loosen the baseline. The detection value drops to near zero. The enforcement side of this problem is where per-agent network destination policies become critical—restricting outbound connections to destinations observed during behavioral profiling, not a static allowlist that breaks on the first new API call.

Cloud-native teams push changes constantly. For AI agents, this includes new model versions that produce different tool call patterns, new tool integrations that add endpoints, updated prompts that shift behavioral profiles without any code change, and canary deployments that run two behavioral normals simultaneously.

Each change triggers a baseline relearning cycle. Alerts spike during normal releases, training security teams to ignore them—which is precisely how alert fatigue sets in. Research consistently shows that more than half of SOC teams feel overwhelmed by alert volume, and CI/CD churn in high-velocity environments is a primary contributor. When a real attack arrives during a deployment window, it is buried under learning-mode noise.

This is where a runtime-derived AI Bill of Materials (AI-BOM) changes the equation. Instead of treating every behavioral shift as a potential anomaly, ARMO’s AI workload discovery tracks what actually executed—which model version, which tools, which dependencies—versus what was declared. CI/CD changes become observable events: you can see that the model version changed, the tool set shifted, and correlate the behavioral difference to a specific deployment event rather than flagging it as an anomaly requiring investigation.

To understand why runtime-first detection catches what baselines miss, it helps to follow the same intent drift event through both detection paradigms—side by side, signal by signal.

An AI support agent runs in a Kubernetes cluster. Its normal workflow: receive a customer ticket, query the support_tickets table, summarize the result, POST it to an internal dashboard at dashboard.internal:8080. A rolling deployment started eighteen minutes ago—the pod running this agent instance was created twelve minutes ago as part of the new ReplicaSet.

A customer submits a ticket containing a crafted indirect prompt injection. The agent processes the ticket and the injected instruction overrides its task context. Instead of its normal query, the agent invokes its database tool with a request targeting customer_pii—a table it has never accessed. It then POSTs the results to an external endpoint the agent has never contacted.

The pod is twelve minutes old. Baseline status: “Learning — insufficient observation data.” All events from this pod carry a low-confidence tag.

The outbound POST to an unknown domain is flagged as “new behavior” with a low anomaly score. But the rolling deployment created nine other new pods in the last twenty minutes, each generating similar “new behavior” alerts as they interact with services for the first time. This exfiltration alert is visually identical to the legitimate learning-mode alerts surrounding it.

The database query against customer_pii is not flagged. The baseline does not have enough history for this pod to know that this table is unusual. The baseline has seen “database reads” from this pod—it cannot distinguish which table was queried because it operates at the connection level, not the application level.

SOC analyst sees: one more low-confidence alert among dozens of learning-mode alerts from the rolling deployment. It goes to the back of the triage queue. By the time it reaches the top, the data is gone and the pod has already been replaced by the next scaling event.

Kernel layer (eBPF). Immediate visibility—no learning window. The eBPF sensor captures the syscall chain from the first moment the pod executes: a new outbound TCP connection to an IP that has never appeared in this cluster, DNS resolution for an unfamiliar domain, and increased read volume on the database socket. These signals fire within milliseconds of the events occurring, at 1–2.5% CPU and 1% memory overhead.

Kubernetes context enrichment. The detection does not attach to the pod—it attaches to the Deployment. Even though this pod is twelve minutes old, the Deployment has weeks of behavioral history in its Application Profile DNA. The query against customer_pii is a first for this Deployment across all of its pods, ever. The external destination is a first for this Deployment. These are Deployment-level firsts, not pod-level “new behavior during learning.”

Application-layer context. The L7 sensor monitoring tool invocations sees the agent call its database tool with specific parameters targeting a table outside its behavioral profile. The outbound POST contains data matching the shape of the query results. The prompt that triggered the sequence contains an injection pattern detectable at the application layer. This is context that kernel-level signals alone cannot provide—the why behind the syscall activity.

Attack story output. Instead of three disconnected alerts requiring manual correlation, ARMO’s Cloud Application Detection and Response produces a single investigation-ready narrative: “Agent [deployment/support-agent] received prompt containing injection pattern in ticket #4521 → invoked database tool with unauthorized query against customer_pii → exfiltrated results via HTTPS POST to [external-endpoint.com]. Full chain duration: 28 seconds, prompt to exfiltration.”

The key difference: in Path 1, the attack is invisible because it happened during a learning window on a new pod. In Path 2, the attack is immediately visible because detection does not depend on baseline convergence—it depends on runtime ground truth enriched with Deployment-level identity and application-layer context. The detection works on the first syscall of the first pod in a brand-new Deployment.

When you assess whether your current tools can catch the failure modes described in this article, these six questions cut through vendor positioning. For each one, listen for the substantive answer—and know what the red flag sounds like.

1. Does detection require a learning period? What happens on the first pod that runs a new model version?

Listen for how long the learning period is, what detection confidence looks like during that window, and what happens during a rolling deployment. Red flag: “We need 24–48 hours of observation before detection is active.” That means every deployment cycle creates a blind spot—and in high-velocity environments, your tool may be in learning mode more often than not.

2. What identity does detection attach to—pod, Deployment, or ServiceAccount?

Listen for whether behavioral profiles survive pod restarts and whether the tool can correlate behavior across multiple pods in the same Deployment. Red flag: “We build per-pod baselines.” Every pod restart resets your detection. In a cluster with active HPA and rolling deployments, per-pod baselines are perpetually in learning mode.

3. Can the system distinguish intent drift from behavioral anomaly?

Listen for whether it correlates action chains (tool call → data access → egress) or only scores individual events against a baseline. Red flag: “We assign anomaly scores to each event.” Individual scoring misses the chain—the sequence that reveals the intent shift, not any single signal.

4. What application-layer context does the system capture?

Listen for prompt content, tool invocations with parameters, agent state, L7 API details—not just syscalls and network flows. Red flag: “We monitor at the kernel level.” Kernel-level alone catches symptoms but never root cause.

5. What does the investigation output look like?

Listen for a unified attack timeline with full context versus individual alerts requiring manual correlation. Red flag: “We produce alerts that your SIEM correlates.” Manual correlation during a rolling deployment means the alert is stale before triage begins. You need investigation-ready attack stories, not raw signals.

6. What is the resource overhead?

Listen for specific CPU and memory consumption per node. Red flag: Anything above 3% CPU, vague answers like “minimal,” or no specific numbers. Runtime detection must be production-safe. ARMO’s eBPF-based sensor operates at 1–2.5% CPU and 1% memory—within the performance budget most platform teams accept.

Behavioral baselines were designed for stable infrastructure with long-lived hosts, slow change, and narrow behavioral patterns. AI agents in Kubernetes are the opposite: pods are ephemeral, models and tools change with every deployment cycle, and agent behavior varies dramatically with every prompt.

Chasing a stable baseline in this environment is solving the wrong problem. The alternative is not “no baselines”—it is baselines anchored in runtime ground truth. Kernel-level observation via eBPF provides immediate visibility without learning windows. Kubernetes-aware identity at the Deployment level ensures behavioral profiles survive pod churn. Application-layer context captures the why behind agent actions—turning disconnected anomaly alerts into investigation-ready attack stories.

The question is not whether to monitor AI agent behavior. It is whether your monitoring can keep up with ephemeral workloads where the detection window closes before baselines converge.

To see how cross-layer signal correlation handles intent drift detection across ephemeral AI workloads, request an ARMO demo.

What is intent drift in AI agents?

Intent drift is when an AI agent’s goals shift—whether from prompt injection, a compromised dependency, memory poisoning, or emergent behavior. Unlike a simple behavioral anomaly, intent drift represents a change in what the agent is trying to accomplish, not just a deviation from observed patterns. The shift is visible in action chains across tool invocations, data access, and network egress, not in any single event.

Why do traditional behavioral baselines fail for AI agents in Kubernetes?

Baselines need stable identities and repeated patterns to define “normal,” but AI agents are intentionally variable and run on infrastructure where pods recycle frequently, IPs change dynamically, and CI/CD pushes new model versions constantly. The combination makes baseline convergence structurally impossible—the baseline tool is perpetually in learning mode, and real attacks hide in that window.

How does eBPF enable detection without learning periods?

eBPF hooks into the Linux kernel to observe syscalls, process events, and network flows from the first moment a workload executes. Combined with Kubernetes identity context at the Deployment level and application-layer visibility into tool invocations and prompt content, runtime detection works immediately without requiring baseline convergence.

What is the difference between behavioral anomaly detection and runtime threat detection for AI agents?

Behavioral anomaly detection scores individual events against a learned baseline and flags deviations. Runtime threat detection observes actual actions in real time, correlates them into action chains across kernel, container, Kubernetes, and application layers, and produces investigation-ready attack stories. The key difference: anomaly detection asks “is this different?” while runtime detection asks “is this an attack?”—and it answers from the first syscall.

Here is a scene every security team knows. A reverse shell opens a connection to...

When your CNAPP flags a suspicious dependency in an AI agent container, your WAF logs...
