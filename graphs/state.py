from typing import Optional
from pydantic import BaseModel, Field

from models.resume import ResumeProfile
from models.evaluation import Evaluation
from models.strategy import Strategy
from models.report import InterviewReport


class InterviewState(BaseModel):

    # -------------------------
    # User Input
    # -------------------------

    role: str = ""
    resume: str = ""
    focus: str = ""

    # -------------------------
    # Runtime
    # -------------------------

    thread_id: str = ""

    current_question: str = ""
    current_answer: str = ""

    # -------------------------
    # Agent Outputs
    # -------------------------

    resume_profile: Optional[ResumeProfile] = None
    evaluation: Optional[Evaluation] = None
    strategy: Optional[Strategy] = None
    report: Optional[InterviewReport] = None

    # -------------------------
    # History
    # -------------------------

    evaluation_history: list = Field(default_factory=list)

    conversation_history: list = Field(default_factory=list)

   
    # -------------------------
    # Interview Status
    # -------------------------

    interview_finished: bool = False