import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from config import settings


# ------------------------------------------------------------------
# Shared singleton clients — created once, reused by all agents.
# Avoids recreating HTTP connection pools per-agent instantiation.
# ------------------------------------------------------------------

_shared_client = None
_fast_client = None


def _get_client(max_tokens: int) -> ChatGroq:
    """Returns a shared ChatGroq instance for a given token budget."""
    global _shared_client, _fast_client
    if max_tokens <= 512:
        if _fast_client is None:
            _fast_client = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY.strip(),
                model_name=settings.MODEL_NAME.strip(),
                temperature=settings.TEMPERATURE,
                max_tokens=max_tokens,
            )
        return _fast_client
    else:
        if _shared_client is None:
            _shared_client = ChatGroq(
                groq_api_key=settings.GROQ_API_KEY.strip(),
                model_name=settings.MODEL_NAME.strip(),
                temperature=settings.TEMPERATURE,
                max_tokens=max_tokens,
            )
        return _shared_client


class LLM:
    """
    Thin wrapper around a shared ChatGroq client.

    Args:
        max_tokens: Output token cap. Pass a small value (e.g. 300) for agents
                    that only emit short responses (questions, strategy JSON).
                    All agents sharing the same budget reuse one HTTP connection.
    """

    def __init__(self, max_tokens=None):
        self._max_tokens = max_tokens if max_tokens is not None else settings.MAX_TOKENS

    @property
    def model(self) -> ChatGroq:
        return _get_client(self._max_tokens)

    def generate(self, prompt: str, system_prompt: str = "", retries: int = 3) -> str:
        last_error = None

        for attempt in range(retries):
            try:
                messages = []
                if system_prompt:
                    messages.append(SystemMessage(content=system_prompt))
                messages.append(HumanMessage(content=prompt))

                response = self.model.invoke(messages)

                if response is None or response.content is None:
                    raise Exception("Model returned an empty response.")

                text = str(response.content).strip()
                if text == "":
                    raise Exception("Model returned a blank response.")

                return text

            except Exception as e:
                last_error = e
                print(f"[LLM Retry {attempt + 1}/{retries}] {e}")
                if attempt < retries - 1:
                    time.sleep(1)

        raise RuntimeError(f"LLM failed after {retries} attempts.\n\n{last_error}")
