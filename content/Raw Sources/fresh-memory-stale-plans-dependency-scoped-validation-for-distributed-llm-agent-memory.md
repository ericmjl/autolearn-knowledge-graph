---
title: "Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory"
type: "raw-source"
url: "https://arxiv.org/html/2609.03340v1"
author: "Evan Chen 1, Shiqiang Wang 2, Christopher G Brinton"
publication: "arXiv"
published: "2026-01-31"
archived: "2026-11-26T06:01:00Z"
---

> [!quote] Original source
> **Author(s):** Evan Chen 1, Shiqiang Wang 2, Christopher G Brinton  
> **Title:** Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory  
> **Published in:** arXiv  
> **Date:** 2026-01-31  
> **Original:** <https://arxiv.org/html/2609.03340v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-fresh-memory-stale-plans-dependency-scoped-validation-for-distributed-llm-agent-memory|Source note]]
Themes: [[Context, memory and tools]], [[Agent design patterns]]
Why it was archived: How do you detect and repair a stale or wrong external source that an agent loop keeps re-reading?

## Archived text

Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory

Abstract

Distributed LLM-agent teams can read the latest shared facts and still act on an obsolete plan. A planner may derive an action from requirement \(r_{3}\), another agent may commit \(r_{4}\), and an executor may receive \(r_{4}\) without replacing the plan derived from \(r_{3}\). We call this stale-plan execution: state freshness does not establish that the plan authorizing an action remains valid. We introduce PlanFence, a dependency-scoped action-validation protocol. Plans cite the exact public records they used, and an executor validates only the records that can affect the pending external action, replanning once or blocking when validation is incomplete. In 30 controlled live workflows with a post-plan revision, a freshness-only executor acts on the obsolete plan in every task, whereas PlanFence completes all tasks without an invalid action. Controlled replay reveals two conditional boundaries: proactive synchronization yields lower coordination stall at low churn, while PlanFence avoids repeated update-path coordination as churn grows and avoids validating unrelated state as the shared keyspace grows. These are controlled safety and systems-cost results, not general task-accuracy gains.

1 Introduction

Distributed large language model (LLM) agent systems increasingly divide a task among specialized roles that plan, retrieve information, and invoke external tools. Frameworks such as AutoGen, MetaGPT, CAMEL, and ChatDev organize these roles across separate processes or devices [25, 11, 15, 18]. Agents may retain private context and local tools while replicating the public task state needed for coordination, making shared memory a first-class systems concern [27, 19, 24]. This separation lets each role operate independently, but it can also separate an external action from the state and plan that authorized it.

Recent persistent-world studies show that agent-authored artifacts and executable programs can outlive their creators and be reused by later agents through a shared environment [17], making the temporal separation between plan derivation and eventual execution concrete.

Consider a planner that reads requirement \(r_{3}\) and derives plan \(p(r_{3})\). Before execution, another agent commits a revised requirement \(r_{4}\). Background propagation may deliver \(r_{4}\) to the executor without replacing \(p(r_{3})\), so the executor can call a tool with arguments derived from the old requirement while already holding the new one. A reservation may use a superseded destination, a fulfillment action may ship a cancelled order, or a deployment may release an obsolete build. We call this failure stale-plan execution. The failure is not stale memory at the executor; what remains stale is the derivation that supplied the action’s arguments. Installing \(r_{4}\) does not change the fact that \(p(r_{3})\) was produced from \(r_{3}\), so state freshness alone cannot establish that a pending plan is still authorized. The executor must instead verify that the plan descends from the current public records on which its action depends. We call this property lineage validity.

One direct solution is to coordinate public state strongly. Every owner can broadcast its current record ID and invalidate plans whose exact parents no longer match, or executors can compare those parents through one strong service [9, 1, 3]. When this coordination is cheap, it is the simplest safe choice. Section 3 measures when one synchronous public-state transfer enters the critical path. The required check, however, is narrower than globally fresh memory: a reservation action depends on its requirement, not on an unrelated catalog record or another workflow’s state. This creates a systems tradeoff between coordinating early over broad shared state and validating only the records relevant to an action when it is about to execute.

We evaluate this distinction through three questions:

- RQ1:
- Can an agent read the latest state and still act on an outdated plan?
- RQ2:
- As public state changes more often, which causes less waiting: synchronizing every update or validating only before an action?
- RQ3:
- As shared state grows, when does checking only action-relevant state reduce coordination cost compared with checking all shared state?

