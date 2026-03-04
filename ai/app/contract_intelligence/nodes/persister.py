"""
Persister node: writes workflow result to UI entities (analyses, clauses, actions).
"""

from __future__ import annotations

from typing import Any, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.models.domain import NodeErrorModel
from app.contract_intelligence.services.ui_sync import sync_workflow_result_to_ui
from app.contract_intelligence.state import ContractState


def _missing_id_error() -> NodeErrorModel:
    return NodeErrorModel(
        node="persister",
        error_type="missing_ids",
        message="analysis_id missing from state",
    )


def _db_error(exc: Exception) -> NodeErrorModel:
    return NodeErrorModel(
        node="persister",
        error_type="db_failure",
        message=str(exc),
    )


def _as_contract_state(state: Union[ContractState, dict[str, Any]]) -> ContractState:
    if isinstance(state, ContractState):
        return state
    return ContractState(**state)


def _get_analysis_id(state: Union[ContractState, dict[str, Any]]) -> str | None:
    if isinstance(state, dict):
        return state.get("analysis_id")
    return getattr(state, "analysis_id", None)


async def persister_node_factory(session: AsyncSession):
    async def node(state: Union[ContractState, dict[str, Any]]) -> dict[str, Any]:
        analysis_id = _get_analysis_id(state)
        if not analysis_id:
            err = _missing_id_error()
            if isinstance(state, ContractState):
                return state.model_copy(update={"errors": [*state.errors, err]}).model_dump()
            errors = list(state.get("errors") or []) + [err.model_dump()]
            return {**state, "errors": errors}
        state_obj = _as_contract_state(state)
        try:
            await sync_workflow_result_to_ui(
                session,
                state_obj,
                analysis_id,
                state_obj.user_id,
            )
            await session.commit()
        except Exception as exc:
            await session.rollback()
            err = _db_error(exc)
            if isinstance(state, ContractState):
                return state.model_copy(update={"errors": [*state.errors, err]}).model_dump()
            errors = list(state.get("errors") or []) + [err.model_dump()]
            return {**state, "errors": errors}
        return state_obj.model_dump() if isinstance(state, ContractState) else state

    return node
