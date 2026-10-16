from services.interview_service import InterviewService

service = InterviewService()

role = input("Target Role: ")
resume = input("Resume Summary: ")
focus = input("Focus Area: ")

print()

question_data = service.start_interview(
    role,
    resume,
    focus,
)

question = question_data.get("question", "") if isinstance(question_data, dict) else str(question_data)
print(question)

while True:

    answer = input("\nYour Answer: ")

    if answer.lower() == "exit":
        print("Interview Ended.")
        break

    result = service.process_answer(answer)

    print("\n========== Evaluation ==========")
    print(result["evaluation"])

    print("\n========== Strategy ==========")
    print(result["strategy"])

    if result["report"] is not None:

        print("\n========== FINAL REPORT ==========\n")
        print(result["report"])

        break

    print("\n========== Next Question ==========")
    print(result["question"])