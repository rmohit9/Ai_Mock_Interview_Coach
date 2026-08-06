from uuid import uuid4

from langgraph.types import Command

from graphs.workflow import graph
from graphs.state import InterviewState


class InterviewService:

    def __init__(self):

        self.thread_id = None

        self.config = None

        self.interview_finished = False

    def start_interview(
        self,
        role,
        resume,
        focus,
    ):

        self.thread_id = str(uuid4())

        self.config = {
            "configurable": {
                "thread_id": self.thread_id
            }
        }

        state = InterviewState(
            role=role,
            resume=resume,
            focus=focus,
            thread_id=self.thread_id,
        )

        result = graph.invoke(
            state,
            config=self.config,
        )

        interrupt = result["__interrupt__"][0]

        return interrupt.value["question"]

    def process_answer(
        self,
        answer,
    ):

        result = graph.invoke(
            Command(
                resume=answer
            ),
            config=self.config,
        )

        if "__interrupt__" in result:

            interrupt = result["__interrupt__"][0]

            return {
                "question": interrupt.value["question"],
                "evaluation": result.get("evaluation"),
                "strategy": result.get("strategy"),
                "report": None,
            }

        self.interview_finished = True

        return {
            "question": None,
            "evaluation": result.get("evaluation"),
            "strategy": result.get("strategy"),
            "report": result.get("report"),
        }