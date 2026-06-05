import streamlit as st
import json
import time
import random
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="GRE Quant Simulator", page_icon="🎓", layout="centered")

SEC1_COUNT = 12
SEC2_COUNT = 15
SEC1_TIME = 21 * 60
SEC2_TIME = 26 * 60

QC_OPTIONS = {
    "A": "Quantity A is greater.",
    "B": "Quantity B is greater.",
    "C": "The two quantities are equal.",
    "D": "The relationship cannot be determined."
}

@st.cache_data
def load_questions():
    path = Path(__file__).parent / "questions_pool.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def initialize_exam():
    questions = load_questions()
    total = SEC1_COUNT + SEC2_COUNT

    if len(questions) < total:
        raise ValueError(f"Need at least {total} questions. Found {len(questions)}")

    rng = random.Random(random.randint(1, 999999))
    sampled = rng.sample(questions, total)

    st.session_state.update({
        "initialized": True,
        "app_mode": "MENU",
        "current_section": 1,
        "current_index": 0,
        "section_start_time": time.time(),
        "sec1_questions": sampled[:SEC1_COUNT],
        "sec2_questions": sampled[SEC1_COUNT:],
        "sec1_answers": {},
        "sec2_answers": {},
        "flagged": set()
    })

def get_questions():
    return st.session_state.sec1_questions if st.session_state.current_section == 1 else st.session_state.sec2_questions

def get_answers():
    return st.session_state.sec1_answers if st.session_state.current_section == 1 else st.session_state.sec2_answers

def get_remaining():
    limit = SEC1_TIME if st.session_state.current_section == 1 else SEC2_TIME
    elapsed = int(time.time() - st.session_state.section_start_time)
    return max(0, limit - elapsed)

def save_answer(value):
    get_answers()[st.session_state.current_index] = value

def render_qc(q):
    if q.get("svg_diagram"):
        st.components.v1.html(q["svg_diagram"], height=300)

    if q.get("context"):
        st.markdown(q["context"])

    c1, c2 = st.columns(2)
    with c1:
        st.info(q.get("quantity_a", ""))
    with c2:
        st.info(q.get("quantity_b", ""))

    current = get_answers().get(st.session_state.current_index, "A")
    choice = st.radio(
        "Select answer",
        list(QC_OPTIONS.keys()),
        index=list(QC_OPTIONS.keys()).index(current) if current in QC_OPTIONS else 0,
        format_func=lambda x: QC_OPTIONS[x]
    )
    save_answer(choice)

def render_mc(q):
    opts = q.get("options") or q.get("choices") or []
    prev = get_answers().get(st.session_state.current_index)

    idx = opts.index(prev) if prev in opts else 0

    choice = st.radio("Select one answer", opts, index=idx)
    save_answer(choice)

def render_ms(q):
    opts = q.get("options") or q.get("choices") or []
    prev = get_answers().get(st.session_state.current_index, [])

    selected = []
    for opt in opts:
        checked = opt in prev
        if st.checkbox(opt, value=checked, key=f"ms_{st.session_state.current_index}_{opt}"):
            selected.append(opt)

    save_answer(selected)

def render_ne(q):
    prev = get_answers().get(st.session_state.current_index, "")
    value = st.text_input("Enter numeric answer", value=str(prev))
    save_answer(value.strip())

def render_question(q):
    qtype = q.get("question_type") or q.get("type")

    st.caption(f"Source: {q.get('book','Unknown')} | ID: {q.get('id','N/A')}")

    if qtype in ["quantitative_comparison", "QC"]:
        render_qc(q)

    elif qtype in ["multiple_selection", "MS"]:
        if q.get("question"):
            st.markdown(q["question"])
        render_ms(q)

    elif qtype in ["numeric_entry", "NE"]:
        st.markdown(q.get("question") or q.get("text") or "")
        render_ne(q)

    else:
        st.markdown(q.get("question") or q.get("text") or q.get("context") or "")
        if q.get("svg_diagram"):
            st.components.v1.html(q["svg_diagram"], height=300)
        render_mc(q)

def is_correct(user, correct):
    if isinstance(correct, list):
        return set(user) == set(correct)
    return str(user).strip() == str(correct).strip()

def calculate_results():
    s1 = sum(
        is_correct(st.session_state.sec1_answers.get(i), q.get("correct_answer"))
        for i, q in enumerate(st.session_state.sec1_questions)
    )

    s2 = sum(
        is_correct(st.session_state.sec2_answers.get(i), q.get("correct_answer"))
        for i, q in enumerate(st.session_state.sec2_questions)
    )

    raw = s1 + s2
    total = SEC1_COUNT + SEC2_COUNT
    scaled = 130 + round((raw / total) * 40)

    return s1, s2, raw, scaled
