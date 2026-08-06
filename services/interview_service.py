from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.strategist import StrategyAgent
from agents.coach import CoachAgent
from utils.logger import InterviewLogger
from agents.resume_analyzer import ResumeAnalyzerAgent


class InterviewService:

    def __init__(self):

        self.interviewer = InterviewerAgent()
        self.evaluator = EvaluatorAgent()
        self.strategist = StrategyAgent()
        self.coach = CoachAgent()
        self.resume_analyzer = ResumeAnalyzerAgent()
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

        self.role = role
        self.resume = resume
        self.resume_profile = self.resume_analyzer.analyze(
            resume
        )

        self.focus = focus

        self.current_question = self.interviewer.start_interview(
            role,
            self.resume_profile.model_dump_json(indent=4),
            focus,
        )

        return self.current_question

    def process_answer(
        self,
        answer,
    ):

        evaluation = self.evaluator.evaluate(
            question=self.current_question,
            answer=answer,
            role=self.role,
        )

        self.all_evaluations.append(
            evaluation.model_dump()
        )

        strategy = self.strategist.decide(
            evaluation
        )

        if strategy.action == "END_INTERVIEW":

            self.interview_finished = True

            report = self.coach.generate_report(
                role=self.role,
                resume_profile=self.resume_profile.model_dump_json(indent=4),
                history=self.interviewer.get_history(),
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

        self.current_question = self.interviewer.continue_interview(
            answer,
            strategy,
        )

        return {
            "evaluation": evaluation,
            "strategy": strategy,
            "report": None,
            "question": self.current_question,
        }