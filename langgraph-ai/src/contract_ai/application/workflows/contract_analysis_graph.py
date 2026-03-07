from langgraph.graph import StateGraph, END

from contract_ai.application.state.contract_state import ContractState
from contract_ai.nodes.classification.document_classifier_node import document_classifier_node
from contract_ai.nodes.document.extract_pages_node import extract_pages_node
from contract_ai.nodes.document.validate_document_node import validate_document_node
from contract_ai.nodes.document.reconstruct_clauses_node import reconstruct_clauses_node
from contract_ai.nodes.document.clean_clauses_node import clean_clauses_node
from contract_ai.nodes.agents.analyse_clauses_node import analyse_clauses_node
from contract_ai.nodes.agents.anomaly_detection_node import anomaly_detection_node
from contract_ai.nodes.aggregation.aggregate_results_node import aggregate_results_node
from contract_ai.nodes.persistence.debug_print_results_node import debug_print_results_node
from contract_ai.nodes.persistence.persist_results_node import persist_results_node
from contract_ai.nodes.report.generate_report_node import generate_report_pdf_node


def route_document(state):
    is_contract = state.get("is_contract")
    print(f"[DEBUG route_document] is_contract={is_contract}")
    if not is_contract:
        return "persist_results"
    return "validate_document"


def build_graph():
    builder = StateGraph(ContractState)

    builder.add_node("extract_pages",       extract_pages_node)
    builder.add_node("reconstruct_clauses", reconstruct_clauses_node)
    builder.add_node("clean_clauses",       clean_clauses_node)
    builder.add_node("document_classifier", document_classifier_node)
    builder.add_node("validate_document",   validate_document_node)
    builder.add_node("analyse_clauses",     analyse_clauses_node)
    builder.add_node("anomaly_detection",   anomaly_detection_node)
    builder.add_node("aggregate_results",   aggregate_results_node)
    builder.add_node("generate_pdf_report", generate_report_pdf_node)
    # Persist to Postgres, then optionally print a debug report.
    builder.add_node("persist_results",     persist_results_node)
    builder.add_node("debug_print_results", debug_print_results_node)

    builder.set_entry_point("extract_pages")

    builder.add_edge("extract_pages",       "reconstruct_clauses")
    builder.add_edge("reconstruct_clauses", "clean_clauses")
    builder.add_edge("clean_clauses",       "document_classifier")

    builder.add_conditional_edges(
        "document_classifier",
        route_document,
        {
            "validate_document": "validate_document",
            "persist_results":   "persist_results",
        },
    )

    builder.add_edge("validate_document",   "analyse_clauses")
    builder.add_edge("analyse_clauses",     "anomaly_detection")
    builder.add_edge("anomaly_detection",   "aggregate_results")
    builder.add_edge("aggregate_results",   "generate_pdf_report")
    builder.add_edge("generate_pdf_report", "persist_results")
    builder.add_edge("persist_results",     "debug_print_results")
    builder.add_edge("debug_print_results", END)

    return builder.compile()