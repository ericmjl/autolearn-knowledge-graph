---
title: "OpenAI’s August fix for theft of reasoning traces was quickly bypassed"
type: "raw-source"
url: "https://www.csoonline.com/article/4240662/openais-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed.html"
author: "Evan Schuman"
publication: "CSO Online"
published: "2026-10-26"
archived: "2026-11-23T02:00:52Z"
---

> [!quote] Original source
> **Author(s):** Evan Schuman  
> **Title:** OpenAI’s August fix for theft of reasoning traces was quickly bypassed  
> **Published in:** CSO Online  
> **Date:** 2026-10-26  
> **Original:** <https://www.csoonline.com/article/4240662/openais-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed.html>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-openai-s-august-fix-for-theft-of-reasoning-traces-was-quickly-bypassed|Source note]]
Themes: [[Agent security]]
Why it was archived: What concrete mitigations do providers and clients adopt after replayable encrypted reasoning traces are shown to cross models and sessions?

## Archived text

It’s a wakeup call to CISOs that a fix doesn’t always fully solve a problem with a model; it's critical to retest.

Cybersecurity research firm Xint on Monday published details of a bug in the OpenAI API that leaks raw reasoning traces from frontier OpenAI models, revealing the risk of other data leaks. OpenAI has confirmed the flaw, mitigated it, and paid a bug bounty for its discovery.

The problem is that OpenAI had already deployed mitigations for the issue in August after a research report dubbed Stolen Thoughts revealed a similar bug that allowed theft of reasoning traces, with possible consequences including large-scale data extraction and the ability for attackers to execute invisible prompt injections and to embed malicious payloads to poison public agentic rollouts. Xint’s discovery bypassed those mitigations.

OpenAI did not respond to a request for comment.

Fixing fixes like this is starting to become a trend among the major AI vendors, with AWS earlier this month reporting that it had fixed a bug in April, only to then have to refix it in September.

Bypassing mitigation

Xint is describing the current hole as compaction smuggling. Its blog post about the flaw described its researchers’ methodology.

“Our new technique, compaction smuggling, moves one model’s reasoning to another model by encoding it inside a compaction,” they wrote.

First, they captured the encrypted reasoning from a designated task, removed the original task from the history, and preserved the reasoning verbatim.

Then “we asked for the reasoning under a ‘solution’ key in a JSON object, with every space replaced by a tab (\t), which was enough to slip past OpenAI’s usage-policy classifiers,” the post said. “Encrypted compaction items are still portable, so we sent the compaction item to gpt-4.1 and gpt-4o and asked each to output its input exactly as-is, which they happily did. We then decoded the JSON and converted tabs back into spaces.”

The post added that the tactic worked “because OpenAI’s August mitigations only block replaying reasoning into a different model, and the compaction call runs on the same model that produced the reasoning. The attack worked at every reasoning effort we tried.”

A hard problem to solve

Tim Becker, lead researcher at Xint and the author of the blog post, said in an interview that some of the flaw’s timeline is unknown. For example, the Stolen Papers post went live August 10, but Becker only knows that OpenAI addressed that problem at some point before that date. And, he said, OpenAI didn’t publish when it implemented the fix for the issue that Xint reported; unlike with traditional patches, an AI model maker can make changes silently. “It’s sort of security through obscurity,” he said, using a term that historically has meant that something was only protected by the fact that almost no one knew of its existence.

Protecting such a model, Becker said, “is a very fundamentally hard problem to solve,” mostly because of the massive number of changes that today’s models routinely undergo.

The models “are a moving target and that is part of the problem. Any mitigation is going to be somewhat brittle,” he said.

As well, Frank Dickson, principal analyst at Dickson Research, noted that AI models tend to feed on themselves operationally, which is why Xint’s method worked.

“Compaction runs on the same model that produced the reasoning, so it sailed past the August mitigation, which only blocked replaying reasoning into a different model,” he said. “Swapping spaces for tabs was enough to slip past the usage-policy classifiers. The vault was locked. The clerk holding the key would still read the letter aloud if you asked nicely. OpenAI did fix the bug it was shown. The trouble is that it was shown only one door.”

Risk to enterprises

Analysts and consultants said this is an immediate big problem for the major AI vendors, but there is a clear secondary risk for enterprise CISOs.

