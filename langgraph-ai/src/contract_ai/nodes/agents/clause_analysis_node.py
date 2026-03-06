from contract_ai.agents.risk.clause_analysis_agent import ClauseAnalysisAgent
from contract_ai.domain.models.clause import ClauseResult

agent = ClauseAnalysisAgent()


def clause_analysis_node(state):
    clause  = state["clause"]
    context = state.get("context", {})

    clause_text     = clause.get("text", "")
    previous_clause = context.get("previous")
    next_clause     = context.get("next")

    try:
        # LLM returns only: severity, risk_explanation, recommended_action
        output = agent.analyze(
            clause_text=clause_text,
            clause_type=clause.get("clause_type"),
            previous_clause=previous_clause,
            next_clause=next_clause,
        )

        # Assemble full ClauseResult by combining LLM output + pipeline fields
        result = ClauseResult(
            title             = clause.get("title") or clause.get("clause_type") or "Unnamed Clause",
            severity          = output.severity,
            original_text     = clause_text,
            risk_explanation  = output.risk_explanation,
            recommended_action= output.recommended_action,
            clause_type       = str(clause.get("clause_type") or ""),
            position_index    = clause.get("position_index"),
            page_number       = clause.get("page_number"),
            risk_score        = output.risk_score,
        )

        print(f"[DEBUG clause_analysis] SUCCESS: {result.title} | severity: {result.severity}")

    except Exception as e:
        import traceback
        # Write to file — LangGraph suppresses stdout in parallel branches
        with open("/tmp/clause_analysis_errors.txt", "a") as f:
            f.write(f"\n--- CRASHED on: {clause_text[:80]} ---\n")
            f.write(f"ERROR: {type(e).__name__}: {e}\n")
            traceback.print_exc(file=f)
        return {"clause_results": []}
    
    return {"clause_results": [result]}
