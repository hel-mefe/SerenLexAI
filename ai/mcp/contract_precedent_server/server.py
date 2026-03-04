from __future__ import annotations

import asyncio
import sys
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.db.session import AsyncSessionMaker
from app.contract_intelligence.models.db import (
    AnalysisRun,
    ClauseResult,
    ContractSection,
    NodeExecution,
)
from app.contract_intelligence.tools.embedder import embed_text
from app.contract_intelligence.tools.retriever import retrieve_similar_clauses


mcp = FastMCP("contract-precedent-db")


async def _get_session() -> AsyncSession:
    return AsyncSessionMaker()


@mcp.tool()
async def search_similar_clauses(
    query_text: str,
    k: int = 5,
    section_type: Optional[str] = None,
    clause_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for clauses similar to the provided text using pgvector.

    Returns a list of clauses with risk metadata and similarity score.
    """
    embedding = await embed_text(query_text)

    async with AsyncSessionMaker() as session:
        base_results = await retrieve_similar_clauses(session=session, embedding=embedding, k=k)

        filtered: List[Dict[str, Any]] = []
        for row in base_results:
            if section_type and row.get("section_type") != section_type:
                continue
            if clause_type and row.get("clause_type") != clause_type:
                continue
            filtered.append(row)

        return filtered


@mcp.tool()
async def get_clause(clause_id: str) -> Dict[str, Any]:
    """
    Fetch a single clause/section by ID, including any linked clause_results.
    """
    async with AsyncSessionMaker() as session:
        section = await session.get(ContractSection, clause_id)
        if section is None:
            return {"error": f"Clause/section {clause_id} not found"}

        # Find any associated clause_results for this section.
        from sqlalchemy import select

        results = await session.scalars(
            select(ClauseResult).where(ClauseResult.section_id == section.id)
        )

        return {
            "id": str(section.id),
            "contract_id": str(section.contract_id),
            "section_type": section.section_type,
            "clause_type": section.clause_type,
            "title": section.title,
            "content": section.content,
            "page_start": section.page_start,
            "page_end": section.page_end,
            "position_index": section.position_index,
            "is_amendment": section.is_amendment,
            "results": [
                {
                    "id": str(r.id),
                    "analysis_run_id": str(r.analysis_run_id),
                    "clause_type": r.clause_type,
                    "section_type": r.section_type,
                    "extracted_text": r.extracted_text,
                    "risk_level": r.risk_level,
                    "risk_score": float(r.risk_score) if r.risk_score is not None else None,
                    "risk_rationale": r.risk_rationale,
                    "recommendation": r.recommendation,
                    "suggested_language": r.suggested_language,
                    "recommendation_priority": r.recommendation_priority,
                    "page_start": r.page_start,
                    "page_end": r.page_end,
                }
                for r in results
            ],
        }


@mcp.tool()
async def get_analysis_run(run_id: str) -> Dict[str, Any]:
    """
    Fetch a single analysis_run and some summary information.
    """
    async with AsyncSessionMaker() as session:
        analysis_run = await session.get(AnalysisRun, run_id)
        if analysis_run is None:
            return {"error": f"analysis_run {run_id} not found"}

        from sqlalchemy import select

        clauses = await session.scalars(
            select(ClauseResult).where(ClauseResult.analysis_run_id == analysis_run.id)
        )

        return {
            "id": str(analysis_run.id),
            "contract_id": str(analysis_run.contract_id),
            "status": analysis_run.status,
            "overall_risk_score": float(analysis_run.overall_risk_score)
            if analysis_run.overall_risk_score is not None
            else None,
            "overall_risk_level": analysis_run.overall_risk_level,
            "score_breakdown": analysis_run.score_breakdown,
            "clause_count": analysis_run.clause_count,
            "high_risk_count": analysis_run.high_risk_count,
            "critical_risk_count": analysis_run.critical_risk_count,
            "workflow_version": analysis_run.workflow_version,
            "total_tokens_used": analysis_run.total_tokens_used,
            "total_latency_ms": analysis_run.total_latency_ms,
            "started_at": analysis_run.started_at.isoformat(),
            "completed_at": analysis_run.completed_at.isoformat()
            if analysis_run.completed_at
            else None,
            "error_summary": analysis_run.error_summary,
            "clause_ids": [str(c.id) for c in clauses],
        }


@mcp.tool()
async def get_run_trace(run_id: str) -> List[Dict[str, Any]]:
    """
    Fetch the full node_executions trace for an analysis run.
    """
    async with AsyncSessionMaker() as session:
        from sqlalchemy import select

        execs = await session.scalars(
            select(NodeExecution)
            .where(NodeExecution.analysis_run_id == run_id)
            .order_by(NodeExecution.executed_at.asc())
        )

        return [
            {
                "id": str(e.id),
                "analysis_run_id": str(e.analysis_run_id),
                "node_name": e.node_name,
                "status": e.status,
                "input_snapshot": e.input_snapshot,
                "output_snapshot": e.output_snapshot,
                "tool_calls": e.tool_calls,
                "model_used": e.model_used,
                "prompt_tokens": e.prompt_tokens,
                "completion_tokens": e.completion_tokens,
                "latency_ms": e.latency_ms,
                "error": e.error,
                "executed_at": e.executed_at.isoformat(),
            }
            for e in execs
        ]


if __name__ == "__main__":
    # Run as an MCP server over stdio.
    # IMPORTANT: never print to stdout; use stderr for logging.
    mcp.run(transport="stdio")

