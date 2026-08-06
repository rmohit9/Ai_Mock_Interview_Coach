from utils.llm import LLM
from utils.prompt_loader import load_prompt


class InterviewerAgent:
    """
    Conducts the interview by asking adaptive questions.

    Responsibilities:
    - Start the interview
    - Continue the interview
    - Generate one question at a time
    """

    def __init__(self):

        self.llm = LLM()

        self.system_prompt = load_prompt("interviewer.txt")

        self.conversation_history = []

    def start_interview(
        self,
        role: str,
        resume_profile: str,
        focus_area: str,
    ) -> str:

        prompt = f"""
Candidate Role:
{role}

Candidate Resume Profile:
{resume_profile}

Interview Focus:
{focus_area}

Instructions

Instructions

• Read the candidate's resume carefully.

• Introduce yourself in ONE short sentence.

• Ask EXACTLY ONE easy interview question.

• Base the first question on the candidate's strongest project.

• If no projects exist, use technologies.

• If no technologies exist, use skills.

• Never ask multiple questions.

• Never evaluate.

• Never provide hints.

• Maximum 35 words.
"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response

    def continue_interview(
        self,
        answer: str,
        strategy,
        memory,
    ) -> str:

        # Keep local history for compatibility
        self.conversation_history.append(
            {
                "role": "user",
                "content": answer,
            }
        )

        history = memory.conversation_text()

        prompt = f"""
Continue the interview.

Conversation History

{history}

Candidate Resume Profile

{memory.resume_profile}

Topics Covered

{memory.topics_covered}

Weak Topics

{memory.weak_topics}

Strong Topics

{memory.strong_topics}

Interview Progress

Question Number:
{memory.question_count}

Current Difficulty:
{memory.current_difficulty}

Strategy


Action:
{strategy.action}

Difficulty:
{strategy.difficulty}

Next Topic:
{strategy.next_topic}

Question Type:
{strategy.question_type}

Reason:
{strategy.reason}

Rules

• Ask EXACTLY ONE interview question.

• Maximum 30 words.

• Never explain your reasoning.

• Never say "I will simplify."

• Never say "Based on your previous answer."

• Never mention candidate scores.

• Never mention interview strategy.

• Never evaluate the answer.

• Follow the strategy exactly.

• Ask about the topic specified in Next Topic.

• Use the specified Question Type.

• If Question Type is Definition, ask a basic definition.

• If Question Type is Concept, test conceptual understanding.

• If Question Type is Implementation, ask how to implement something.

• If Question Type is Scenario, ask a practical real-world problem.

• If Question Type is Optimization, ask how to improve an existing solution.

• If Question Type is Debugging, ask how to identify or fix an issue.

• Use the candidate's resume whenever possible.

• Do not repeat previous questions.

• Keep the interview conversational and professional.
"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

        self.conversation_history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response

    def get_history(self):

        history = ""

        for message in self.conversation_history:

            history += (
                f"{message['role'].upper()}:\n"
            )

            history += message["content"]

            history += "\n\n"

        return history