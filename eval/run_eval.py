import sys

sys.path.insert(0, ".")

import pandas as pd
from eval.metrics import evaluate_results
from pathlib import Path

Path("results").mkdir(exist_ok=True)

# Merge results with expected keywords from queries.csv
results = pd.read_csv("results/results_v1.csv")
queries = pd.read_csv("data/queries.csv")[["query_id", "expected_keywords"]]
merged = results.merge(queries, on="query_id")
merged.to_csv("results/results_v1_merged.csv", index=False)

# Run evaluation
evaluate_results(
    input_csv="results/results_v1_merged.csv", output_csv="results/eval_v1.csv"
)

results_v2 = pd.read_csv("results/results_v2.csv")
merged_v2 = results_v2.merge(queries, on="query_id")
merged_v2.to_csv("results/results_v2_merged.csv", index=False)

evaluate_results(
    input_csv="results/results_v2_merged.csv", output_csv="results/eval_v2.csv"
)
