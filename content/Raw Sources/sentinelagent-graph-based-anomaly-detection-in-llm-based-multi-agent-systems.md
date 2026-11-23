---
title: "SentinelAgent: Graph-based Anomaly Detection in LLM-based Multi-Agent Systems"
type: "raw-source"
url: "https://arxiv.org/html/2505.24201v1"
author: "Xu He Affiliation Visa Inc"
publication: "arXiv"
published: "2025-05-19"
archived: "2026-11-23T14:01:12Z"
---

> [!quote] Original source
> **Author(s):** Xu He Affiliation Visa Inc  
> **Title:** SentinelAgent: Graph-based Anomaly Detection in LLM-based Multi-Agent Systems  
> **Published in:** arXiv  
> **Date:** 2025-05-19  
> **Original:** <https://arxiv.org/html/2505.24201v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-sentinelagent-graph-based-anomaly-detection-in-llm-based-multi-agent-systems|Source note]]
Themes: [[Agent security]]
Why it was archived: How does protocol drift in multi-agent systems get detected or contained in production long-horizon runs?

## Archived text

SentinelAgent: Graph-based Anomaly Detection in LLM-based Multi-Agent Systems

Abstract

The rise of large language model (LLM)-based multi-agent systems (MAS) introduces new security and reliability challenges. While these systems show great promise in decomposing and coordinating complex tasks, they also face multi-faceted risks across prompt manipulation, unsafe tool usage, and emergent agent miscoordination. Existing guardrail mechanisms only offer partial protection, primarily at the input-output level, and fall short in addressing systemic or multi-point failures in MAS. In this work, we present a system-level anomaly detection framework tailored for LLM-based MAS, integrating structural modeling with runtime behavioral oversight. Our approach consists of two components. First, we propose a graph-based framework that models agent interactions as dynamic execution graphs, enabling semantic anomaly detection at node, edge, and path levels. Second, we introduce a pluggable SentinelAgent, an LLM-powered oversight agent that observes, analyzes, and intervenes in MAS execution based on security policies and contextual reasoning. Our approach bridges abstract detection logic with actionable enforcement, enabling the identification of not only single-point failures and prompt injection attacks, but also complex threats such as multi-agent collusion and latent exploit paths. We validate the effectiveness of our framework through two case studies, namely, an AI-powered email assistant and a Microsoft’s Magentic-One system, highlighting its capability to detect covert risks and attribute explainable root cause. This work establishes a foundation for building more trustworthy, transparent, and secure agent-based AI ecosystems.

I Introduction

Large language models (LLMs) have revolutionized how autonomous systems perceive and interact with the world [1, 2]. The Multi-Agent System (MAS) extends the application of large language models (LLMs) in complicated task scenarios, which require decomposition, delegation, and inter-agent coordination. These systems, ranging from pipeline planners like BabyAGI [3] to generalist frameworks like AutoGPT [4], OpenAgents [5], and Microsoft’s MagenticOne [6], leverage multiple specialized agents to communicate, plan, invoke tools, and adapt to evolving goals. Besides, many AI agent frameworks, such as Langgraph [7] and CrewAI [8], allow developers to define their own AI workflow and agent systems. As MAS continue to scale in capability and scope, ensuring their safety, robustness, and reliability has become an urgent research problem.

As MAS becomes powerful and complex, it is exposed to a spectrum of new failure modes not easily addressed by traditional LLM safety techniques, such as input/output guardrail [9]. We identify three primary risk categories in MAS. The first involves prompt-level vulnerabilities [10], such as prompt injection, jailbreaks, or hallucinated completions that allow attackers to override intended behavior. The second stems from unsafe tool and environment interactions [11, 12], when agents invoke APIs, access files, or perform system actions without adequate safeguards. The third, multi-agent coordination risks [13, 14], is most subtle, including adversarial communication, emergent collusion, and misaligned delegation logic. These failures are distributed by nature and may bypass single-point input-output validation.

To address this multifaceted risk landscape, we introduce a three-tier formulation of anomaly detection in MAS. At the highest level, global anomaly detection asks whether the system’s final output violates the user’s intent or task specification. If an issue is found, single-point failure localization attempts to trace the fault to a specific agent or tool. For more complex scenarios, multi-point failure attribution seeks to identify emergent problems that arise from a chain of actions, distributed across multiple agents and execution steps. This layered formulation reflects the inherent complexity of MAS reasoning and coordination, and guides the design of our detection framework.

Current defense mechanisms, such as prompt guard [15], output filters [16], or stepwise validators [17], are ill-suited for covering all three-tier detections. These approaches typically operate at the granularity of individual agents or inputs and lack visibility into system-wide structure or inter-agent dependencies. As a result, they fail to detect cross-agent anomalies or explain how faults propagate through the system. Moreover, most existing solutions do not scale to diverse MAS topologies or provide reusable abstractions for anomaly reasoning.

In this work, we propose a new graph-based anomaly detection framework for MAS. To our knowledge, we are the first to model MAS execution as a dynamic interaction graph, where agents and tools are represented as nodes, and communications, tool invocations, or reasoning steps are captured as typed, directed edges. This graph representation enables a unified view of static structure and dynamic behavior, allowing us to reason about failures at multiple resolutions. Node status reflects local behaviors and deviations (e.g., misuse of tools or hallucinated output), edge status captures risky communication and unintended control flow (e.g., indirect prompt injection or collusive delegation), and paths through the graph correspond to high-risk execution trajectories or attack chains. Our framework is topology-agnostic and can adapt naturally to round-robin pipelines, centralized orchestrators, or shared-memory ledger systems. It also supports semantic inspection and trace-based reasoning, making it especially effective for detecting distributed or stealthy failures.

To operationalize this framework in real MAS environments, we introduce the SentinelAgent, an autonomous, LLM-powered runtime monitor that observes, analyzes, and optionally intervenes in the execution of other agents. The SentinelAgent builds and updates the execution graph in real time, applies anomaly detection logic over node and edge behavior, and can enforce security policies through alerts, rewrites, or collaborative negotiation with misbehaving agents. By integrating structure-aware detection with LLM-based reasoning, the SentinelAgent bridges high-level anomaly semantics with actionable oversight.

