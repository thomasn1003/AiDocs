import numpy as np
import requests
from . import config


def embed(texts: list[str]) -> np.ndarray:
    resp = requests.post(
        f"{config.OLLAMA_URL}/api/embed",
        json={"model": config.EMBED_MODEL, "input": texts},
        timeout=300,
    )
    resp.raise_for_status()
    return np.array(resp.json()["embeddings"], dtype=np.float32)


def generate(prompt: str) -> str:
    resp = requests.post(
        f"{config.OLLAMA_URL}/api/chat",
        json={
            "model": config.CHAT_MODEL,
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
            "options": {"temperature": 0.2},
        },
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]
