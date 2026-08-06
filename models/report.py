from typing import List
from pydantic import BaseModel


class InterviewReport(BaseModel):

    candidate_summary: str

    overall_score: float

    technical_score: float

    communication_score: float

    confidence_score: float

    problem_solving_score: float

    depth_score: float

    completeness_score: float

    strengths: List[str]

    weaknesses: List[str]

    improvement_plan: List[str]

    recommended_learning_topics: List[str]

    hiring_recommendation: str

    final_remarks: str