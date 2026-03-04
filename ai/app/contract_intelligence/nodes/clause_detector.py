from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.prompts.clause_detector import (
    CLAUSE_DETECTOR_SYSTEM_PROMPT,
)
from app.contract_intelligence.state import ContractState


class ClauseDetectionOutput(BaseModel):
    clause_type: str
    extracted_text: str
    key_terms: List[str]
    defined_terms_used: List[str]
    cross_references: List[str]
    is_amendment: bool
    original_text_if_amended: str


async def _detect_for_chunk(
    llm: ChatOpenAI,
    chunk: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    content = chunk.get("content") or ""
    if not content.strip():
        return None

    chunk_payload = {
        "chunk_id": chunk.get("id"),
        "clause_number": chunk.get("clause_number"),
        "section_type": chunk.get("section_type"),
        "content": content,
    }

    sys_prompt = CLAUSE_DETECTOR_SYSTEM_PROMPT

    result: ClauseDetectionOutput = await llm.ainvoke(
        {
            "role": "user",
            "content": {
                "system": sys_prompt,
                "chunk": chunk_payload,
            },
        }
    )

    if result.clause_type == "non_substantive":
        return {
            "clause_type": "non_substantive",
            "extracted_text": "",
            "key_terms": [],
            "defined_terms_used": [],
            "cross_references": [],
            "is_amendment": False,
            "original_text_if_amended": "",
            "chunk_id": chunk.get("id"),
            "page_start": chunk.get("page_start"),
            "page_end": chunk.get("page_end"),
        }

    return {
        "clause_type": result.clause_type,
        "extracted_text": result.extracted_text or content,
        "key_terms": result.key_terms,
        "defined_terms_used": result.defined_terms_used,
        "cross_references": result.cross_references,
        "is_amendment": bool(result.is_amendment),
        "original_text_if_amended": result.original_text_if_amended,
        "chunk_id": chunk.get("id"),
        "page_start": chunk.get("page_start"),
        "page_end": chunk.get("page_end"),
        "section_type": chunk.get("section_type"),
    }


async def clause_detector_node(state: ContractState) -> ContractState:
    if state.get("fatal_error"):
        return state

    sections = state.get("sections") or state.get("normalized_chunks") or []
    errors = list(state.get("errors") or [])

    settings = get_settings()
    raw_llm = ChatOpenAI(
        model=settings.primary_llm,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    llm = raw_llm.with_structured_output(ClauseDetectionOutput)

    semaphore = asyncio.Semaphore(settings.max_concurrent_clause_tasks)

    async def wrapped(chunk: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        async with semaphore:
            try:
                return await _detect_for_chunk(llm, chunk)
            except Exception as exc:
                errors.append(
                    {
                        "node": "clause_detector",
                        "clause_id": chunk.get("id"),
                        "error_type": "clause_detection_failed",
                        "message": str(exc),
                    }
                )
                return None

    tasks = [wrapped(ch) for ch in sections]
    results = await asyncio.gather(*tasks)

    clauses: List[Dict[str, Any]] = [r for r in results if r is not None]

    new_state: ContractState = dict(state)
    new_state["clauses"] = clauses
    new_state["errors"] = errors
    return new_state

