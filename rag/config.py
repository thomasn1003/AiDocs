OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"   # ollama pull nomic-embed-text
CHAT_MODEL = "llama3.2"            # ollama pull llama3.2
CHUNK_SIZE = 800                   # characters per chunk
CHUNK_OVERLAP = 150                # characters shared between neighbors
TOP_K = 4                          # passages retrieved per question
INDEX_PATH = "index.npz"
