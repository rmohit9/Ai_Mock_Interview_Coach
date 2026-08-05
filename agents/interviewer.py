from utils.llm import LLM
from utils.prompt_loader import load_prompt


class InterviewerAgent:
    """
    Handles the interview conversation.

    Responsibilities:
    - Start the interview
    - Ask interview questions
    - Maintain conversation history
    """

    def __init__(self):

        self.llm = LLM()

        self.system_prompt = load_prompt("interviewer.txt")

        self.conversation_history = []

    def start_interview(
        self,
        role: str,
        resume: str,
        focus_area: str,
    ) -> str:

        prompt = f"""
Candidate Role:
{role}

Resume Summary:
{resume}

Focus Area:
{focus_area}

Start a realistic interview.

Introduce yourself briefly.

Ask ONLY the first interview question.
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
        candidate_answer: str,
        strategy,
    ) -> str:

        self.conversation_history.append(
            {
                "role": "user",
                "content": candidate_answer,
            }
        )

        history = ""

        for message in self.conversation_history:

            history += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n\n"
            )

        prompt = f"""
        Continue the interview.

        Conversation so far:

        {history}

        Latest Strategy:

        Action: {strategy.action}

        Difficulty: {strategy.difficulty}

        Reason:
        {strategy.reason}

        Follow the strategy exactly.

        If the strategy says:

        - DECREASE_DIFFICULTY -> Ask an easier question.
        - INCREASE_DIFFICULTY -> Ask a harder question.
        - ASK_FOLLOW_UP -> Ask a follow-up on the previous answer.
        - SWITCH_TOPIC -> Change to another relevant topic.
        - END_INTERVIEW -> Do not ask another question.

        Ask ONLY ONE question.
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

        return self.conversation_history