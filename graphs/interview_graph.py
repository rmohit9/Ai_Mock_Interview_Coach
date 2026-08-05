from typing import TypedDict

from langgraph.graph import StateGraph, END

from models.interview_state import InterviewState


class GraphState(TypedDict):

    state: InterviewState