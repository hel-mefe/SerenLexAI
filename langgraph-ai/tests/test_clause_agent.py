# test_clause_agent.py — run this standalone outside the graph
from contract_ai.agents.risk.clause_analysis_agent import ClauseAnalysisAgent
from contract_ai.domain.models.clause import ClauseAnalysisOutput

agent = ClauseAnalysisAgent()

test_clause = """
The Supplier's total aggregate liability to the other Party shall not 
exceed the lower of: (i) the fees actually paid in the three calendar 
months preceding the event; or (ii) £15,000, whichever is lesser.
"""

try:
    result = agent.analyze(
        clause_text=test_clause,
        clause_type="liability",
    )
    print(f"SUCCESS: {result}")
except Exception as e:
    import traceback
    traceback.print_exc()