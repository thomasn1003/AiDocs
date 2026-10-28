# Local AI Document Assistant

Ask natural-language questions about your own documents (PDF, TXT, MD). Everything
runs locally: embeddings and answers come from a model served by [Ollama](https://ollama.com).

## How it works
1. **Load** documents from `docs/` (`rag/loader.py`)
2. **Chunk** text into ~800-char overlapping pieces (`rag/chunker.py`)
3. **Embed** each chunk with `nomic-embed-text` (`rag/ollama_client.py`)
4. **Search**: embed the question, rank chunks by cosine similarity (`rag/store.py`)
5. **Generate**: pass the top passages to a local LLM (`llama3.2`) with an instruction to
   answer only from context and cite `[1]`, `[2]`... (`rag/pipeline.py`)
6. **Show sources**: file, page, similarity score, and snippet for every passage used

## Setup
```bash
# 1. Install Ollama, then pull the models
ollama pull nomic-embed-text
ollama pull llama3.2

# 2. Python deps
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3a. Web UI
python app.py            # open http://localhost:5000, upload files, ask questions

# 3b. Or command line
python ingest.py docs
python cli.py
```

Models and chunk settings live in `rag/config.py`.

## Ideas to extend
- Swap the NumPy search for FAISS or ChromaDB
- Stream tokens to the UI
- Incremental indexing (skip unchanged files)
- Add .docx support and a conversation history
