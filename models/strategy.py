from pydantic import BaseModel


class Strategy(BaseModel):
    action: str
    difficulty: str
    next_topic: str
    question_type: str
    reason: str