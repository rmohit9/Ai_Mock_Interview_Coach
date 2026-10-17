from typing import List, Optional
from pydantic import BaseModel


class Evaluation(BaseModel):

    technical: int

    communication: int

    confidence: int

    problem_solving: int

    depth: int

    completeness: int

    strengths: List[str]

    weaknesses: List[str]

    suggestions: List[str]

    # True when the candidate skipped the question (no LLM evaluation)
    skipped: bool = False