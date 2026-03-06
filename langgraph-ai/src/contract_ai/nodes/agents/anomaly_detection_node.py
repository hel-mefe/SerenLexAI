from contract_ai.agents.anomaly.contract_anomaly_agent import ContractAnomalyAgent

agent = ContractAnomalyAgent()


def anomaly_detection_node(state):

    clauses = state.get("clause_results", [])

    simplified_clauses = [
        {
            "index":    getattr(c, "position_index", None),
            "text":     getattr(c, "original_text", ""),
            "severity": getattr(c, "severity", ""),
            "type":     getattr(c, "clause_type", ""),
        }
        for c in clauses
    ]

    result = agent.detect(simplified_clauses)

    # Agent returns {"anomalies": [...]} — extract the list
    anomalies = result.get("anomalies", []) if isinstance(result, dict) else []

    print(f"[DEBUG anomaly_detection] anomalies found: {len(anomalies)}")

    # Key must match ContractState — "anomalies" not "contract_anomalies"
    return {"anomalies": anomalies}