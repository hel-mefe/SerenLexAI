from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    # API base path and versioning
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"

    # Document upload limits
    UPLOAD_MAX_PAGES: int = 20
    UPLOAD_MAX_FILE_SIZE_MB: int = 10

    # Directory for uploaded PDFs (shared with ai_worker via volume)
    UPLOAD_DIR: str = "/app/uploads"

    # Directory for generated risk report PDFs (shared with ai_worker via volume)
    REPORTS_DIR: str = "/app/reports"

    # Messaging / background processing
    REDIS_URL: str = "redis://serenlex_redis:6379/0"

    class Config:
        # Resolve the .env file relative to the backend package root so that
        # scripts can be executed from any working directory.
        env_file = str(Path(__file__).resolve().parent.parent / ".env")


settings = Settings()