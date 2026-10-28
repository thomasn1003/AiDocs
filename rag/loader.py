from pathlib import Path
from pypdf import PdfReader

SUPPORTED = {".txt", ".md", ".pdf"}


def load_file(path: Path) -> list[tuple[str, int | None]]:
    """Return [(text, page_number_or_None), ...] for a file."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return [(p.extract_text() or "", i + 1) for i, p in enumerate(reader.pages)]
    if ext in {".txt", ".md"}:
        return [(path.read_text(encoding="utf-8", errors="ignore"), None)]
    return []


def load_directory(folder: str):
    for path in sorted(Path(folder).rglob("*")):
        if path.suffix.lower() in SUPPORTED:
            for text, page in load_file(path):
                if text.strip():
                    yield path.name, page, text
