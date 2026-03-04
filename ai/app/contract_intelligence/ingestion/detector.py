from __future__ import annotations

from mimetypes import guess_type
from typing import Literal, Tuple


InputFormat = Literal["pdf", "docx", "text"]


class UnsupportedFormatError(ValueError):
    pass


def detect_input_format(
    file_name: str | None,
    content_type: str | None,
    raw_input: bytes | str,
) -> Tuple[InputFormat, str]:
    """
    Detect the logical input format for the ingestion layer.

    Returns a tuple of (input_format, reason).
    Raises UnsupportedFormatError if the format is not supported.
    """
    # Text inputs passed as plain strings are always treated as text.
    if isinstance(raw_input, str):
        return "text", "input_is_plain_text"

    # Prefer explicit content_type when available.
    if content_type:
        if content_type in {"application/pdf"}:
            return "pdf", "content_type_pdf"
        if content_type in {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }:
            return "docx", "content_type_docx"
        if content_type.startswith("text/"):
            return "text", "content_type_text"

    # Fallback to file_name extension if present.
    if file_name:
        lower = file_name.lower()
        if lower.endswith(".pdf"):
            return "pdf", "extension_pdf"
        if lower.endswith(".docx"):
            return "docx", "extension_docx"
        if lower.endswith(".txt"):
            return "text", "extension_txt"

    # As a last resort, use mimetypes.
    if file_name:
        guessed, _ = guess_type(file_name)
        if guessed:
            if guessed == "application/pdf":
                return "pdf", "mimetypes_pdf"
            if guessed.startswith("text/"):
                return "text", "mimetypes_text"

    raise UnsupportedFormatError(
        "Unsupported file format. Supported formats: PDF, DOCX, plain text."
    )

