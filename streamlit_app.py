import streamlit as st
import streamlit.components.v1 as components

from services.interview_service import InterviewService
from utils.pdf_parser import PDFParser


# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Mock Interview Coach",
    page_icon="🤖",
    layout="wide",
)


# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def scroll_to_top():
    """Scrolls browser window to top on rerun."""
    components.html("<script>window.scrollTo(0, 0);</script>", height=0, width=0)


def format_score(val):
    """Formats numeric value or string to x/10 format safely."""
    if val is None:
        return "N/A"
    val_str = str(val).strip()
    if "/" in val_str:
        return val_str
    try:
        f = float(val_str)
        if f.is_integer():
            return f"{int(f)}/10"
        return f"{f:.1f}/10"
    except Exception:
        return f"{val_str}/10"


def calculate_overall_score(eval_obj):
    """Computes real arithmetic mean of all 6 evaluation categories."""
    if not eval_obj:
        return 0.0
    scores = [
        getattr(eval_obj, "technical", None),
        getattr(eval_obj, "communication", None),
        getattr(eval_obj, "confidence", None),
        getattr(eval_obj, "problem_solving", None),
        getattr(eval_obj, "depth", None),
        getattr(eval_obj, "completeness", None),
    ]
    valid_scores = [s for s in scores if isinstance(s, (int, float))]
    if not valid_scores:
        return 0.0
    return round(sum(valid_scores) / len(valid_scores), 1)


def get_difficulty_color(difficulty):
    diff = str(difficulty).lower()
    if "easy" in diff:
        return "🟢"
    elif "hard" in diff:
        return "🔴"
    return "🟡"  # Medium / Default


# -------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------