Our Approach. We separate the safety invariant from the mechanism used to establish it. The invariant is exact lineage validity at a protected action; the systems choice is when and over what scope to check it. This separation leads to PlanFence, a dependency-scoped protocol placed at the action boundary. Each plan cites the exact public records used to derive it, and a tool wrapper declares which records can affect the pending action. Before an external call, the executor validates those dependencies with their owners. A changed input triggers one replan and a second check; an incomplete parent chain, dependency declaration, or owner response blocks the action. PlanFence coordinates public records, not private prompts or hidden reasoning. Figure 1 summarizes this action-boundary gate, from detecting a changed dependency through replanning to the final authorize-or-block decision.

Our main contributions are summarized as follows:

- • 

We identify stale-plan execution and formalize lineage validity, distinguishing current executor state from current plan authorization. In 30 controlled live workflows, the freshness-only owner-head check issues an obsolete action in every task, while PlanFence completes all tasks without an invalid action.

- • 

We design and implement PlanFence for distributed agent memory. Its action-boundary gate binds plans to exact public inputs, validates only tool-declared dependencies with their owners, and permits one replan before failing closed.

- • 

We compare safe coordination policies under identical schedules and map their coordination-stall boundary. Proactive synchronization has lower stall at low update rates; PlanFence avoids repeated unrelated-state coordination as updates grow. Against an equally safe batched all-key check, it lowers both stall and traffic across the tested 8–128 key loopback and AT&T settings.

2 Related Work

Provenance and validation.

Data provenance records which inputs produced a derived object [5], while optimistic concurrency control validates whether a recorded read set remains current before commit [13]. PlanFence uses the same underlying ideas for a different boundary: a generated plan records its public inputs, and an executor validates them before an external action rather than before a database transaction commits. Unlike a database transaction, an LLM-generated plan may persist across role calls, replicas, and state refreshes long after the read that produced it; unless the runtime records exact parents, the executor has no read set to validate at the tool boundary.

Distributed consistency.

Strong registers, proactive replication, epidemic propagation, and CRDTs offer different ways to expose current replica state [3, 9, 1, 7, 20]. Other systems ration consistency or provide application-level choices between latency and freshness [12, 14, 22, 4]. PlanFence does not introduce another consistency model. It specifies which record versions must still authorize the pending action, and it can use either proactive propagation or action-time owner queries to establish that fact.

LLM-agent coordination and memory.

LLM multi-agent systems organize role collaboration and communication through fixed or learned interaction structures [25, 11, 15, 18, 8, 30, 28, 29]; MCP and A2A provide interfaces for tools and agent interaction [2, 10]. Agent memory research instead emphasizes retrieval, experience, and shared memory [16, 26, 6, 21, 23, 27, 19, 24]. Most of this work asks what agents should communicate, retrieve, or retain; persistent-world systems also study artifacts that survive their creators and acquire executable descent. SwarmWorld records content-addressed parent-child program lineages, lets later agents inherit and modify persistent programs, and commits model-generated plans as bounded action queues while the shared world continues to evolve [17]. Its runtime checks determine whether each attempted action is currently legal under spatial, material, energetic, ownership, and permission constraints. This technological lineage supports inheritance and attribution; PlanFence instead uses exact derivation lineage to determine whether a pending action remains authorized by the current versions of its action-relevant public inputs, as reported by their owners.

3 Motivation and Problem Formulation

Strong coordination can keep public state current, but its placement determines whether communication enters the action’s critical path. Figure 2 measures one authenticated TCP synchronization as payload size, delay, and loss change. The operation is inexpensive on favorable paths, yet paying it after every dirty update can accumulate substantial delay as content grows or network conditions deteriorate. Carrier names denote fixed historical traces, not current provider performance.

An executor does not need to reproduce an entire memory system at action time. It needs enough evidence to answer three questions: which public versions produced this plan, which public items can affect this action, and which versions their owners currently authorize. We introduce the corresponding objects in that order and then state the action-validity condition.

3.1 Public state has versions

Let \(\mathcal{A}=\{a_{1},\ldots,a_{N}\}\) be the agents. In distributed agent memory, each agent may hold a local copy of the team’s public state. Private scratchpads, prompts, and hidden reasoning are not public records and lie outside the lineage model.

A semantic key \(x\in\mathcal{X}\) identifies one logical public item across revisions, while a record ID identifies one immutable version of that item. The application assigns \(x\) an authoritative owner \(o(x)\in\mathcal{A}\), whose currently authorized record ID is the head \(H(x)\). Derived public records retain the exact IDs of the versions used to produce them.

Figure 1 instantiates these objects. The semantic key \(x_{\rm req}\) denotes the requirement, and records \(r_{3}\) and \(r_{4}\) are immutable versions with IDs \(\mathrm{id}_{3}\) and \(\mathrm{id}_{4}\). After the revision, the owner reports \(H(x_{\rm req})=\mathrm{id}_{4}\), while plan \(p_{3}=p(r_{3})\) still cites \(\mathrm{id}_{3}\) as its exact parent. Installing \(r_{4}\) changes the executor’s local state, but it does not rewrite the derivation recorded by \(p_{3}\).

