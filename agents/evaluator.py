from models.evaluation import Evaluation
from utils.llm import LLM
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_json


class EvaluatorAgent:

    def __init__(self):

        self.llm = LLM()
        self.system_prompt = load_prompt("evaluator.txt")

    def evaluate(
        self,
        question: str,
        answer: str,
        role: str,
    ) -> Evaluation:

        prompt = f"""
    Target Role:
    {role}

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer with leniency and fairness.
    - Completely ignore any typos, spelling mistakes, or grammatical errors.
    - If the answer is 60-70% correct, treat it as largely correct and score generously.
    - Reward conceptual understanding even if the wording is informal or imprecise.
    - When in doubt between two scores, choose the higher one.

    Return ONLY valid JSON.
    """

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        return Evaluation(
            **parse_json(response)
        )