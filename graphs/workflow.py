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
# Graph Components & Shared Agents
# --------------------------------------------------

builder = StateGraph(InterviewState)
memory = MemorySaver()

resume_agent = ResumeAnalyzerAgent()
interviewer_agent = InterviewerAgent()
evaluator_agent = EvaluatorAgent()
strategy_agent = StrategyAgent()
coach_agent = CoachAgent()


# --------------------------------------------------
# Resume Node
# --------------------------------------------------

def resume_node(state: InterviewState):
    profile = resume_agent.analyze(state.resume)
    state.resume_profile = profile
    return state


# --------------------------------------------------
# Generate Question Node
# --------------------------------------------------

def generate_question_node(state: InterviewState):
    """Generates the next interview question without interrupting."""
    # First question of interview
    if state.question_count == 0:
        question = interviewer_agent.start_interview(
            role=state.role,
            resume_profile=state.resume_profile.model_dump_json(indent=4) if state.resume_profile else "",
            focus_area=state.focus,
        )
    else:
        question = interviewer_agent.continue_interview(
            answer=state.current_answer,
            strategy=state.strategy,
            state=state,
        )

    state.current_question = question
    state.question_count += 1

    # Record interviewer turn in state
    state.conversation_history.append(
        {
            "role": "assistant",
            "content": question,
        }
    )

    return state


# --------------------------------------------------
# Wait For Answer Node (Interrupt Point)
# --------------------------------------------------

def wait_for_answer_node(state: InterviewState):
    """
    Interrupts the graph to yield the question to the candidate
    and awaits the user's answer. When resumed, question is NOT regenerated.
    """
    topic = state.strategy.next_topic if state.strategy else state.focus
    difficulty = state.strategy.difficulty if state.strategy else "Easy"
    question_type = state.strategy.question_type if state.strategy else "Concept"

    answer = interrupt(
        {
            "question": state.current_question,
            "question_count": state.question_count,
            "topic": topic,
            "difficulty": difficulty,
            "question_type": question_type,
        }
    )

    state.current_answer = answer

    # Record candidate turn in state
    state.conversation_history.append(
        {
            "role": "user",
            "content": answer,
        }
    )

    return state


# --------------------------------------------------
# Evaluator Node
# --------------------------------------------------

def evaluator_node(state: InterviewState):
    evaluation = evaluator_agent.evaluate(
        question=state.current_question,
        answer=state.current_answer,
        role=state.role,
    )

    state.evaluation = evaluation
    state.evaluation_history.append(evaluation.model_dump())

    return state


# --------------------------------------------------
# Skip Node (fast-path — no LLM calls)
# --------------------------------------------------

def skip_node(state: InterviewState):
    """
    Records a skipped question without calling any LLM.
    Appends a sentinel entry to evaluation_history so question_count
    stays consistent for the should_continue router.
    """
    from models.evaluation import Evaluation
    from models.strategy import Strategy

    skipped_eval = Evaluation(
        technical=0,
        communication=0,
        confidence=0,
        problem_solving=0,
        depth=0,
        completeness=0,
        strengths=[],
        weaknesses=["Question skipped"],
        suggestions=["Attempt this type of question in future interviews."],
        skipped=True,
    )
    state.evaluation = skipped_eval
    state.evaluation_history.append(skipped_eval.model_dump())
    state.skipped = False  # Reset flag for next question

    # Ensure a valid strategy exists so continue_interview never gets None
    if state.strategy is None:
        state.strategy = Strategy(
            action="CONTINUE",
            difficulty="Easy",
            next_topic=state.focus,
            question_type="Concept",
            reason="Candidate skipped previous question; continuing at easy difficulty.",
        )

    return state


# --------------------------------------------------
# Strategy Node
# --------------------------------------------------

def strategy_node(state: InterviewState):
    strategy = strategy_agent.decide(state.evaluation)
    state.strategy = strategy
    return state


# --------------------------------------------------
# Route after answer: skip fast-path vs normal eval
# --------------------------------------------------

def route_after_answer(state: InterviewState):
    """Routes to skip_node (no LLM) or evaluator based on skipped flag."""
    if state.skipped:
        return "skip"
    return "evaluator"


# --------------------------------------------------
# Coach Node
# --------------------------------------------------

def coach_node(state: InterviewState):
    report = coach_agent.generate_report(
        role=state.role,
        resume_profile=state.resume_profile.model_dump_json(indent=4) if state.resume_profile else "",
        history="\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in state.conversation_history
        ),
        evaluations=state.evaluation_history,
    )

    state.report = report
    state.interview_finished = True

    return state


# --------------------------------------------------
# Conditional Routing
# --------------------------------------------------

def should_continue(state: InterviewState):
    question_count = len(state.evaluation_history)

    # Must ask at least 4 questions
    if question_count < 4:
        return "generate_question"

    # Between 4 and 6 questions, allow the Strategy Agent to decide
    if question_count < 6:
        if state.strategy and state.strategy.action == "END_INTERVIEW":
            return "coach"
        return "generate_question"

    # Hard stop after 6 answered questions
    return "coach"


# --------------------------------------------------
# Graph Construction
# --------------------------------------------------

builder.add_node("resume", resume_node)
builder.add_node("generate_question", generate_question_node)
builder.add_node("wait_for_answer", wait_for_answer_node)
builder.add_node("evaluator", evaluator_node)
builder.add_node("skip", skip_node)
builder.add_node("strategy", strategy_node)
builder.add_node("coach", coach_node)

builder.add_edge(START, "resume")
builder.add_edge("resume", "generate_question")
builder.add_edge("generate_question", "wait_for_answer")

# After the candidate responds, route to skip fast-path or normal evaluator
builder.add_conditional_edges(
    "wait_for_answer",
    route_after_answer,
    {
        "evaluator": "evaluator",
        "skip": "skip",
    },
)

builder.add_edge("evaluator", "strategy")

# Skipped questions keep the previous strategy and go straight to next question
builder.add_conditional_edges(
    "skip",
    should_continue,
    {
        "generate_question": "generate_question",
        "coach": "coach",
    },
)

builder.add_conditional_edges(
    "strategy",
    should_continue,
    {
        "generate_question": "generate_question",
        "coach": "coach",
    },
)

builder.add_edge("coach", END)

graph = builder.compile(
    checkpointer=memory,
)