from graphs.state import InterviewState

from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.strategist import StrategyAgent
from agents.coach import CoachAgent


resume_agent = ResumeAnalyzerAgent()

interviewer_agent = InterviewerAgent()

evaluator_agent = EvaluatorAgent()

strategy_agent = StrategyAgent()

coach_agent = CoachAgent()


def resume_node(state: InterviewState):

    profile = resume_agent.analyze(
        state.resume
    )

    state.resume_profile = profile

    return state


def interviewer_node(state: InterviewState):

    if state.current_answer == "":

        question = interviewer_agent.start_interview(

            role=state.role,

            resume_profile=state.resume_profile.model_dump_json(
                indent=4
            ),

            focus_area=state.focus,
        )

    else:

        question = interviewer_agent.continue_interview(

            answer=state.current_answer,

            strategy=state.strategy,

            memory=None,
        )

    state.current_question = question

    return state


def evaluator_node(state: InterviewState):

    evaluation = evaluator_agent.evaluate(

        question=state.current_question,

        answer=state.current_answer,

        role=state.role,
    )

    state.evaluation = evaluation

    return state


def strategy_node(state: InterviewState):

    strategy = strategy_agent.decide(
        state.evaluation
    )

    state.strategy = strategy

    return state


def coach_node(state: InterviewState):

    report = coach_agent.generate_report(

        role=state.role,

        resume_profile=state.resume_profile.model_dump_json(
            indent=4
        ),

        history=interviewer_agent.get_history(),

        evaluations=[
            state.evaluation.model_dump()
        ],
    )

    state.report = report

    state.interview_finished = True

    return state