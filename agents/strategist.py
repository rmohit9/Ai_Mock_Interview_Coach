from models.strategy import Strategy

from utils.llm import LLM
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_json


class StrategyAgent:

    def __init__(self):

        # Strategy JSON is small — cap tokens low for faster responses
        self.llm = LLM(max_tokens=400)

        self.system_prompt = load_prompt(
            "strategist.txt"
        )

    def decide(
        self,
        evaluation,
    ) -> Strategy:

        prompt = f"""
Latest Evaluation

{evaluation.model_dump_json(indent=4)}

Decide the next interview strategy.

Return JSON only.
"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        return Strategy(
            **parse_json(response)
        )