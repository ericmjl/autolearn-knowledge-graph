---
type: "source-note"
title: "Notes on: What we learned evaluating an LLM classifier and a code parser against their previous results | Endor Labs"
raw: "what-we-learned-evaluating-an-llm-classifier-and-a-code-parser-against-their-previous"
url: "https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing"
created_at: "2026-11-25T00:01:19Z"
updated_at: "2026-11-25T00:01:19Z"
---
- Archived full text: [[what-we-learned-evaluating-an-llm-classifier-and-a-code-parser-against-their-previous|Full archived text, with credits]]
- Link: <https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing>

## What it says

Endor Labs lessons from running two evals (an LLM classifier and a deterministic code parser) against their previous results. An eval is a quality thermometer, not a pass/fail smoke detector: it runs a real system on a fixed dataset, scores every result, and compares each run to the last accepted baseline. The article covers dataset design, the four-part structure (dataset, runner, grader, baseline), where the right answer comes from, and three operational principles (missing result is never a pass, only stable cases belong in PR checks, honest-range labels). The classifier eval triple-samples every case and re-samples flips five more times before believing them; gains go into the baseline automatically while losses wait for a person. The deterministic parser eval caught a six-file regression hidden behind six improved codebases, something unit tests never measured.

## Claims drawn from this source

- **An eval is a test for quality, not correctness.** It runs your real system on a fixed set of real cases, scores every result, and tells you whether this version is better or worse than the last trusted one. Tests ask whether it works; evals ask how well and whether that changed.
- **Every eval has four parts: dataset, runner, grader, baseline.** The dataset is versioned inputs each with a good-result expectation and reason; the runner goes through the real path, not a mock; the grader turns outputs into scores; the baseline stores the last person-accepted run's scores.
- **The right answer source determines the grader design.** Labeled datasets, reference facts, and benchmarks each support comparison-style graders; judge-based, property-check, and pairwise/human comparison graders handle cases with no answer key.
- **Unstable runs need repeated sampling before a flip is real.** The classifier eval sends every case three times and takes majority; a case that disagrees with its baseline is sampled five more times before the eval believes the flip. A flip that shows once is noise; a flip that shows on every sample is a change.
- **Gains enter the baseline automatically; losses wait for a person.** In the classifier run, improved cases were written into the baseline on their own, while the one case that flipped negative was held out and the run went red until a person decided.
- **Evals catch trade-offs hidden behind green unit tests.** A parser change improved files parsed in six codebases by one to five files each but dropped six files out of roughly 860 in a large compiler codebase; unit tests stayed green because nobody had written that case, and the eval measured the trade.
- **A missing result is never a pass.** Count unanswered checks as inconclusive, keep them out of every score, and treat a run with no results at all as a failure rather than a quiet green. A grader that counts a timeout as a pass hides the exact failure the eval exists to catch.
- **Only stable cases belong in PR checks.** A case that flips between runs fails pull requests at random; keep unstable cases in the nightly run, and promote a case to the PR slice only once it has held steady.
- **Some labels are honestly a range.** When two reviewers would reasonably disagree, let the case accept either adjacent severity level instead of forcing a coin flip into the answer key.
