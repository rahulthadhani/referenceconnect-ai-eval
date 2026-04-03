from pathlib import Path

docs = list(Path("data/documents").glob("*.txt"))
total_words = sum(
    len(p.read_text(encoding="utf-8", errors="ignore").split()) for p in docs
)

print(f"Documents: {len(docs)}")
print(f"Total words: {total_words:,}")
print(f"Avg words/doc: {total_words // len(docs)}")
print()

for p in docs:
    wc = len(p.read_text(encoding="utf-8", errors="ignore").split())
    status = "[OK]" if wc >= 100 else "[SHORT]"
    print(f"  {status}  {p.name}: {wc} words")
