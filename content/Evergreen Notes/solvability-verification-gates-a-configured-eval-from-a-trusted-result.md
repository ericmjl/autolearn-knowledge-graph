---
type: "evergreen"
title: "Solvability verification gates a configured eval from a trusted result"
created_at: "2026-11-27T09:02:35Z"
updated_at: "2026-11-27T09:02:35Z"
inputs: ["notes-on-inspect-cyber", "two-config-files-make-sandboxed-cyber-evals-reproducible"]
provenance_urls: ["https://inspect.cyber.aisi.org.uk/configuration-validation.html", "https://www.aisi.gov.uk/blog/inspect-cyber", "https://simonwillison.net/2026/Aug/5/incident-report/", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["How does Inspect Cyber's two-file sandbox structure verify solvability before a result is trusted?"]
---
Agent synthesis

Solvability verification gates a configured eval from a trusted result. An eval can parse, load, and start a run while being unsolvable, and the first failure that surfaces gets misread as an agent limitation instead of a setup bug. Inspect Cyber's configuration-validation page shows the mechanism: a verify_solutions() solver bypasses the model entirely, executes a reference solution script in the sandbox, and pushes the result through the scoring pipeline. Any score below perfect flags a misconfiguration before a costly suite run.

The Kali Linux case shows why the check belongs in CI. A change to Kali made many evaluations unsolvable, and developers who verify solutions as part of CI would have spotted the break sooner, with more time to fix it. The two-file reproducibility note says the eval is a spec that re-runs (see: two config files make sandboxed cyber evals reproducible); this note says the spec is only trustworthy once a solution script proves it is solvable, because variants and sandbox settings are otherwise conventions on paper. Run the verify step on every config change, not just before a release.

The mechanism rewards realistic scripts. verify_solutions() ignores the prompt, runs ./solution.sh in the sandbox (solution.bat on Windows, selected by os_type: windows metadata), and can copy extra files like a Python script invoked from solution.sh. Keep the scripts free of privileged knowledge of the evaluation, so the check grades the environment rather than the model. The synthesis with the reproducibility note is sharp: re-running an eval with different prompts and affordances only separates a model weakness from a harness weakness when the baseline is proven solvable. Solvability is the gate that makes the two-file structure honest.

Block any eval from the suite whose solution variant fails verification, and re-run that verification in CI whenever the sandbox or eval config changes.

## Where it comes from

- [[notes-on-inspect-cyber|Inspect Cyber]]

## What this builds on

- [[two-config-files-make-sandboxed-cyber-evals-reproducible|Two config files make sandboxed cyber evals reproducible]]
