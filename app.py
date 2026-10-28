from pathlib import Path
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from rag.store import VectorStore
from rag.pipeline import answer
from rag.loader import SUPPORTED

app = Flask(__name__)
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)
store = VectorStore()
store.load()


@app.get("/")
def index():
    return render_template("index.html", indexed=len(store.meta))


@app.post("/upload")
def upload():
    for f in request.files.getlist("files"):
        name = secure_filename(f.filename or "")
        if Path(name).suffix.lower() in SUPPORTED:
            f.save(DOCS / name)
    try:
        n = store.build(str(DOCS))
        store.save()
        return jsonify(chunks=n)
    except Exception as e:  # e.g. Ollama not running
        return jsonify(error=str(e)), 500


@app.post("/ask")
def ask():
    question = (request.json or {}).get("question", "").strip()
    if not question:
        return jsonify(error="Empty question"), 400
    if not store.meta:
        return jsonify(error="Upload and index documents first"), 400
    try:
        return jsonify(answer(store, question))
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
