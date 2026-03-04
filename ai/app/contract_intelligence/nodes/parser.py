from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.models.domain import SectionModel, NodeErrorModel
from app.contract_intelligence.prompts.parser import (
    SECTION_PARSER_SYSTEM_PROMPT,
    SECTION_TYPES,
)
from app.contract_intelligence.state import ContractState


class SectionAssignment(BaseModel):
    chunk_id: str
    section_type: str


class SectionParserOutput(BaseModel):
    assignments: List[SectionAssignment]


class SectionParserService:
    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.primary_llm
        self._api_key = settings.openai_api_key

    def _build_llm(self) -> ChatOpenAI:
        llm = ChatOpenAI(
            model=self._model,
            temperature=0,
            api_key=self._api_key,
        )
        return llm.with_structured_output(SectionParserOutput)

    def _chunk_summaries(self, state: ContractState) -> List[Dict[str, Any]]:
        chunks = state.normalized_chunks or state.chunks
        return [
            {
                "chunk_id": chunk.id,
                "clause_number": chunk.clause_number,
                "content": chunk.content,
            }
            for chunk in chunks
        ]

    async def _invoke_llm(
        self, llm: ChatOpenAI, summaries: List[Dict[str, Any]]
    ) -> SectionParserOutput:
        system_prompt = SECTION_PARSER_SYSTEM_PROMPT.format(
            section_types=", ".join(SECTION_TYPES)
        )
        payload = {"system": system_prompt, "chunks": summaries}
        return await llm.ainvoke(payload)

    def _build_sections(
        self, state: ContractState, output: SectionParserOutput
    ) -> List[SectionModel]:
        chunks = state.normalized_chunks or state.chunks
        by_id = {a.chunk_id: a.section_type for a in output.assignments}
        sections: List[SectionModel] = []
        for chunk in chunks:
            section_type = by_id.get(chunk.id, "other")
            if section_type not in SECTION_TYPES:
                section_type = "other"
            data = chunk.model_dump()
            data["section_type"] = section_type
            sections.append(SectionModel(**data))
        return sections

    def _fallback_sections(self, state: ContractState) -> List[SectionModel]:
        chunks = state.normalized_chunks or state.chunks
        sections: List[SectionModel] = []
        for chunk in chunks:
            data = chunk.model_dump()
            data["section_type"] = "other"
            sections.append(SectionModel(**data))
        return sections

    def _append_error(self, state: ContractState, exc: Exception) -> ContractState:
        error = NodeErrorModel(
            node="section_parser",
            error_type="section_parser_failed",
            message=str(exc),
        )
        return state.model_copy(update={"errors": [*state.errors, error]})

    async def run(self, state: ContractState) -> ContractState:
        if state.fatal_error:
            return state
        llm = self._build_llm()
        summaries = self._chunk_summaries(state)
        try:
            output = await self._invoke_llm(llm, summaries)
            sections = self._build_sections(state, output)
            return state.model_copy(update={"sections": sections})
        except Exception as exc:
            fallback = self._fallback_sections(state)
            errored = self._append_error(state, exc)
            return errored.model_copy(update={"sections": fallback})


_service = SectionParserService()


async def section_parser_node(state: ContractState) -> ContractState:
    return await _service.run(state)

