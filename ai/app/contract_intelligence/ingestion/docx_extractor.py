from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import docx


@dataclass
class DocxLayoutBlock:
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


def extract_docx_layout_blocks(docx_bytes: bytes) -> dict[str, Any]:
    """
    Extract layout-aware blocks from a DOCX document.

    DOCX does not expose page numbers directly; we treat the whole document
    as page 1 for ingestion purposes. Downstream chunking tracks logical
    positions and we can approximate pages once rendered to PDF, if needed.
    """
    document = docx.Document(docx_bytes)
    blocks: List[DocxLayoutBlock] = []

    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Derive basic styling information from runs and paragraph style.
        font_sizes: list[float] = []
        is_bold = False

        for run in para.runs:
            if run.font.size:
                font_sizes.append(float(run.font.size.pt))
            if run.bold:
                is_bold = True

        avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else None

        style_name = para.style.name if para.style is not None else ""
        block_type_hint = None
        if style_name and "Heading" in style_name:
            block_type_hint = "heading"

        blocks.append(
            DocxLayoutBlock(
                text=text,
                font_size=avg_font_size,
                is_bold=is_bold,
                page_number=1,
                block_type_hint=block_type_hint,
            )
        )

    return {
        "blocks": [b.to_dict() for b in blocks],
        "page_count": 1,
    }

