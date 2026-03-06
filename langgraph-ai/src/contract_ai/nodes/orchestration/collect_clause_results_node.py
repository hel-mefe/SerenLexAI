def collect_clause_results_node(state):
    """
    Fan-in node called once per completed branch.
    Returns {} every time — downstream routing checks if all
    branches are done before proceeding to anomaly_detection.
    """
    results  = state.get("clause_results", [])
    expected = len(state.get("clause_tasks", []))
    print(f"[DEBUG collect] got {len(results)} of {expected} expected")
    return {}


def route_after_collect(state):
    """
    Only proceed to anomaly_detection when ALL clause branches
    have completed. Otherwise stay — LangGraph will call
    collect_clause_results again on the next branch completion.
    """
    results  = state.get("clause_results", [])
    expected = len(state.get("clause_tasks", []))

    if len(results) >= expected:
        print(f"[DEBUG collect] all {expected} results in — proceeding")
        return "anomaly_detection"

    # Not done yet — route back to self to wait
    return "collect_clause_results"