from __future__ import annotations

import fitz


class PDFParserError(ValueError):
    pass


def parse_pdf_text(file_bytes: bytes) -> str:
    if not file_bytes:
        raise PDFParserError("Uploaded file is empty")

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            pages = []
            for page in doc:
                extracted = page.get_text("text") or ""
                if extracted.strip():
                    pages.append(extracted.strip())
    except Exception as exc:  # pragma: no cover - defensive branch
        raise PDFParserError("Unable to parse PDF") from exc

    text = "\n\n".join(pages).strip()
    if not text:
        raise PDFParserError("No textual content found in PDF")
    return text
