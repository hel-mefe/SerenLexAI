from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key; read from OPENAI_KEY or OPENAI_API_KEY",
        validation_alias=AliasChoices("OPENAI_KEY", "OPENAI_API_KEY"),
    )
    database_url: str  # asyncpg format
    embedding_model: str = "text-embedding-3-small"
    primary_llm: str = "gpt-4o"
    fast_llm: str = "gpt-4o-mini"
    workflow_version: str = "1.0.0"
    max_concurrent_clause_tasks: int = 5
    max_file_size_mb: int = 50
    ocr_fallback_enabled: bool = True
    min_extractable_chars: int = 100
    chunk_max_tokens: int = 800
    rag_similar_clauses_k: int = 3
    redis_url: str = "redis://serenlex_redis:6379/0"

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    print('***** OPENAI_KEY ==> ', os.getenv("OPENAI_KEY"))
    return Settings()  # type: ignore[call-arg]

