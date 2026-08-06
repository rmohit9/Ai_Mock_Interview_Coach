from models.resume import ResumeProfile

from utils.llm import LLM
from utils.prompt_loader import load_prompt
from utils.json_parser import parse_json
from models.resume import ResumeProfile


class ResumeAnalyzerAgent:

    def __init__(self):

        self.llm = LLM()

        self.system_prompt = load_prompt(
            "resume_analyzer.txt"
        )

    def analyze(
        self,
        resume_text: str,
    ) -> ResumeProfile:

        prompt = f"""
Analyze the following resume.

Resume:

{resume_text}

Return JSON only.
"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        return ResumeProfile(
            **parse_json(response)
        )