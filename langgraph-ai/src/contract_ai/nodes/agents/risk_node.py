from contract_ai.agents.risk.clause_analysis_agent import ClauseAnalysisAgent

agent = ClauseAnalysisAgent()


def risk_node(state):

    clauses = state["clauses_detected"]

    results = []

    for clause in clauses:

        clause_text = clause.get("text")

        if not clause_text:
            continue

        result = agent.analyze(clause_text)

        result.original_text = clause_text
        result.position_index = clause.get("position_index")
        # Optional page information if available from upstream pipeline
        if hasattr(result, "page_number"):
            result.page_number = clause.get("page_number")

        results.append(result)

    return {"clause_results": results}