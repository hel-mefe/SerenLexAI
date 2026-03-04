from __future__ import annotations

from typing import Any, Dict, Tuple

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.ingestion.chunker import build_chunks_from_blocks
from app.contract_intelligence.ingestion.detector import (
    UnsupportedFormatError,
    detect_input_format,
)
from app.contract_intelligence.ingestion.docx_extractor import (
    extract_docx_layout_blocks,
)
from app.contract_intelligence.ingestion.pdf_extractor import (
    extract_pdf_layout_blocks,
)


def ingest_document(
    *,
    contract_id: str,
    raw_input: bytes | str,
    file_name: str | None,
    content_type: str | None,
) -> Tuple[str, Dict[str, Any]]:
    """
    High-level ingestion entrypoint.

    Returns (input_format, ingestion_result) where ingestion_result contains:
      - extracted_blocks: list[dict]
      - chunks: list[dict]
      - page_count: int
      - used_ocr: bool
      - ocr_error: Optional[str]
    Raises UnsupportedFormatError for unsupported formats.
    """
    settings = get_settings()

    if isinstance(raw_input, bytes) and len(raw_input) > settings.max_file_size_mb * 1024 * 1024:
        raise ValueError(
            f"File too large. Maximum supported size is {settings.max_file_size_mb} MB."
        )

    input_format, _ = detect_input_format(
        file_name=file_name,
        content_type=content_type,
        raw_input=raw_input,
    )

    if input_format == "text":
        if isinstance(raw_input, bytes):
            text = raw_input.decode("utf-8", errors="ignore")
        else:
            text = raw_input
        # Treat each non-empty line as a basic block; page number is 1.
        blocks = [
            {
                "text": line.strip(),
                "font_size": None,
                "is_bold": False,
                "page_number": 1,
                "block_type_hint": None,
            }
            for line in text.splitlines()
            if line.strip()
        ]
        page_count = 1
        used_ocr = False
        ocr_error = None
    elif input_format == "pdf":
        if not isinstance(raw_input, bytes):
            raise ValueError("PDF input must be bytes.")
        pdf_result = extract_pdf_layout_blocks(raw_input)
        blocks = pdf_result["blocks"]
        page_count = int(pdf_result["page_count"])
        used_ocr = bool(pdf_result["used_ocr"])
        ocr_error = pdf_result["ocr_error"]
    elif input_format == "docx":
        if not isinstance(raw_input, bytes):
            raise ValueError("DOCX input must be bytes.")
        docx_result = extract_docx_layout_blocks(raw_input)
        blocks = docx_result["blocks"]
        page_count = int(docx_result["page_count"])
        used_ocr = False
        ocr_error = None
    else:  # pragma: no cover - defensive
        raise UnsupportedFormatError(
            "Unsupported input format. Supported: pdf, docx, text."
        )

    chunks = build_chunks_from_blocks(contract_id=contract_id, extracted_blocks=blocks)

    ingestion_result: Dict[str, Any] = {
        "extracted_blocks": blocks,
        "chunks": chunks,
        "page_count": page_count,
        "used_ocr": used_ocr,
        "ocr_error": ocr_error,
    }
    return input_format, ingestion_result

