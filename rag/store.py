import json
import numpy as np
from . import config
from .chunker import chunk_text
from .loader import load_directory
from .ollama_client import embed


class VectorStore:
    def __init__(self):
        self.vectors = np.zeros((0, 1), dtype=np.float32)
        self.meta: list[dict] = []

    def build(self, folder: str, batch_size: int = 32) -> int:
        meta = []
        for source, page, text in load_directory(folder):
            for chunk in chunk_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP):
                meta.append({"source": source, "page": page, "text": chunk})
        if not meta:
            raise ValueError(f"No supported documents found in '{folder}'")
        vecs = []
        for i in range(0, len(meta), batch_size):
            vecs.append(embed([m["text"] for m in meta[i:i + batch_size]]))
        mat = np.vstack(vecs)
        mat /= np.linalg.norm(mat, axis=1, keepdims=True) + 1e-10  # unit vectors
        self.vectors, self.meta = mat, meta
        return len(meta)

    def search(self, query: str, k: int = config.TOP_K) -> list[dict]:
        q = embed([query])[0]
        q /= np.linalg.norm(q) + 1e-10
        scores = self.vectors @ q  # cosine similarity
        top = np.argsort(scores)[::-1][:k]
        return [{**self.meta[i], "score": float(scores[i])} for i in top]

    def save(self, path: str = config.INDEX_PATH):
        np.savez_compressed(path, vectors=self.vectors, meta=json.dumps(self.meta))

    def load(self, path: str = config.INDEX_PATH) -> bool:
        try:
            data = np.load(path, allow_pickle=False)
        except FileNotFoundError:
            return False
        self.vectors = data["vectors"]
        self.meta = json.loads(str(data["meta"]))
        return True
