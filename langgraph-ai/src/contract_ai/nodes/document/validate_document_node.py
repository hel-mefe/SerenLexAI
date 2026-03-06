from contract_ai.infrastructure.vision.document_validator import DocumentValidator

validator = DocumentValidator()


def validate_document_node(state):

    pages = state["page_images"]

    validator.validate(pages)

    return {}