3.2 What evidence must authorize an action?

Exact derivation. For a protected action \(a\), let \(L(a)\) be the plan root or roots authorizing its arguments. Immutable parent links record the exact public versions from which those roots were derived.

Declared scope. The tool wrapper declares \(D(a)\subseteq\mathcal{X}\), the public keys whose values can affect the action. This declaration belongs to application code rather than generated prose.

Authoritative currency. For every \(x\in D(a)\), the executor asks owner \(o(x)\) for its currently authorized version \(H(x)\). Starting from \(L(a)\), it also follows exact parents until it reaches the version of \(x\) used by the plan; denote that record ID by \(F_{a}(x)\). The map \(F_{a}\) is the plan’s dependency frontier. An action is lineage-valid at the logged validation point exactly when

3.3 Why each condition is necessary

Equation (1) separates the evidence needed to authorize an action. RQ1 asks whether reading the latest state is enough to authorize a pending plan. It is not: a fresh local requirement cannot show which requirement produced a cached plan, whereas the plan’s exact parent does. For the stale plan, \(F_{a}(x_{\rm req})=\mathrm{id}_{3}\) while \(H(x_{\rm req})=\mathrm{id}_{4}\). Replanning over \(r_{4}\) changes the frontier to \(\mathrm{id}_{4}\) and makes the same check pass.

RQ2 asks when to pay for owner-head coordination: after every update or only when an action is about to execute. A system may distribute authoritative heads proactively or query them at the action boundary, but it cannot infer current authorization from an arbitrary local copy. RQ3 asks how much state to check. The declared set \(D(a)\) contains the action-relevant state, so a change outside \(D(a)\) does not invalidate the action; choosing \(D(a)=\mathcal{X}\) instead recovers all-key validation.

The guarantee consequently requires exact binding, action-time validation, benign authoritative owners, authenticated transport, immutable parent links, and a complete tool-declared \(D(a)\). A missing parent, unavailable or malformed owner response, or incomplete declaration makes validation inconclusive and blocks the action. The check is not an atomic multi-owner snapshot or a transaction spanning the later external service call; Section 6 discusses those boundaries.

4 Dependency-Scoped PlanFence

The three requirements above map directly to PlanFence. Writers first record exact derivation, tool wrappers declare the action’s dependency scope, and the executor compares the resulting frontier with owner heads immediately before execution. A mismatch causes one refresh and replan before the action is revalidated or blocked.

4.1 Recording action-relevant lineage

Application code attaches exact parent IDs whenever it writes a derived public record. Thus a requirement revision cites its previous version, and a role decision cites the requirement visible when the decision was produced. Tool wrappers separately declare \(D(a)\). This dependency contract is part of the trusted computing base: a wrapper must capture dynamic public reads or conservatively declare a broader set.

At validation, owner \(o(x)\) returns the current immutable record ID \(H(x)\) for each declared key. Exact message and conflict checks are implementation details given in Appendix A. Metadata normally moves without record content; the executor fetches and verifies changed content only after it observes a mismatch.

4.2 Dependency-scoped action gate

Algorithm 1 implements the gate. The executor first traverses local exact parents and rejects an incomplete lineage. It then queries \(o(x)\) for every \(x\in D(a)\) concurrently. Matching frontiers authorize the action; a mismatch returns verified current records for one fresh plan. The caller invokes the gate once more with replanned set, so a second change or any incomplete response blocks instead of creating an unbounded replan loop.

4.3 Coordination cost and policy boundary

Let \(R\) be dirty owner updates between protected actions and \(d=|D(a)|\). Per-update metadata sync distributes \(O(RN)\) owner heads early and compares the plan’s parents with the installed heads. Centralized lineage serializes \(O(R)\) commits and later reads. At action time, batched all-key validation checks and serializes \(|\mathcal{X}|\) heads, whereas PlanFence checks only the \(d\) keys in \(D(a)\).

These are head-item counts rather than TCP request counts: either action-time policy can batch multiple heads into one request per contacted owner. PlanFence fetches content only for dependencies whose IDs changed. The comparison does not make PlanFence universally cheaper. When \(R\) is small and links are fast, proactive synchronization removes action-time owner round trips; as churn or irrelevant shared state grows, its broader coordination becomes more costly. The experiments measure this crossover rather than inferring it from the asymptotic terms.

5 Experiments

5.1 Experimental Design

Together with the transport microbenchmark in Figure 2, we use live five-agent workflows and controlled replay. The live workflows test stale-plan execution and repair; controlled replay compares safety, stall, and traffic under identical schedules.

