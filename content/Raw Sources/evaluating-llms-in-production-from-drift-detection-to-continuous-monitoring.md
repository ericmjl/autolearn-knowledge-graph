---
title: "Evaluating LLMs in production: From drift detection to continuous monitoring"
type: "raw-source"
url: "https://wandb.ai/site/articles/evaluating-llms-in-production/"
author: "Weights & Biases (no individual author named)"
publication: "Weights & Biases"
published: "2026-06-03"
archived: "2026-11-27T03:01:11Z"
---

> [!quote] Original source
> **Author(s):** Weights & Biases (no individual author named)  
> **Title:** Evaluating LLMs in production: From drift detection to continuous monitoring  
> **Published in:** Weights & Biases  
> **Date:** 2026-06-03  
> **Original:** <https://wandb.ai/site/articles/evaluating-llms-in-production/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-evaluating-llms-in-production-from-drift-detection-to-continuous-monitoring|Source note]]
Themes: [[Evals and agent quality]], [[Loop engineering]]
Why it was archived: How do teams detect and repair judge drift when the model or prompt shifts after launch?

## Archived text

For more information or if you need help retrieving your data, please contact Weights & Biases Customer Support at support@wandb.com

The rise of large language models promises a revolution in AI, but deploying them reliably in the real world introduces a complex new frontier: LLMOps. If you’ve attempted to manage LLMs with traditional MLOps tools, you’ve likely discovered they can fall short. Why? Because LLMs simply don’t play by the old rules.

Traditional machine learning operations were built for a different era. These systems thrive on deterministic outputs from models trained on fixed datasets. They track prediction accuracy against clear ground-truth labels, and the performance metrics map directly to predictable business outcomes.

LLM systems, however, elegantly (or sometimes chaotically) violate every one of these assumptions. A single user query can trigger a complex chain of events involving vector database retrieval, multiple reasoning steps, calls to external APIs, and the synthesis of a final, coherent response. What’s more, identical inputs can produce different outputs due to the stochastic nature of these models. And unfortunately, quality metrics are difficult to quantify. Factors like creativity, tone, and the ability to address underlying user intent often matter far more than simple binary correctness. Standard dashboards, designed for traditional ML, miss these crucial dimensions entirely.

The biggest headaches often emerge from the persistent gap between development and production environments. Models trained on pristine, curated datasets frequently behave differently when faced with the messy reality of user queries. External dependencies can change without warning, and user expectations continuously shift as competitors release new features. Without specialized instrumentation and monitoring, these critical changes often surface only through the unfortunate avenue of user complaints.

This article presents a robust framework for continuous LLM evaluation, a system designed to bridge this gap by connecting granular development traces directly to real-time production monitoring. We’ll start by exploring the unique challenges and new forms of degradation LLMs face. Then, we’ll demonstrate these problems through a controlled experiment on retrieval drift before diving into a practical tutorial on implementing a complete observability loop with Weights & Biases.

“Figure 1: Four distinct types of drift in production LLM systems, each requiring different monitoring approaches.”

LLMs are dynamic systems, meaning their performance in production is never static. They are constantly susceptible to various forms of “drift,” where their behavior or the data they encounter subtly shifts over time. Recognizing these distinct categories is the critical first step to effective monitoring.

As we research further, it becomes clear that teams cannot predict which drift strikes first. The key isn’t anticipation, but rather having clear visibility into each component that matters more than anticipating the failure mode. When retrieval degrades, your traces should immediately highlight it. When model behavior shifts, historical comparisons should reveal the change. And when user queries evolve, robust distribution monitoring should surface the new patterns.

Many teams initially rely on offline evaluation using a static test set. They collect a fixed set of examples, run their models, score the outputs, and consider the evaluation complete. However, real-world production deployment invariably invalidates this static approach.

The fundamental solution is to treat your evaluation dataset as a living artifact that evolves alongside your LLM system. This means regularly incorporating new, representative examples from production usage into your evaluation set. This practice ensures your test distribution remains accurately aligned with actual user behavior, rather than being frozen in time based on initial development assumptions.

The mechanics of this approach require a clear separation of datasets. A development set is actively used during rapid iteration as you experiment with prompts, adjust parameters, or try new models. This set inevitably gets “burned” through repeated exposure, leading teams to unconsciously optimize for these specific examples rather than general quality. Conversely, a test set, which is touched much less frequently, provides a more reliable ground truth for measuring actual progress. This separation prevents overfitting to evaluation metrics while maintaining a stable, unbiased baseline for measurement.

