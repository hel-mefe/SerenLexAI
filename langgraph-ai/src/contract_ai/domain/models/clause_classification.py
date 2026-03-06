from pydantic import BaseModel
from contract_ai.domain.value_objects.clause_type import ClauseType


class ClauseClassification(BaseModel):

    clause_type: ClauseType