import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # LLM
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    # Document processing
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "20"))


settings = Settings()