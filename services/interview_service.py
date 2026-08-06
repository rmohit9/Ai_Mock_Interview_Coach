from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.strategist import StrategyAgent
from agents.coach import CoachAgent
from agents.resume_analyzer import ResumeAnalyzerAgent

from memory.interview_memory import InterviewMemory

from utils.logger import InterviewLogger


class InterviewService:

    def __init__(self):

        self.interviewer = InterviewerAgent()
        self.evaluator = EvaluatorAgent()
        self.strategist = StrategyAgent()
        self.coach = CoachAgent()
        self.resume_analyzer = ResumeAnalyzerAgent()

        self.memory = InterviewMemory()

        self.resume_profile = None

        self.role = ""
        self.resume = ""
        self.focus = ""

        self.current_question = ""

        self.all_evaluations = []

        self.interview_finished = False

    def start_interview(
        self,
        role,
        resume,
        focus,
    ):

        # Reset interview state
        self.memory = InterviewMemory()

        self.all_evaluations = []

        self.interview_finished = False

        self.current_question = ""

        if not resume.strip():

            raise ValueError(
                "Resume text is empty."
            )

        self.role = role
        self.resume = resume
        self.focus = focus

        try:

            self.resume_profile = self.resume_analyzer.analyze(
                resume
            )

        except Exception as e:

            raise Exception(
                f"Resume analysis failed: {str(e)}"
            )

        self.memory.resume_profile = (
            self.resume_profile.model_dump()
        )

        self.current_question = self.interviewer.start_interview(
            role,
            self.resume_profile.model_dump_json(
                indent=4
            ),
            focus,
        )

        self.memory.add_question(
            self.current_question
        )

        return self.current_question

    def process_answer(
        self,
        answer,
    ):

        self.memory.add_answer(
            answer
        )

        evaluation = self.evaluator.evaluate(
            question=self.current_question,
            answer=answer,
            role=self.role,
        )

        self.memory.add_evaluation(
            evaluation.model_dump()
        )

        self.all_evaluations.append(
            evaluation.model_dump()
        )

        strategy = self.strategist.decide(
            evaluation
        )

        self.memory.add_strategy(
            strategy.model_dump()
        )

        if strategy.action == "END_INTERVIEW":

            self.interview_finished = True

            report = self.coach.generate_report(
                role=self.role,
                resume_profile=self.resume_profile.model_dump_json(
                    indent=4
                ),
                history=self.memory.conversation_text(),
                evaluations=self.all_evaluations,
            )

            InterviewLogger.save(
                report.model_dump()
            )

            return {
                "evaluation": evaluation,
                "strategy": strategy,
                "report": report,
                "question": None,
            }

        self.current_question = (
            self.interviewer.continue_interview(
                answer,
                strategy,
                self.memory,
            )
        )

        self.memory.add_question(
            self.current_question
        )

        return {
            "evaluation": evaluation,
            "strategy": strategy,
            "report": None,
            "question": self.current_question,
        }