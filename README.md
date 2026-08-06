# AI Mock Interview Coach

## Overview

AI Mock Interview Coach is a multi-agent AI interview platform designed to simulate realistic technical interviews. The system analyzes a candidate's resume, conducts an adaptive interview, evaluates each response, dynamically adjusts question difficulty, and generates a comprehensive interview report with actionable feedback.

The application is built using **LangGraph**, **LangChain**, **Mistral AI**, and **Streamlit**, demonstrating a production-oriented multi-agent orchestration architecture.

---

## Features

- Resume analysis and structured profile extraction
- Adaptive AI interviewer
- Dynamic interview strategy based on candidate performance
- Multi-dimensional answer evaluation
- Progressive difficulty adjustment
- Context-aware follow-up questions
- Final interview coaching report
- Human-in-the-loop interview flow using LangGraph interrupts
- Interactive Streamlit interface

---

## Architecture

### Multi-Agent System

The system consists of five specialized AI agents.

### 1. Resume Analyzer Agent

Responsibilities

- Analyze the candidate's resume
- Extract structured candidate information
- Identify projects, technologies and skills
- Recommend interview topics

Output

- ResumeProfile

---

### 2. Interviewer Agent

Responsibilities

- Conduct the interview
- Ask one question at a time
- Adapt questions using the Strategy Agent
- Maintain natural interview flow

Output

- Interview Question

---

### 3. Evaluator Agent

Responsibilities

- Evaluate each candidate answer
- Score multiple interview dimensions
- Identify strengths and weaknesses
- Suggest improvements

Evaluation Dimensions

- Technical Knowledge
- Communication
- Confidence
- Problem Solving
- Depth
- Completeness

Output

- Evaluation

---

### 4. Strategy Agent

Responsibilities

- Decide interview progression
- Increase or decrease difficulty
- Select the next topic
- Decide interview termination

Possible Actions

- ASK_FOLLOW_UP
- INCREASE_DIFFICULTY
- DECREASE_DIFFICULTY
- SWITCH_TOPIC
- END_INTERVIEW

Output

- Strategy

---

### 5. Coach Agent

Responsibilities

- Generate the final interview report
- Summarize interview performance
- Recommend learning topics
- Provide hiring recommendation

Output

- InterviewReport

---

## LangGraph Workflow

```
                Resume
                   │
                   ▼
        Resume Analyzer
                   │
                   ▼
          Interviewer Agent
                   │
                   ▼
      Human Candidate (Interrupt)
                   │
                   ▼
          Evaluator Agent
                   │
                   ▼
           Strategy Agent
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
 Interview Continues     Coach Agent
          │                 │
          └────────┬────────┘
                   ▼
                  END
```

---

## Project Structure

```
AI_Mock_Interview_Coach/
│
├── agents/
│   ├── resume_analyzer.py
│   ├── interviewer.py
│   ├── evaluator.py
│   ├── strategist.py
│   └── coach.py
│
├── graphs/
│   ├── workflow.py
│   └── state.py
│
├── models/
│   ├── resume.py
│   ├── evaluation.py
│   ├── strategy.py
│   └── report.py
│
├── prompts/
│   ├── resume_analyzer.txt
│   ├── interviewer.txt
│   ├── evaluator.txt
│   ├── strategist.txt
│   └── coach.txt
│
├── services/
│   └── interview_service.py
│
├── utils/
│
├── streamlit_app.py
│
├── config.py
│
├── requirements.txt
│
└── README.md
```

---

## Technologies Used

### AI Frameworks

- LangGraph
- LangChain

### LLM

- Mistral AI

### Backend

- Python

### User Interface

- Streamlit

### Data Validation

- Pydantic

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd AI_Mock_Interview_Coach
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
MISTRAL_API_KEY=your_api_key

MODEL_NAME=mistral-medium

TEMPERATURE=0.4

MAX_TOKENS=1024
```

---

## Running the Application

```bash
streamlit run streamlit_app.py
```

---

## Interview Workflow

1. Enter the target job role.
2. Upload or paste resume content.
3. Select interview focus.
4. Resume Analyzer extracts candidate profile.
5. Interview begins with an introductory question.
6. Candidate answers each question.
7. Evaluator scores the response.
8. Strategy Agent determines the next interview action.
9. Interview continues until completion.
10. Coach Agent generates the final interview report.

---

## Design Decisions

### Why LangGraph?

LangGraph enables stateful orchestration with human-in-the-loop interactions, making it well suited for adaptive interview workflows.

### Why Multiple Agents?

Each agent has a single responsibility, making the system modular, maintainable, and easier to extend.

### Why Structured Outputs?

Using structured Pydantic models improves reliability, simplifies validation, and ensures predictable communication between agents.

### Why Strategy Agent?

Separating interview strategy from question generation allows adaptive difficulty adjustment while keeping the interviewer focused solely on asking questions.

---

## Tradeoffs

### Advantages

- Modular architecture
- Easily extensible
- Clear separation of responsibilities
- Adaptive interview progression
- Human-in-the-loop execution
- Maintainable prompt design

### Limitations

- Depends on LLM response quality
- Interview duration varies based on strategy decisions
- Currently supports text-based interviews only

---

## Example Interview Transcript




**Strategy**

Action

INCREASE_DIFFICULTY

---

**Interviewer**

How did you implement document retrieval in your RAG project?

---

## Final Report

The final report includes:

- Candidate Summary
- Overall Score
- Technical Score
- Communication Score
- Confidence Score
- Problem Solving Score
- Depth Score
- Completeness Score
- Strengths
- Weaknesses
- Improvement Plan
- Recommended Learning Topics
- Hiring Recommendation
- Final Remarks

---

## Future Improvements

- Voice-based interviews
- Resume upload using PDF parsing
- Role-specific interview templates
- Interview analytics dashboard
- Persistent interview history
- Database integration
- Authentication
- Cloud deployment
