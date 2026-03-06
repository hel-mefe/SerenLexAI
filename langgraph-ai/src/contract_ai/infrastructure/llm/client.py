from langchain_openai import ChatOpenAI
from contract_ai.infrastructure.config.settings import settings


def get_llm():

    return ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0.1,
    )
