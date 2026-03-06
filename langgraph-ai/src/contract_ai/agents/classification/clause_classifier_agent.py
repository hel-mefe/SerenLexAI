from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from contract_ai.infrastructure.llm.client import get_llm
from contract_ai.domain.models.clause_classification import ClauseClassification


class ClauseClassifierAgent:

    def __init__(self):

        self.llm = get_llm()

        self.parser = PydanticOutputParser(
            pydantic_object=ClauseClassification
        )

        # Use partial_variables to bind format_instructions at prompt
        # construction time — this avoids LangChain misreading the JSON
        # schema curly braces inside format_instructions as template variables
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are an expert legal contract analyst.

Classify the type of the following clause.

Possible clause types:

definitions
liability
termination
payment
confidentiality
indemnification
intellectual_property
governing_law
force_majeure
other
""",
                ),
                (
                    "user",
                    """
Clause:

{clause}

Return JSON following this schema:

{format_instructions}
""",
                ),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

    def classify(self, clause_text: str) -> ClauseClassification:

        chain = self.prompt | self.llm | self.parser

        # format_instructions no longer needed here — already bound via partial
        return chain.invoke({"clause": clause_text})