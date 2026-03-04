from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.models.domain import NodeErrorModel
from app.contract_intelligence.prompts.explainer import EXPLAINER_SYSTEM_PROMPT
from app.contract_intelligence.state import ContractState


async def explainer_node(state: ContractState) -> ContractState:
    if state.fatal_error:
        return state

    errors: list[NodeErrorModel] = list(state.errors or [])

    summary_payload: Dict[str, Any] = {
        "overall_risk_score": state.risk_score,
        "overall_risk_level": state.risk_level,
        "score_breakdown": state.score_breakdown,
        "classified_clauses": [c.model_dump() for c in (state.classified_clauses or [])],
        "recommendations": [r.model_dump() for r in (state.recommendations or [])],
    }

    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.primary_llm,
        temperature=0,
        api_key=settings.openai_api_key,
    )

    try:
        completion = await llm.ainvoke(
            [
                ("system", EXPLAINER_SYSTEM_PROMPT),
                (
                    "user",
                    f"Here is the structured analysis data:\n\n{summary_payload}\n\n"
                    "Write the 3–5 paragraph explanation as instructed.",
                ),
            ]
        )
        explanation_text = completion.content if isinstance(completion.content, str) else str(
            completion.content
        )
    except Exception as exc:
        errors.append(
            NodeErrorModel(
                node="explainer",
                clause_id=None,
                error_type="explainer_failed",
                message=str(exc),
            )
        )
        explanation_text = ""

    return state.model_copy(update={"explanation": explanation_text, "errors": errors})

