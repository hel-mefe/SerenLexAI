from contract_ai.agents.classification.document_classifier_agent import (
    DocumentClassifierAgent
)

agent = DocumentClassifierAgent()


def document_classifier_node(state):

    raw_text = state.get("raw_text")

    result = agent.classify(raw_text)

    return {
        "is_contract": result["is_contract"],
        "document_type": result.get("document_type")
    }