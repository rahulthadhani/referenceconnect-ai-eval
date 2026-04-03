import os
import time
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def keyword_accuracy(answer: str, expected_keywords: str) -> float:
    keywords = [kw.strip().lower() for kw in expected_keywords.split(",")]
    hits = sum(1 for kw in keywords if kw in answer.lower())
    return round(hits / len(keywords), 3)


def response_stats(answer: str, latency_ms: int) -> dict:
    return {"word_count": len(answer.split()), "latency_ms": latency_ms}


def llm_relevance_score(query: str, answer: str) -> dict:
    prompt = f"""You are an AI evaluation assistant.
Rate the relevance and quality of this answer to the given question on a scale of 1 to 5.

Question: {query}
Answer: {answer}

Scoring guide:
1 = Completely irrelevant or refuses to answer
2 = Partially related but mostly unhelpful
3 = Somewhat helpful but missing key information
4 = Mostly helpful with minor gaps
5 = Fully relevant and complete answer

Respond with JSON only, no explanation outside the JSON:
{{"score": <int>, "reason": "<one sentence explanation>"}}"""

    try:
        response = llm.invoke(prompt)
        raw = response.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw.strip())
        return {
            "relevance_score": int(result["score"]),
            "relevance_reason": result["reason"],
        }
    except Exception as e:
        print(f"  [WARN] LLM scoring failed: {e}")
        return {"relevance_score": 0, "relevance_reason": "scoring error"}


def evaluate_results(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)
    results = []

    print(f"Evaluating {len(df)} results...\n")

    for _, row in df.iterrows():
        query_id = row["query_id"]
        query = row["query"]
        answer = row["answer"]
        expected_keywords = (
            row["expected_keywords"] if "expected_keywords" in row else ""
        )
        latency_ms = row["latency_ms"]

        # Keyword accuracy
        accuracy = (
            keyword_accuracy(answer, expected_keywords) if expected_keywords else 0.0
        )

        # Response stats
        stats = response_stats(answer, latency_ms)

        # LLM relevance score
        relevance = llm_relevance_score(query, answer)
        time.sleep(0.5)  # avoid rate limits

        result = {
            "query_id": query_id,
            "query": query,
            "category": row["category"],
            "answer": answer,
            "word_count": stats["word_count"],
            "latency_ms": stats["latency_ms"],
            "keyword_accuracy": accuracy,
            "relevance_score": relevance["relevance_score"],
            "relevance_reason": relevance["relevance_reason"],
            "model_version": row["model_version"],
        }

        results.append(result)
        print(
            f"[{query_id}] relevance={relevance['relevance_score']}/5 | accuracy={accuracy} | {row['category']}"
        )

    out_df = pd.DataFrame(results)
    out_df.to_csv(output_csv, index=False)
    print(f"\n[OK] Saved {output_csv} ({len(out_df)} rows)")
    return out_df