We validate our approach through two case studies that reflect distinct multi-agent system architectures and operational challenges. The first case involves an automated email assistant, which exhibits central orchestration and deterministic workflows, while the second focuses on Microsoft’s Magentic-One, a general-purpose agent system with dynamic planning, shared memory, and extensive tool access. In both settings, our framework successfully detects covert anomalies such as unauthorized tool use, prompt-level manipulation, and multi-agent collusion, while providing interpretable diagnostics and execution traces. These results demonstrate the generalizability and practical utility of our framework across heterogeneous MAS deployments. In future work, we plan to extend our evaluation to larger-scale benchmarks, integrate our SentinelAgent with open agent platforms, and further explore automated policy refinement and adaptive graph reasoning mechanisms.

Our contributions are as follows:

- • 

We present a system-level risk landscape for LLM-based multi-agent systems and formulate the anomaly detection problem as a three-tier diagnostic task aligned with real-world failure modes.

- • 

We propose the first graph-based framework for MAS anomaly detection, introducing a topology-agnostic representation that supports anomaly reasoning across diverse agent architectures.

- • 

We develop the SentinelAgent Agent as a runtime instantiation of our framework, enabling real-time execution tracing, semantic anomaly detection, and policy-based intervention in live MAS environments.

- • 

We demonstrate the effectiveness of our approach through case studies on realistic MAS deployments, including an automated email assistant and the general-purpose Magentic-One system, showcasing our ability to detect covert faults and explain anomalous behaviors.

II Threat Landscape and Problem Formulation

II-A Risk Taxonomy in Multi-Agent Systems

MAS operates across complex interaction channels involving prompt processing, tool invocation, memory access, and multi-turn inter-agent communication. As these systems scale in autonomy and task diversity, they increasingly face security and reliability threats that cannot be explained by conventional, single-agent reasoning. We group these risks into three main categories, based on their origin and systemic manifestation, as shown in Figure 1.

Risk 1: Prompt vulnerabilities. Prompt-level vulnerabilities occur between users and agents. These include prompt injection, jailbreak attempts, hallucinated completions, and information leakage due to overly permissive generation. Such failures exploit the LLM’s sensitivity to natural language inputs, often leading to behavior that diverges from user intent or violates system constraints. While prompt filtering and output classifiers exist, they offer limited protection, especially under multi-turn or multi-agent delegation settings where an adversarial prompt may propagate indirectly [18].

Risk 2: Tool Misuse. The second risk category arises from tool and environment interaction. Agents with access to external functions, such as file readers, web APIs, or shell commands, can misuse these tools if task understanding or context alignment fails. On the contrary, if these tools are compromised, they can also become a springboard for attackers to break into the internals of the MAS. Even when individual actions appear valid, improper parameter construction, unauthorized API access, or unintentional system calls may lead to privilege escalation, side-channel leakage, or persistent state corruption. These failures often stem from semantic misinterpretations rather than direct policy violations.

Risk 3: Agent Coordination Risk. The third category focuses on coordination-based threats in multi-agent execution. MAS relies heavily on task delegation, role distribution, and memory sharing. This distributed structure, while powerful, enables subtle vulnerabilities such as adversarial message passing, decision amplification through feedback loops, and emergent collusion between agents. Crucially, no individual agent may appear malicious; rather, systemic failure arises from cascading misalignments, role ambiguity, or inconsistent intermediate states.

II-B Threat Model

We consider a threat model tailored to LLM-based multi-agent systems. The system consists of multiple autonomous agents powered by large language models, an orchestrator or task planner, and a shared execution environment that includes external tools or APIs.

Adversaries. We assume that threats can originate from three distinct sources. First, external adversaries may interact with the system through user-facing prompts, submitting inputs that are carefully crafted to override safety constraints, mislead the agents, or trigger unintended tool behaviors. Second, threats may stem from flawed system design: poorly specified agent roles, ambiguous tool permissions, or inadequate task delegation logic can create vulnerabilities even in the absence of a malicious actor. Third, failures may emerge from the LLM backbone itself. Due to their probabilistic nature and sensitivity to language context, LLMs can hallucinate tool invocations, misinterpret instructions, or violate constraints despite alignment efforts—posing a latent, model-internal risk.

Adversary Capability. In terms of capability, we assume that adversaries have full control over user-facing prompts and messages, allowing them to initiate indirect attacks via prompt injection, ambiguous queries, or adversarial task framing. They may also manipulate inter-agent communication indirectly, for instance by influencing shared memory content or crafting messages that propagate downstream misbehavior. Importantly, adversaries can exploit legitimate functionality, constructing long, seemingly benign execution chains that ultimately violate task or safety goals. However, we assume that the execution infrastructure and the SentinelAgent remain uncompromised. The SentinelAgent is treated as a trusted component with privileged access to trace data and system state, capable of monitoring and, when needed, intervening in agent execution.

II-C Multi-Tier Anomaly Detection Objectives

To effectively monitor and mitigate the above risks, we propose a three-tier anomaly detection framework aligned with how these failures manifest.

At the first tier, global anomaly detection determines whether the overall output of a MAS violates the task specification, user intent, or expected safety constraints. This can include hallucinated answers, incomplete results, or task divergence. While global anomalies are the most visible form of failure, they are also the hardest to diagnose, especially in open-ended tasks without strict ground truth.

The second tier, single-point failure localization, aims to trace an observed error back to a specific agent, decision point, or tool invocation. This task is complicated by MAS properties such as internal state opacity and multi-hop delegation. It requires fine-grained traceability, including comparisons between observed behavior and declared agent intentions or tool affordances.

