# AI Search Evaluation — Findings Report

## Project Overview
This project evaluates a RAG-based search system across 40 simulated customer 
queries spanning 6 categories: policy, how-to, comparison, pricing, contact, 
and technical. Two model versions were compared using LLM-as-judge relevance 
scoring, keyword accuracy, response length, and latency.

---

## Key Findings

### Overall Performance
| Metric | V1 Baseline | V2 Improved | Delta |
|---|---|---|---|
| Avg Relevance Score (1–5) | 4.25 | 4.88 | +0.62 |
| Keyword Accuracy | 51.7% | 73.5% | +21.8% |
| Avg Word Count | 24 words | 70 words | +46 words |
| Avg Latency | 1,531ms | 2,191ms | +660ms |

### What Improved Most
- **Policy queries** showed the largest relevance gain (+1.00), jumping from 
  3.86 to 4.86. V1 frequently refused to answer policy questions due to 
  insufficient context retrieval.
- **Technical queries** improved by +0.92, driven by better chunk retrieval 
  (k=3 → k=5) surfacing more relevant document sections.
- **Keyword accuracy increased by +22%** across all categories, indicating 
  that v2 answers are covering the expected topics more completely.

### The Latency Tradeoff
V2 is 660ms slower on average. This is a direct consequence of retrieving 
5 chunks instead of 3 — more context means better answers but higher latency. 
In a production system, this tradeoff would need to be evaluated against 
user experience requirements. For a customer support use case, the accuracy 
gain likely justifies the latency cost.

### Remaining Weaknesses
- **Comparison queries** remain the weakest category (4.00 in v2), as the 
  document corpus does not contain direct plan-to-plan comparisons.
- **4 queries still scored below 3/5 in v2**, all involving specific product 
  details not present in the knowledge base.

---

## What Changed Between V1 and V2
| Change | V1 | V2 |
|---|---|---|
| Chunks retrieved (k) | 3 | 5 |
| System prompt | Strict — refuse if unsure | Instructed to use partial context |
| Model | gpt-4o-mini | gpt-4o-mini |

---

## Recommendations
1. **Expand the document corpus** with comparison pages and plan-specific 
   FAQs to address the weakest query category.
2. **Investigate hybrid retrieval** — combining keyword search with vector 
   search (BM25 + embeddings) to improve recall on specific technical queries.
3. **Set a latency budget** — if sub-2000ms responses are required, consider 
   caching common queries or reducing chunk size to speed up retrieval.
4. **Run evaluation on real user queries** — the simulated query set covers 
   common patterns but real user language is more varied and unpredictable.

---

## Methodology
- **LLM-as-judge:** Each (query, answer) pair was scored 1–5 by GPT-4o-mini 
  using a structured prompt. This is a standard industry technique for 
  scalable answer quality evaluation.
- **Keyword accuracy:** Expected keywords were defined per query and checked 
  against the answer using exact string matching.
- **Corpus:** 10 documents scraped from public help centers (Slack, Zapier, 
  Figma, Notion) plus 6 manually authored domain-specific documents.