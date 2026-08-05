from models.strategy import Strategy
from utils.llm import LLM
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_json


class StrategyAgent:

    def __init__(self):
        self.llm = LLM()
        self.system_prompt = load_prompt("strategist.txt")

    def decide(self, evaluation: Strategy) -> Strategy:

        prompt = f"""
Latest Evaluation:

{evaluation.model_dump_json(indent=4)}

Decide what should happen next.

Return ONLY valid JSON.
"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        return Strategy(**parse_json(response))