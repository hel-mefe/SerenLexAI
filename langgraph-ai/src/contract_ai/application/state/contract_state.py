from typing import Any, TypedDict


class ContractState(TypedDict):
    # --- Input ---
    analysis_id: str
    pdf_path: str
    page_images: list[str]

    # --- Document classification ---
    raw_text: str
    is_contract: bool
    document_type: str | None

    # --- Clause extraction ---
    clauses_detected: list

    # --- Clause analysis results (written once by analyse_clauses_node) ---
    clause_results: list

    # --- Aggregation ---
    anomalies: list
    risk_score: int
    overall_risk: str
    flagged_count: int
    high_count: int
    medium_count: int
    low_count: int

    # --- PDF report ---
    report_pdf_path: str

    # --- Final output ---
    final_report: dict[str, Any]