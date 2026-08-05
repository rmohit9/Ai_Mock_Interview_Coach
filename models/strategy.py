from pydantic import BaseModel


class Strategy(BaseModel):
    action: str
    reason: str
    difficulty: str