Ensuring stability in your evaluation signals also demands deliberate choices about randomness. Always keep prompts identical across all model comparisons and runs. When using an LLM-as-a-Judge for automated testing, set the temperature parameter to 0 for both the judge and the target model. This crucial step eliminates sampling variance, which can introduce frustrating noise into your metrics. Without these controls, distinguishing genuine improvements from mere random fluctuations becomes nearly impossible.

These practices might seem obvious in retrospect, but many teams learn them through painful experience. Imagine changing three variables simultaneously, watching your scores fluctuate wildly, and then wasting days debugging whether the model truly improved or if you simply got lucky with a random sample.

Can an LLM-as-a-Judge completely replace human evaluation? In short: no. However, they are necessary because human evaluation simply doesn’t scale to the sheer volume of outputs generated in production.

LLM judge systems empower you to evaluate thousands of outputs efficiently without exhausting your team with manual scoring. You design a prompt that explains the task and rubric, provides example outputs, and has the LLM return numerical ratings. This method works remarkably well for assessing factual correctness, coherence, and many aspects of style consistency.

Yet these automated judges also have inherent failure modes that require active monitoring. LLM judges occasionally drift and start giving uneven ratings. Platform provider model updates can subtly shift their scoring behavior, and edge cases in your system’s outputs can trigger unexpected reasoning. These problems can compound silently until you realize that your automated evaluation metrics no longer accurately reflect real user satisfaction.

Catching this “judge drift” requires strategic manual sampling. Regularly read through chunks of judged outputs periodically to surface scoring bugs or strange edge cases that automated methods miss. This manual work, though sometimes tedious, is vital to preventing cascading failures in which flawed evaluation signals lead to misguided optimization decisions.

The fundamental limitation for automated judges appears in tasks without a single verifiable answer. Anything driven by creativity, tone, or personal preference exposes the limits of automated judging. Your LLM judge might confidently rate a response as helpful, while actual users might find it annoying, or vice versa. For these inherently subjective outputs, human validation becomes necessary for quality assurance. The challenge then lies in strategically sampling outputs to ensure reviewers see representative examples without being overwhelmed by an unmanageable volume.

To truly illustrate the insidious nature of retrieval drift, let’s dive into a controlled experiment using LangChain’s public documentation. Our goal is to clearly show how degraded retrieval impacts the quality of an LLM’s response long before aggregate metrics typically flag a problem.

To illustrate, we constructed a simple RAG system. For retrieval, we used sentence-transformers, and for generation and evaluation, we employed Anthropic’s claude-sonnet-4-20250514. The core query we aimed to answer was: “How do I create a basic chain in LangChain? Provide a simple code example.”

We created two distinct document pools for retrieval:

Healthy Pool: Contains three current LangChain documentation pages, covering the introduction, expression language, and chains.

Degraded Pool: Included the same current documents, but crucially, we added an outdated version from LangChain v0.0.200 (a release roughly eight months prior to the current documentation), along with some irrelevant content.

To simulate production scenarios where noisy query matching might pull extra context, we retrieved the top 3 documents for the healthy scenario and the top 4 for the degraded scenario.

All experimental data were sourced from publicly available information to ensure full reproducibility.

The healthy document pool used the current LangChain documentation fetched from:

The degraded pool added an outdated version of LangChain from the v0.0.200 release (August 2023), retrieved directly from the GitHub repository at the v0.0.200 tag. Documents were fetched using Python’s requests library, cleaned with BeautifulSoup4 to extract plain text, and then segmented to maintain semantic coherence.

Embeddings for these documents were generated using the sentence-transformers library with the all-MiniLM-L6-v2 model. Retrieval itself relied on cosine similarity ranking. LLM responses were generated using Claude Sonnet 4 (claude-sonnet-4-20250514) via the Anthropic API, with temperature=0 set for consistent, reproducible outputs. Quality evaluation was performed using the same model as an LLM-as-a-Judge, with a precise prompt: “Rate this answer’s accuracy and relevance on a scale of 1 to 5. Consider whether the code examples are current and the explanation is clear. Return ONLY a single number between 1 and 5, nothing else.”

The results starkly illustrate the impact of retrieval drift across multiple critical dimensions:

The drop in quality is severe, plummeting from a perfect score of 5.0 to a barely acceptable 3.0. This represents a staggering 40% reduction in quality, as rated by our LLM judge.

