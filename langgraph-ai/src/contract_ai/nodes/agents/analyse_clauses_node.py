import re

from contract_ai.agents.classification.clause_classifier_agent import ClauseClassifierAgent
from contract_ai.agents.risk.clause_analysis_agent import ClauseAnalysisAgent
from contract_ai.agents.risk.clause_feedback_agent import ClauseFeedbackAgent
from contract_ai.domain.models.clause import ClauseResult

classifier = ClauseClassifierAgent()
analyser   = ClauseAnalysisAgent()
feedback   = ClauseFeedbackAgent()


def analyse_clauses_node(state):
    """
    Processes all clauses sequentially — classify then analyse each one.
    Replaces the fan-out/fan-in pattern (map_clauses → clause_classification
    → clause_analysis → collect_clause_results) which cannot accumulate
    results across parallel Send branches in LangGraph without a checkpointer.
    """
    clauses = state["clauses_detected"]
    results = []

    for i, clause in enumerate(clauses):
        clause_text     = clause.get("text", "")
        previous_clause = clauses[i - 1] if i > 0 else None
        next_clause     = clauses[i + 1] if i < len(clauses) - 1 else None

        # Step 1: classify
        try:
            classification = classifier.classify(clause_text)
            clause_type    = classification.clause_type
        except Exception as e:
            print(f"[WARNING analyse_clauses] classify failed on clause {i}: {e}")
            clause_type = "other"

        # Step 2: analyse
        try:
            output = analyser.analyze(
                clause_text=clause_text,
                clause_type=clause_type,
                previous_clause=previous_clause,
                next_clause=next_clause,
            )

            result = ClauseResult(
                title              = clause.get("title") or str(clause_type) or "Unnamed Clause",
                severity           = output.severity,
                original_text      = clause_text,
                risk_explanation   = output.risk_explanation,
                recommended_action = output.recommended_action,
                clause_type        = str(clause_type),
                position_index     = clause.get("position_index"),
                page_number        = clause.get("page_number"),
                number             = clause.get("number"),
                risk_score         = output.risk_score,
            )

            print(f"[DEBUG analyse_clauses] [{i+1}/{len(clauses)}] {result.title} | {result.severity}")
            results.append(result)

        except Exception as e:
            import traceback
            print(f"[WARNING analyse_clauses] analyse failed on clause {i}: {e}")
            traceback.print_exc()

    print(f"[DEBUG analyse_clauses] done — {len(results)} results")

    # ------------------------------------------------------------------
    # Build cross‑references between clauses (by number mentions)
    # ------------------------------------------------------------------

    def _norm_number(n: str | None) -> str | None:
        if not n:
            return None
        s = str(n).strip().lower()
        # strip surrounding parentheses, e.g. "(a)" -> "a"
        if s.startswith("(") and s.endswith(")"):
            s = s[1:-1].strip()
        return s or None

    # Map normalised clause number -> index in results
    number_to_index: dict[str, int] = {}
    for idx, r in enumerate(results):
        key = _norm_number(getattr(r, "number", None))
        if key and key not in number_to_index:
            number_to_index[key] = idx

    # Regex to find references like "clause 12.3" or "section 5.2"
    ref_pattern = re.compile(r"\b(?:clause|section)\s+([0-9]+(?:\.[0-9]+)*)\b", re.IGNORECASE)

    for idx, r in enumerate(results):
        text = getattr(r, "original_text", "") or ""
        refs: list[int] = []
        ref_numbers: list[str] = []
        for m in ref_pattern.finditer(text):
            raw_label = m.group(1).strip()
            ref_num_norm = _norm_number(raw_label)
            if not ref_num_norm:
                continue
            target_idx = number_to_index.get(ref_num_norm)
            # Always record the raw reference label, even if we cannot
            # resolve it to a known clause index.
            if raw_label not in ref_numbers:
                ref_numbers.append(raw_label)
            if target_idx is None or target_idx == idx:
                continue
            if target_idx not in refs:
                refs.append(target_idx)

        if refs:
            r.references = refs
        if ref_numbers:
            r.reference_numbers = ref_numbers

    # ------------------------------------------------------------------
    # Run feedback loop only on non‑low clauses; LOW results are kept.
    # ------------------------------------------------------------------
    non_low = [r for r in results if (r.severity or "").lower() != "low"]
    low     = [r for r in results if (r.severity or "").lower() == "low"]

    refined = feedback.run_feedback_loop(non_low, iterations=1) if non_low else []
    final_results = refined + low

    return {"clause_results": final_results}