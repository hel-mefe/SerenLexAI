from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from contract_ai.domain.models.clause import ClauseAnalysisOutput, ClauseResult
from contract_ai.infrastructure.llm.client import get_llm
from contract_ai.infrastructure.llm.prompts.clause_analysis_prompt import SYSTEM_PROMPT


class ClauseAnalysisAgent:

    def __init__(self):

        self.llm = get_llm()

        self.parser = PydanticOutputParser(pydantic_object=ClauseAnalysisOutput)

        # Use .partial() to bind format_instructions at construction time
        # so the JSON schema curly braces never get parsed as template variables
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "user",
                    """
You are analyzing a clause from a legal contract.

Context clauses (may be empty):
{context}

Clause type:
{clause_type}

Clause to analyze:
{clause}

Tasks:
1. Determine the risk severity (LOW, MEDIUM, HIGH)
2. Explain clearly why the clause introduces risk
3. Provide a concrete recommended action

Return JSON following this schema:

{format_instructions}
""",
                ),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

    def analyze(
        self,
        clause_text: str,
        clause_type: str | None = None,
        previous_clause: dict | None = None,
        next_clause: dict | None = None,
    ) -> ClauseAnalysisOutput:

        context_text = ""

        if previous_clause and previous_clause.get("text"):
            context_text += f"\nPrevious clause:\n{previous_clause['text']}\n"

        if next_clause and next_clause.get("text"):
            context_text += f"\nNext clause:\n{next_clause['text']}\n"

        chain = self.prompt | self.llm | self.parser

        # format_instructions already bound via .partial() — don't pass here
        return chain.invoke(
            {
                "clause":      clause_text,
                "clause_type": clause_type or "unknown",
                "context":     context_text or "None",
            }
        )