What makes this particularly insidious is the counterintuitive observation that the average relevance score actually increased (to 0.471) in the degraded scenario. The outdated document scored a high 0.631 relevance, surpassing even the current documents, which averaged 0.418. From the retrieval system’s narrow perspective, it had found a highly “relevant” match. However, from the perspective of the LLM’s final output, this “highly relevant” outdated context introduced significant confusion, directly degrading the response quality by 40%.

Analyzing the actual LLM responses further clarifies the problem. The healthy retrieval produced accurate code using LangChain’s current LCEL (LangChain Expression Language) syntax, complete with modern pipe operators and up-to-date imports like ChatPromptTemplate and StrOutputParser. In stark contrast, the degraded retrieval mixed modern patterns with outdated ones: it presented both LCEL and the deprecated LLMChain class alongside SimpleSequentialChain, which was replaced in LangChain’s v0.1 release.

A developer following the degraded response would unknowingly write code using deprecated patterns. This code might work initially, but it would inevitably fail when dependencies update, or, worse, the developer would waste hours debugging why examples from “the documentation” don’t match current best practices.

Our experiment yielded two crucial and somewhat counterintuitive observations:

Cost and latency don’t always reflect quality: Although the degraded scenario ingested 28% more input tokens, the total cost surprisingly slightly decreased (9.318¢ vs. 9.492¢), and overall latency decreased (8.2s vs. 9.8s). This happened because the LLM, faced with a conflicting and confusing context, likely generated a shorter, less useful, and less confident response, thereby saving on expensive output tokens. The alarming takeaway: a significantly worse answer was, surprisingly, cheaper and faster to generate.

Trace visibility is everything: The most important signal was the retrieval trace. It clearly showed the outdated document (v0.0.200/docs/modules/chains.rst) scoring the highest relevance (0.631). This visual anomaly was the true early warning signal, appearing immediately in the trace, long before any aggregate metric (such as overall cost or an average quality score) fully signaled the severity of the problem. Without trace visibility, this issue would manifest as a mysterious quality drop; with traces, you see the root cause (the problematic document) in the very first degraded query.

Here is a visualization of the cost and quality impact, illustrating these crucial findings:

Figure 2: from the Weights & Biases dashboard: Quality degradation from retrieval drift in a LangChain RAG system. While costs remained relatively stable, response quality dropped 40% when outdated documentation entered the retrieval pool.

This experiment powerfully demonstrates a broader, more critical principle for monitoring LLM systems. Aggregate metrics (like overall quality scores, average latency, or cost per query) are crucial. They tell you something is wrong. However, it’s the component-level traces that tell you what is wrong and where to look.

Consider the ripple effects. A 28% increase in input tokens might eventually trigger a cost alert, but only after your system has processed thousands of degraded, more expensive queries. A quality drop from 5 to 3 will show up in user satisfaction scores, but only after users have received incorrect information, experienced frustration, and potentially formed negative impressions. The trace, however, shows an outdated document with an anomalously high relevance score, giving you that critical signal immediately on the very first degraded query.

Effective production monitoring for LLMs absolutely needs both layers:

Without traces, you’re essentially debugging with incomplete information, sifting through symptoms with limited visibility into root causes. With traces, you can move directly from symptoms to the precise root cause, enabling much faster, more targeted interventions.

The powerful principles we’ve discussed (trace logging during inference, automated evaluation on logged data, and visual monitoring for pattern detection) demand robust infrastructure. While you could build a custom solution, modern LLMOps platforms are designed to provide these capabilities out of the box. This section will walk through a practical implementation using W&B Weave, though similar workflows apply to other platforms like LangSmith, Langfuse, or custom solutions.

Production monitoring begins with structured logging that captures component-level data at every step. Each request needs instrumentation to track inputs, outputs, latency, and costs. Here’s how this looks in practice using W&B Weave’s elegant decorators:

import weave

import numpy as np

from anthropic import Anthropic

# Initialize tracking for your project

weave.init('llm-drift-monitoring-tutorial')

# Initialize your Anthropic client

claude_client = Anthropic()

def calculate_cost(usage):

    """Calculate cost for Claude Sonnet 4

    \$3/M input tokens, \$15/M output tokens"""

    input_cost = (usage.input_tokens / 1_000_000) * 3

    output_cost = (usage.output_tokens / 1_000_000) * 15

    return input_cost + output_cost

@weave.op()

