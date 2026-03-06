from langgraph.types import Send


def map_clauses_node(state):
    """
    Fan-out node: stores clause_tasks for the barrier count, then the
    graph's fan_out_clauses routing function emits the actual Sends.

    clause_tasks must be set HERE in the node return so it's in state
    before collect_clause_results_node checks len(clause_tasks).
    """
    clauses = state["clauses_detected"]
    print(f"[DEBUG map_clauses] clauses_detected count: {len(clauses)}")

    # Store clause_tasks so collect_clause_results_node knows the expected count
    return {"clause_tasks": clauses}