At the third tier, multi-point failure attribution addresses the most complex setting, where no single agent is at fault. Instead, the failure results from interaction patterns across multiple agents and rounds—e.g., a prompt injection propagating across agents, a chain of misclassifications, or an unnoticed logic loop. Detection at this level involves reconstructing long-range dependencies, temporal event graphs, and distributed coordination traces.

These three tiers naturally align with the previously defined risk classes: global anomaly detection is often triggered by prompt-level attacks, local agent faults are typically associated with unsafe tool usage, and distributed failures emerge from inter-agent miscoordination. Together, they motivate the need for a holistic detection framework capable of reasoning across structure, semantics, and time.

III Multi-Agent System Topologies and Their Implications

The structure of MAS significantly influences both its behavior and the complexity of anomaly detection. Following the taxonomy in [19], we categorize MAS topologies into three representative types, as shown in Figure 2 and discuss how each topology impacts our proposed detection framework.

III-A Round Robin

In the round-robin topology, agents are consulted in a fixed, cyclic order. Each agent is responsible for processing or transforming the current task state before passing it to the next. This model is fully deterministic and often found in pipeline-style workflows or autonomous looped chains (e.g., BabyAGI variants [3]).

Implications for Anomaly Detection:

From an anomaly detection perspective, round-robin topologies offer several advantages. Since the execution path is predetermined and consistent across runs, global failure detection becomes relatively straightforward. Any deviation from the expected output or intermediate state can be directly mapped to a specific segment of the loop. This determinism also aids in localizing single-point faults: if the outcome changes unexpectedly, the fault likely lies in the most recently executed agent or its immediate predecessor.

However, despite the simplicity, the round-robin design is not immune to more subtle forms of failure. While complex multi-agent interactions or adversarial coordination are less likely due to the constrained topology, issues such as cumulative error propagation, slow degradation of outputs, or logic drift over multiple iterations can still occur. These issues often manifest gradually and may evade detection if monitoring focuses solely on final outputs. Therefore, even in this topology, it is beneficial to integrate intermediate checks and behavioral profiling of each agent’s state transformations.

III-B Central Orchestrator

In a central orchestrator topology, a single agent or controller is responsible for managing the workflow by dynamically assigning tasks to other agents or tools. Rather than following a fixed path, execution unfolds based on the orchestrator’s interpretation of the current state and user intent. This design is prominent in systems such as AutoGPT or LangGraph-based planners, where agent selection, ordering, and tool usage are context-sensitive and often vary across runs.

Implications for Anomaly Detection: This flexibility enhances generality and task adaptability, but it also introduces significant challenges for anomaly detection. Since execution paths are non-deterministic and runtime-dependent, tracing failures requires dynamic graph reconstruction rather than simple path matching. Furthermore, the orchestrator acts as a central point of logic interpretation and decision-making. Any misclassification, faulty planning, or unvalidated delegation can propagate erroneous behavior throughout the system, even if the individual agents behave according to their own specifications. Another concern is the opaqueness of inter-agent dependencies. The orchestrator may invoke multiple agents sequentially or in parallel, but without explicit constraints or validation layers, these agents may operate on inconsistent assumptions or conflicting data. Anomaly detection in this topology must therefore incorporate reasoning not only over agent behavior but also over orchestration intent and planning coherence.

III-C Central Orchestrator with External Ledger

A more advanced evolution of the orchestrated design involves the integration of an external task ledger—an append-only memory or blackboard shared among agents. In this topology, the orchestrator still manages control flow, but intermediate task states, plans, and outputs are persistently stored in the ledger. This architecture is exemplified by Microsoft’s Magentic-One, which uses ledger-based coordination to support iterative and long-horizon planning across rounds.

Implications for Anomaly Detection: The presence of shared memory significantly enhances task consistency and enables agents to collaborate asynchronously. However, it also introduces a new class of vulnerabilities and diagnostic complexities. The ledger becomes both a source of truth and a target of potential compromise. Malicious or misinformed agents can insert misleading entries, poisoning downstream decisions without triggering immediate anomalies. From a detection perspective, this structure necessitates temporal and historical reasoning. Abnormalities may not manifest in a single execution cycle but only become visible through ledger evolution. Attack paths in this topology may span multiple rounds, where early-stage prompt injection or logic drift leads to unsafe tool usage later in the workflow. As such, anomaly detection systems must model both control flow and memory flow, and incorporate temporal invariants to identify delayed or distributed failures.

Each topology presents distinct challenges for anomaly detection. Deterministic structures simplify trace-based reasoning but offer limited flexibility. Dynamic orchestration improves generality but complicates attribution. Systems with shared state require hybrid reasoning over both communication and memory flows.

Our proposed graph-based framework is topology-agnostic and can adapt to each of these structures by instantiating the appropriate graph shape and incorporating metadata such as ledger state, orchestration decisions, and round-based transitions.

IV Graph-Based Anomaly Detection Framework

To diagnose complex anomalies in multi-agent systems, we require a modeling framework that captures both the structural organization of agents and their evolving execution dynamics. Existing representations, such as flat logs, JSON trees, or message traces, fail to express long-range dependencies, control flow semantics, or agent-tool interaction patterns in a unified and analyzable way. We propose a graph-based framework for MAS anomaly detection to address this limitation.

IV-A Graph Modeling of MAS

Node and Edge. As shown in Figure 3, we model each MAS execution instance as a directed interaction graph \(G=(V,E)\), where nodes represent entities (agents or tools) and edges represent interactions (messages and invocations). Each node is attached with property information: agent nodes include metadata such as system prompts, declared capabilities, and roles (e.g., orchestrator, executor, summarizer), while tool nodes represent callable functions or APIs with input/output constraints. Edges are structured and timestamped, encoding message content, tool arguments, response traces, and reasoning thoughts.

The MAS graph consists of two phases. At the initialization stage, we extract the static graph from the system’s architecture, which encodes all allowable interaction paths. An agent node can have an accessible tool list, while a tool node should have a list of agents to invoke it. However, the authentication and authorization of tool access are not enforced in real practice, which leads to potential security risks. At the execution stage, we capture the actual trace of interactions to instantiate edges, named the dynamic execution graph. This dual perspective allows us to reason about design-time vulnerabilities (e.g., risky topologies and lack of authentication and authorization) and runtime anomalies (e.g., unexpected message chains).

