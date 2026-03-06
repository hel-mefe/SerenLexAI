from pydantic import BaseModel
from typing import List, Optional


class ClauseBlock(BaseModel):
    number: Optional[str]
    title: Optional[str]
    text: str


class SectionBlock(BaseModel):
    title: str
    content: str


class ContractStructure(BaseModel):
    sections: List[SectionBlock]
    clauses: List[ClauseBlock]