---
title: "Breaking Claude Code Opus 5 Auto Mode"
type: "raw-source"
url: "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/"
author: "Simon Willison"
publication: "Simon Willison’s Weblog"
published: "2026-08-27"
archived: "2026-11-21T04:01:13Z"
---

> [!quote] Original source
> **Author(s):** Simon Willison  
> **Title:** Breaking Claude Code Opus 5 Auto Mode  
> **Published in:** Simon Willison’s Weblog  
> **Date:** 2026-08-27  
> **Original:** <https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-breaking-claude-code-opus-5-auto-mode|Source note]]
Themes: [[Agent security]]
Why it was archived: Claude Code auto mode is a containment control for coding agents; the wiki covers injection and the trifecta but not auto-mode classifiers

## Archived text

27th August 2026 - Link Blog

Breaking Claude Code Opus 5 Auto Mode. Anthropic are putting a great deal of faith in Claude Code's auto mode for protecting their coding agent users against prompt injection attacks. They recently made that the default and have made bold claims about its effectiveness.

Johann Rehberger is one of the most credible prompt injection researchers active today. He found an attack against auto mode which he claims works 80% of the time, by tricking Claude Code into downloading and uncompressing a zip archive, then executing code that imports base64 without noticing that this will import and execute a local struct.py file extracted from the archive.

In a few cases auto mode directly prevented the agent from preventing harmful code from continuing to execute!

In a few runs Claude tried to terminate the malware process once it noticed the compromise, but Auto Mode denied the cleanup command.

Claude detects the compromise, but Auto Mode blocks its cleanup command

The safety mechanism itself can become part of the failure. The classifier allowed the creation of the malware process, but then it blocked the command intended to stop it!

I agree with Johann's conclusion here: the only safe way to run agents if there's any risk of attracting the attention of an adversarial attack is with a sandbox:

- Run unattended coding agents in a container, VM or OS sandbox.
- Restrict network egress.
- Monitor your agents.
- Do not expose home directories, SSH keys, cloud credentials,… to the agent runtime. [...]

Update 30th August 2026: On Lobste.rs hyperpape points out that this doesn't fit the bill of a classic prompt injection attack because at no point are malicious instructions from the website accidentally followed by the LLM. They're right: this is more of a confused environment attack where the nature of the environment that the agent is exposed to results in an exploit.

Recent articles

- Running the full server-side Datasette Python app in the browser with service workers and Pyodide - 17th November 2026
- Locating the source of a mysterious beep with Claude - 9th November 2026
- Hide your slop PR descriptions behind  - 9th November 2026
- Qwen 3.8 27B on my laptop can interpret model weights, too - 3rd November 2026
