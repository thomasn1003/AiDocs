"""Index every .txt/.md/.pdf in a folder: python ingest.py docs"""
import sys
from rag.store import VectorStore

folder = sys.argv[1] if len(sys.argv) > 1 else "docs"
store = VectorStore()
n = store.build(folder)
store.save()
print(f"Indexed {n} chunks from '{folder}' -> index.npz")
