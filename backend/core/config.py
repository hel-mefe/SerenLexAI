from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    # API base path and versioning
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"

    class Config:
        env_file = ".env"


settings = Settings()