Live and controlled workflows. Five Qwen3.5 agents solve reservation, fulfillment, and deployment workflows through separate processes and agent-local public state. These runs test whether a model-generated plan can remain stale after the executor reads a revised requirement. A separate post-hoc audit found the defining pattern in 15/30 exploratory workflows: the executor read the revision but acted from a plan tied to the initial requirement. Those plans did not yet attach immutable memory records as exact parents, and we do not use this exploratory count to estimate natural failure incidence. Appendix A.4 reports the full exploratory audit. The matched intervention below supplies the causal comparison.

For policy comparison, controlled replay deliberately fixes the decisions in 30 public workflow templates while executing the same memory, transport, and validation paths through 3-8 agent-local copies. This design attributes invalid actions, waiting time, and traffic to the memory policy rather than model-output variation. The live workflows ground the basic five-agent, one-revision case. Higher update rates, wider dependency sets, larger keyspaces, and deeper parent chains are controlled stress tests.

Baselines. We use the same policy names in every table and figure. Local replica acts from installed state, while Owner-head freshness reads the current dependency without proving that the plan descends from it. Both deliberately omit lineage. The safe policies bind a plan to exact input IDs and replan once after a mismatch. Centralized lineage uses one shared service; Metadata sync, \(K=1\) announces every dirty owner head; Per-key all-key validation queries each shared key separately; Batched all-key validation returns all shared-key heads in one request per owner; and PlanFence queries only \(D(a)\). We additionally test Majority-replica validation and All-replica dependency validation as strong distributed controls. Metadata sync with \(K>1\) is a safety-cost sensitivity, not a safe headline competitor, because it may compare against an obsolete announced head. In conceptual terms, eager invalidation after every owner update is Metadata sync (\(K=1\)), one strong shared memory service is Centralized lineage, a global epoch is a broad all-key check, and quorum-style reads are represented by the replica controls.

Workloads and comparisons. Each episode forms a plan, changes public requirements, and attempts a protected action under every policy. The primary setting uses eight semantic keys, five agents, 64 work units, one action dependency, and nominal update targets \(\rho\in\{0.25,1,4,16\}\). At \(H=64\), the schedules realize 0.25, 1.0, \(42/11\approx 3.82\), and 14 updates per protected action. We test loopback and fixed AT&T, T-Mobile, and Verizon LTE traces.

The keyspace study varies 8-128 shared keys at five agents, one dependency, \(H=64\), and \(\rho=4\). Its primary reactive baseline batches all-key heads into one request per owner; per-key requests expose an implementation sensitivity. Team size, dependency count, episode length, and quorum provide additional cost checks. Symmetric artifact consumption is retained only as a safety and payload-path control. Appendix B reports the complete grids and secondary sensitivity controls.

Metrics and analysis. The safety endpoint counts issued actions whose plan does not reach every current declared input. We report raw safety, availability, and task-completion counts. Coordination stall is time waiting for synchronization or validation, and distributed traffic includes inter-replica and central-service bytes. Cost comparisons pair identical schedules and bootstrap over workflow families; differences below 10% are treated as practical ties. Appendix A.1 gives the zero-event bounds, resampling procedure, completion criterion, and timeout treatment.

Table 1 provides the safety and cost overview. Its first invalid-action and availability columns establish the safety boundary: a current record is insufficient unless the pending plan is bound to that exact record. Among policies with zero invalid actions and full availability, the cost columns then expose the systems choice. Figures 3 through 5 show why no policy minimizes both coordination stall and traffic in every measured regime.

5.2 RQ1: Can Latest State Still Lead to an Outdated Plan?

Fresh owner state does not invalidate an obsolete derivation; exact lineage does. Table 1 stages the race from Figure 1. Local replicas and owner-head checks without lineage both issue 330/330 actions from obsolete plans. Every strong policy that binds the plan to its inputs instead issues 330/330 lineage-valid actions. Appendix A.6 extends this check across the aligned policy audit: among 32,700 scheduled actions, it finds no invalid action for any method that enforces exact lineage. The sharp counts are protocol outcomes rather than model-accuracy estimates because every staged schedule deliberately places a revision between planning and action.

The stale-plan failure persists when model-generated plans drive tool use. Table 2 follows five Qwen3.5 agents through reservation, fulfillment, and deployment workflows from role-local public state, inserting one requirement revision after planning but before the protected action. Reading the newest owner record without checking the plan issues an obsolete primary action in all 30 tasks. Centralized lineage and PlanFence instead detect the changed input, invoke one fresh planner call, and complete all 30 tasks without an invalid primary action. Their auditors unnecessarily repeat 4 and 10 already-valid actions, respectively; we retain these model-side false positives and do not use the study for synchronization-cost comparison. PlanFence therefore matches centralized-lineage safety and completion in an interactive five-agent system while preserving distributed, owner-managed memory.

