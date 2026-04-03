# ReferenceConnect AI Evaluation System

An end-to-end AI search evaluation system that simulates the query pipeline of a 
production RAG-based product, then automatically scores output quality across 
relevance, accuracy, and latency — replicating the evaluation workflow used by 
AI product and analytics teams.

## Results

| Metric | V1 Baseline | V2 Improved | Delta |
|---|---|---|---|
| Avg Relevance Score (1–5) | 4.25 | 4.88 | +0.62 |
| Keyword Accuracy | 51.7% | 73.5% | +21.8% |
| Avg Word Count | 24 words | 70 words | +46 words |
| Avg Latency | 1,531ms | 2,191ms | +660ms |

## Project Structure
referenceconnect-ai-eval/
├── data/
│   ├── documents/        # scraped + authored knowledge base (16 docs)
│   ├── queries.csv       # 40 simulated customer queries across 6 categories
│   ├── scraper.py        # web scraper for help center docs
│   └── verify.py         # corpus verification script
├── rag/
│   ├── pipeline.py       # document loading, embedding, RAG chain
│   ├── run_baseline.py   # runs all queries through v1 and saves results
│   ├── run_v2.py         # runs all queries through v2 and saves results
│   └── test_query.py     # quick single-query test
├── eval/
│   ├── metrics.py        # LLM-as-judge scoring, keyword accuracy, latency
│   ├── run_eval.py       # runs evaluation pipeline on v1 and v2
│   └── export_excel.py   # exports formatted Excel report
├── results/
│   ├── eval_v1.csv       # v1 evaluation results
│   ├── eval_v2.csv       # v2 evaluation results
│   └── eval_report.xlsx  # formatted Excel report with 4 sheets
├── dashboard.py          # Streamlit analytics dashboard
├── FINDINGS.md           # written analysis and recommendations
└── requirements.txt

## What It Does

1. **Scrapes and builds a document corpus** from public help centers (Slack, Zapier, Figma, Notion) using BeautifulSoup
2. **Embeds documents into a vector store** using OpenAI embeddings and ChromaDB
3. **Runs 40 simulated customer queries** through two versions of a RAG pipeline
4. **Evaluates output quality** using three metrics:
   - LLM-as-judge relevance scoring (1–5) via GPT-4o-mini
   - Keyword accuracy against expected answer keywords
   - Response length and latency tracking
5. **Compares v1 vs v2** — v2 improvements include increased chunk retrieval (k=3→k=5) and an improved system prompt
6. **Visualizes results** in an interactive Streamlit dashboard with three views: overview, query explorer, and error patterns
7. **Exports findings** to a formatted Excel report and written analysis

## Tech Stack

| Layer | Tools |
|---|---|
| RAG Pipeline | LangChain, ChromaDB, OpenAI API (gpt-4o-mini) |
| Evaluation | LLM-as-judge, Pandas, custom keyword matching |
| Dashboard | Streamlit, Plotly |
| Data Collection | requests, BeautifulSoup |
| Reporting | openpyxl, Markdown |

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Add your OpenAI API key to a `.env` file:
OPENAI_API_KEY=sk-...

## Running the Project
```bash
# 1. Scrape documents
python data/scraper.py

# 2. Build vectorstore
python rag/pipeline.py

# 3. Run baselines
python rag/run_baseline.py
python rag/run_v2.py

# 4. Evaluate
python eval/run_eval.py

# 5. Export Excel
python eval/export_excel.py

# 6. Launch dashboard
streamlit run dashboard.py
```

## Key Findings

- Policy and technical queries improved the most in v2 (+1.00 and +0.92 relevance respectively)
- Comparison queries remain the weakest category — the corpus lacks direct plan-to-plan content
- V2's latency increase (+660ms) is a direct tradeoff for retrieving more chunks — a real production consideration
- Full analysis in [FINDINGS.md](FINDINGS.md)