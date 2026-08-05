from typing import List

from pydantic import BaseModel


class InterviewReport(BaseModel):

    overall_score: float

    technical_score: float

    communication_score: float

    confidence_score: float

    depth_score: float

    completeness_score: float

    strengths: List[str]

    weaknesses: List[str]

    recommendations: List[str]

    hiring_recommendation: str

    overall_feedback: str