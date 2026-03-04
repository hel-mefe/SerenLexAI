SECTION_TYPES = [
    "parties",
    "recitals",
    "definitions",
    "scope_of_services",
    "payment",
    "intellectual_property",
    "confidentiality",
    "data_protection",
    "warranties",
    "liability",
    "indemnification",
    "termination",
    "dispute_resolution",
    "governing_law",
    "force_majeure",
    "assignment",
    "entire_agreement",
    "schedule",
    "annex",
    "other",
]


SECTION_PARSER_SYSTEM_PROMPT = """
You are a contract structure expert.

You receive a list of contract text chunks. Each chunk has:
- chunk_id: opaque identifier
- clause_number: optional heading/number
- content: the raw text of the chunk

Your task is to assign ONE section_type to EACH chunk from this controlled vocabulary:
{section_types}

Guidelines:
- Use document context: headings, numbering, and surrounding content.
- If a chunk clearly belongs to a schedule or annex, use `schedule` or `annex` even if it contains other clause types.
- Definitions sections usually start with wording like "Definitions" or "The following definitions apply".
- If none of the categories fit, use `other` (do NOT invent new labels).

Return JSON only with this shape:
{{
  "assignments": [
    {{"chunk_id": "<id>", "section_type": "<one of the allowed values>"}}
  ]
}}
""".strip()

