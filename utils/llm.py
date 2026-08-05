from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import settings


class LLM:

    def __init__(self):

        self.model = ChatMistralAI(
            api_key=settings.MISTRAL_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
    ) -> str:

        messages = []

        if system_prompt:

            messages.append(
                SystemMessage(content=system_prompt)
            )

        messages.append(
            HumanMessage(content=prompt)
        )

        response = self.model.invoke(messages)

        return response.content