5.3 RQ2: Synchronize Every Update or Validate Before Action?

Per-update synchronization has lower stall in the measured low-churn regime, while PlanFence has lower stall than the safe proactive alternatives at \(\rho\geq 4\). Figure 3 maps this boundary across loopback and three cellular traces. Each cell compares PlanFence with the faster of per-update metadata sync and centralized lineage. The proactive choice has a lower point estimate in seven of the eight cells with \(\rho\leq 1\), while both loopback comparisons are practical ties under our 10% threshold. PlanFence leads in all eight cells with \(\rho\geq 4\), by 1.5\(\times\) to 7.1\(\times\) relative to the next-lowest safe policy.

Delaying metadata synchronization trades safety for lower stall. Figure 4 makes this tradeoff explicit on the AT&T trace: increasing \(K\) reduces proactive coordination but leaves the announced head obsolete between barriers and admits more lineage violations. Table 4 reports the underlying counts and costs. Tables 5 and 7 vary team size and episode length. Across these \(\rho=4\) sensitivity checks, PlanFence has lower stall than centralized lineage and metadata sync (\(K=1\)) for \(N=3,5,8\) and \(H=16,64,256\), with 8.0-8.2 KiB/action of traffic. The secondary endpoints use three templates and serve as sensitivity checks rather than standalone population estimates. The measured crossover marks a shift from paying coordination after every update to paying it when an action validates its dependencies.

5.4 RQ3: Check Action-Relevant State or All Shared State?

With equal post-replan validation, dependency scope lowers both stall and traffic across the measured keyspaces. Table 1 first compares centralized lineage, metadata sync (\(K=1\)), and PlanFence in the primary eight-key compact-state setting on the AT&T trace at nominal \(\rho=4\). All three complete 330/330 valid actions, while PlanFence uses 230.8 ms and 8.1 KiB per action, compared with 508.6 ms/15.6 KiB for centralized lineage and 403.4 ms/23.5 KiB for metadata sync; the ordering also holds on the other traces. Figure 5 next compares PlanFence with batched all-key validation under the same one-replan, two-validation path as the shared keyspace grows from 8 to 128 keys.

The action depends on one key. Batched all-key validation checks every shared key in one request per owner, whereas PlanFence queries only the dependency owner. Under these matched semantics, PlanFence lowers median stall from 115.5 to 67.8 ms/action at eight loopback keys and from 199.2 to 66.0 ms/action at 128 keys. Across three AT&T trace offsets, the corresponding medians are 365.7 versus 295.3 ms/action at eight keys and 428.7 versus 345.2 ms/action at 128 keys. Its traffic remains near 8.1 KiB/action while the all-key check grows from 16.4 to 81.7 KiB/action.

The benefit also depends on how much of the keyspace the action actually uses. Appendix Table 6 holds \(|\mathcal{X}|=8\) fixed and widens the dependency set. PlanFence lowers stall by 14.9% and traffic by 50.6% at \(d=1\). At \(d=2\), stall is a practical tie while traffic remains 32.0% lower. At \(d=8=|\mathcal{X}|\), the two validation scopes coincide and both stall and traffic are practical ties. This convergence is the expected boundary of dependency scoping rather than a regime in which PlanFence should dominate.

Independent trace phases support the same aggregate pattern. At 128 keys, the paired PlanFence-minus-batched-all-key stall interval excludes zero at every AT&T trace offset, and the traffic interval excludes zero in every measured network/keyspace stratum. At eight keys, one of the three stall intervals crosses zero, so the latency ordering is not pointwise uniform. Table 8 in Appendix B reports every aggregate, and Table 9 reports the independent AT&T trace offsets. When both methods enforce the same safety rule, PlanFence preserves valid completion while avoiding all-key work that is irrelevant to the pending action.

6 Limitations

Our evaluation is designed to isolate the behavior of the memory policy rather than measure general agent capability. Controlled replay lets every policy face the same decisions and update schedules, while the live workflows show that a model-generated plan can become stale and be repaired before execution. The evidence nevertheless covers only three workflow families, 3-8 agents, constructed keyspaces, and a small set of historical network traces. We therefore treat the stress-test intervals as descriptive and do not infer a general improvement in task quality from them.

PlanFence’s safety guarantee also depends on a clear systems boundary. Owners must be benign, parent links exact, and each tool wrapper responsible for a complete dependency declaration. The present design does not address Byzantine owners, owner migration, inferred dependencies, semantic merging, or private reasoning that never enters the public lineage. Moreover, validation is atomic neither across multiple owners nor with the external action itself; applications that require either property need a transaction mechanism that spans the corresponding boundary. These assumptions determine when the action fence is safe, while engineering choices such as connection reuse, metadata placement, and artifact access can still shift the measured coordination-cost crossover.

