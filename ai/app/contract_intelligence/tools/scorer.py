from __future__ import annotations

from typing import Any, Dict, List, Tuple


CLAUSE_WEIGHTS: dict[str, float] = {
    "liability": 2.5,
    "indemnification": 2.2,
    "ip": 2.0,
    "payment": 1.8,
    "termination": 1.7,
    "data_protection": 1.5,
    "confidentiality": 1.3,
    "warranties": 1.3,
    "dispute_resolution": 1.2,
    "governing_law": 1.0,
    "other": 0.8,
}


def compute_overall_score(
    classified_clauses: List[Dict[str, Any]]
) -> Tuple[float, str, Dict[str, Any]]:
    """
    Deterministic risk scoring based on classified clauses.
    """
    if not classified_clauses:
        return 0.0, "low", {
            "by_section": {},
            "top_risks": [],
            "clause_count": 0,
            "high_risk_count": 0,
            "critical_risk_count": 0,
        }

    section_scores: dict[str, float] = {}
    section_weights: dict[str, float] = {}
    contributions: list[tuple[float, dict[str, Any]]] = []
    high_risk_count = 0
    critical_risk_count = 0

    for clause in classified_clauses:
        score = clause.get("risk_score")
        if score is None:
            continue
        section_type = clause.get("section_type") or "other"
        weight = CLAUSE_WEIGHTS.get(section_type, CLAUSE_WEIGHTS["other"])
        contribution = float(score) * weight

        section_scores[section_type] = section_scores.get(section_type, 0.0) + contribution
        section_weights[section_type] = section_weights.get(section_type, 0.0) + weight

        contributions.append(
            (
                contribution,
                {
                    "clause_type": clause.get("clause_type"),
                    "section_type": section_type,
                    "score": float(score),
                    "page_start": clause.get("page_start"),
                    "page_end": clause.get("page_end"),
                },
            )
        )

        level = clause.get("risk_level")
        if level == "high":
            high_risk_count += 1
        elif level == "critical":
            critical_risk_count += 1

    by_section: dict[str, float] = {}
    weighted_total = 0.0
    total_weight = 0.0

    for section, total in section_scores.items():
        w = section_weights[section]
        section_avg = total / w if w else 0.0
        by_section[section] = round(section_avg, 2)
        weighted_total += total
        total_weight += w

    overall = weighted_total / total_weight if total_weight else 0.0

    if overall < 3.5:
        level = "low"
    elif overall < 5.5:
        level = "medium"
    elif overall < 7.5:
        level = "high"
    else:
        level = "critical"

    contributions.sort(key=lambda x: x[0], reverse=True)
    top_risks = [meta for _, meta in contributions[:3]]

    breakdown: Dict[str, Any] = {
        "by_section": by_section,
        "top_risks": top_risks,
        "clause_count": len(classified_clauses),
        "high_risk_count": high_risk_count,
        "critical_risk_count": critical_risk_count,
    }

    return round(overall, 2), level, breakdown

