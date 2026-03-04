from __future__ import annotations

from time import perf_counter
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.graph.builder import build_contract_graph
from app.contract_intelligence.state import ContractState


async def run_contract_analysis(
    initial_state: ContractState,
    session: AsyncSession,
) -> ContractState:
    """
    Orchestrate a single contract analysis run using the LangGraph workflow.

    This function measures total latency and attaches it to the final state.
    It assumes that contract_id and analysis_run_id are already present in
    the initial_state and that ingestion has populated chunks/extracted_blocks.
    """
    app = build_contract_graph(session)
    start = perf_counter()
    final_state: ContractState = await app.ainvoke(initial_state)
    elapsed_ms = int((perf_counter() - start) * 1000)
    return final_state.model_copy(
        update={"total_latency_ms": elapsed_ms, "total_tokens_used": final_state.total_tokens_used or 0}
    )

