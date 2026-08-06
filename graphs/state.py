from typing import Optional

from typing_extensions import TypedDict

from models.resume_profile import ResumeProfile
from models.evaluation import Evaluation
from models.strategy import Strategy
from models.report import Report


class InterviewState(TypedDict):

    role: str

    resume: str

    focus: str

    answer: str

    question: str

    resume_profile: Optional[ResumeProfile]

    evaluation: Optional[Evaluation]

    strategy: Optional[Strategy]

    report: Optional[Report]

    interview_finished: bool