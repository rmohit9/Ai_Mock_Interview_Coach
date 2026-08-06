import json
import re


def parse_json(text: str) -> dict:
    """
    Extracts and parses JSON from an LLM response.

    Handles:
    - Markdown code blocks
    - Extra text before/after JSON
    - Blank responses
    """

    if not text:
        raise ValueError("Empty response received from LLM.")

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    text = text.strip()

    # Extract first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        text = match.group(0)

    try:
        return json.loads(text)

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Invalid JSON returned by the LLM.\n\n{e}"
        )