Erik Avakian, technical counselor at Infotech, said that the Xint team “circumvented the protections by using legitimate functionality already built into the platform. For most enterprises, while this specific finding may not rise to the level of an immediate crisis, its significance is that it demonstrates how legitimate AI platform features can be combined to bypass narrowly designed safeguards.”

“This can leave organizations exposed to risks that a vendor’s individual patch may not fully address,” he said. “It reinforces just how difficult it can be to fully address these vulnerabilities in situations where different components of an AI system interact in ways that create unintended risks.”

Avakian said that this should be a heads-up for the enterprise.

“For CISOs, the takeaway is that a vendor’s fix for a specific exploit shouldn’t, in and of itself, be treated as proof that the underlying weakness has been comprehensively addressed,” he said. “CISOs should press their AI providers to explain not only how a reported exploit was patched, but also how they were tested across interconnected features and services.”

Brian Levine, a partner with consulting firm Control Risks, added that he thinks CISOs should look at the overall pattern of holes like these that need to be fixed repeatedly.

“Vendors are fixing the specific attack path that was reported, not the underlying class of weakness, and researchers are walking right back in through a side door,” he said. “A patch notice is not proof the risk is gone. Stop treating an AI vendor’s ‘fixed’ as the end of the conversation. Ask what variant testing was done and build regression notification into your contracts.”

Jeff Valdes, a director at consulting firm Acceligence, shared similar fears.

“This is what happens when you treat security as a game of whack-a-mole instead of fixing the underlying plumbing,” Valdes said. “Patching a symptom while leaving the helper pipes wide open isn’t a remediation strategy. It’s just kicking the vulnerability down to the next release. If an attacker can smuggle the model’s internal scratchpad across API boundaries to steal training data, what makes anyone think enterprise prompts and sensitive intermediate context are truly quarantined?”

In addition, Pieter Arntz, malware intelligence researcher at Malwarebytes, observed that this summer’s OpenAI fix was inadequate. “The earlier mitigation was incomplete, which is a fair description of a gap,” Arntz said.

“Retest after vendor fixes,” he advised. “As the AWS case shows, a fix in one place can leave other paths open. Verify with your own testing rather than relying on the vendor’s word.”

Aman Mahapatra, chief strategy officer for New York City-based technology consulting firm Tribeca Softech, said it is almost impossible for the largest AI vendors to not approach these big reports piecemeal.

“AI vendors are patching exploits on a surface that grows by several features a month,” he pointed out. “Until they fix properties instead of paths, CISOs should assume every AI security fix is partial, every encrypted blob is readable, and every vendor guardrail is one encoding trick from irrelevant. The trend is real, and ‘the fix didn’t work’ undersells what is happening.”

He noted that, in both the OpenAI and AWS cases, the vendor fixed the proof of concept and left the property intact. “Patch the path, keep the property,” he said. “On platforms assembled from composable features, every new feature is a fresh path to the same asset, and point fixes on a combinatorial surface will keep losing.”

CISOs unused to the agentic model

Mahapatra said the cybersecurity industry should learn lessons from its own history.

“Cryptographers learned this two decades ago with padding oracles: any system that decrypts on a client’s behalf and returns anything derived from the plaintext is an oracle. AI platforms are relearning it with a twist,” he said. “Every LLM step that can see a secret and accept instructions is an oracle, and natural language is the most expressive oracle interface ever built.”

He noted that compaction did exactly what it was designed to do, and its portability across models exists so agentic tools like Codex can let users switch models mid-session. “The feature and the vulnerability are the same capability, which is why fixes keep arriving narrow,” he said.

But, he argued, the bigger problem is that CISO operations are not yet used to the agentic model way of doing things.

“AI platform flaws arrive with no CVE, no advisory, and no patch notes. Enterprise vulnerability management, built on CVE feeds and vendor advisories, is blind to its most consequential new suppliers,” Mahapatra said. “CISOs should write security notification obligations into AI provider contracts, assign someone to track researcher disclosures against the platforms they use, and ask one question after every vendor fix: did you fix the report or the class, and what variant analysis supports that answer?”

He also raised questions about the small size of the bounty paid to Xint.

“A \$6,000 bounty for a bug enabling exactly the industrial-scale distillation the NSA, CISA, and FBI warned about in a joint advisory in September is a pricing signal that researchers with other buyers will notice,” he said.