7 Conclusion

Stale-plan execution is a lineage failure: current state can coexist with an obsolete derivation. PlanFence records exact parents, validates declared dependencies, replans once, and fails closed. Per-update synchronization has lower stall at low churn; PlanFence avoids repeated coordination as churn grows. Against batched all-key validation, it lowers measured stall and traffic when actions depend on a sparse subset of shared state, and the advantage vanishes as the dependency set reaches the full keyspace. We claim neither universal dominance nor general task-quality gains.

References

- [1] (2012) Consistency tradeoffs in modern distributed database system design: cap is only part of the story. Computer 45 (2), pp. 37–42. Cited by: §1, §2.
- [2] (2024) Model context protocol. Note: modelcontextprotocol.io Cited by: §2.
- [3] (1995) Sharing memory robustly in message-passing systems. Journal of the ACM 42 (1), pp. 124–142. Cited by: §1, §2.
- [4] (2012) Probabilistically bounded staleness for practical partial quorums. Cited by: §2.
- [5] (2001) Why and where: a characterization of data provenance. In International conference on database theory, pp. 316–330. Cited by: §2.
- [6] (2025) Mem0: building production-ready ai agents with scalable long-term memory. arXiv preprint arXiv:2504.19413. Cited by: §2.
- [7] (1987) Epidemic algorithms for replicated database maintenance. In Proceedings of the sixth annual ACM Symposium on Principles of distributed computing, pp. 1–12. Cited by: §2.
- [8] (2024) Improving factuality and reasoning in language models through multiagent debate. In International Conference on Machine Learning (ICML), Cited by: §2.
- [9] (2002) Brewer’s conjecture and the feasibility of consistent, available, partition-tolerant web services. ACM SIGACT News 33 (2), pp. 51–59. Cited by: §1, §2.
- [10] (2025) Agent2Agent (A2A) protocol. Note: github.com/a2aproject/A2A Cited by: §2.
- [11] (2024) MetaGPT: meta programming for a multi-agent collaborative framework. In International Conference on Learning Representations (ICLR), Cited by: §1, §2.
- [12] (2009) Consistency rationing in the cloud: pay only when it matters. In Proceedings of the VLDB Endowment (VLDB), Vol. 2, pp. 253–264. Cited by: §2.
- [13] (1981) On optimistic methods for concurrency control. ACM Transactions on Database Systems (TODS) 6 (2), pp. 213–226. Cited by: §2.
- [14] (2012) Making \(\{\)geo-replicated\(\}\) systems fast as possible, consistent when necessary. In 10th USENIX Symposium on Operating Systems Design and Implementation (OSDI 12), pp. 265–278. Cited by: §2.
- [15] (2023) CAMEL: communicative agents for “mind” exploration of large language model society. In Advances in Neural Information Processing Systems (NeurIPS), Cited by: §1, §2.
- [16] (2023) MemGPT: towards LLMs as operating systems. arXiv preprint arXiv:2310.08561. Cited by: §2.
- [17] (2026) SwarmWorld: stigmergic technological evolution in societies of language-model agents. arXiv preprint arXiv:2608.26081. Cited by: §1, §2.
- [18] (2024) Communicative agents for software development. In Annual Meeting of the Association for Computational Linguistics (ACL), Cited by: §1, §2.
- [19] (2025) Collaborative memory: multi-user memory sharing in LLM agents with dynamic access control. arXiv:2505.18279. Cited by: §1, §2.
- [20] (2011) Conflict-free replicated data types. In Symposium on Self-Stabilizing Systems (SSS), pp. 386–400. Cited by: §2.
- [21] (2023) Reflexion: language agents with verbal reinforcement learning. In Advances in neural information processing systems, Vol. 36, pp. 8634–8652. Cited by: §2.
- [22] (2013) Consistency-based service level agreements for cloud storage. In Proceedings of the twenty-fourth ACM symposium on operating systems principles, pp. 309–324. Cited by: §2.
- [23] (2023) Voyager: an open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291. Cited by: §2.
- [24] (2025) MIRIX: multi-agent memory system for LLM-based agents. arXiv:2507.07957. Cited by: §1, §2.
- [25] (2023) AutoGen: enabling next-gen LLM applications via multi-agent conversation framework. arXiv preprint arXiv:2308.08155. Cited by: §1, §2.
- [26] (2025) A-MEM: agentic memory for LLM agents. arXiv preprint arXiv:2502.12110. Cited by: §2.
- [27] (2026) Multi-agent memory from a computer architecture perspective: visions and challenges ahead. arXiv:2603.10062. Cited by: §1, §2.
- [28] (2025) Cut the crap: an economical communication pipeline for LLM-based multi-agent systems. ICLR (arXiv:2410.02506). Cited by: §2.
- [29] (2025) Multi-agent architecture search via agentic supernet. ICML (arXiv:2502.04180). Cited by: §2.
- [30] (2024) GPTSwarm: language agents as optimizable graphs. ICML (arXiv:2402.16823). Cited by: §2.

