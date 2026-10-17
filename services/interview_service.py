from uuid import uuid4

from langgraph.types import Command

from graphs.workflow import graph
from graphs.state import InterviewState


class InterviewService:

    def __init__(self):
        self.thread_id = str(uuid4())
        self.config = None
        self.graph = graph
        self.interview_finished = False

    def start_interview(
        self,
        role: str,
        resume: str,
        focus: str,
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

        result = self.graph.invoke(
            state,
            config=self.config,
        )

        if "__interrupt__" in result and len(result["__interrupt__"]) > 0:
            interrupt = result["__interrupt__"][0]
            val = interrupt.value
            return val

        return {
            "question": "Could not generate interview question. Please try again.",
            "difficulty": "Easy",
            "topic": focus,
            "question_type": "Concept",
        }

    def process_answer(
        self,
        answer: str,
    ):
        result = self.graph.invoke(
            Command(
                resume=answer
            ),
            config=self.config,
        )

        if "__interrupt__" in result and len(result["__interrupt__"]) > 0:
            interrupt = result["__interrupt__"][0]
            val = interrupt.value
            question_str = val.get("question", "") if isinstance(val, dict) else str(val)
            question_data = val if isinstance(val, dict) else {}

            return {
                "question": question_str,
                "question_data": question_data,
                "evaluation": result.get("evaluation"),
                "strategy": result.get("strategy"),
                "report": None,
            }

        self.interview_finished = True

        return {
            "question": None,
            "question_data": {},
            "evaluation": result.get("evaluation"),
            "strategy": result.get("strategy"),
            "report": result.get("report"),
        }

    def skip_question(self):
        """Skips the current question by submitting 'Not Answered' as the answer."""
        return self.process_answer("Not Answered")

    def end_interview(self):
        from graphs.workflow import coach_node

        state_snapshot = self.graph.get_state(self.config)
        if not state_snapshot or not state_snapshot.values:
            return None

        state = state_snapshot.values
        if hasattr(state, "strategy") and state.strategy:
            state.strategy.action = "END_INTERVIEW"

        state = coach_node(state)
        return state.report