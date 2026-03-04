from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.contract_intelligence.nodes.clause_detector import clause_detector_node
from app.contract_intelligence.nodes.document_classifier import document_classifier_node
from app.contract_intelligence.nodes.explainer import explainer_node
from app.contract_intelligence.nodes.normalize import normalize_node
from app.contract_intelligence.nodes.parser import section_parser_node
from app.contract_intelligence.nodes.persister import persister_node_factory
from app.contract_intelligence.nodes.risk_classifier import risk_classifier_node_factory
from app.contract_intelligence.nodes.score_calculator import score_calculator_node
from app.contract_intelligence.nodes.recommender import recommender_node
from app.contract_intelligence.state import ContractState


def _route_after_classifier(state: ContractState) -> Literal["persister", "section_parser"]:
    """If document is not a contract, skip to persister; otherwise run full pipeline."""
    if state.document_type == "not_contract":
        return "persister"
    return "section_parser"


def build_contract_graph(session: AsyncSession):
    """
    Build and compile the LangGraph workflow for contract analysis.

    The graph is re-built per-run so that nodes which depend on the DB session
    (risk_classifier, persister) can close over that session safely.
    After normalization, a document_classifier node decides contract vs not_contract;
    non-contracts skip clause analysis and go straight to persister.
    """
    workflow = StateGraph(ContractState)

    # Nodes that do not require DB session
    workflow.add_node("normalize", normalize_node)
    workflow.add_node("document_classifier", document_classifier_node)
    workflow.add_node("section_parser", section_parser_node)
    workflow.add_node("clause_detector", clause_detector_node)
    workflow.add_node("score_calculator", score_calculator_node)
    workflow.add_node("recommender", recommender_node)
    workflow.add_node("explainer", explainer_node)

    # Nodes that require DB session
    risk_classifier_node = risk_classifier_node_factory(session)
    persister_node = persister_node_factory(session)

    # These are async factory functions; resolve them synchronously here.
    # LangGraph expects callables, not awaitables.
    async def risk_node(state: ContractState) -> ContractState:  # type: ignore[override]
        node_callable = await risk_classifier_node
        return await node_callable(state)

    async def persist_node(state: ContractState) -> ContractState:  # type: ignore[override]
        node_callable = await persister_node
        return await node_callable(state)

    workflow.add_node("risk_classifier", risk_node)
    workflow.add_node("persister", persist_node)

    # Edges
    workflow.add_edge(START, "normalize")
    workflow.add_edge("normalize", "document_classifier")
    workflow.add_conditional_edges("document_classifier", _route_after_classifier, {"persister": "persister", "section_parser": "section_parser"})
    workflow.add_edge("section_parser", "clause_detector")
    workflow.add_edge("clause_detector", "risk_classifier")
    workflow.add_edge("risk_classifier", "score_calculator")
    workflow.add_edge("score_calculator", "recommender")
    workflow.add_edge("recommender", "explainer")
    workflow.add_edge("explainer", "persister")
    workflow.add_edge("persister", END)

    app = workflow.compile()
    return app