Appendix A Implementation Details

Table 3 lists the settings needed to reproduce the runtime behavior. Five agent processes participate. Replicated methods use one SQLite memory process per agent, while central lineage uses one shared SQLite memory process. All communication uses authenticated TCP. Public records are immutable JSON objects in durable SQLite stores. Paired policies receive the same initial records and schedules, and network impairments begin only after setup. We rerun only trials that terminate before any policy decision because of infrastructure failure. Policy-induced blocks, failures, and timeouts remain in all reported denominators.

Each stored public version carries its semantic key, immutable record ID, authoritative owner, monotone owner sequence, exact parent IDs, record type, content size, and public content or content address. An owner accepts a head update only when the writer identity matches the declared owner and the sequence increases; duplicate owner sequences are conflicts. Head announcements send the metadata envelope, while consumers fetch content only after discovering that their local version is obsolete.

A.1 Metrics and statistical analysis

Binary endpoints are reported as raw counts. For zero observed invalid actions, the one-sided 95% exact-binomial upper bounds are 0.90% for 0/330, 9.5% for 0/30, and 0.023% for 0/13,200. These bounds describe empirical implementation coverage; the protocol invariant remains conditional on the assumptions in Section 4. Cost comparisons pair identical schedules and use 2,000 bootstrap draws that resample the three workflow families as clusters. We regard a 10% reduction in median stall or traffic as practically meaningful when safety does not weaken and availability falls by no more than five percentage points. With three families, the intervals describe stability across those families rather than population-wide uncertainty. In Figure 2, the 117.42 ms line is an analytical reference rather than an end-to-end target; elapsed durations from 2 s transport timeouts remain in the latency summaries.

A.2 Controlled live prompting and tool grounding

Each role receives the same short system instruction with its role and workflow family substituted. The user content is a stable JSON object assembled from only the role’s local public state and prior public handoffs. The tool schema then enumerates every permitted identifier, action name, and argument object.

One public correction is allowed after a schema violation. The correction contains the rejection reason and required tool name but no hidden answer. A second violation fails the attempt. Model-facing handoffs contain role content only; raw memory-record IDs, owner IDs, and evaluator fields remain inside the workflow adapter.

A.3 Protected-action and replan harness

The replay uses the same validation code but replaces the model replan with a recorded fresh public decision. It therefore measures the memory mechanism and network path without attributing fixed decisions to new model calls.

A.4 Exploratory live-workflow audit

Before examining stale plans, we verified that the model and tools could solve the workflow with centralized state. All 30 paired tasks completed, and all 480 role decisions satisfied their public tool schemas.

The prespecified audit then asked whether the executor itself read an obsolete requirement. Only 3/30 runs did, below its prespecified threshold of 15. A separate post-hoc analysis revealed a different failure: 28/30 generated plans cited the initial application requirement, and in 15 cases the executor read the revision but still issued the invalid action from that stale plan. These cases span deployment, fulfillment, and reservation with counts 6, 2, and 7. The model produced 240 accepted role decisions from 241 responses, with no unrecovered schema, workflow-contract, or infrastructure failure.

Those plan records stored the application requirement ID in their public payload but did not yet attach the immutable memory record as a parent. The audit therefore shows that generated plans can remain stale; the replay and the matched live study provide the exact-lineage comparison.

A.5 Matched controlled-live check

The matched study crosses three workflow families, ten evaluation seeds, and three memory methods, for 90 attempts. Each task forms a plan over the initial requirement and then receives one owner revision before execution. Owner-head freshness exposes the new record without checking whether the plan used it. Centralized lineage and PlanFence instead validate the plan, fetch the revised input, invoke one isolated planner call, and validate again before acting.

Owner-head freshness issues the stale action and fails all 30 tasks. Centralized lineage and PlanFence each complete 30/30 tasks with no invalid action and one successful replan per task. Their auditors unnecessarily repeat 4 and 10 valid actions, respectively. This model-side variation prevents a live cost comparison, but it does not alter the safety outcome because every protected primary action was already valid.

All 90 attempts complete, and the model produces 780 accepted role decisions from 784 responses. Four initial schema errors are corrected by the one allowed public retry; none remains unrecovered. Each paired centralized-lineage and PlanFence run follows the same workflow steps, and no infrastructure or tool-contract failure occurs.

