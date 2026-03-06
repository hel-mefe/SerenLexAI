from langgraph.types import Send


def map_clauses_node(state):
    """
    Fan-out node: emits one Send per clause so each clause is processed
    independently and in parallel by clause_classification.

    Each Send passes:
      - clause:  the clause dict (text, position_index, number, title)
      - context: neighbouring clauses for richer analysis
    """
    clauses = state["clauses_detected"]
    print(f"[DEBUG map_clauses] clauses_detected count: {len(clauses)}")
    print(f"[DEBUG map_clauses] first clause: {clauses[0] if clauses else 'EMPTY'}")

    sends = []
    for i, clause in enumerate(clauses):
        previous_clause = clauses[i - 1] if i > 0 else None
        next_clause = clauses[i + 1] if i < len(clauses) - 1 else None

        sends.append(
            Send(
                "clause_classification",
                {
                    # carry forward top-level ids so nodes can reference them
                    "analysis_id": state["analysis_id"],

                    "clause": clause,
                    "context": {
                        "previous": previous_clause,
                        "next": next_clause,
                    },
                },
            )
        )

    # Also store clause_tasks so collect_clause_results can use
    # len(clause_tasks) as the expected total for the fan-in barrier
    return {"clause_tasks": clauses}