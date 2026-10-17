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

        # Questions are max 30 words — cap tokens low for faster responses
        self.llm = LLM(max_tokens=400)

        self.system_prompt = load_prompt("interviewer.txt")

        self.conversation_history = []

    def reset(self):
        self.conversation_history = []

    def start_interview(
        self,
        role: str,
        resume_profile: str,
        focus_area: str,
        ) -> str:
        self.reset()

        prompt = f"""
Candidate Role:
{role}

Candidate Resume Profile:
{resume_profile}

Interview Focus:
{focus_area}

Instructions

Read the candidate's resume carefully.

Identify the strongest technology or programming language from the resume.

Introduce yourself in ONE short sentence.

Start the interview with ONE EASY question not just the generic chatgpt text like: Hello , it's great to have you here. I'll be conducting your technical interview today. Let's begin with a foundational question ask actual questions based on the candidate's resume and the strongest technology or programming language identified.

The first question should assess basic understanding.

Never start with:

• Project architecture

• Optimization

• System Design

• Scalability

• Debugging

Preferred order for the first question:

1. Programming Language

2. Framework

3. Database

4. AI/ML Concept

5. Project Purpose

Examples

Good

"What is Python?"

"What is Flask?"

"What is REST API?"

"What is Machine Learning?"

"What problem does your RAG chatbot solve?"

Bad

"Explain the architecture of your chatbot."

"How would you optimize retrieval latency?"

"Design a scalable backend."

Rules

Ask EXACTLY ONE question.

Maximum 30 words.

Never evaluate.

Never explain.

Never provide hints.

Never ask multiple questions.

Return ONLY the interview question.
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
        state,
    ) -> str:

        # Save latest user answer
        self.conversation_history.append(
            {
                "role": "user",
                "content": answer,
            }
        )

        # Build conversation history from LangGraph state
        history = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in state.conversation_history
        )

        prompt = f"""
Continue the interview.

Conversation History

{history}

Candidate Resume Profile

{state.resume_profile.model_dump_json(indent=4)}

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

Interview Progress Rules

The strategy has already decided:

• Topic

• Difficulty

• Question Type

You must strictly follow them.

Question progression must feel natural.

Easy:
Definition → Concept

Medium:
Implementation → Practical Usage

Hard:
Scenario → Optimization → Debugging

Never jump directly from Definition to Optimization.

Never ask architecture before implementation.

Never switch topics unless the strategy explicitly changes the topic.

If the strategy says DECREASE_DIFFICULTY:

Ask a simpler question about the SAME topic.

If the strategy says INCREASE_DIFFICULTY:

Ask a more advanced question about the SAME topic.

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

            history += f"{message['role'].upper()}:\n"
            history += message["content"]
            history += "\n\n"

        return history