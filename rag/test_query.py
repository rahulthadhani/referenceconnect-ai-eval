import sys

sys.path.insert(0, ".")

from rag.pipeline import load_vectorstore, build_qa_chain

vectordb = load_vectorstore()
chain, retriever = build_qa_chain(vectordb)

test_queries = [
    "What is the return policy?",
    "How do I reset my password?",
    "How do I contact support?",
]

for query in test_queries:
    print(f"\nQ: {query}")
    answer = chain.invoke(query)
    sources = [doc.metadata["source"] for doc in retriever.invoke(query)]
    print(f"A: {answer}")
    print(f"Sources: {sources}")
    print("-" * 60)
