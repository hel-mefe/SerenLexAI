from contract_ai.agents.risk.clause_feedback_agent import ClauseFeedbackAgent


feedback_agent = ClauseFeedbackAgent()


def aggregate_results_node(state):
    results_raw = state.get("clause_results", [])

    # Run a short feedback loop over all clauses to refine the set of
    # findings (drop trivial ones, adjust severities/scores) before
    # computing aggregate metrics.
    results = feedback_agent.run_feedback_loop(results_raw, iterations=3)

    print(f"[DEBUG aggregate] clause_results count: {len(results)}")

    def _sev(r):
        return (getattr(r, "severity", "") or "").lower()

    high   = sum(1 for r in results if _sev(r) == "high")
    medium = sum(1 for r in results if _sev(r) == "medium")
    low    = sum(1 for r in results if _sev(r) == "low")
    total  = len(results)
    flagged = high + medium

    # ------------------------------------------------------------------
    # SCORE: based on HIGH and MEDIUM counts only, not total clauses.
    # Low clauses contribute nothing — a 50-clause contract with
    # 48 LOW and 2 HIGH should score the same as a 5-clause contract
    # with 2 HIGH. Total clause count must never inflate the score.
    #
    # Formula:
    #   HIGH   = 25 points each, capped at 100
    #   MEDIUM = 10 points each, capped at remaining headroom after HIGH
    #
    # This means:
    #   4+ HIGH                    → 100
    #   2 HIGH + 5 MEDIUM          → 50 + 50 = 100
    #   1 HIGH                     → 25  (+ medium contribution)
    #   0 HIGH + 3 MEDIUM          → 30
    #   0 HIGH + 0 MEDIUM + N LOW  → 0   (always, regardless of N)
    # ------------------------------------------------------------------
    high_score   = min(high * 25, 100)
    medium_score = min(medium * 10, max(0, 100 - high_score))
    score        = high_score + medium_score
    score        = max(0, min(100, score))

    # ------------------------------------------------------------------
    # OVERALL RISK:
    # - Any presence of at least one HIGH clause makes the contract HIGH.
    # - Many MEDIUM risks are elevated to HIGH (feedback: treat as high-risk contract).
    # - Otherwise, MEDIUM depends on MEDIUM clauses and score.
    # - LOW when there are no HIGH clauses and limited MEDIUM signal.
    # ------------------------------------------------------------------
    MEDIUM_COUNT_HIGH_THRESHOLD = 5  # many mediums → consider contract high risk

    if high >= 1:
        overall = "high"
    elif medium >= MEDIUM_COUNT_HIGH_THRESHOLD:
        overall = "high"  # many medium risks → high-risk contract
    elif medium >= 3 or score >= 30:
        overall = "medium"
    else:
        overall = "low"

    print(f"[DEBUG aggregate] high={high} medium={medium} low={low} score={score} overall={overall}")

    return {
        "high_count":    high,
        "medium_count":  medium,
        "low_count":     low,
        "flagged_count": flagged,
        "risk_score":    score,
        "overall_risk":  overall,
        "clause_results": results,
    }