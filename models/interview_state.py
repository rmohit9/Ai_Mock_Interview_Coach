
from typing import List, Dict

from pydantic import BaseModel, Field


class InterviewState(BaseModel):

    role: str

    resume: str

    focus_area: str

    conversation_history: List[Dict] = Field(default_factory=list)

    question_number: int = 0

    difficulty: str = "Medium"

    evaluations: List[Dict] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)

    weaknesses: List[str] = Field(default_factory=list)

    interview_complete: bool = False