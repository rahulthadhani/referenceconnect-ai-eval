# ReferenceConnect AI Evaluation System

An AI search evaluation system that uses RAG (Retrieval-Augmented Generation) 
to answer user queries, then scores output quality across relevance, accuracy, 
and latency — replicating the evaluation workflow used in production AI products.

## Project Status
- [x] Phase 1: Project setup, web scraper, document corpus
- [ ] Phase 2: RAG pipeline
- [ ] Phase 3: Evaluation metrics engine
- [ ] Phase 4: Analytics dashboard
- [ ] Phase 5: Findings report + Excel export

## Tech Stack
- Python, LangChain, ChromaDB, OpenAI
- Pandas, Streamlit, Plotly

## Setup
\```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
\```