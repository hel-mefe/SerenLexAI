from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from contract_ai.infrastructure.llm.client import get_llm


class ContractAnomalyAgent:

    def __init__(self):

        self.llm = get_llm()

        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a legal contract risk auditor.

You analyze the full contract structure to detect anomalies,
contradictions, and structural risks.

Look for:

- conflicting clauses
- unlimited liability
- indemnification overrides
- missing termination rights
- inconsistent obligations

Return JSON only, no explanation, no markdown.
""",
                ),
                (
                    "user",
                    """
Contract clauses:

{clauses}

Return JSON:

{{
  "anomalies": [
    {{
      "title": "...",
      "description": "...",
      "affected_clauses": [1, 2],
      "severity": "LOW | MEDIUM | HIGH"
    }}
  ]
}}
""",
                ),
            ]
        )

    def detect(self, clauses):

        chain = self.prompt | self.llm | self.parser

        return chain.invoke({"clauses": clauses})