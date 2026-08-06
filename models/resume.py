from typing import List
from pydantic import BaseModel


class ResumeProfile(BaseModel):

    candidate_name: str

    experience_level: str

    education: List[str]

    skills: List[str]

    projects: List[str]

    technologies: List[str]

    strengths: List[str]

    weaknesses: List[str]