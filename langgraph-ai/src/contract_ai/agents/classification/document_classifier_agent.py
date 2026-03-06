from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from contract_ai.infrastructure.llm.client import get_llm


class DocumentClassifierAgent:

    def __init__(self):

        self.llm = get_llm()

        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a legal document classifier.

Determine if the document is a CONTRACT.

Examples of contracts:
- service agreements
- master service agreements
- NDAs
- employment contracts
- licensing agreements

Documents that are NOT contracts:
- invoices
- reports
- presentations
- emails
- marketing documents
""",
                ),
                (
                    "user",
                    """
Document text:

{text}

Return JSON only, no explanation, no markdown:

{{
  "is_contract": true | false,
  "document_type": "..."
}}
""",
                ),
            ]
        )

    def classify(self, text):

        chain = self.prompt | self.llm | self.parser

        return chain.invoke({"text": text[:4000]})