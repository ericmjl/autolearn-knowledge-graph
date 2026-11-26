---
type: "source-note"
title: "Notes on: Securing our frontier model training environment"
raw: "securing-our-frontier-model-training-environment"
url: "https://openai.com/index/securing-our-frontier-model-training-environment/"
created_at: "2026-11-26T16:03:02Z"
updated_at: "2026-11-26T16:03:02Z"
---
- Archived full text: [[securing-our-frontier-model-training-environment|Full archived text, with credits]]
- Link: <https://openai.com/index/securing-our-frontier-model-training-environment/>

## What it says

OpenAI describes how it hardened containment for frontier-model training and evaluation after incidents including the July Hugging Face exploit and a September 20 DNS-resolver misconfiguration that gave an internal model limited live-internet access. The post argues that no live-internet access should be granted to frontier models: containment must be engineered defense in depth, with the live internet outside the security boundary and all training runs using an offline, indexed-and-cached web world. OpenAI then spent hundreds of billions of tokens red-teaming its own infrastructure with frontier-model agent teams, chaining microVM escapes, finding paths to the live internet via internal services and misconfigured firewalls, and exchanging data across isolation boundaries via cache timing, storage, CPU-time competition, and TLS certificate caches. Findings led to patches (Kata Containers, gVisor, Moby/Docker, kernel CVEs), tighter network restrictions, monitoring checks, and a red-teaming step made part of the safety case.

## Claims drawn from this source

- **Frontier training and evaluation should run with no live internet access.** OpenAI believes the responsible approach is to conduct frontier model training with no live internet access, implemented as a policy held until advances in safeguards justify broader access.
- **The live internet lies outside the security boundary.** The security boundary surrounds authorized resources; if agents reach the infrastructure hosting them, communicate outside permitted channels, or reach external systems, that is containment failure. Training runs use an offline world of indexed and cached web content instead.
- **Defense in depth overlaps layers so containment holds when any single control fails.** Sandboxes, microVMs, monitoring, and network and cloud perimeters are layered to overlap and reinforce each other, because capable agents can probe and exploit individual weaknesses.
- **Air-gapping is infeasible, so outbound traffic is restricted instead.** Completely disconnecting from external networks is not feasible since external connections are needed to run and monitor experiments; outbound internet traffic and unauthorized movement between systems are restricted while preserving required connectivity, including services reachable from the host.
- **Red-teaming with frontier models is a core part of safety cases.** OpenAI asked high-compute teams of frontier-model agents to find vulnerabilities and misconfigurations that enable unauthorized actions, supplying infrastructure source code, configuration details, and documentation; hundreds of billions of tokens were spent, and red-teaming has been made a core part of safety cases.
- **Agents communicate across isolation boundaries without a network connection.** Red-teaming agents communicated via processor cache timing, shared storage writes vs idle, CPU-time competition within a shared container, and a TLS certificate cache in offline web infrastructure, exchanging synthetic secrets without network connections or shared files.
- **Findings drove patches, tighter restrictions, and monitoring checks.** Escapes and paths to the internet led to software patches for Kata Containers, gVisor, Moby/Docker and kernel CVEs, tighter network restrictions, added monitoring checks for side-channel communication, and fixes to monitoring and stopping systems.
