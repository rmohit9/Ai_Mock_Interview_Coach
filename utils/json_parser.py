import json
import re


def parse_json(text: str):
    """
    Removes markdown code blocks and converts the response into a Python dictionary.
    """

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    return json.loads(text)