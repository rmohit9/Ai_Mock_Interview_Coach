import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "qwen/qwen3.8-27b")
    TEMPERATURE: float = 0.6
    MAX_TOKENS: int = 1000


settings = Settings()

if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")