"""
Worker service: creates UI Analysis + Action, runs pipeline, syncs result to UI.
"""

from __future__ import annotations

import base64
import uuid
from typing import Any, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.db.session import AsyncSessionMaker
from app.contract_intelligence.graph.runner import run_contract_analysis
from app.contract_intelligence.ingestion import ingest_document
from app.contract_intelligence.models.domain import BlockModel, ChunkModel
from app.contract_intelligence.models.tasks import AnalysisTaskPayload
from app.contract_intelligence.models.ui_entities import Action, Analysis
from app.contract_intelligence.services.ui_sync import emit_action
from app.contract_intelligence.state import ContractState


def _blocks_from_ingestion(blocks: list[dict[str, Any]]) -> list[BlockModel]:
    return [BlockModel(**b) for b in blocks]


def _chunks_from_ingestion(chunks: list[dict[str, Any]]) -> list[ChunkModel]:
    return [ChunkModel(**c) for c in chunks]


def _guess_source_type(
    file_name: str | None,
    content_type: str | None,
) -> str:
    if content_type and "pdf" in content_type:
        return "pdf"
    if content_type and "word" in content_type:
        return "docx"
    if file_name:
        lower = file_name.lower()
        if lower.endswith(".pdf"):
            return "pdf"
        if lower.endswith(".docx"):
            return "docx"
    return "text"


class AnalysisWorker:
    def __init__(self) -> None:
        self._settings = get_settings()

    def _decode_input(self, payload: AnalysisTaskPayload) -> bytes | str:
        if not payload.is_base64:
            return payload.raw_input
        return base64.b64decode(payload.raw_input)

    async def _create_analysis_and_emit_start(
        self,
        session: AsyncSession,
        payload: AnalysisTaskPayload,
        source_type: str,
    ) -> Tuple[str, str]:
        title = payload.file_name or "Contract"
        user_id = uuid.UUID(payload.user_id) if payload.user_id else None

        analysis: Analysis | None = None

        # If a contract_id is provided, reuse the existing analysis row
        if payload.contract_id:
            analysis_id = uuid.UUID(payload.contract_id)
            result = await session.get(Analysis, analysis_id)
            analysis = result  # type: ignore[assignment]

        if analysis is None:
            analysis = Analysis(
                title=title,
                original_filename=payload.file_name,
                source_type=source_type,
                status="running",
                user_id=user_id,
            )
            session.add(analysis)
        else:
            analysis.status = "running"
            analysis.source_type = source_type
            if payload.file_name:
                analysis.original_filename = payload.file_name

        await session.flush()
        await emit_action(
            session,
            analysis.id,
            user_id,
            "PROCESSING_STARTED",
            "Document uploaded",
            title,
            meta={"filename": payload.file_name},
        )
        await session.commit()
        return str(analysis.id), str(analysis.id)

    def _build_state(
        self,
        analysis_id: str,
        raw_input: bytes | str,
        input_format: str,
        ingestion_result: dict[str, Any],
        payload: AnalysisTaskPayload,
    ) -> ContractState:
        blocks = _blocks_from_ingestion(ingestion_result["extracted_blocks"])
        chunks = _chunks_from_ingestion(ingestion_result["chunks"])
        return ContractState(
            contract_id=analysis_id,
            analysis_run_id=analysis_id,
            raw_input=raw_input,
            input_format=input_format,
            extracted_blocks=blocks,
            chunks=chunks,
            page_count=ingestion_result["page_count"],
            metadata=payload.metadata,
            analysis_id=analysis_id,
            user_id=payload.user_id,
        )

    async def run(self, payload: AnalysisTaskPayload) -> None:
        raw_input = self._decode_input(payload)
        async with AsyncSessionMaker() as session:
            source_type = _guess_source_type(
                payload.file_name,
                payload.content_type,
            )
            analysis_id, _ = await self._create_analysis_and_emit_start(
                session, payload, source_type
            )
            input_format, ingestion = ingest_document(
                contract_id=analysis_id,
                raw_input=raw_input,
                file_name=payload.file_name,
                content_type=payload.content_type,
            )
            state = self._build_state(
                analysis_id,
                raw_input,
                input_format,
                ingestion,
                payload,
            )
            await run_contract_analysis(initial_state=state, session=session)
