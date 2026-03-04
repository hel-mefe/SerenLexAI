from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.config import get_settings


settings = get_settings()


async def retrieve_similar_clauses(
    session: AsyncSession,
    embedding: list[float],
    k: int | None = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve semantically similar clauses from prior analyses using pgvector.

    Returns a list of dicts containing:
      - id
      - clause_type
      - section_type
      - extracted_text
      - risk_level
      - risk_score
      - similarity
    """
    limit = k or settings.rag_similar_clauses_k

    # Raw SQL for pgvector cosine similarity using the <=> operator.
    query = text(
        """
        SELECT
            cs.id,
            cs.section_type,
            cs.clause_type,
            cs.content AS extracted_text,
            cr.risk_level,
            cr.risk_score,
            1 - (cs.embedding <=> :embedding::vector) AS similarity
        FROM contract_sections cs
        LEFT JOIN clause_results cr ON cr.section_id = cs.id
        WHERE cs.embedding IS NOT NULL
        ORDER BY cs.embedding <=> :embedding::vector
        LIMIT :limit
        """
    )

    rows = (
        await session.execute(
            query,
            {"embedding": embedding, "limit": limit},
        )
    ).mappings()

    results: List[Dict[str, Any]] = []
    for row in rows:
        results.append(
            {
                "id": str(row["id"]),
                "clause_type": row["clause_type"],
                "section_type": row["section_type"],
                "extracted_text": row["extracted_text"],
                "risk_level": row["risk_level"],
                "risk_score": float(row["risk_score"]) if row["risk_score"] is not None else None,
                "similarity": float(row["similarity"]) if row["similarity"] is not None else None,
            }
        )

    return results