Status Semantics. At runtime, we can label nodes and edges with their behavioral status, reflecting their alignment with expected system behavior. The agent node is evaluated based on whether its observable behavior conforms to its declared roles. For instance, an agent that invokes a tool outside its permission scope, generates hallucinated plans, or exhibits inconsistent reasoning is marked anomalous. Tool nodes are monitored for consistency, which is expected to produce outputs consistent with their contract and prevent misuse (e.g., unsafe file access, invalid response structure).

Edges encode semantic transitions between nodes, such as planning messages, tool invocations, or reasoning outputs, and are analyzed for signs of adversarial content, unintended control flows, or covert prompt injection. For example, a message from one agent to another that alters task parameters without proper authorization may represent a coordination vulnerability.

Node vs. Edge Status. The decoupling between node and edge status is fundamental to our anomaly detection approach. Node status characterizes inherent properties and behaviors of agents and tools, focusing on their internal operations, role conformity, and individual decision-making integrity. In contrast, edge status evaluates the relational aspects of the system, how entities interact, communicate, and influence each other over time. We maintain this dual status model because many security vulnerabilities manifest asymmetrically: some anomalies arise from compromised entity behavior (e.g., a single agent making hallucinated claims), while others emerge from the interaction patterns themselves (e.g., valid-looking messages that collectively implement a privilege escalation). By monitoring both dimensions, our framework achieves comprehensive coverage of the attack surface, detecting anomalies that would be invisible if only examining either entities or interactions in isolation. This separation also enables targeted remediation strategies, addressing entity-level issues through agent resets or capability restrictions, while resolving interaction anomalies through communication filtering or topology adjustments.

IV-B Attack Path-Based Failure Attribution

Attack Path. While node and edge status support local anomaly detection, some MAS failures emerge from multi-step execution chains, sequences of interactions that are individually benign but jointly harmful. To capture such failures and trace root-cause attribution, we define the concept of attack paths: subgraphs whose structure and content match known risk patterns derived from empirical traces or security analysis. For example, an attack path might involve a prompt injection that propagates through an orchestrator, bypasses verification, and ultimately triggers unsafe tool usage (e.g., code executor). Detection of attack paths requires both structural matching (does a known risky subgraph exist?) and semantic interpretation (do node/edge behaviors match known exploit attributes?). These paths enable the failure attribution that cannot be localized to a single agent or message and support multi-point anomaly reasoning.

Mapping Graph Semantics to Detection Objectives. Our graph-based framework supports the three-tier anomaly detection objectives. Global anomalies (Tier 1), such as output failure to complete a task, are typically reflected in terminal node behaviors and root-to-leaf execution paths. Single-point failures (Tier 2) are localized to nodes or edges whose status obviously diverges from the specification. Multi-point anomalies (Tier 3), such as collusion or gradual logic drift, can be detected by matching attack paths.

On the other hand, the graph abstraction aligns with the risk taxonomy outlined in Section II. Prompt-level failures (R1) are captured through anomalous reasoning nodes or misaligned outputs. Unsafe tool usage (R2) corresponds to tool node or edge status. Multi-agent coordination risks (R3) are most evident in attack paths, requiring trace-based and pattern-aware analysis.

IV-C Implementation of the Graph-Based Approach

While the graph representation provides the structural foundation for anomaly detection, its practical effectiveness depends on its ability to operate in real-world MAS deployments. We adopt an LLM-as-judge strategy, leveraging the understanding and reasoning capabilities of LLMs to evaluate agent and tool behaviors against security policies. Meanwhile, we also involve humans in the loop to enhance our security policy and assess detection results to reduce false alerts. To implement this, we introduce the SentinelAgent in the following section. The SentinelAgent is responsible for constructing and maintaining the interaction graph at runtime, applying LLM reasoning to detect anomalies, and generating alerts. The SentinelAgent works as a pluggable oversight module for implementing our theoretical framework, which runs synchronously with the task agents in the MAS but operates independently.

V SentinelAgent for Runtime Oversight

V-A SentinelAgent Architecture

As shown in Figure 4, the SentinelAgent consists of three functional modules that operate in a continuous loop:

Event Monitor. Event Monitor intercepts runtime events via instrumentation hooks placed in the MAS. We leverage standard observability frameworks (e.g., OpenTelemetry [20]) to collect events with minimal overhead. The module performs event interception and buffering through non-blocking message queues to ensure minimal latency impact on main execution paths. It restructures raw event trace logs into typed graph elements (nodes, edges) using schema-validated transformations. Additionally, it would enrich the context by augmenting raw event data with system state and historical information. System state includes current agent permissions, active tools, memory contents, and resource utilization metrics, while historical information encompasses previous interactions, past violations, and execution patterns that provide temporal context for behavior analysis. Specifically, we implement the Event Monitor using the Phoenix platform, open-sourced by Arize [21], which can collect execution traces of agent systems in near real time. Then, SentinelAgent can parse the traces into the interaction graph.

Behavior Analyzer. The Behavior Analyzer is responsible for evaluating the interaction graph against expected behavioral patterns. The module implements node and edge status evaluation using both rule-based classifiers for authentication and authorization checks and LLM-based semantic reasoning for complex behavior interpretation.

It first conducts node and edge status analysis using LLM as a judge to detect adversarial content, prompt injections, or malicious payload transmission. Specifically, we employ the IBM Granite Guardian 3.2 model to detect jailbreak in prompt and function calling hallucination in response [22] for node status. For the direct and indirect prompt injection issue in edge status, we use Llamafirewall [17] to check the alignment in conversation between nodes. Once any abnormal status is detected, SentinelAgent can report a single-point error.