def retrieve_documents(query: str, doc_pool: list, k: int = 3):

    """Retrieval step automatically logged with inputs/outputs"""

    embeddings = get_embeddings([query] + doc_pool)

    similarities = calculate_similarity(embeddings[0], embeddings[1:])

    top_docs = get_top_k(doc_pool, similarities, k)
    
    return {

        "docs": top_docs,

        "relevance_scores": similarities[:k],

        "avg_relevance": np.mean(similarities[:k])

    }

@weave.op()

def generate_response(query: str, context: str):

    """Generation step automatically logged with token counts and cost"""

    response = claude_client.messages.create(

        model="claude-sonnet-4-20250514",

        max_tokens=1024,

        temperature=0,

        messages=[{

            "role": "user",

            "content": f"Context: {context}\n\nQuery: {query}"

        }]

    )
    
    return {

        "response": response.content[0].text,

        "input_tokens": response.usage.input_tokens,

        "output_tokens": response.usage.output_tokens,

        "cost": calculate_cost(response.usage)

    }

@weave.op()

def rag_pipeline(query: str, doc_pool: list):

    """End to end pipeline creates a nested trace"""

    retrieval = retrieve_documents(query, doc_pool)

    context = "\n\n".join(retrieval["docs"])

    result = generate_response(query, context)
    
    return {

        "response": result["response"],

        "metrics": {

            "retrieval_relevance": retrieval["avg_relevance"],

            "input_tokens": result["input_tokens"],

            "output_tokens": result["output_tokens"],

            "cost": result["cost"]

        }

    }

The magic here is the @weave.op() decorator. It automatically logs every function call with its full context: inputs, outputs, execution time, and creates a trace showing the nested operation hierarchy. Token counts are extracted directly from the Anthropic API response objects (response.usage.input_tokens and response.usage.output_tokens). Costs are calculated using Anthropic’s published pricing (\$3 per million input tokens and \$15 per million output tokens for Claude Sonnet 4).

For the drift simulation in this example, we ran identical queries with different document pools each “day,” manually setting timestamps to create the temporal separation visible in the monitoring charts. This compressed timeline effectively demonstrates drift patterns that would typically emerge over weeks or months in real production systems.

“Figure 3: Trace visibility transforms debugging from guessing (left) to diagnosis (right). Component-level inspection reveals the outdated document causing quality degradation.”

Running your LangChain experiment with Weave instrumentation produces detailed traces for every single query. The W&B trace view provides an incredibly granular look at the exact execution flow: the rag_pipeline call triggers retrieve_documents, which returns specific documents with their relevance scores. This then feeds into generate_response, which consumes those documents and returns an LLM response along with token counts and calculated cost.

Figure 4: Component-level trace showing nested operations (retrieve then generate) with metrics at each step. This query used 418 input tokens and 356 output tokens, with an average retrieval relevance of 0.154.

The trace detail in the image reveals a wealth of information invisible to aggregate metrics. You can see precisely which documents were retrieved, their individual relevance scores, how many tokens the context consumed, and how long each step took. When quality degrades, you can immediately drill into the trace and identify the problematic document that caused the issue, or pinpoint a slow-performing step.

This capability directly matches what we observed in our drift experiment. We saw that an outdated LangChain documentation page had a higher relevance score than current, accurate documents, leading the retrieval system to prefer it. Without this level of trace visibility, the problem would manifest as a mysterious, hard-to-debug drop in quality. With traces, you can see the root cause in the very first degraded query, enabling swift action.

Weave automatically aggregates these individual traces into meaningful time series metrics. The platform continuously tracks costs, latency, token consumption, and any custom metrics you define (like retrieval relevance) across all queries. This forms the crucial continuous-monitoring layer, designed to surface drift in real time.

Figure 5: Real-time cost and latency trends. The cost chart shows per-request spending over time, while p95 latency reveals performance patterns

Figure 6: Token consumption patterns showing the distribution of prompts versus completions. Each point is a query that shows how context size correlates with response length.

These interactive dashboards provide a real-time pulse on your system’s health. The “completion tokens vs prompt tokens” chart shows the relationship between the size of the context provided to the LLM (prompt tokens) and the length of its response (completion tokens) across all queries. Each dot represents a single query.

This view is incredibly powerful for surfacing retrieval drift through unexpected token patterns. If your typical queries usually consume between 350 to 450 prompt tokens, but you suddenly see clusters appearing at 450 to 470, it’s a strong indicator that your retrieval system is pulling more context than usual. This often happens before quality metrics overtly degrade. The system is simply working harder (and potentially incurring higher costs and higher latency) to maintain the same output quality.

