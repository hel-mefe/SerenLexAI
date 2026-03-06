def debug_print_results_node(state):

    print("\n")
    print("=" * 60)
    print("CONTRACT ANALYSIS REPORT")
    print("=" * 60)

    overall_risk = state.get("overall_risk")
    risk_score = state.get("risk_score")

    print(f"\nOverall Risk: {overall_risk}")
    print(f"Risk Score: {risk_score}")

    print("\nClauses Summary")
    print("-" * 20)

    print(f"HIGH: {state.get('high_count', 0)}")
    print(f"MEDIUM: {state.get('medium_count', 0)}")
    print(f"LOW: {state.get('low_count', 0)}")

    print("\n" + "=" * 60)
    print("CLAUSES")
    print("=" * 60)

    clause_results = state.get("clause_results", [])

    for clause in clause_results:

        print("\n")

        print(f"[Clause {clause.position_index}] {clause.title}")
        print(f"Type: {clause.clause_type}")
        print(f"Severity: {clause.severity}")

        print("\nText:")
        print(clause.original_text)

        print("\nExplanation:")
        print(clause.risk_explanation)

        print("\nRecommended Action:")
        print(clause.recommended_action)

        print("\n" + "-" * 60)

    anomalies = state.get("contract_anomalies", [])

    if anomalies:

        print("\n" + "=" * 60)
        print("CONTRACT ANOMALIES")
        print("=" * 60)

        for i, anomaly in enumerate(anomalies):

            print(f"\n{i + 1}. {anomaly['title']}")
            print(f"Severity: {anomaly['severity']}")

            print("\nExplanation:")
            print(anomaly["description"])

            print("\nAffected clauses:")
            print(anomaly["affected_clauses"])

            print("\n" + "-" * 60)

    print("\n")
    print("=" * 60)
    print("END OF REPORT")
    print("=" * 60)
    print("\n")

    return state