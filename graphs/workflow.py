from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt


from graphs.state import InterviewState

from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.strategist import StrategyAgent
from agents.coach import CoachAgent

# --------------------------------------------------
# Graph Components
# --------------------------------------------------

builder = StateGraph(InterviewState)
memory = MemorySaver()
evaluator_agent = EvaluatorAgent()
strategy_agent = StrategyAgent()
coach_agent = CoachAgent()


# --------------------------------------------------
# Agents
# --------------------------------------------------

resume_agent = ResumeAnalyzerAgent()

interviewer_agent = InterviewerAgent()


# --------------------------------------------------
# Resume Node
# --------------------------------------------------

def resume_node(state: InterviewState):

    profile = resume_agent.analyze(
        state.resume
    )

    state.resume_profile = profile

    return state


# --------------------------------------------------
# Interviewer Node
# --------------------------------------------------

def interviewer_node(state: InterviewState):

    # First question
    if state.current_question == "":

        question = interviewer_agent.start_interview(

            role=state.role,

            resume_profile=state.resume_profile.model_dump_json(
                indent=4
            ),

            focus_area=state.focus,
        )

    # Remaining questions
    else:

        question = interviewer_agent.continue_interview(

            answer=state.current_answer,

            strategy=state.strategy,

            state=state,
        )

    state.current_question = question

    # Save assistant message
    state.conversation_history.append(
        {
            "role": "assistant",
            "content": question,
        }
    )

    # Pause graph
    answer = interrupt(
        {
            "question": question,
        }
    )

    state.current_answer = answer

    # Save user message
    state.conversation_history.append(
        {
            "role": "user",
            "content": answer,
        }
    )

    return state

def evaluator_node(state: InterviewState):

    evaluation = evaluator_agent.evaluate(
        question=state.current_question,
        answer=state.current_answer,
        role=state.role,
    )

    state.evaluation = evaluation
    state.evaluation_history.append(
    evaluation.model_dump()
    )

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

        history="\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in state.conversation_history
        ),

        evaluations=state.evaluation_history
    )

    state.report = report

    state.interview_finished = True

    return state

def should_continue(state: InterviewState):

    question_count = len(state.evaluation_history)

    # Never end before 5 answered questions
    if question_count < 4:
        return "interviewer"

    # Between 5 and 6 questions,
    # allow the Strategy Agent to decide
    if question_count < 6:

        if state.strategy.action == "END_INTERVIEW":
            return "coach"

        return "interviewer"

    # Hard stop after 7 questions
    return "coach"


# --------------------------------------------------
# Graph
# --------------------------------------------------

builder.add_node(
    "resume",
    resume_node,
)

builder.add_node(
    "interviewer",
    interviewer_node,
)
builder.add_node(
    "evaluator",
    evaluator_node,
)

builder.add_node(
    "strategy",
    strategy_node,
)

builder.add_node(
    "coach",
    coach_node,
)

builder.add_edge(
    START,
    "resume",
)

builder.add_edge(
    "resume",
    "interviewer",
)

builder.add_edge(
    "interviewer",
    "evaluator",
)

builder.add_edge(
    "evaluator",
    "strategy",
)

builder.add_conditional_edges(

    "strategy",

    should_continue,

    {

        "interviewer": "interviewer",

        "coach": "coach",

    },

)

builder.add_edge(
    "coach",
    END,
)
graph = builder.compile(
    checkpointer=memory,
)