The latency chart shows the distribution of execution times for your LLM calls. Most queries might complete consistently within 6 to 7 seconds. However, any outliers exceeding 7 seconds clearly indicate either exceptionally complex queries, potential system performance bottlenecks, or an LLM behaving unexpectedly. These are all signals worth investigating to maintain a smooth user experience.

Running our three-day drift simulation with Weave instrumentation produced concrete results visible in these monitoring dashboards:

Day 1 (Healthy baseline):

Day 2 (Introducing noise/early drift):

Day 3 (Full degradation):

Notice something critical here: the quality scores remained stable at 4.0 across all three days. On the surface, this might lead you to believe the system is perfectly healthy. However, the monitoring dashboard immediately reveals the truth: token consumption increased by 12% and average retrieval relevance dropped by 3%. These are crucial early warning signals, visible in the monitoring dashboard before your primary quality metrics or, more importantly, your users, even begin to show problems.

This demonstrates a key insight: cost and efficiency drift often precede quality drift. By the time user satisfaction drops due to declining quality, you may have already processed thousands of queries at an inflated cost. Monitoring these component-level metrics and their distributions catches these issues much earlier in the degradation curve.

Weave seamlessly connects monitoring to evaluation through its powerful Evaluation API. This allows you to automatically score recent production data and continuously track quality trends over time:

import weave

@weave.op()

def judge_quality(query: str, response: str):

    """LLM as judge scorer for automated evaluation"""

    score = judge_llm.invoke(

        f"Rate this response's accuracy, helpfulness, and coherence "

        f"on a scale of 1 to 5 for the query '{query}': {response}. "

        f"Return ONLY a single number between 1 and 5, nothing else."

    )
    
    try:

        return {"quality_score": int(score.strip())}

    except ValueError:

        return {"quality_score": 0}

# Recent queries from your production logs in W&B

recent_queries_sample = [

    {"query": "How to do X in LangChain?", "response": "Response for X"},

    {"query": "Explain Y in Python.", "response": "Response for Y"},

    # ... up to 100 recent production queries

]

# Set up the evaluation

evaluation = weave.Evaluation(

    dataset=recent_queries_sample,

    scorers=[judge_quality]

)

# Run the evaluation against your pipeline

results = evaluation.evaluate(rag_pipeline)

print("Evaluation results available in W&B.")

This code creates a continuous feedback loop: production traffic gets logged, recent queries are automatically evaluated, quality trends are monitored, and any anomalies trigger immediate investigation. The entire workflow remains within a single platform, eliminating the need to jump between disconnected logging infrastructure, bespoke evaluation scripts, and disparate monitoring dashboards. This streamlined approach significantly reduces context switching and accelerates the debugging process.

Beyond the generic dashboards, many monitoring signals are overlooked until problems become critical. These are the metrics that offer the earliest insights into potential drift.

Cost tracking needs to be granular, at the individual request level, not just monthly aggregates. You need clear visibility into token consumption per query. If typical requests consume 696 tokens (like our Day 1 baseline) and you suddenly see clusters of 782-token requests appearing, something has changed. Investigate immediately, before users notice quality drops or your monthly bill spikes.

Many early warning signs appear in trace behavior before aggregate quality metrics show any degradation. Look for unexpected token usage patterns, higher latency without a corresponding increase in query complexity, or odd retrieval behavior. If your RAG system suddenly retrieves four documents per query instead of three, examine whether those additional documents truly add value or merely introduce noise. If generation latency doubles without any changes to the prompt, investigate whether the model is engaging in more reasoning steps than necessary.

One common oversight is ignoring latency and the computational “reasoning effort” in model evaluations. Public benchmarks rarely report these metrics, but they are enormously important for production viability. Some newer, more complex “thinking” models can be significantly slower and more expensive to run, making them impractical despite potentially higher accuracy scores. A model that scores 2% better on your offline benchmark but takes 10 times longer to respond might be the wrong choice for your low-latency application.

Quality monitoring requires full observability of each component of your LLM application, rather than relying solely on final output scores. You need a single, unified view into model behavior, retrieval changes, data shifts, and evolving user patterns. When something looks strange in the traces (an odd scorer behavior, weird retrieval patterns, anything that doesn’t match your expectations), investigate proactively before it compounds into a larger, user-visible problem.

The solution to managing LLMs in production isn’t about simply adding more tools to an already complicated stack. Instead, teams need a single, integrated platform that seamlessly connects experiment logging, evaluation, and production monitoring.