defaults = {
    "started": False,
    "finished": False,
    "question": "",
    "question_data": {},
    "user_answer": "",
    "resume_text": "",
    "role": "",
    "focus": "",
    "question_count": 0,
    "questions_history": [],
    "evaluation": None,
    "report": None,
    "next_question": None,
    "next_question_data": {},
    "show_evaluation": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "service" not in st.session_state:
    st.session_state.service = InterviewService()


# -------------------------------------------------------
# Sidebar - Interview Info & Transcript History
# -------------------------------------------------------

with st.sidebar:
    st.header("📋 Session Dashboard")
    if st.session_state.started:
        st.markdown(f"**Target Role:** `{st.session_state.role}`")
        st.markdown(f"**Focus Area:** `{st.session_state.focus}`")
        
        progress_val = min(1.0, max(0.1, st.session_state.question_count / 5.0))
        st.progress(progress_val, text=f"Question {st.session_state.question_count} of ~5")
        
        if st.session_state.report is None:
            if st.button("⏹️ Conclude & Generate Final Report", use_container_width=True):
                with st.spinner("Generating final interview report..."):
                    report = st.session_state.service.end_interview()
                    st.session_state.report = report
                    st.session_state.show_evaluation = True
                    scroll_to_top()
                    st.rerun()

        st.divider()
        st.subheader("📝 Question History")
        if st.session_state.questions_history:
            for item in st.session_state.questions_history:
                q_num = item["q_num"]
                q_score = calculate_overall_score(item.get("evaluation"))
                with st.expander(f"Q{q_num}: {item['question'][:38]}... ({q_score}/10)"):
                    st.markdown(f"**Question:** {item['question']}")
                    st.markdown(f"**Your Answer:** {item['answer']}")
                    st.markdown(f"**Score:** `{q_score}/10`")
        else:
            st.caption("No questions answered yet.")

        st.divider()
        if st.button("🔄 Restart Interview", use_container_width=True):
            restart()
    else:
        st.info("Start a new interview by filling out the setup form on the right.")


# -------------------------------------------------------
# Header Section
# -------------------------------------------------------

col1, col2 = st.columns([5, 2])

with col1:
    st.title("🤖 AI Mock Interview Coach")
    st.caption("AI Powered Multi-Agent Adaptive Interview Platform")

with col2:
    if st.session_state.started:
        st.markdown(f"**Target Role:** `{st.session_state.role}`")
        if st.button("Restart Session", use_container_width=True, key="header_restart"):
            restart()

st.divider()


# -------------------------------------------------------
# Interview Setup Phase
# -------------------------------------------------------

if not st.session_state.started:

    role = st.text_input("Target Role", placeholder="e.g. AI Engineer, Python Backend Developer, Data Scientist")
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    focus = st.selectbox("Interview Focus", ["Technical", "Behavioral", "Mixed"])

    if st.button("Start Interview", use_container_width=True, type="primary"):

        if not role.strip():
            st.error("Please enter target role.")
            st.stop()

        if uploaded_resume is None:
            st.error("Please upload your resume in PDF format.")
            st.stop()

        with st.spinner("Reading Resume..."):
            resume_text = PDFParser.extract_text(uploaded_resume)

        with st.spinner("Analyzing Resume & Generating First Interview Question..."):
            start_res = st.session_state.service.start_interview(
                role, resume_text, focus
            )

            if isinstance(start_res, dict):
                question_str = start_res.get("question", "")
                question_meta = start_res
            else:
                question_str = str(start_res)
                question_meta = {}

        st.session_state.role = role
        st.session_state.focus = focus
        st.session_state.resume_text = resume_text
        st.session_state.question = question_str
        st.session_state.question_data = question_meta
        st.session_state.question_count = 1
        st.session_state.started = True

        scroll_to_top()
        st.rerun()


# -------------------------------------------------------
# Active Interview Phase
# -------------------------------------------------------

else:

    # --- Question & Answer Input View ---
    if not st.session_state.show_evaluation:

        q_data = st.session_state.question_data if isinstance(st.session_state.question_data, dict) else {}
        difficulty = q_data.get("difficulty", "Easy")
        topic = q_data.get("topic", st.session_state.focus)
        category = q_data.get("question_type", q_data.get("category", "Concept"))
        diff_icon = get_difficulty_color(difficulty)

        st.subheader(f"Question {st.session_state.question_count}")

        # Badges row
        b1, b2, b3 = st.columns(3)
        b1.markdown(f"**Difficulty:** {diff_icon} {difficulty.capitalize()}")
        b2.markdown(f"**Topic:** 🏷️ `{topic}`")
        b3.markdown(f"**Category:** 📂 `{category}`")

        st.info(st.session_state.question)
        st.write("")

        answer = st.text_area(
            "Your Answer",
            height=220,
            placeholder="Type your detailed answer here...",
            key="current_answer_input",
        )

        submit = st.button(
            "Submit Answer",
            use_container_width=True,
            type="primary",
            disabled=st.session_state.show_evaluation,
        )

        # Handle Submit
        if submit:
            if not answer.strip():
                st.warning("Please enter your answer before submitting.")
            else:
                st.session_state.user_answer = answer
                with st.spinner("Evaluating your response with AI Evaluator..."):
                    result = st.session_state.service.process_answer(answer)

                st.session_state.evaluation = result.get("evaluation")
                st.session_state.report = result.get("report")
                st.session_state.show_evaluation = True

                # Save history record
                st.session_state.questions_history.append(
                    {
                        "q_num": st.session_state.question_count,
                        "question": st.session_state.question,
                        "answer": answer,
                        "evaluation": st.session_state.evaluation,
                    }
                )

                if result.get("report") is None:
                    next_q_res = result.get("question")
                    next_q_meta = result.get("question_data", {})
                    if isinstance(next_q_res, dict):
                        st.session_state.next_question = next_q_res.get("question", "")
                        st.session_state.next_question_data = next_q_res
                    else:
                        st.session_state.next_question = str(next_q_res) if next_q_res else ""
                        st.session_state.next_question_data = next_q_meta if isinstance(next_q_meta, dict) else {}
                else:
                    st.session_state.next_question = None

                scroll_to_top()
                st.rerun()

    # --- Evaluation & Final Report View ---
    if st.session_state.show_evaluation:

        # If interview is still ongoing, show top navigation button
        if st.session_state.report is None:
            st.info(
                f"✅ **Answer for Question {st.session_state.question_count} evaluated!** "
                f"Review the coach's feedback below, then click **Proceed to Next Question ➜**."
            )
            col_next_1, _ = st.columns([2, 3])
            with col_next_1:
                if st.button("Proceed to Next Question ➜", key="btn_next_top", type="primary", use_container_width=True):
                    st.session_state.question = st.session_state.next_question
                    st.session_state.question_data = st.session_state.next_question_data
                    st.session_state.next_question = None
                    st.session_state.next_question_data = {}
                    st.session_state.question_count += 1
                    st.session_state.show_evaluation = False
                    st.session_state.evaluation = None
                    scroll_to_top()
                    st.rerun()

        # Display previous question & candidate answer
        st.subheader("💡 Context & Your Answer")
        with st.expander("Show Question & Submitted Answer", expanded=True):
            st.markdown(f"**Question {st.session_state.question_count}:** {st.session_state.question}")
            st.markdown(f"**Your Answer:** {st.session_state.user_answer}")

        evaluation = st.session_state.evaluation

        if evaluation:
            st.divider()

            overall_eval_score = calculate_overall_score(evaluation)
            st.markdown(f"### 📊 Question Score: `{format_score(overall_eval_score)}`")
            st.header("Evaluation Breakdowns")

            c1, c2, c3 = st.columns(3)
            c1.metric("Technical", format_score(getattr(evaluation, "technical", None)))
            c2.metric("Communication", format_score(getattr(evaluation, "communication", None)))
            c3.metric("Confidence", format_score(getattr(evaluation, "confidence", None)))

            c4, c5, c6 = st.columns(3)
            c4.metric("Problem Solving", format_score(getattr(evaluation, "problem_solving", None)))
            c5.metric("Depth", format_score(getattr(evaluation, "depth", None)))
            c6.metric("Completeness", format_score(getattr(evaluation, "completeness", None)))

            st.divider()

            left, right = st.columns(2)

            with left:
                st.subheader("Strengths")
                if getattr(evaluation, "strengths", None):
                    for item in evaluation.strengths:
                        st.success(f"✔️ {item}")
                else:
                    st.info("No explicit strengths identified.")

            with right:
                st.subheader("Weaknesses")
                if getattr(evaluation, "weaknesses", None):
                    for item in evaluation.weaknesses:
                        st.error(f"⚠️ {item}")
                else:
                    st.success("No weaknesses identified.")

            st.subheader("Suggestions for Improvement")
            if getattr(evaluation, "suggestions", None):
                for item in evaluation.suggestions:
                    st.info(f"💡 {item}")

            st.divider()

        # --- Next Question Trigger at Bottom ---
        if st.session_state.report is None:

            if st.button(
                f"Proceed to Next Question (Question {st.session_state.question_count + 1}) ➜",
                use_container_width=True,
                type="primary",
                key="btn_next_bottom",
            ):
                with st.spinner("Loading Next Question..."):
                    st.session_state.question = st.session_state.next_question
                    st.session_state.question_data = st.session_state.next_question_data
                    st.session_state.next_question = None
                    st.session_state.next_question_data = {}
                    st.session_state.question_count += 1
                    st.session_state.show_evaluation = False
                    st.session_state.evaluation = None

                scroll_to_top()
                st.rerun()

        # --- Final Report Display ---
        else:

            report = st.session_state.report

            st.divider()
            st.header("🎯 Final Interview Report")

            st.metric(
                "Overall Score",
                format_score(report.overall_score),
            )

            st.divider()

            st.subheader("Candidate Summary")
            st.write(report.candidate_summary)

            st.divider()

            st.subheader("Overall Performance")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Technical", format_score(report.technical_score))
                st.metric("Confidence", format_score(report.confidence_score))
            with c2:
                st.metric("Communication", format_score(report.communication_score))
                st.metric("Problem Solving", format_score(report.problem_solving_score))
            with c3:
                st.metric("Depth", format_score(report.depth_score))
                st.metric("Completeness", format_score(report.completeness_score))

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

            st.divider()

            st.subheader("Recommended Learning Topics")
            if report.recommended_learning_topics:
                for item in report.recommended_learning_topics:
                    st.info(item)

            st.divider()

            st.subheader("Hiring Recommendation")
            recommendation = str(report.hiring_recommendation).lower()
            if "strong" in recommendation or "recommend" in recommendation:
                st.success(report.hiring_recommendation)
            elif "borderline" in recommendation:
                st.warning(report.hiring_recommendation)
            else:
                st.error(report.hiring_recommendation)

            st.divider()

            st.subheader("Final Remarks")
            st.write(report.final_remarks)

            st.divider()

            if st.button("Start New Interview", use_container_width=True, key="report_restart"):
                restart()


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()
st.caption("AI Mock Interview Coach • Multi-Agent System Engine")