from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.strategist import StrategyAgent
from agents.coach import CoachAgent

interviewer = InterviewerAgent()
evaluator = EvaluatorAgent()
strategist = StrategyAgent()
coach = CoachAgent()

role = input("Target Role: ")
resume = input("Resume Summary: ")
focus = input("Focus Area: ")

print()

question = interviewer.start_interview(
    role,
    resume,
    focus,
)

print(question)

all_evaluations = []

while True:

    answer = input("\nYour Answer: ")

    if answer.lower() == "exit":
        print("\nInterview Ended.")
        break

    evaluation = evaluator.evaluate(
        question=question,
        answer=answer,
        role=role,
    )

    all_evaluations.append(
        evaluation.model_dump()
    )

    print("\n========== Evaluation ==========")
    print(evaluation)

    strategy = strategist.decide(evaluation)

    print("\n========== Strategy ==========")
    print(strategy)

    if strategy.action == "END_INTERVIEW":
        print("\nInterview Finished.")
        break

    question = interviewer.continue_interview(
        answer=answer,
        strategy=strategy,
    )

    print("\n========== Next Question ==========")
    print(question)


report = coach.generate_report(
    role=role,
    history=interviewer.get_history(),
    evaluations=all_evaluations,
)

print("\n========== FINAL REPORT ==========\n")
print(report)