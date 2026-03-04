from __future__ import annotations

from typing import Any, Dict, List

from langchain_openai import ChatOpenAI

from app.contract_intelligence.config import get_settings
from app.contract_intelligence.prompts.explainer import EXPLAINER_SYSTEM_PROMPT
from app.contract_intelligence.state import ContractState


async def explainer_node(state: ContractState) -> ContractState:
    if state.get("fatal_error"):
        return state

    errors = list(state.get("errors") or [])

    summary_payload: Dict[str, Any] = {
        "overall_risk_score": state.get("risk_score"),
        "overall_risk_level": state.get("risk_level"),
        "score_breakdown": state.get("score_breakdown"),
        "classified_clauses": state.get("classified_clauses"),
        "recommendations": state.get("recommendations"),
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
            {
                "node": "explainer",
                "clause_id": None,
                "error_type": "explainer_failed",
                "message": str(exc),
            }
        )
        explanation_text = ""

    new_state: ContractState = dict(state)
    new_state["explanation"] = explanation_text
    new_state["errors"] = errors
    return new_state