Then, the analyzer performs execution path pattern matching against the attack path library to identify partial or complete matches. If SentinelAgent detects a suspicious execution path, it would also search whether any abnormal status on this trace has been reported. Meanwhile, SentinelAgent would reconduct the node and edge status checks to capture missed anomalies, the double check would adopt a lower risk confidence threshold (that is, a stricter malicious checking constraint) in detection models (e.g, Granite Guardian and Llama Guard). Then, SentinelAgent would combine the detected attack path and abnormal status to form a report to depict comprehensive risk attribution. To prevent potential misjudgments, if no abnormal state is found on the suspicious execution path, it will be reported to the security personnel, who will further determine whether there is real abnormal behavior.

Risk Responder. The Risk Responder determines appropriate responses to detected anomalies based on our defined risk taxonomy and multi-tier anomaly detection objectives. The module implements a multi-tiered alert classification system that categorizes detected issues according to severity, confidence, and potential impact.

For Tier-1 global anomalies (task-level failures), the system generates alerts that highlight systemic issues affecting overall output. For Tier-2 single-point failures (individual agent or tool anomalies), alerts contain specific entity identifiers and violation details. For Tier-3 multi-point anomalies, the Responder provides a detailed attack path description.

Tier-3 alert is enriched with root-cause attribution analysis, tracing the anomaly back to its origin point within the interaction graph. This attribution includes identifying the entry point of adversarial inputs, mapping the propagation path across nodes, and highlighting the specific vulnerabilities associated with each node. Based on this analysis, the Risk Responder generates tailored remediation recommendations for security personnel, such as agent prompt refinements, permission boundary adjustments, or topology modifications to prevent similar exploitation in the future.

V-B Operation Procedure of SentinelAgent

The SentinelAgent’s operation consists of two phases: an initialization stage for system analysis and policy configuration, and an execution stage for runtime monitoring and enforcement.

Initialization Stage. During system cold start, the SentinelAgent would analyze the MAS architecture. First, it conducts configuration extraction and topology mapping by ingesting all available system specifications, such as agent role setting, task description, and tool descriptions, to construct the initial static graph representation of the MAS. Next, through LLM-driven behavior analysis, the system uses the extracted configuration to synthesize a catalog of expected normal behaviors and potential abnormal behaviors for each agent role. Initially, any execution beyond predicted normal execution paths for common task workflows can be classified as potential attack paths. However, it would cause high false positives. So we infer abnormal behaviors based on agent capabilities, tool access permissions, and vulnerability patterns specific to the system topology.

This LLM-driven analysis is followed by human-in-the-loop refinement, where security experts review and refine the LLM-generated behavior models and attack paths. Experts validate predicted risks, add domain-specific attack vectors that may not be captured by general models, and specify organization-specific security policies. For example, in MAS with the orchestrator agent, the orchestrator usually can access all other agents with specific tasks. If the orchestrator is compromised, it can cause huge damage to MAS. Therefore, the designer may define an extra policy to constrain the access permission of the orchestrator under certain scenarios. We showcase such scenarios in Section VI. This initialization process combines the scalability of automated analysis with human expertise, creating a tailored security model for the specific MAS deployment that balances protection with operational needs.

Execution Stage. During system operation, the SentinelAgent maintains continuous oversight using the three modules introduced above. The system benefits from periodic human auditing, where security analysts regularly review detected anomalies across all tiers, evaluate the accuracy of root-cause attribution analyses, examine system trace logs to discover potential false negatives, and analyze emerging patterns that may indicate novel attack vectors. These reviews inform dynamic policy updates, where the Watchdog’s behavior models and attack path library are continuously refined by adding newly discovered attack patterns to the detection library, adjusting detection thresholds for each anomaly tier to optimize the precision-recall balance, updating policy specifications to address emerging threats or changing requirements, and fine-tuning LLM prompts to improve semantic reasoning accuracy. This execution-time integration creates a learning security system that improves over time while maintaining core protections against known risks.

VI Case Studies and Evaluation

To demonstrate the effectiveness of our proposed framework, we conduct evaluations on two MAS cases.

VI-A Case Study I: Email Assistant System

System Overview The first case study examines an automated email assistant system designed for intelligent inbox management, similar to a CrewAI usage example found on Github [23]. The system operates under a centralized orchestrator topology, as illustrated in Figure 5. It comprises three specialized agents: a Classifier for priority assessment, a Summarizer for content extraction, and a Responder for automated reply generation, and four tools: email listener for incoming email retrieval, an email sender for outgoing responses, a system info checker for calendar and task context. The classifier agent serves as the primary decision point, routing emails to appropriate downstream agents based on content analysis and priority. The system is designed to autonomously manage email interactions. Detailed specifications of individual agent responsibilities are provided in the appendix.

Graph Modeling and Execution Patterns. We abstract the system into the directed interaction graph, mark each nodes with a unique identifier, and visualize the graph in Figure 5. The circle nodes represent agents, while the square nodes represent tools. Combining the system configuration, we infer the execution paths and interaction patterns that define the system’s operational behavior. We summarize the execution paths in Table I, which includes both benign operations and potential attack scenarios.

As listed in Table I, the system exhibits three primary benign execution patterns. The first is the high-priority workflow, in which incoming emails are processed sequentially by the Email Listener, Classifier, and Summarizer before notifying the user. The second pattern is the autonomous response workflow, where the Email Listener and Classifier route suitable emails directly to the Responder, which then generates replies sent out by the Email Sender. The third, context-aware workflow, incorporates intermediate consultations with the System Info Checker, enabling the system to provide calendar-dependent responses when necessary.

However, the system is also vulnerable to specific attack paths that exploit its design. SentinelAgent identifies two primary attack paths. The first attack path involves an adversary crafting a malicious email that deceive the Classifier, and trigger the Responder to send unauthorized replies. For example, the attacker could hajack the Responder and send out a reply that appears to be from the user, but contains fake information to victim receivers. The second attack path aims to steal users’ sensitive information by expliting the System Info Checker. An adversary could manipulate the Summarizer to extract confidential data from emails and send it to an unauthorized recipient.