A.6 Evaluation coverage

The 30-template corpus includes 241 retained live latency samples, while the aligned policy grid schedules 32,700 actions: every exact-lineage method remains safe and available, and stale or delayed-sync controls account for all 4,143 invalid actions. The matched keyspace study completes 13,200/13,200 actions and supplies the scope-cost comparison. The artifact control completes 15,360/15,360 actions with zero lineage violations and two verified fetches per policy and action; because it uses a different action path, it supports payload-path safety but not comparative stall.

Appendix B Controlled-replay ablations

The following studies ask whether the main boundary survives changes in synchronization cadence, team size, dependency count, and episode length. “Valid” means an issued action whose plan reaches every current declared input; a blocked action never enters that numerator. Unless noted otherwise, the tables use compact records, the AT&T trace, and \(\rho=4\).

Large-artifact safety control. Across 960 runs and 15,360 protected actions, every policy fetches and verifies the same changed public artifact twice per action, and every exact-lineage action remains valid. Because this control uses a different action path, we use it to verify payload-path safety but not comparative stall.

B.1 Independent AT&T trace phases

Changing the start point within the AT&T trace changes absolute latency but preserves the pointwise ordering. Table 9 reports the independently replayed 0, 5, and 15 second offsets at both keyspace endpoints. Both exact-lineage methods complete every action. PlanFence has lower median stall and traffic in all six paired aggregates. The paired stall interval excludes zero in five of the six 30-template strata; the eight-key, five-second interval crosses zero and remains a descriptive comparison.

B.2 Learned policy selection does not dominate a transparent rule under OOD shift

Could a learned selector reduce coordination cost without weakening the safety path? We allow it to choose among centralized lineage, metadata sync (\(K=1\)), and PlanFence, all of which retain deterministic exact-lineage validation. Malformed or unavailable selector output falls back to PlanFence. The transparent reference uses metadata sync when \(\rho\leq 1\) and PlanFence otherwise; learned selectors may also choose centralized lineage.

We derive 1,332 examples from the complete controlled-replay campaign, each aggregating six workflows from three families. A policy is eligible if it issues no invalid action and completes every scheduled action. Among eligible policies within 10% of the lowest stall, the target is the policy with the least wire traffic; we call this a safe near-optimal choice. The split contains 648 training, 144 development, and 180 in-distribution (ID) examples. Four disjoint 90-example out-of-distribution (OOD) blocks hold out, respectively, the Verizon trace, interpolated update rates \(\{0.5,2,8\}\), endpoint key counts \(\{8,128\}\), and their compound shift. Selectors see only pre-action workload dimensions and static trace calibration, never profile identity, workflow text, outcomes, or future trace events. Neural results use three-seed ensembles.

Learned selectors improve ID selection but do not consistently dominate the transparent rule under shift. Table 10 reports 95.0-96.7% safe near-optimal selection for the learned models on ID examples, compared with 89.4% for the transparent rule. Under shift, the tree and tabular networks fall to 84.4-94.2%. DeBERTa-v3-base reaches 96.1%, but its conservative three-model batch-one inference costs 34.08 ms. We consider a selector robust only if it is no worse in completion, safe near-optimal choice, Pareto domination, traffic regret, and p95 stall regret after inference, with at least one strict improvement in every OOD block. None passes all four blocks: the tabular models pass only the keyspace block, and neither DeBERTa model passes any block after inference cost. Exact-lineage safety nevertheless remains deterministic under every selector.

Appendix C Validation assumptions and component sensitivities

These studies ask which components the guarantee requires: following the full parent chain, replanning after a detected change, declaring every dependency, and blocking when validation cannot finish. They isolate mechanism behavior rather than network cost or natural error frequency.

The same lineage traversal used by PlanFence authorizes intact chains through depth eight and blocks whenever an intermediate record is missing. Checking only a direct parent works at depth one but cannot prove deeper chains. Replanning turns all 3,000 detected races into valid actions; validation without replanning blocks all 3,000. Reading a fresh requirement without checking its plan, or trusting an arbitrary replica’s head, issues an invalid action in every race. Table 11 reports the raw outcomes.

Figure 6 tests the static dependency-contract assumption over 30 templates and 100 race seeds. Of four truedependencies, one remains declared while the other three are independentlyomitted. Unsafe issuance rises from 0% to 37.4% as the omission probability reaches 50%. Overdeclaration remains safe but grows owner-head checks from four to 36 per action. Under owner outage, missing lineage, malformed owner heads, and a second version change, fail-closed validation blocks all four cases with no issued action; the corresponding fail-open ablation issues an invalid action in all four. These results justify complete contracts and fail-closed behavior; they do not establish how often either failure occurs in deployed multi-agent systems.