def build_review():
    review = []

    for section_name, questions, answers in [
        (
            "Section 1",
            st.session_state.sec1_questions,
            st.session_state.sec1_answers
        ),
        (
            "Section 2",
            st.session_state.sec2_questions,
            st.session_state.sec2_answers
        )
    ]:

        for i, q in enumerate(questions):

            user_answer = answers.get(i)

            correct_answer = q.get("correct_answer")

            correct = is_correct(
                user_answer,
                correct_answer
            )

            review.append({
                "section": section_name,
                "number": i + 1,
                "question": q,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "correct": correct
            })

    return review
def render_sidebar():
    remaining = get_remaining()

    mins, secs = divmod(remaining, 60)

    st.sidebar.metric("⏱️ Time Remaining", f"{mins:02d}:{secs:02d}")

    questions = get_questions()
    answers = get_answers()

    st.sidebar.subheader("Questions")

    for i in range(len(questions)):
        flag = "🚩" if i in st.session_state.flagged else ""
        status = "✅" if i in answers else "⚪"

        if st.sidebar.button(f"{status} {flag} Q{i+1}", key=f"nav_{i}"):
            st.session_state.current_index = i
            st.rerun()

def advance_section():
    if st.session_state.current_section == 1:
        st.session_state.current_section = 2
        st.session_state.current_index = 0
        st.session_state.section_start_time = time.time()
    else:
        st.session_state.current_section = "FINISHED"

    st.rerun()

def render_exam():
    st_autorefresh(interval=1000, key="timer")

    if get_remaining() == 0:
        advance_section()

    render_sidebar()

    questions = get_questions()
    idx = st.session_state.current_index
    q = questions[idx]

    st.subheader(
        f"Section {st.session_state.current_section} - Question {idx + 1} of {len(questions)}"
    )

    render_question(q)

    st.divider()

    if st.button("🚩 Flag / Unflag"):
        if idx in st.session_state.flagged:
            st.session_state.flagged.remove(idx)
        else:
            st.session_state.flagged.add(idx)
        st.rerun()

    c1, c2, c3 = st.columns(3)

    with c1:
        if idx > 0 and st.button("⬅️ Previous"):
            st.session_state.current_index -= 1
            st.rerun()

    with c3:
        if idx < len(questions) - 1:
            if st.button("Next ➡️"):
                st.session_state.current_index += 1
                st.rerun()
        else:
            label = "Go to Section 2 🚀" if st.session_state.current_section == 1 else "🏁 Finish Exam"
            if st.button(label):
                advance_section()

def render_results():
    s1, s2, raw, scaled = calculate_results()

    st.title("🏁 GRE Score Report")

    a, b = st.columns(2)

    with a:
        st.metric("Scaled Score", f"{scaled}/170")

    with b:
        st.metric("Correct Answers", raw)

    st.progress((scaled - 130) / 40)
    st.divider()

    st.subheader("Question Review")

    review = build_review()

    show_all = st.checkbox(
        "Show correct questions too",
        value=False
    )
    for item in review:

        if not show_all and item["correct"]:
            continue

        q = item["question"]

        icon = "✅" if item["correct"] else "❌"

        with st.expander(
            f"{icon} {item['section']} - Question {item['number']}"
        ):

            st.write(
                f"Your Answer: {item['user_answer']}"
            )

            st.write(
                f"Correct Answer: {item['correct_answer']}"
            )

            if q.get("question"):
                st.markdown(q["question"])

            if q.get("context"):
                st.markdown(q["context"])

            if q.get("svg_diagram"):
                st.components.v1.html(
                    q["svg_diagram"],
                    height=300
                )

            if q.get("explanation"):
                st.info(q["explanation"])
    st.divider()

    if st.button("🔄 New Simulation"):
        st.session_state.clear()
        st.rerun()

if "initialized" not in st.session_state:
    initialize_exam()

if st.session_state.app_mode == "MENU":
    st.title("🎯 GRE Quant Simulator")

    if st.button("🚀 Start Quant Simulation", use_container_width=True):
        st.session_state.app_mode = "EXAM"
        st.session_state.section_start_time = time.time()
        st.rerun()

    st.stop()

if st.session_state.current_section == "FINISHED":
    render_results()
else:
    render_exam()
