from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class InterviewMemory:

    resume_profile: dict = field(default_factory=dict)

    conversation: list = field(default_factory=list)

    evaluations: list = field(default_factory=list)

    strategies: list = field(default_factory=list)

    topics_covered: list = field(default_factory=list)

    weak_topics: list = field(default_factory=list)

    strong_topics: list = field(default_factory=list)

    current_difficulty: str = "Easy"

    question_count: int = 0

    started_at: datetime = field(default_factory=datetime.now)

    def add_question(self, question):

        self.question_count += 1

        self.conversation.append(
            {
                "type": "question",
                "number": self.question_count,
                "content": question,
                "time": datetime.now().isoformat(),
            }
        )

    def add_answer(self, answer):

        self.conversation.append(
            {
                "type": "answer",
                "content": answer,
                "time": datetime.now().isoformat(),
            }
        )

    def add_evaluation(self, evaluation):

        self.evaluations.append(evaluation)

        technical = evaluation["technical"]

        problem = evaluation["problem_solving"]

        if technical <= 4:

            if "Technical Knowledge" not in self.weak_topics:

                self.weak_topics.append(
                    "Technical Knowledge"
                )

        elif technical >= 8:

            if "Technical Knowledge" not in self.strong_topics:

                self.strong_topics.append(
                    "Technical Knowledge"
                )

        if problem <= 4:

            if "Problem Solving" not in self.weak_topics:

                self.weak_topics.append(
                    "Problem Solving"
                )

        elif problem >= 8:

            if "Problem Solving" not in self.strong_topics:

                self.strong_topics.append(
                    "Problem Solving"
                )

    def add_strategy(self, strategy):

        self.current_difficulty = strategy["difficulty"]

        self.strategies.append(strategy)

    def conversation_text(self):

        history = ""

        for item in self.conversation:

            if item["type"] == "question":

                history += (
                    f"Interviewer: {item['content']}\n\n"
                )

            else:

                history += (
                    f"Candidate: {item['content']}\n\n"
                )

        return history

    def interview_progress(self):

        return {
            "question_number": self.question_count,
            "difficulty": self.current_difficulty,
            "weak_topics": self.weak_topics,
            "strong_topics": self.strong_topics,
        }