import uuid

from contract_ai.application.workflows.contract_analysis_graph import build_graph


def main():
    graph = build_graph()

    state = {
        "analysis_id": str(uuid.uuid4()),
        "pdf_path":    "thorngate.pdf",
    }

    print(f"[DEBUG run] invoking graph with state: {state}")
    result = graph.invoke(state)
    print(f"[DEBUG run] is_contract: {result.get('is_contract')}")
    print(f"[DEBUG run] clause_results count: {len(result.get('clause_results', []))}")
    print(f"[DEBUG run] overall_risk: {result.get('overall_risk')}")
    print(f"[DEBUG run] report_pdf_path: {result.get('report_pdf_path')}")


if __name__ == "__main__":
    main()