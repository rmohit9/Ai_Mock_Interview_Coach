from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    MODEL_NAME: str = "llama-3.1-8b-instant"

    TEMPERATURE: float = 0.7

    MAX_TOKENS: int = 1024


settings = Settings()

if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")