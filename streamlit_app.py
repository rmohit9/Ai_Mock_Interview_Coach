import streamlit as st
from services.interview_service import InterviewService
from utils.pdf_parser import PDFParser

st.set_page_config(
    page_title="AI Mock Interview Coach",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Mock Interview Coach")
st.markdown("---")

# -------------------------------
# Session State
# -------------------------------

if "service" not in st.session_state:
    st.session_state.service = InterviewService()

if "started" not in st.session_state:
    st.session_state.started = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "finished" not in st.session_state:
    st.session_state.finished = False

# -------------------------------
# Start Interview
# -------------------------------

if not st.session_state.started:

    role = st.text_input("Target Role")

    uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

    focus = st.selectbox(
        "Focus Area",
        [
            "Technical",
            "Behavioral",
            "Mixed"
        ]
    )

    if st.button("Start Interview"):

        if role.strip() == "":
            st.error("Please enter the target role.")
            st.stop()

        resume_text = ""

        if uploaded_resume is not None:
            resume_text = PDFParser.extract_text(uploaded_resume)

        question = st.session_state.service.start_interview(
            role,
            resume_text,
            focus
        )

        st.session_state.question = question
        st.session_state.started = True

        st.rerun()

# -------------------------------
# Interview
# -------------------------------

else:

    st.subheader("Interview Question")

    st.info(st.session_state.question)

    answer = st.text_area(
        "Your Answer",
        height=200
    )

    if st.button("Submit Answer"):

        if answer.strip() == "":
            st.warning("Please enter your answer.")
            st.stop()

        result = st.session_state.service.process_answer(
            answer
        )

        st.divider()

        st.subheader("Evaluation")

        evaluation = result["evaluation"]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Technical",
                evaluation.technical
            )

            st.metric(
                "Communication",
                evaluation.communication
            )

            st.metric(
                "Confidence",
                evaluation.confidence
            )

        with col2:

            st.metric(
                "Depth",
                evaluation.depth
            )

            st.metric(
                "Completeness",
                evaluation.completeness
            )

        st.subheader("Strengths")

        for item in evaluation.strengths:
            st.success(item)

        st.subheader("Weaknesses")

        for item in evaluation.weaknesses:
            st.error(item)

        st.subheader("Suggestions")

        for item in evaluation.suggestions:
            st.info(item)

        st.divider()

        strategy = result["strategy"]

        st.subheader("Strategy Decision")

        st.write(f"### Action: {strategy.action}")

        st.write(f"Difficulty: {strategy.difficulty}")

        st.write(strategy.reason)

        if result["report"] is not None:

            report = result["report"]

            st.divider()

            st.header("Final Interview Report")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Overall Score",
                report.overall_score
            )

            c2.metric(
                "Technical",
                report.technical_score
            )

            c3.metric(
                "Communication",
                report.communication_score
            )

            st.subheader("Strengths")

            for s in report.strengths:
                st.success(s)

            st.subheader("Weaknesses")

            for w in report.weaknesses:
                st.error(w)

            st.subheader("Recommendations")

            for r in report.recommendations:
                st.info(r)

            st.subheader("Hiring Recommendation")

            st.success(report.hiring_recommendation)

            st.subheader("Overall Feedback")

            st.write(report.overall_feedback)

            st.balloons()

            st.session_state.finished = True

        else:

            st.session_state.question = result["question"]

            st.rerun()