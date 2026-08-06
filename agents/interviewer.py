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
        resume_profile: str,
        focus_area: str,
    ) -> str:

        prompt = f"""
    Candidate Role:
    {role}

    Candidate Resume Profile:

    {resume_profile}

    Focus Area:
    {focus_area}

    Instructions:

    1. Read the resume profile carefully.
    2. Ask questions based on the candidate's projects.
    3. Ask questions based on the candidate's skills.
    4. Ask questions based on technologies mentioned.
    5. Start with an easy question.
    6. Ask ONLY one question.
    7. Do not evaluate.
    8. Do not provide hints.

    Introduce yourself briefly and ask the first interview question.
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
    ) -> str:

        self.conversation_history.append(
            {
                "role": "user",
                "content": answer,
            }
        )

        history = ""

        for msg in self.conversation_history:

            history += (
                f"{msg['role'].upper()}: "
                f"{msg['content']}\n\n"
            )

        prompt = f"""
    Continue the interview.

    Conversation:

    {history}

    Strategy Decision

    Action:
    {strategy.action}

    Difficulty:
    {strategy.difficulty}

    Reason:
    {strategy.reason}

    Rules:

    If action is ASK_FOLLOW_UP:
    Ask a follow-up.

    If action is INCREASE_DIFFICULTY:
    Ask a harder question.

    If action is DECREASE_DIFFICULTY:
    Ask an easier question.

    If action is SWITCH_TOPIC:
    Move to another skill/project.

    Ask ONLY one interview question.
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