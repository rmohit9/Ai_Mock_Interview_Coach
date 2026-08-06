import time

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
        retries: int = 3,
    ) -> str:

        last_error = None

        for attempt in range(retries):

            try:

                messages = []

                if system_prompt:

                    messages.append(
                        SystemMessage(
                            content=system_prompt
                        )
                    )

                messages.append(
                    HumanMessage(
                        content=prompt
                    )
                )

                response = self.model.invoke(
                    messages
                )

                if response is None:

                    raise Exception(
                        "No response received from the model."
                    )

                if response.content is None:

                    raise Exception(
                        "Model returned an empty response."
                    )

                text = str(
                    response.content
                ).strip()

                if text == "":

                    raise Exception(
                        "Model returned a blank response."
                    )

                return text

            except Exception as e:

                last_error = e

                print(
                    f"[LLM Retry {attempt + 1}/{retries}] {e}"
                )

                if attempt < retries - 1:

                    time.sleep(2)

        raise RuntimeError(
            f"LLM failed after {retries} attempts.\n\n{last_error}"
        )