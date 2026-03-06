from pydantic import BaseModel


class ClauseAnalysisOutput(BaseModel):
    """
    What the LLM is asked to return for each clause.
    """
    severity: str
    risk_explanation: str
    recommended_action: str
    # Optional numeric score in range 0–100 (0 = no risk, 100 = extreme risk)
    risk_score: int | None = None


class ClauseResult(BaseModel):
    """
    Full clause result stored in state and persisted to the database.
    Populated by combining LLM output + pipeline-provided fields.
    """
    title: str
    severity: str
    original_text: str
    risk_explanation: str
    recommended_action: str
    clause_type: str | None = None
    position_index: int | None = None
    page_number: int | None = None
    # Original document numbering, e.g. "12", "5.2", "(a)"
    number: str | None = None
    # Optional numeric risk score carried through from the LLM
    risk_score: int | None = None
    # Indices of other clauses this clause explicitly refers to
    references: list[int] | None = None
    # Raw clause/section numbers mentioned in this clause text
    reference_numbers: list[str] | None = None