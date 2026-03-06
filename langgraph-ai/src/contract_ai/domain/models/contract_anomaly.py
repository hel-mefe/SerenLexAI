from pydantic import BaseModel
from typing import List

class ContractAnomaly(BaseModel):
    title: str
    description: str
    affected_clauses: List[int]
    severity: str

