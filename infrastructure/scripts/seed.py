from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Sequence
import sys

from sqlalchemy import func, select

# Ensure the backend package is importable when this script is executed from
# the infrastructure directory or project root.
ROOT_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from core.database import SessionLocal

# Import all related models so SQLAlchemy can resolve string-based
# relationship targets such as "User" and "Action" when mappers initialize.
from models.user import User  # noqa: F401
from models.analysis import Analysis
from models.clauses import Clause
from models.actions import Action


def _seed_analyses(session) -> Sequence[Analysis]:
    """
    Insert a small set of analyses roughly matching the frontend mocks.
    """
    # Anchor date so the relative dates look similar to the UI examples.
    now = datetime.utcnow()

    definitions = [
        {
            "title": "Service Agreement — Acme Corp",
            "days_ago": 0,
            "risk": "High",
            "clauses": 12,
            "score": 84,
        },
        {
            "title": "Software License — TechStart Ltd",
            "days_ago": 1,
            "risk": "Medium",
            "clauses": 8,
            "score": 52,
        },
        {
            "title": "Consulting Contract — BuildCo",
            "days_ago": 3,
            "risk": "Low",
            "clauses": 5,
            "score": 21,
        },
        {
            "title": "Partnership Agreement — InnovateLab",
            "days_ago": 4,
            "risk": "High",
            "clauses": 15,
            "score": 91,
        },
        {
            "title": "NDA — Quantum Systems",
            "days_ago": 5,
            "risk": "Low",
            "clauses": 3,
            "score": 18,
        },
        {
            "title": "Employment Contract — Sarah Chen",
            "days_ago": 6,
            "risk": "Medium",
            "clauses": 9,
            "score": 47,
        },
        {
            "title": "Vendor Agreement — SupplyChain Inc",
            "days_ago": 7,
            "risk": "High",
            "clauses": 14,
            "score": 79,
        },
        {
            "title": "Lease Agreement — Office Tower B",
            "days_ago": 8,
            "risk": "Medium",
            "clauses": 11,
            "score": 63,
        },
        {
            "title": "SaaS Subscription — CloudHost Pro",
            "days_ago": 9,
            "risk": "Low",
            "clauses": 6,
            "score": 29,
        },
    ]

    analyses: list[Analysis] = []

    for definition in definitions:
        created_at = now - timedelta(days=definition["days_ago"])

        high = (
            definition["clauses"]
            if definition["risk"] == "High"
            else 0
        )
        medium = (
            definition["clauses"]
            if definition["risk"] == "Medium"
            else 0
        )
        low = (
            definition["clauses"]
            if definition["risk"] == "Low"
            else 0
        )

        analysis = Analysis(
            title=definition["title"],
            original_filename=None,
            source_type="upload",
            status="completed",
            overall_risk=definition["risk"],
            risk_score=definition["score"],
            flagged_count=definition["clauses"],
            high_count=high,
            medium_count=medium,
            low_count=low,
            raw_text=None,
        )

        # Manually set timestamps so they align with our "days_ago" anchor.
        analysis.created_at = created_at
        analysis.updated_at = created_at

        session.add(analysis)
        analyses.append(analysis)

    session.flush()
    return analyses


def _seed_clauses(session, analysis: Analysis) -> None:
    """
    Insert clause records for a single analysis to back the report page.
    """
    definitions = [
        {
            "title": "Unlimited Liability Clause",
            "severity": "High",
            "original_text": (
                "The service provider shall bear unlimited liability for "
                "any damages arising from the service."
            ),
            "risk_explanation": (
                "Unlimited liability exposes your company to uncapped "
                "financial risk in the event of a dispute or failure."
            ),
            "recommended_action": (
                "Negotiate a liability cap equal to the total contract "
                "value or 12 months of fees."
            ),
        },
        {
            "title": "Auto-Renewal Clause",
            "severity": "Medium",
            "original_text": (
                "This agreement shall automatically renew for successive "
                "one-year terms unless terminated 90 days prior."
            ),
            "risk_explanation": (
                "The 90-day termination window is unusually long and may "
                "cause unintended renewals."
            ),
            "recommended_action": (
                "Request a reduction to a 30-day notice period with "
                "explicit written confirmation of renewal."
            ),
        },
        {
            "title": "Intellectual Property Assignment",
            "severity": "High",
            "original_text": (
                "All work product created under this agreement is the sole "
                "property of the client."
            ),
            "risk_explanation": (
                "Broad IP assignment may include pre-existing tools and "
                "frameworks owned by your company."
            ),
            "recommended_action": (
                "Carve out pre-existing IP and limit assignment to work "
                "product created solely for this engagement."
            ),
        },
        {
            "title": "Governing Law",
            "severity": "Low",
            "original_text": (
                "This agreement shall be governed by the laws of the State "
                "of Delaware."
            ),
            "risk_explanation": (
                "Jurisdiction may require travel or legal representation in "
                "an unfamiliar state."
            ),
            "recommended_action": (
                "Negotiate for jurisdiction in your operating state or "
                "agree to remote arbitration."
            ),
        },
    ]

    for index, definition in enumerate(definitions):
        clause = Clause(
            analysis_id=analysis.id,
            title=definition["title"],
            severity=definition["severity"],
            original_text=definition["original_text"],
            risk_explanation=definition["risk_explanation"],
            recommended_action=definition["recommended_action"],
            clause_type=None,
            position_index=index,
        )
        session.add(clause)

    session.flush()


def _seed_actions(session, primary_analysis: Analysis) -> None:
    """
    Insert a small history stream similar to the frontend mock history.
    """
    now = datetime.utcnow()

    events = [
        {
            "type": "UPLOAD",
            "title": "Contract Uploaded",
            "description": "Service Agreement — Acme Corp",
            "analysis": primary_analysis,
            "seconds_ago": 1200,
        },
        {
            "type": "COMPLETED",
            "title": "Analysis Completed",
            "description": "12 clauses flagged · High Risk",
            "analysis": primary_analysis,
            "seconds_ago": 0,
        },
        {
            "type": "FAILED",
            "title": "Analysis Failed",
            "description": "Parsing error detected",
            "analysis": None,
            "seconds_ago": 86400,
        },
    ]

    for event in events:
        created_at = now - timedelta(seconds=event["seconds_ago"])

        action = Action(
            type=event["type"],
            title=event["title"],
            description=event["description"],
            analysis_id=(
                event["analysis"].id if event["analysis"] is not None else None
            ),
            user_id=None,
            meta=None,
        )
        action.created_at = created_at
        action.updated_at = created_at

        session.add(action)

    session.flush()


def main() -> None:
    """
    Seed the database with initial analyses, clauses and actions.

    The seeding is idempotent at the table level: if there is already at
    least one analysis present, the script will not insert duplicates.
    """
    session = SessionLocal()

    try:
        existing = session.scalar(
            select(func.count(Analysis.id))
        ) or 0

        if existing > 0:
            print("Seed skipped: analyses already exist.")
            return

        analyses = _seed_analyses(session)

        if analyses:
            # Use the first analysis as the primary one for clauses and actions.
            _seed_clauses(session, analyses[0])
            _seed_actions(session, analyses[0])

        session.commit()
        print("Seed completed successfully.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()