Anomaly Detection and Attack Mitigation We use the email assistant system to synthesize the normal and attack exection traces for evalution, which is repeatable (See Appendix). By applying SentinelAgent , we can monitor the execution graph in real-time and identify deviations from expected patterns. We successfully detected two attack scenarios. Notably, since two attack paths share the same benign execution path, the SentinelAgent can identify the attack by analyzing the execution graph and detecting deviations from the node and edge status.

For the first attack scenario, where the adversary manipulates the Classifier to trigger unauthorized responses from the Responder, the SentinelAgent detects anomalies through:

- • 

Path deviation analysis: Identifying incorrect transitions from the Classifier to the Responder rather than passing to the Summarizer.

- • 

Content constraint validation: Detecting prompt instructions in the email that violate response generation policies. The Responder is manipulated to copy fake content from the incoming email or generate business-related content, instead of providing standard greetings or procedural replies.

- • 

Tool Parameter assessment: Recognizing unsafe parameters in tool invocation sequences, such as unauthorized email receiver addresses.

For the second attack scenario, where the adversary attempts to extract sensitive information using the System Info Checker, the SentinelAgent identifies anomalies through:

- • 

Path deviation analysis: Identifying incorrect transitions from the Classifier to the Responder rather than passing to the Summarizer.

- • 

Tool invocation validation: Detecting unauthorized tool invocations, such as the Responder attempting to request more calendar information, such as task details, from the System Info Checker, which is beyond its intended scope. This indicates that the Responder is trying to access sensitive information without proper authorization. access the System Info Checker without proper authorization. The Responder is manipulated to request user’s calendar information or task details without proper authorization.

- • 

Content constraint validation: Identifying prompt instructions that attempt to extract confidential data from emails.

Upon detection, the system flags the execution graph as compromised and raises appropriate alerts for two attack scenarios, demonstrating effective real-time threat mitigation.

VI-B Case Study II: Magentic-One Generalist System

System Architecture and Capabilities

The second case study analyzes Magentic-One, a general-purpose multi-agent system engineered for complex, open-ended tasks including document analysis, web-based information retrieval, and code execution. The system implements a hub-and-spoke architectural pattern with a central Orchestrator agent coordinating three specialized worker agents: FileSurfer for document management, WebSurfer for internet-based research, and CodeExecutor for computational tasks, as shown in Figure 6. Additionally, the system maintains a persistent shared ledger that serves as a collective memory store accessible to all agents.

Graph Representation and Execution Dynamics.

The system graph representation positions the Orchestrator as the central hub node, with peripheral agent nodes connected to their respective specialized tools: file system interfaces, web retrieval mechanisms, and sandboxed code execution environments. The shared ledger functions as a global memory node, facilitating inter-agent communication and task state persistence.

Typical benign execution follows a structured delegation pattern: the Orchestrator receives user queries, dispatches appropriate subtasks to FileSurfer for document retrieval, coordinates with CodeExecutor for analysis and summarization, and consolidates results through the shared ledger before presenting final outputs to users.

Advanced Attack Detection

We test the framework using a sophisticated attack scenario involving code injection masqueraded as a legitimate summarization request. The attack vector exploits the system’s code execution capabilities by embedding malicious instructions within seemingly benign user queries. When processed, the Orchestrator forwards the request without adequate validation, leading CodeExecutor to execute injected code containing data exfiltration logic.

The SentinelAgent demonstrates robust detection capabilities through comprehensive analysis:

- • 

Input validation: Recognition of ambiguous or potentially malicious instructions in user-to-orchestrator communications

- • 

Planning validation: Detection of inadequate tool selection validation by the orchestrator

- • 

Behavioral analysis: Identification of policy violations in CodeExecutor output patterns

The detection mechanism successfully traces the complete attack chain, from initial prompt ambiguity through orchestrator misclassification to unsafe code execution, matching the observed pattern against stored risk signatures. Upon detection, the SentinelAgent isolates the compromised execution path and generates comprehensive diagnostic reports for security analysis. The detailed malicious execution trace and detection results, please check the Appendix.

VI-C Evaluation Results and Critical Analysis

These comprehensive case studies validate our framework’s effectiveness across diverse multi-agent architectures and operational scenarios. Both evaluations demonstrate successful detection of sophisticated attacks that would likely evade conventional output-validation approaches. Significantly, our approach achieves this detection capability without requiring intrusive access to internal agent states, instead leveraging structured graph analysis and behavioral pattern recognition.

VI-C1 Key Findings

Our evaluation reveals several critical insights:

- 1. 

Architectural adaptability: The graph-based modeling approach successfully accommodates both deterministic pipeline architectures and dynamic planning systems

- 2. 

Explainable detection: Graph structure enables transparent attribution of anomalies across multi-hop execution sequences

- 3. 

Granular analysis: Combined node and edge status monitoring provides precise localization of security violations

- 4. 

Semantic understanding: Attack path analysis captures distributed failure modes spanning multiple interaction rounds

VI-C2 Implications for Secure MAS Deployment

These results provide strong empirical support for our central thesis that structure-aware, runtime-integrated oversight mechanisms are essential for secure deployment of LLM-driven multi-agent systems. The demonstrated capability to detect sophisticated attacks across diverse architectures suggests broad applicability of our approach to real-world MAS implementations.

The framework’s success in identifying covert anomalies while maintaining operational transparency positions it as a valuable tool for both security practitioners and system developers. In the subsequent section, we examine broader implications, acknowledge current limitations, and outline promising directions for future research and development.

VII Discussion and Generalization

The preceding case studies demonstrate that our framework effectively detects, attributes, and explains anomalies in complex multi-agent systems. In this section, we reflect on the broader implications of our approach, identify its current limitations, and outline promising directions for future research.

VII-A Advantages over Existing Approaches

Our graph-based anomaly detection framework, instantiated through the SentinelAgent, provides several key advantages over traditional guardrail or logging-based methods.

