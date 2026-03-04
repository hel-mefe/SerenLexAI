from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pdfplumber
from PIL import Image

from app.contract_intelligence.config import get_settings

try:
    import pytesseract
except Exception:  # pragma: no cover - optional dependency at runtime
    pytesseract = None  # type: ignore[assignment]


@dataclass
class LayoutBlock:
    text: str
    font_size: float | None
    is_bold: bool
    page_number: int
    block_type_hint: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "font_size": self.font_size,
            "is_bold": self.is_bold,
            "page_number": self.page_number,
            "block_type_hint": self.block_type_hint,
        }


class PdfExtractionError(Exception):
    pass


def _extract_with_pdfplumber(pdf_bytes: bytes) -> tuple[List[LayoutBlock], int]:
    blocks: List[LayoutBlock] = []
    total_chars = 0
    page_count = 0

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page_count = len(pdf.pages)
        for page_index, page in enumerate(pdf.pages, start=1):
            # Use extract_words to preserve layout and basic font information.
            words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
            if words:
                # Group words by y-position to approximate lines/blocks.
                lines: dict[int, list[dict[str, Any]]] = {}
                for w in words:
                    y0 = int(w["top"])
                    lines.setdefault(y0, []).append(w)

                for y, line_words in sorted(lines.items(), key=lambda kv: kv[0]):
                    text = " ".join(w["text"] for w in line_words).strip()
                    if not text:
                        continue

                    avg_font_size = sum(w.get("size", 0.0) or 0.0 for w in line_words) / max(
                        len(line_words), 1
                    )
                    is_bold = any(
                        isinstance(w.get("fontname"), str)
                        and "Bold" in w.get("fontname", "")
                        for w in line_words
                    )

                    blocks.append(
                        LayoutBlock(
                            text=text,
                            font_size=avg_font_size or None,
                            is_bold=is_bold,
                            page_number=page_index,
                            block_type_hint=None,
                        )
                    )
                    total_chars += len(text)

    return blocks, total_chars if page_count > 0 else 0


def _extract_with_ocr(pdf_bytes: bytes) -> tuple[List[LayoutBlock], int, int]:
    if pytesseract is None:
        raise PdfExtractionError(
            "OCR fallback requested but pytesseract is not installed or not importable."
        )

    blocks: List[LayoutBlock] = []
    total_chars = 0
    page_count = 0

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page_count = len(pdf.pages)
        for page_index, page in enumerate(pdf.pages, start=1):
            # Render page to image (uses pdfplumber's Pillow integration)
            pil_image: Optional[Image.Image]
            try:
                pil_image = page.to_image(resolution=300).original
            except Exception as exc:  # pragma: no cover - defensive
                raise PdfExtractionError(f"OCR rendering failed for page {page_index}: {exc}")

            ocr_text = pytesseract.image_to_string(pil_image)
            for line in ocr_text.splitlines():
                text = line.strip()
                if not text:
                    continue
                blocks.append(
                    LayoutBlock(
                        text=text,
                        font_size=None,
                        is_bold=False,
                        page_number=page_index,
                        block_type_hint=None,
                    )
                )
                total_chars += len(text)

    return blocks, total_chars, page_count


def extract_pdf_layout_blocks(pdf_bytes: bytes) -> dict[str, Any]:
    """
    Extract layout-aware text blocks from a PDF, with OCR fallback.

    Returns a dict with keys:
      - blocks: list[dict]
      - page_count: int
      - used_ocr: bool
      - ocr_error: Optional[str]
    """
    settings = get_settings()

    # First attempt: pdfplumber text extraction.
    blocks, total_chars = _extract_with_pdfplumber(pdf_bytes)
    used_ocr = False
    ocr_error: str | None = None

    # OCR fallback if extraction is suspiciously low relative to pages.
    if (
        settings.ocr_fallback_enabled
        and total_chars < settings.min_extractable_chars
    ):
        try:
            blocks, total_chars, page_count = _extract_with_ocr(pdf_bytes)
            used_ocr = True
        except Exception as exc:
            ocr_error = str(exc)
            # We still return whatever pdfplumber found, even if very little.
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                page_count = len(pdf.pages)
    else:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            page_count = len(pdf.pages)

    return {
        "blocks": [b.to_dict() for b in blocks],
        "page_count": page_count,
        "used_ocr": used_ocr,
        "ocr_error": ocr_error,
        "total_chars": total_chars,
    }

