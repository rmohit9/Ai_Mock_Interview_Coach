from models.report import InterviewReport

from utils.llm import LLM
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_json


class CoachAgent:

    def __init__(self):

        self.llm = LLM()

        self.system_prompt = load_prompt(
            "coach.txt"
        )

    def generate_report(
        self,
        role,
        history,
        evaluations,
    ) -> InterviewReport:

        prompt = f"""
Candidate Role:

{role}

Conversation History:

{history}

Evaluation Results:

{evaluations}

Generate the final interview report.

Return ONLY JSON.
"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        return InterviewReport(
            **parse_json(response)
        )