First, the structural modeling of agent behavior allows for multi-resolution diagnostics. By representing interactions as nodes, edges, and paths, we can localize faults precisely or analyze systemic failures holistically. This stands in contrast to flat logging approaches, which obscure dependencies and offer limited context for forensic analysis.

Second, our method supports topology-agnostic oversight. Whether the MAS follows a centralized planner, a decentralized ledger, or a round-robin pipeline, the interaction graph flexibly adapts to capture the corresponding execution semantics. This enables generalization across domains and supports scalable deployment.

Third, the SentinelAgent’s integration at runtime allows for real-time detection and policy enforcement without modifying the internal logic of existing agents. This makes the framework compatible with black-box agents and reduces integration complexity in production systems.

Finally, the combination of symbolic graph analysis and LLM-based reasoning enables explainability. Detected anomalies are not just flagged but can be semantically interpreted, attributed to specific decision points, and conveyed in natural language—making them actionable for both developers and system operators.

VII-B Limitations and Challenges

Despite these strengths, our approach also faces several limitations. Most critically, the accuracy and coverage of anomaly detection depend on the quality of the policy definitions and graph semantics. In practice, designing complete and robust detection rules may require substantial domain knowledge or empirical tuning.

Moreover, the SentinelAgent itself is implemented on top of a large language model and thus inherits many of the same challenges, such as potential hallucination, inconsistency, or susceptibility to adversarial inputs. While our use of structured graph semantics mitigates some of these risks, the LLM component still constitutes a point of uncertainty.

There are also computational considerations. Although our instrumentation is designed to minimize runtime overhead, the cost of maintaining and analyzing execution graphs, especially in long-running or large-scale MAS, may be non-trivial. Future optimizations such as graph pruning, event filtering, or asynchronous monitoring may be necessary to ensure scalability.

VII-C Generalization to Other MAS and Environments

Our framework is designed to be broadly applicable. It can be extended to MAS operating in different domains—e.g., finance, healthcare, education—or those using specialized agent protocols or toolchains. The graph abstraction allows system-specific roles, data types, and constraints to be encoded as attributes without altering the core detection logic.

Additionally, while our current instantiation focuses on LLM-based agents, the architecture is compatible with non-LLM components. For instance, robotic systems using rule-based agents or hybrid planners can still be modeled and monitored using the same graph structure, provided that their interaction semantics are observable.

VII-D Future Directions

Several opportunities exist to strengthen and extend our work. One direction is the development of automated policy learning mechanisms, where the SentinelAgent bootstraps its anomaly detection logic from empirical traces or adversarial simulation. Reinforcement learning, program synthesis, or large-scale fine-tuning could support such adaptation.

Another direction is to integrate formal verification tools into the framework. By combining runtime graph analysis with offline model checking or static analysis, we could achieve stronger correctness guarantees and reduce reliance on heuristics or handcrafted rules.

Finally, we envision extending the SentinelAgent beyond detection and enforcement, toward active collaboration. Rather than merely identifying risks, it could advise agents in real time, suggest task revisions, or negotiate safe delegation protocols—transforming oversight into co-optimization.

VIII Related Work

The safety and security of large language models (LLMs) and agentic systems have been the focus of increasing research attention, particularly as these models are deployed in complex, interactive settings. Prior work can be broadly categorized into three areas: LLM input-output hardening, function/tool usage control, and multi-agent safety.

Prompt-level defenses such as prompt injection mitigation and hallucination reduction have been explored in various contexts. Techniques include adversarial training [10], prompt templating with restricted input slots [15], and output post-processing via fact-checkers or classifiers [22]. Guardrail frameworks such as ReAct, Guidance, and Guardrails AI offer mechanisms to impose syntactic or semantic constraints on LLM outputs, but they are typically bound to pre-defined templates and lack contextual awareness of system-level consequences.

To address the growing use of function calls and tool integrations, recent work has proposed techniques like structured output validation [4], tool invocation wrappers [5], and intent classification layers [6] that aim to regulate when and how LLMs call external APIs. While useful for sandboxed environments, these solutions often lack real-time oversight and struggle with long-horizon behavior tracking, making them insufficient in agent systems that involve memory, planning, or adaptive behaviors.

In the realm of multi-agent systems, research on agent coordination has traditionally focused on alignment, incentive design, and game-theoretic modeling [2]. However, relatively little work has addressed security concerns in LLM-driven multi-agent interactions, such as adversarial communication, emergent collusion, or protocol manipulation. Early efforts have begun exploring controlled multi-agent dialogues [3], but such systems typically rely on static rules or assume trust among agents.

A few recent systems attempt to extend guardrails beyond prompt-level safety. For example, ToolFormer [24] incorporates external APIs into LLMs through training, and AutoGPT-like architectures have experimented with feedback loops and execution constraints. However, these systems often conflate planning and oversight, and lack an explicit monitoring layer to enforce safety at runtime.

In contrast, our approach introduces a dedicated, policy-driven SentinelAgent that operates in parallel to task agents. Unlike prior work that treats safety as a pre-processing or post-processing step, our system enforces safety through live auditing, contextual reasoning, and selective intervention during agent execution. This separation of concerns between task performance and oversight enables more modular, extensible, and robust safety enforcement in both single-agent and multi-agent settings.

IX Conclusion

This paper presents a comprehensive anomaly detection mechanism for Multi-Agent Systems that enhances system reliability through proactive monitoring and fault detection. Our approach integrates dynamic interaction graphs and runtime oversight. By modeling agent execution as a typed, directed graph and reasoning over node, edge, and path semantics, we enable fine-grained diagnostics that span from local misbehavior to distributed system failures. Through case studies in both task-specific and generalist multi-agent systems (MAS) settings, we demonstrate that our framework offers actionable insights, root-cause attribution, and policy-enforceable oversight, all without compromising the modularity or autonomy of existing agents. Future work will focus on optimizing the monitoring overhead and extending the framework to handle more complex fault scenarios in large-scale distributed systems.

References

