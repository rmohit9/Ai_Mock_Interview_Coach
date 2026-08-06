from typing import List
from pydantic import BaseModel


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""
    gpa: str = ""
    percentage: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    github_url: str = ""


class ResumeProfile(BaseModel):

    candidate_name: str = ""

    experience_level: str = ""

    primary_domain: str = ""

    education: List[Education] = []

    skills: List[str] = []

    projects: List[Project] = []

    technologies: List[str] = []

    strengths: List[str] = []

    weaknesses: List[str] = []

    recommended_interview_topics: List[str] = []