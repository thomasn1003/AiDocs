from .ollama_client import generate

PROMPT = """You are a document assistant. Answer the question using ONLY the numbered \
context passages below. Cite the passages you used like [1] or [2]. If the answer \
is not in the context, say you couldn't find it in the documents.

Context:
{context}

Question: {question}

Answer:"""


def answer(store, question: str) -> dict:
    hits = store.search(question)
    context = "\n\n".join(
        f"[{i}] ({h['source']}{', p.' + str(h['page']) if h['page'] else ''}) {h['text']}"
        for i, h in enumerate(hits, 1)
    )
    text = generate(PROMPT.format(context=context, question=question))
    return {"answer": text, "sources": hits}