Context switching is a productivity killer during debugging. When investigating a production issue, you need immediate access to development experiments that tested similar scenarios. When running evaluations, you need production traces to verify that your test set still accurately reflects reality. When experimenting with a new prompt, you need cost and latency data from production to make informed tradeoffs about model choice and sampling parameters.

Tools designed with this unified workflow in mind let you spot bugs by focusing on traces and visually verifying that responses look as expected. The goal of this visibility is to answer “what is changing?” with concrete evidence, rather than forcing educated guesses based on incomplete signals. Our LangChain experiment powerfully demonstrated this principle: seeing the outdated document in the retrieval trace immediately explained the drop in quality, without requiring complex cross-dashboard correlation analysis.

This approach demands that evaluation and monitoring be treated as ongoing, continuous practices, rather than a mere deployment checklist. It requires discipline to regularly review traces, maintain “golden datasets” with fresh examples, and proactively investigate anomalous patterns, even when aggregate metrics temporarily appear acceptable. The alternative is far worse: waiting for problems to become glaringly obvious through widespread user complaints or significant cost overruns.

Teams that get this right build a crucial “muscle memory” around reading traces, understanding component interactions, and investigating anomalies early. While perhaps less “exciting” than shipping new features, it’s the bedrock that keeps LLM systems reliable and trustworthy over time. You catch the subtle retrieval degradation affecting 5% of queries before half your users complain. You notice the prompt change that increased token consumption by 12% before the monthly bill arrives. You observe a shift in model behavior that will eventually degrade quality, leading to a plummet in user satisfaction scores.

The ultimate goal isn’t perfect monitoring, because perfect monitoring is an impossible dream for systems with inherent stochasticity and subjective quality criteria. The goal is sufficient visibility to notice when things start drifting before they become emergencies. Our experiments clearly illustrated how subtle changes can have measurable impacts: a 40% drop in quality from just one outdated document, or a 12% increase in tokens with otherwise stable quality scores. Catching these critical patterns early requires component-level trace visibility that standard dashboarding simply cannot provide.

All experiments described in this article use publicly available data and open-source tools to ensure full reproducibility. The complete source code, including data fetching scripts, experiment runners, and analysis notebooks, is available on GitHub at: https://github.com/abduldattijo/llm-evaluation-experiments

To reproduce the LangChain drift experiment and the W&B Weave observability tutorial:

# Clone the repository

git clone https://github.com/abduldattijo/llm-evaluation-experiments

cd llm-evaluation-experiments

# Install dependencies

pip install -r requirements.txt

# Set your Anthropic API key

export ANTHROPIC_API_KEY="your-anthropic-api-key-here"

# Run the RAG drift detection experiment

python experiments/rag_drift_experiment.py

# Set your Weights & Biases API key

export WANDB_API_KEY="your-wandb-api-key-here"

# Run the W&B monitoring tutorial

python experiments/weave_observability_tutorial.py

The experiments were run with the following versions (full dependency specifications with pinned versions are in requirements.txt in the repository):

Both experiments leverage LangChain’s public documentation:

All documents are cached within the repository under data/documents_cache/ to ensure consistent results across multiple runs. This cache includes both the raw HTML and the processed plain-text versions.

Running both experiments should incur approximately \$0.03 to \$0.05 in API fees:

Weights & Biases Weave is free for individual use, offering up to 100GB of trace storage per month.

The drift detection principles demonstrated here are highly adaptable and can be implemented with various other tool combinations:

The repository includes notebooks/alternative_implementations.ipynb, which shows how to adapt the experiments for different tool stacks, providing flexibility for your specific environment.

Found an issue, have an idea for an improvement, or want to contribute? The repository welcomes contributions:

The framework presented here (continuous evaluation with component-level visibility) represents the minimum viable approach for operating robust LLM systems in production. Data drift, model drift, retrieval drift, and behavioral drift are not “if” but “when” they will happen. The critical question for any organization is whether you possess the instrumentation to see them coming, the evaluation infrastructure to measure their impact, and the trace visibility to diagnose their root causes effectively, all before they cascade into user-visible failures and business impact.

Implementing these practices isn’t just about preventing failures; it’s about building resilient, trustworthy AI applications that can adapt, evolve, and perform reliably in the dynamic and unpredictable landscape of real-world usage.

All experiments and code are open source at https://github.com/abduldattijo/llm-evaluation-experiments. Contributions, questions, and alternative implementations are welcome.
