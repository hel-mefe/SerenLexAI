from __future__ import annotations

from typing import List

from langchain_openai import OpenAIEmbeddings

from app.contract_intelligence.config import get_settings


_settings = get_settings()

_embeddings = OpenAIEmbeddings(
    model=_settings.embedding_model,
    api_key=_settings.openai_api_key,
)


async def embed_text(text: str) -> List[float]:
    """
    Async wrapper around the embeddings client.

    LangChain's OpenAIEmbeddings is sync; we call it in a threadpool-friendly
    way via its existing interface. For most contract sizes this is sufficient.
    """
    # The underlying implementation is synchronous; however, LangGraph/async
    # environments can tolerate occasional sync calls for embeddings.
    return _embeddings.embed_query(text)

