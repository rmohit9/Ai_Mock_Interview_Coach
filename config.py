from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY")

    MODEL_NAME: str = "mistral-small-latest"

    TEMPERATURE: float = 0.7

    MAX_TOKENS: int = 1024


settings = Settings()

if not settings.MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in .env")