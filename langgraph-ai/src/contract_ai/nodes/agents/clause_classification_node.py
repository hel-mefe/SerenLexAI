from contract_ai.agents.classification.clause_classifier_agent import ClauseClassifierAgent

agent = ClauseClassifierAgent()


def clause_classification_node(state):
    """
    Classifies clause type and stores the enriched clause back into
    branch-local state key 'clause' for clause_analysis_node to read.

    Since this node runs in an isolated Send branch, 'clause' here
    is the branch-local input — not shared ContractState.
    clause_analysis_node reads it from the same branch-local state.
    """
    clause = state["clause"]
    clause_text = clause.get("text", "")

    try:
        classification = agent.classify(clause_text)
        print(f"[DEBUG clause_classification] SUCCESS: {classification}")
        clause_type = classification.clause_type
    except Exception as e:
        import traceback
        print(f"[DEBUG clause_classification] CRASHED:")
        traceback.print_exc()
        clause_type = "other"

    # Return enriched clause — stays in branch-local state only
    # clause_analysis_node reads this via the regular edge within the branch
    return {
        "clause":  {**clause, "clause_type": clause_type},
        "context": state.get("context", {}),
    }