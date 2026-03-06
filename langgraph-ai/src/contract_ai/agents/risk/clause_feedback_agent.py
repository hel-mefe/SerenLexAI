from __future__ import annotations

import json
from typing import Any, Iterable, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from contract_ai.infrastructure.llm.client import get_llm


class ClauseFeedbackAgent:
    """
    Runs a small feedback loop over the full set of analysed clauses
    to refine severities, scores and explanations, and to drop trivial
    or imprecise findings.

    It does NOT create new clauses – only updates or removes existing
    ones based on their index.
    """

    def __init__(self) -> None:
        self.llm = get_llm()
        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert contract risk reviewer.

You receive a list of clauses that have already been analysed for risk.
Each clause has:
- id (its index in the original list)
- title
- text
- current severity (LOW, MEDIUM, HIGH)
- numeric risk_score in [0, 100]
- risk_explanation
- recommended_action

Your job is to run a refinement pass and make the overall set of findings
very precise and focused:

- Remove clauses that are trivial, duplicative or not really risky
  (set keep=false for those).
- Downgrade MEDIUM to LOW where the risk is minor or mostly theoretical.
- HIGH clauses are critical: if a clause is genuinely HIGH risk, it
  should stay HIGH unless you decide it is not a meaningful finding
  at all, in which case you may drop it (keep=false) rather than
  downgrading it.
- Make sure LOW clauses are truly low‑risk and useful; many LOWs in a
  long contract should not make the contract appear high risk.
- Prefer a small number of precise MEDIUM/HIGH findings over a long list
  of noisy LOWs.

IMPORTANT MAPPINGS (you MUST respect them):
- LOW:    risk_score 0–49
- MEDIUM: risk_score 50–84
- HIGH:   risk_score 85–100

You may:
- adjust severity
- adjust risk_score
- refine the explanation and recommended_action
- drop clauses (keep=false) that do not add meaningful signal

You MUST NOT:
- invent new clauses
- change clause ids
- return more clauses than you received
                    """,
                ),
                (
                    "user",
                    """
Refinement iteration {iteration}/{total_iterations}

Current high‑level context:
- Total clauses analysed: {total_clauses}
- HIGH clauses: {high_count}
- MEDIUM clauses: {medium_count}
- LOW clauses: {low_count}

Here is the current list of clauses as JSON:

{clauses_json}

Return JSON only, no explanation, no markdown, with this exact shape:

{{
  "clauses": [
    {{
      "id": <int>,              // original clause index
      "keep": <true|false>,
      "severity": "LOW|MEDIUM|HIGH",
      "risk_score": <int 0-100>,
      "risk_explanation": "<updated explanation>",
      "recommended_action": "<updated recommendation>"
    }},
    ...
  ]
}}
                    """,
                ),
            ]
        )

    def run_feedback_loop(
        self,
        results: Iterable[Any],
        iterations: int = 1,
    ) -> List[Any]:
        """
        Run up to `iterations` refinement passes over the clause results.

        The input `results` is typically a list of ClauseResult objects
        but may also be a list of dicts; this function preserves the
        original object type (ClauseResult instances are updated in-place).
        """
        results_list = list(results)
        if not results_list or iterations <= 0:
            return results_list

        for it in range(1, iterations + 1):
            serialised = self._serialise(results_list)
            context = self._compute_context(results_list)

            chain = self.prompt | self.llm | self.parser

            try:
                response = chain.invoke(
                    {
                        "iteration": it,
                        "total_iterations": iterations,
                        "total_clauses": context["total_clauses"],
                        "high_count": context["high_count"],
                        "medium_count": context["medium_count"],
                        "low_count": context["low_count"],
                        "clauses_json": json.dumps(serialised, ensure_ascii=False),
                    }
                )
            except Exception as exc:  # pragma: no cover - defensive
                print(f"[WARNING ClauseFeedbackAgent] iteration {it} failed: {exc}")
                break

            updates = []
            if isinstance(response, dict):
                updates = response.get("clauses", []) or []

            if not updates:
                break

            new_results = self._apply_updates(results_list, updates)

            # If nothing relevant changed (same number of clauses and same
            # severity labels), stop early.
            def _sev(r: Any) -> str:
                if isinstance(r, dict):
                    return str(r.get("severity", "")).lower()
                return str(getattr(r, "severity", "") or "").lower()

            before_sevs = [_sev(r) for r in results_list]
            after_sevs = [_sev(r) for r in new_results]
            if len(new_results) == len(results_list) and before_sevs == after_sevs:
                break

            results_list = new_results

            if not results_list:
                break

        return results_list

    def _serialise(self, results: List[Any]) -> List[dict]:
        serialised: List[dict] = []
        for idx, r in enumerate(results):
            if isinstance(r, dict):
                get = r.get
            else:
                get = lambda k, default=None: getattr(r, k, default)  # type: ignore[assignment]

            # Collect lightweight reference information (ids and titles) for
            # any explicitly linked clauses discovered earlier in the pipeline.
            refs_compact: list[dict] = []
            ref_ids = None
            if isinstance(r, dict):
                ref_ids = r.get("references")
            else:
                ref_ids = getattr(r, "references", None)

            if isinstance(ref_ids, list):
                for ref_idx in ref_ids:
                    try:
                        j = int(ref_idx)
                    except (TypeError, ValueError):
                        continue
                    if j < 0 or j >= len(results):
                        continue
                    other = results[j]
                    if isinstance(other, dict):
                        title_other = other.get("title", "")
                        number_other = other.get("number", None)
                    else:
                        title_other = getattr(other, "title", "")
                        number_other = getattr(other, "number", None)
                    refs_compact.append(
                        {
                            "id": j,
                            "number": number_other,
                            "title": title_other,
                        }
                    )

            serialised.append(
                {
                    "id": idx,
                    "title": get("title", ""),
                    "severity": (get("severity", "") or "").upper(),
                    "risk_score": get("risk_score"),
                    "text": get("original_text", ""),
                    "risk_explanation": get("risk_explanation", ""),
                    "recommended_action": get("recommended_action", ""),
                    "references": refs_compact,
                }
            )
        return serialised

    def _compute_context(self, results: List[Any]) -> dict:
        def _sev(r: Any) -> str:
            if isinstance(r, dict):
                return str(r.get("severity", "")).lower()
            return str(getattr(r, "severity", "") or "").lower()

        high = sum(1 for r in results if _sev(r) == "high")
        med = sum(1 for r in results if _sev(r) == "medium")
        low = sum(1 for r in results if _sev(r) == "low")

        return {
            "total_clauses": len(results),
            "high_count": high,
            "medium_count": med,
            "low_count": low,
        }

    def _apply_updates(self, original: List[Any], updates: List[dict]) -> List[Any]:
        """
        Apply LLM-suggested updates to the original results list.

        Each update entry should contain:
          - id (int)
          - keep (bool)
          - severity (str)
          - risk_score (int)
          - risk_explanation (str)
          - recommended_action (str)
        """
        updates_by_id: dict[int, dict] = {}
        for u in updates:
            try:
                idx = int(u.get("id"))
            except (TypeError, ValueError):
                continue
            if idx < 0 or idx >= len(original):
                continue
            updates_by_id[idx] = u

        new_results: List[Any] = []
        for idx, item in enumerate(original):
            upd = updates_by_id.get(idx)
            if not upd:
                # No update for this clause — keep as is.
                new_results.append(item)
                continue

            if upd.get("keep") is False:
                # Explicitly dropped.
                continue

            # Preserve original severity so we can enforce invariants
            if isinstance(item, dict):
                original_sev = str(item.get("severity", "")).lower()
            else:
                original_sev = str(getattr(item, "severity", "") or "").lower()

            severity = upd.get("severity")
            risk_score = upd.get("risk_score")
            risk_explanation = upd.get("risk_explanation")
            recommended_action = upd.get("recommended_action")

            if isinstance(item, dict):
                # Never downgrade HIGH clauses via feedback; they can only
                # be removed (keep=false) or kept as HIGH.
                if severity:
                    sev_norm = str(severity).lower()
                    if original_sev == "high" and sev_norm != "high":
                        pass
                    else:
                        item["severity"] = sev_norm
                if risk_score is not None:
                    try:
                        score_val = max(0, min(100, int(risk_score)))
                        if original_sev == "high":
                            score_val = max(score_val, 85)
                        item["risk_score"] = score_val
                    except (TypeError, ValueError):
                        pass
                if risk_explanation:
                    item["risk_explanation"] = risk_explanation
                if recommended_action:
                    item["recommended_action"] = recommended_action
                new_results.append(item)
            else:
                # Assume a ClauseResult-like object with attributes.
                if severity:
                    sev_norm = str(severity).lower()
                    if original_sev != "high" or sev_norm == "high":
                        item.severity = sev_norm
                if risk_score is not None:
                    try:
                        score_val = max(0, min(100, int(risk_score)))
                        if original_sev == "high":
                            score_val = max(score_val, 85)
                        item.risk_score = score_val
                    except (TypeError, ValueError):
                        pass
                if risk_explanation:
                    item.risk_explanation = risk_explanation
                if recommended_action:
                    item.recommended_action = recommended_action
                new_results.append(item)

        return new_results

