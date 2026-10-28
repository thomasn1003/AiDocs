"""Terminal chat: python cli.py"""
from rag.store import VectorStore
from rag.pipeline import answer

store = VectorStore()
if not store.load():
    raise SystemExit("No index found. Run: python ingest.py docs")

while True:
    q = input("\nAsk> ").strip()
    if q.lower() in {"", "exit", "quit"}:
        break
    result = answer(store, q)
    print("\n" + result["answer"] + "\n\nSources:")
    for i, s in enumerate(result["sources"], 1):
        page = f", p.{s['page']}" if s["page"] else ""
        print(f"  [{i}] {s['source']}{page} (score {s['score']:.2f})")
