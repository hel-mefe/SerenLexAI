from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from app.contract_intelligence.config import get_settings


HEADING_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^\d+\.\s"),  # 1. ...
    re.compile(r"^\d+\.\d+"),  # 1.1 ...
    re.compile(r"^[A-Z]\d+"),  # A1 etc.
    re.compile(r"^\([a-z]\)"),  # (a) ...
    re.compile(r"^Schedule\s+[A-Z]"),
    re.compile(r"^Annex\s+\d+"),
)

SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.;])\s+(?=[A-Z(])")


@dataclass
class Chunk:
    id: str
    contract_id: str
    clause_number: Optional[str]
    section_type_hint: Optional[str]
    content: str
    page_start: int
    page_end: int
    char_count: int
    token_count_estimate: int
    chunk_index: int
    is_schedule: bool = False
    has_annotation: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "clause_number": self.clause_number,
            "section_type_hint": self.section_type_hint,
            "content": self.content,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "char_count": self.char_count,
            "token_count_estimate": self.token_count_estimate,
            "chunk_index": self.chunk_index,
            "is_schedule": self.is_schedule,
            "has_annotation": self.has_annotation,
        }


def _is_heading(block: Dict[str, Any], body_font_size: float) -> bool:
    text = (block.get("text") or "").strip()
    if not text:
        return False

    font_size = float(block.get("font_size") or 0.0)
    is_bold = bool(block.get("is_bold"))
    block_type_hint = block.get("block_type_hint")

    if block_type_hint == "heading":
        return True

    if font_size > body_font_size * 1.05:
        return True

    if is_bold and font_size >= body_font_size:
        return True

    for pattern in HEADING_PATTERNS:
        if pattern.match(text):
            return True

    return False


def _estimate_body_font_size(blocks: Iterable[Dict[str, Any]]) -> float:
    sizes: list[float] = []
    for b in blocks:
        size = b.get("font_size")
        if size:
            try:
                sizes.append(float(size))
            except (TypeError, ValueError):
                continue
    if not sizes:
        return 10.0
    sizes.sort()
    mid = len(sizes) // 2
    if len(sizes) % 2 == 1:
        return sizes[mid]
    return (sizes[mid - 1] + sizes[mid]) / 2.0


def _group_blocks_by_heading(
    blocks: List[Dict[str, Any]],
) -> List[Tuple[Optional[str], List[Dict[str, Any]], bool]]:
    """
    Group blocks under the nearest preceding heading.

    Returns list of tuples: (clause_number, blocks, is_schedule)
    """
    body_font_size = _estimate_body_font_size(blocks)
    groups: list[tuple[Optional[str], list[Dict[str, Any]], bool]] = []
    current_heading: Optional[str] = None
    current_blocks: list[Dict[str, Any]] = []
    is_schedule = False

    for block in blocks:
        text = (block.get("text") or "").strip()
        if not text:
            # keep blank lines as part of current group
            current_blocks.append(block)
            continue

        if _is_heading(block, body_font_size):
            # Flush previous group.
            if current_blocks:
                groups.append((current_heading, current_blocks, is_schedule))
                current_blocks = []

            heading_text = text
            current_heading = heading_text
            is_schedule = heading_text.startswith("Schedule") or heading_text.startswith("Annex")
            continue

        current_blocks.append(block)

    if current_blocks:
        groups.append((current_heading, current_blocks, is_schedule))

    return groups


def _split_long_text_into_sentences(text: str, max_tokens: int) -> List[str]:
    """
    Split text into sentence-like segments without breaking mid-phrase.
    """
    approx_tokens = max(len(text) // 4, 1)
    if approx_tokens <= max_tokens:
        return [text]

    sentences = SENTENCE_SPLIT_REGEX.split(text)
    segments: list[str] = []
    current: list[str] = []
    current_chars = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        sent_tokens = max(len(sent) // 4, 1)
        if current and (current_chars // 4 + sent_tokens) > max_tokens:
            segments.append(" ".join(current).strip())
            current = [sent]
            current_chars = len(sent)
        else:
            current.append(sent)
            current_chars += len(sent) + 1

    if current:
        segments.append(" ".join(current).strip())

    return [s for s in segments if s]


def build_chunks_from_blocks(
    contract_id: str,
    extracted_blocks: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Main chunking entrypoint.

    Consumes layout-aware blocks and produces clause-bounded chunks suitable
    for downstream analysis. This function is intentionally conservative:
    it prefers slightly longer chunks over splitting clauses mid-sentence.
    """
    settings = get_settings()
    max_tokens = settings.chunk_max_tokens

    # Normalize page numbers and basic fields.
    normalized_blocks: list[Dict[str, Any]] = []
    for b in extracted_blocks:
        text = (b.get("text") or "").rstrip()
        if not text:
            continue
        page_number = int(b.get("page_number") or 1)
        normalized_blocks.append(
            {
                "text": text,
                "font_size": b.get("font_size"),
                "is_bold": bool(b.get("is_bold")),
                "page_number": page_number,
                "block_type_hint": b.get("block_type_hint"),
            }
        )

    groups = _group_blocks_by_heading(normalized_blocks)

    chunks: list[Chunk] = []
    chunk_index = 0

    for heading, group_blocks, is_schedule in groups:
        if not group_blocks:
            continue

        combined_text = "\n".join(b["text"] for b in group_blocks).strip()
        if not combined_text:
            continue

        # If the logical clause is too long, split on sentence boundaries.
        segments = _split_long_text_into_sentences(combined_text, max_tokens=max_tokens)

        page_numbers = [int(b.get("page_number") or 1) for b in group_blocks]
        page_start = min(page_numbers) if page_numbers else 1
        page_end = max(page_numbers) if page_numbers else 1

        # Build a namespaced clause number for schedules/annexes.
        base_clause = heading.strip() if heading else None
        clause_number: Optional[str] = base_clause
        if base_clause and is_schedule:
            safe = base_clause.replace(" ", "_")
            clause_number = safe

        for segment in segments:
            char_count = len(segment)
            token_est = max(char_count // 4, 1)
            c = Chunk(
                id=str(uuid.uuid4()),
                contract_id=contract_id,
                clause_number=clause_number,
                section_type_hint=None,
                content=segment,
                page_start=page_start,
                page_end=page_end,
                char_count=char_count,
                token_count_estimate=token_est,
                chunk_index=chunk_index,
                is_schedule=is_schedule,
                has_annotation=False,
            )
            chunks.append(c)
            chunk_index += 1

    return [c.to_dict() for c in chunks]

