
import os

class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "local")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "local")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL", "http://localhost:11434")

settings = Settings()
