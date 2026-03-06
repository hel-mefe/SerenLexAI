from contract_ai.infrastructure.vision.clause_cleaner import ClauseCleaner

cleaner = ClauseCleaner()


def clean_clauses_node(state):

    clauses = state["clauses_detected"]
    print(f"[DEBUG clean_clauses] input count: {len(clauses)}")

    cleaned = cleaner.clean(clauses)
    print(f"[DEBUG clean_clauses] output count: {len(cleaned)}")

    return {"clauses_detected": cleaned}