- [1] Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan, and Hoang D. Nguyen. Multi-agent collaboration mechanisms: A survey of llms, 2025.
- [2] Erik Miehling, Karthikeyan Natesan Ramamurthy, Kush R. Varshney, Matthew Riemer, Djallel Bouneffouf, John T. Richards, Amit Dhurandhar, Elizabeth M. Daly, Michael Hind, Prasanna Sattigeri, Dennis Wei, Ambrish Rawat, Jasmina Gajcin, and Werner Geyer. Agentic ai needs a systems theory, 2025.
- [3] Yashar Talebirad and Amirhossein Nadiri. Multi-agent collaboration: Harnessing the power of intelligent llm agents, 2023.
- [4] Hui Yang, Sifu Yue, and Yunzhong He. Auto-gpt for online decision making: Benchmarks and additional opinions, 2023.
- [5] Tianbao Xie, Fan Zhou, Zhoujun Cheng, Peng Shi, Luoxuan Weng, Yitao Liu, Toh Jing Hua, Junning Zhao, Qian Liu, Che Liu, Leo Z. Liu, Yiheng Xu, Hongjin Su, Dongchan Shin, Caiming Xiong, and Tao Yu. Openagents: An open platform for language agents in the wild, 2023.
- [6] Adam Fourney, Gagan Bansal, Hussein Mozannar, Cheng Tan, Eduardo Salinas, Erkang, Zhu, Friederike Niedtner, Grace Proebsting, Griffin Bassman, Jack Gerrits, Jacob Alber, Peter Chang, Ricky Loynd, Robert West, Victor Dibia, Ahmed Awadallah, Ece Kamar, Rafah Hosn, and Saleema Amershi. Magentic-one: A generalist multi-agent system for solving complex tasks, 2024.
- [7] LangChain. Langgraph: A library for building stateful multi-agent applications. 2024. https://github.com/langchain-ai/langgraph.
- [8] CrewAI Contributors. Fast and flexible multi-agent automation framework. https://github.com/crewAIInc/crewAI, 2024. Accessed: 2025-05-19.
- [9] Norman Shinn and Dawn Song. Guardrails ai: Enforcing llm behavior with structure and policies. Arxiv preprint arXiv:2306.07397, 2023.
- [10] Blake Bullwinkel, Amanda Minnich, Shiven Chawla, Gary Lopez, Martin Pouliot, Whitney Maxwell, Joris de Gruyter, Katherine Pratt, Saphir Qi, Nina Chikanov, Roman Lutz, Raja Sekhar Rao Dheekonda, Bolor-Erdene Jagdagdorj, Eugenia Kim, Justin Song, Keegan Hines, Daniel Jones, Giorgio Severi, Richard Lundeen, Sam Vaughan, Victoria Westerhoff, Pete Bryan, Ram Shankar Siva Kumar, Yonatan Zunger, Chang Kawaguchi, and Mark Russinovich. Lessons from red teaming 100 generative ai products, 2025.
- [11] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. Model context protocol (mcp): Landscape, security threats, and future research directions, 2025.
- [12] Xiaoyuan Qi, Yuan Zheng, and Dawn Song. Why are web ai agents more vulnerable than standalone llms? Arxiv preprint arXiv:2310.02013, 2023.
- [13] Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, and Ion Stoica. Why do multi-agent llm systems fail?, 2025.
- [14] Alexander Meinke, Bronson Schoen, Jérémy Scheurer, Mikita Balesni, Rusheb Shah, and Marius Hobbhahn. Frontier models are capable of in-context scheming, 2025.
- [15] Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, and Madian Khabsa. Llama guard: Llm-based input-output safeguard for human-ai conversations, 2023.
- [16] Inkit Padhi, Manish Nagireddy, Giandomenico Cornacchia, Subhajit Chaudhury, Tejaswini Pedapati, Pierre Dognin, Keerthiram Murugesan, Erik Miehling, Martín Santillán Cooper, Kieran Fraser, Giulio Zizzo, Muhammad Zaid Hameed, Mark Purcell, Michael Desmond, Qian Pan, Zahra Ashktorab, Inge Vejsbjerg, Elizabeth M. Daly, Michael Hind, Werner Geyer, Ambrish Rawat, Kush R. Varshney, and Prasanna Sattigeri. Granite guardian, 2024.
- [17] Sahana Chennabasappa, Cyrus Nikolaidis, Daniel Song, David Molnar, Stephanie Ding, Shengye Wan, Spencer Whitman, Lauren Deason, Nicholas Doucette, Abraham Montilla, Alekhya Gampa, Beto de Paola, Dominik Gabi, James Crnkovich, Jean-Christophe Testud, Kat He, Rashnil Chaturvedi, Wu Zhou, and Joshua Saxe. Llamafirewall: An open source guardrail system for building secure ai agents, 2025.
- [18] Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, and Mario Fritz. Not what you’ve signed up for: Compromising real-world llm-integrated applications with indirect prompt injection, 2023.
- [19] Harold Triedman, Rishi Jha, and Vitaly Shmatikov. Multi-agent systems execute arbitrary malicious code, 2025.
- [20] OpenTelemetry. Opentelemetry collector, 2023. OpenTelemetry Collector.
- [21] Arize AI. Phoenix Documentation. https://docs.arize.com/phoenix, 2025. Accessed: May 23, 2025.
- [22] IBM Research. Ibm granite guardian 3.2 documentation. https://www.ibm.com/granite/docs/models/guardian/, 2025. Accessed: May 23, 2025.
- [23] crewAIInc. Email auto responder flow example. https://github.com/crewAIInc/crewAI-examples/tree/main/email_auto_responder_flow/src/email_auto_responder_flow, 2025. Accessed: May 25, 2025.
- [24] Timo Schick, Yeganeh Kordi Dwivedi-Yu, Romal Thoppilan, Lesly Hou, Saghar Hosseini, Shashi Narayan, Nathanael Schärli, Jonathan H. Clark, and Mike Lewis. Toolformer: Language models can teach themselves to use tools. arXiv preprint arXiv:2302.04761, 2023.
