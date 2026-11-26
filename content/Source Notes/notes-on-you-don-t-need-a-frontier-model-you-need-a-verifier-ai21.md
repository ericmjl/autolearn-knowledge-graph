---
type: "source-note"
title: "Notes on: You don't need a frontier model. You need a verifier. | AI21"
raw: "you-don-t-need-a-frontier-model-you-need-a-verifier-ai21"
url: "https://www.ai21.com/blog/you-need-a-verifier/"
created_at: "2026-11-26T14:01:24Z"
updated_at: "2026-11-26T14:01:24Z"
---
- Archived full text: [[you-don-t-need-a-frontier-model-you-need-a-verifier-ai21|Full archived text, with credits]]
- Link: <https://www.ai21.com/blog/you-need-a-verifier/>

## What it says

AI21 argues that agentic search systems fail on selection, not generation: correct answers are usually already in the candidate pool, but majority voting cannot overturn a popular wrong answer. Adding an independent verifier that re-researches each candidate and vetoes the wrong ones lifts a frontier pool from 83.3 to 93.4 on FACTS-Search, past published SOTA, and a trained 8B verifier recovers most of that lift at a fraction of the cost.

## Claims drawn from this source

- **The binding constraint in agentic search is selection, not generation.** Pass@k sits far above single-shot accuracy (pass@1) across every generator tested: correct answers are routinely present in the pool and simply not selected.
- **Majority voting cannot overturn a popular wrong answer.** When half the pool confidently repeats the same wrong entity, voting does not filter the error, it certifies it.
- **Checking is far cheaper than generating.** Answering a hard multi-hop question takes a chain of searches, dead ends, and synthesis; verifying a proposed answer is narrower: research one claim and rule on it.
- **An independent verifier beats SOTA on a frontier pool.** A generator ensemble (Claude Haiku, Sonnet, Opus, Qwen3-Coder-30B-A3B at k=4) scores 83.3 under plain majority voting and 93.4 with a Claude Opus verifier on top, past the published SOTA of 89.4 (GPT-5.6 Sol).
- **Headroom is larger for small generators.** An all-open-source pool (Qwen3-14B and Qwen3-Coder-30B-A3B at k=4) votes to 60.1; a Claude Opus verifier lifts it to 80.4 at $1.76 per question, with 20 points sitting in the pool.
- **A stock small verifier recovers almost nothing; training is required.** A stock Qwen3-8B verifier moves the efficient pool from 60.1 to 62.5 (plus 2.4 points), against Opus's plus 20.3 on the same candidates.
- **Verifier training needs SFT then RL.** RL alone reward-hacks the class imbalance (tool-use rate falls from 94% to 0% in nine steps) and settles into one narrow search behavior; SFT alone teaches the search skill but dilutes the verdict; composed, tool use stays high and becomes adaptive while the verdict sharpens.
- **Verifier metrics must be computed per question and averaged.** Rollout-level verdict metrics (accuracy, precision, recall, F1) routinely improved while the system got worse. Three gaps assign blame: verification lift (precision), aggregator headroom, and the recall cap (fraction of solvable questions where the verifier rejects every correct answer).
- **Precision generalizes across benchmark and tool for free; recall needs a small adaptation.** The FACTS-trained verifier transfers out-of-the-box to BrowseComp-Plus, lifting the downstream vote from 39% to 51%, but empties the pool on 27% of solvable questions; a final SFT on about 85 held-out-domain questions (~15 steps) closes that gap to 4% and lifts the system to 69%.
