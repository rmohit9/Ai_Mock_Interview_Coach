from typing import List

from pydantic import BaseModel


class Evaluation(BaseModel):

    technical: int

    communication: int

    confidence: int

    depth: int

    completeness: int

    strengths: List[str]

    weaknesses: List[str]

    suggestions: List[str]