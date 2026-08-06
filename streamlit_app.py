import streamlit as st

from services.interview_service import InterviewService
from utils.pdf_parser import PDFParser

st.set_page_config(
    page_title="AI Mock Interview Coach",
    page_icon="🤖",
    layout="wide",
)

# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "service" not in st.session_state:
    st.session_state.service = InterviewService()

if "started" not in st.session_state:
    st.session_state.started = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "finished" not in st.session_state:
    st.session_state.finished = False

# -------------------------------------------------------
# Header
# -------------------------------------------------------

col1, col2 = st.columns([6,1])

with col1:

    st.title("🤖 AI Mock Interview Coach")

    st.caption(
        "AI Powered Multi-Agent Interview Platform"
    )

with col2:

    if st.session_state.started:

        if st.button(
            "Restart Interview",
            use_container_width=True,
        ):

            for key in list(st.session_state.keys()):

                del st.session_state[key]

            st.rerun()

st.divider()

# -------------------------------------------------------
# Interview Setup
# -------------------------------------------------------

if not st.session_state.started:

    role = st.text_input(
        "Target Role",
        placeholder="Example: AI Engineer"
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    focus = st.selectbox(
        "Interview Focus",
        [
            "Technical",
            "Behavioral",
            "Mixed"
        ]
    )

    if st.button(
        "Start Interview",
        use_container_width=True,
    ):

        if role.strip() == "":

            st.error(
                "Please enter a target role."
            )

            st.stop()

        if uploaded_resume is None:

            st.error(
                "Please upload your resume."
            )

            st.stop()

        with st.spinner(
            "Reading Resume..."
        ):

            resume_text = PDFParser.extract_text(
                uploaded_resume
            )

        with st.spinner(
            "Analyzing Resume..."
        ):

            question = (
                st.session_state.service.start_interview(
                    role,
                    resume_text,
                    focus,
                )
            )

        st.session_state.question = question

        st.session_state.started = True

        st.rerun()

# -------------------------------------------------------
# Interview Screen
# -------------------------------------------------------

else:
        st.subheader("Interview Question")

        st.info(st.session_state.question)

        st.write("")

        answer = st.text_area(
            "Your Answer",
            height=220,
            placeholder="Type your answer here..."
        )

        col1, col2 = st.columns([3,1])

        with col1:

            submit = st.button(
                "Submit Answer",
                use_container_width=True
            )

        with col2:

            end = st.button(
                "End Interview",
                use_container_width=True
            )

        if end:

            st.session_state.finished = True

            st.success("Interview Ended.")

            st.stop()

        if submit:

            if answer.strip() == "":

                st.warning(
                    "Please enter your answer."
                )

                st.stop()

            with st.spinner(
                "Evaluating your answer..."
            ):

                result = (
                    st.session_state
                    .service
                    .process_answer(answer)
                )

            evaluation = result["evaluation"]

            strategy = result["strategy"]

            st.divider()

            st.header("Evaluation")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Technical",
                evaluation.technical
            )

            c2.metric(
                "Communication",
                evaluation.communication
            )

            c3.metric(
                "Confidence",
                evaluation.confidence
            )

            c4, c5, c6 = st.columns(3)

            c4.metric(
                "Problem Solving",
                evaluation.problem_solving
            )

            c5.metric(
                "Depth",
                evaluation.depth
            )

            c6.metric(
                "Completeness",
                evaluation.completeness
            )

            st.divider()

            left, right = st.columns(2)

            with left:

                st.subheader("Strengths")

                if evaluation.strengths:

                    for item in evaluation.strengths:

                        st.success(item)

                else:

                    st.info(
                        "No strengths identified."
                    )

            with right:

                st.subheader("Weaknesses")

                if evaluation.weaknesses:

                    for item in evaluation.weaknesses:

                        st.error(item)

                else:

                    st.success(
                        "No weaknesses identified."
                    )

            st.subheader("Suggestions")

            if evaluation.suggestions:

                for item in evaluation.suggestions:

                    st.info(item)

            st.divider()

            if result["report"] is None:

                st.divider()

                st.session_state.question = result["question"]

                st.subheader("Next Question")

                st.success(st.session_state.question)

                st.stop()

            else:

                report = result["report"]

                st.divider()

                st.header("🎯 Final Interview Report")

                st.metric(
                    "Overall Score",
                    report.overall_score
                )

                st.divider()

                st.subheader("Candidate Summary")

                st.write(
                    report.candidate_summary
                )

                st.divider()

                st.subheader("Performance")

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Technical",
                        report.technical_score
                    )

                    st.metric(
                        "Confidence",
                        report.confidence_score
                    )

                with c2:

                    st.metric(
                        "Communication",
                        report.communication_score
                    )

                    st.metric(
                        "Problem Solving",
                        report.problem_solving_score
                    )

                with c3:

                    st.metric(
                        "Depth",
                        report.depth_score
                    )

                    st.metric(
                        "Completeness",
                        report.completeness_score
                    )

                st.divider()

                left, right = st.columns(2)

                with left:

                    st.subheader("Strengths")

                    if report.strengths:

                        for item in report.strengths:

                            st.success(item)

                    else:

                        st.info("No strengths available.")

                with right:

                    st.subheader("Weaknesses")

                    if report.weaknesses:

                        for item in report.weaknesses:

                            st.error(item)

                    else:

                        st.success("No weaknesses available.")

                st.divider()

                st.subheader("Improvement Plan")

                if report.improvement_plan:

                    for item in report.improvement_plan:

                        st.info(item)

                else:

                    st.success(
                        "No major improvements required."
                    )

                st.divider()

                st.subheader(
                    "Recommended Learning Topics"
                )

                if report.recommended_learning_topics:

                    for topic in report.recommended_learning_topics:

                        st.info(topic)

                else:

                    st.success(
                        "No additional learning topics."
                    )

                st.divider()

                st.subheader(
                    "Hiring Recommendation"
                )

                recommendation = (
                    report.hiring_recommendation.lower()
                )

                if "strong" in recommendation:

                    st.success(
                        report.hiring_recommendation
                    )

                elif "recommend" in recommendation:

                    st.success(
                        report.hiring_recommendation
                    )

                elif "borderline" in recommendation:

                    st.warning(
                        report.hiring_recommendation
                    )

                else:

                    st.error(
                        report.hiring_recommendation
                    )

                st.divider()

                st.subheader("Final Remarks")

                st.write(
                    report.final_remarks
                )

                st.balloons()

                st.session_state.finished = True

                st.divider()

                if st.button(
                    "Start New Interview",
                    use_container_width=True,
                ):

                    for key in list(
                        st.session_state.keys()
                    ):

                        del st.session_state[key]

                    st.rerun()