from pathlib import Path
from typing import List
import PyPDF2


def load_text_from_txt(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_text_from_pdf(path: Path) -> str:
    text_parts: List[str] = []
    with path.open("rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""
            text_parts.append(page_text)
    return "\n".join(text_parts)
