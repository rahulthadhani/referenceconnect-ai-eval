import sys
import time
import pandas as pd
from pathlib import Path

sys.path.insert(0, ".")
from rag.pipeline import load_vectorstore, build_qa_chain

OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

queries_df = pd.read_csv("data/queries.csv")
vectordb = load_vectorstore()
chain, retriever = build_qa_chain(vectordb, version="v2")

results = []
print(f"Running {len(queries_df)} queries (v2)...\n")

for _, row in queries_df.iterrows():
    query = row["query"]
    category = row["category"]
    query_id = row["query_id"]

    start = time.time()
    answer = chain.invoke(query)
    elapsed_ms = round((time.time() - start) * 1000)

    sources = [doc.metadata["source"] for doc in retriever.invoke(query)]
    word_count = len(answer.split())

    results.append(
        {
            "query_id": query_id,
            "query": query,
            "category": category,
            "answer": answer,
            "sources": str(sources),
            "word_count": word_count,
            "latency_ms": elapsed_ms,
            "model_version": "v2",
        }
    )

    print(f"[{query_id}] {category} | {word_count} words | {elapsed_ms}ms")

df = pd.DataFrame(results)
df.to_csv(OUTPUT_DIR / "results_v2.csv", index=False)
print(f"\n[OK] Saved results/results_v2.csv ({len(df)} rows)")
