from enum import Enum


class ClauseType(str, Enum):

    DEFINITIONS = "definitions"
    LIABILITY = "liability"
    TERMINATION = "termination"
    PAYMENT = "payment"
    CONFIDENTIALITY = "confidentiality"
    INDEMNIFICATION = "indemnification"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    GOVERNING_LAW = "governing_law"
    FORCE_MAJEURE = "force_majeure"
    OTHER = "other"