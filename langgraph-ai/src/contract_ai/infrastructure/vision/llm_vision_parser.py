import json
import base64
import re
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from contract_ai.domain.models.contract_structure import ContractStructure
from contract_ai.infrastructure.config.settings import settings


class LLMVisionParser:

    def __init__(self):

        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0,
        )

    def _encode_image(self, image_path: str):

        with open(Path(image_path), "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _extract_json(self, text: str):
        """
        Extract JSON object from LLM response.
        Handles:
        - ```json blocks
        - explanations before JSON
        """

        # remove code blocks
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        # find first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found in LLM response")

        return json.loads(match.group())

    def parse_page(self, image_path: str):

        base64_image = self._encode_image(image_path)

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": """
You are parsing a contract page.

Extract structured data.

Return JSON only.

Schema:

{
 "sections": [{"title": "...", "content": "..."}],
 "clauses": [{"number": "...", "title": "...", "text": "..."}]
}

Rules:
- Preserve clause numbering
- Ignore headers/footers
- Do not invent text
"""
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
            ]
        )

        response = self.llm.invoke([message])

        content = response.content

        if isinstance(content, str):
            data = self._extract_json(content)
        else:
            data = content

        return ContractStructure(**data)