from pathlib import Path


PROMPT_DIR = Path("prompts")


def load_prompt(filename: str) -> str:

    path = PROMPT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()