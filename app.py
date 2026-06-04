import streamlit as st
import time
import random
import json
import os

st.set_page_config(page_title="Official Shorter GRE Quant Simulator", page_icon="🎓", layout="centered")

# --- ΦΟΡΤΩΣΗ ΕΡΩΤΗΣΕΩΝ ΑΠΟ JSON ---
@st.cache_data
def load_questions():
    filename = "questions_pool.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Φόρτωση των ελεγμένων ερωτήσεων από το JSON σας
RAW_QUESTIONS = load_questions()

# --- ΡΥΘΜΙΣΕΙΣ SHORTER GRE ---
SEC1_COUNT = 12
SEC1_TIME = 21 * 60  # 21 λεπτά

SEC2_COUNT = 15
SEC2_TIME = 26 * 60  # 26 λεπτά

TOTAL_REQUIRED = SEC1_COUNT + SEC2_COUNT  # 27 ερωτήσεις συνολικά

# Μηχανισμός ασφαλείας: Αν το JSON δεν έχει ακόμα 27 ερωτήσεις, συμπληρώνει αυτόματα dummy ερωτήσεις
ALL_QUESTIONS = list(RAW_QUESTIONS)
while len(ALL_QUESTIONS) < TOTAL_REQUIRED:
    current_len = len(ALL_QUESTIONS)
    ALL_QUESTIONS.append({
        "id": f"DUMMY_{current_len}",
        "book": "GRE Question Bank (Placeholder)",
        "type": "MC",
        "question": f"Placeholder Question {current_len}: If $x + 2 = 5$, what is the value of $x$?",
        "choices": ["1", "2", "3", "4", "5"],
        "correct_answer": "3",
        "explanation": "This is a placeholder question because your JSON pool has less than 27 questions. $x = 5 - 2 = 3$."
    })

QC_OPTIONS = [
    "A: Quantity A is greater.",
    "B: Quantity B is greater.",
    "C: The two quantities are equal.",
    "D: The relationship cannot be determined from the information given."
]
QC_KEYS = ["A", "B", "C", "D"]

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE ---
if "initialized" not in st.session_state:
    # Επιλογή τυχαίων ερωτήσεων για όλο το τεστ (12 για το Sec1 και 15 για το Sec2)
    sampled = random.sample(ALL_QUESTIONS, TOTAL_REQUIRED)
    st.session_state.sec1_questions = sampled[:SEC1_COUNT]
    st.session_state.sec2_questions = sampled[SEC1_COUNT:]
    
    st.session_state.current_section = 1  # 1 ή 2 ή "FINISHED"
    st.session_state.current_index = 0
    st.session_state.sec1_answers = {}
    st.session_state.sec2_answers = {}
    st.session_state.section_start_time = time.time()
    st.session_state.initialized = True

# --- ΔΙΑΧΕΙΡΙΣΗ ΧΡΟΝΟΥ ΑΝΑ SECTION ---
if st.session_state.current_section != "FINISHED":
    limit = SEC1_TIME if st.session_state.current_section == 1 else SEC2_TIME
    elapsed = time.time() - st.session_state.section_start_time
    remaining = max(0, limit - int(elapsed))
    
    # Αν λήξει ο χρόνος του Section
    if remaining == 0:
        if st.session_state.current_section == 1:
            st.session_state.current_section = 2
            st.session_state.current_index = 0
            st.session_state.section_start_time = time.time()
            st.toast("⏱️ Section 1 time is up! Moving to Section 2.")
            st.rerun()
        else:
            st.session_state.current_section = "FINISHED"
            st.rerun()
else:
    remaining = 0

# --- SIDEBAR ΠΛΟΗΓΗΣΗΣ ---
st.sidebar.title("Shorter GRE Quant")

if st.session_state.current_section != "FINISHED":
    st.sidebar.markdown(f"### **🗂️ Section {st.session_state.current_section}**")
    mins, secs = divmod(remaining, 60)
    st.sidebar.metric(label="⏱️ Time Remaining", value=f"{mins:02d}:{secs:02d}")
    
    # Επιλογή ενεργού σετ ερωτήσεων και απαντήσεων ανάλογα με το Section
    questions = st.session_state.sec1_questions if st.session_state.current_section == 1 else st.session_state.sec2_questions
    answers = st.session_state.sec1_answers if st.session_state.current_section == 1 else st.session_state.sec2_answers
    
    st.sidebar.subheader("Review/Navigate")
    for i in range(len(questions)):
        status = "✅" if i in answers else "⚪"
        if st.sidebar.button(f"{status} Question {i+1}", key=f"nav_{i}"):
            st.session_state.current_index = i
            st.rerun()
            
    st.sidebar.divider()
    if st.session_state.current_section == 1:
        if st.sidebar.button("➡️ Submit Section 1", use_container_width=True, type="secondary"):
            st.session_state.current_section = 2
            st.session_state.current_index = 0
            st.session_state.section_start_time = time.time()
            st.rerun()
    else:
        if st.sidebar.button("🚨 Final Test Submit", use_container_width=True, type="primary"):
            st.session_state.current_section = "FINISHED"
            st.rerun()

# --- ΚΥΡΙΩΣ ΟΘΟΝΗ ΕΞΕΤΑΣΗΣ ---
if st.session_state.current_section != "FINISHED":
    questions = st.session_state.sec1_questions if st.session_state.current_section == 1 else st.session_state.sec2_questions
    answers = st.session_state.sec1_answers if st.session_state.current_section == 1 else st.session_state.sec2_answers
    
    current_q = questions[st.session_state.current_index]
    
    st.subheader(f"Section {st.session_state.current_section} — Question {st.session_state.current_index + 1} of {len(questions)}")
    st.caption(f"Source: {current_q['book']} | ID: {current_q['id']}")
    st.divider()
    
    # --- ΠΡΟΒΟΛΗ ΑΝΑΛΟΓΑ ΜΕ ΤΟΝ ΤΥΠΟ ΕΡΩΤΗΣΗΣ ---
    if current_q["type"] == "QC":
        st.markdown(current_q["context"])
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Quantity A**\n\n### {current_q['quantity_a']}")
        with col2:
            st.success(f"**Quantity B**\n\n### {current_q['quantity_b']}")
            
        prev_ans = answers.get(st.session_state.current_index, None)
        default_idx = QC_KEYS.index(prev_ans) if prev_ans in QC_KEYS else None
        
        user_choice = st.radio("Select your answer:", QC_OPTIONS, index=default_idx, key=f"q_{st.session_state.current_section}_{st.session_state.current_index}")
        if user_choice:
            answers[st.session_state.current_index] = QC_KEYS[QC_OPTIONS.index(user_choice)]

    elif current_q["type"] == "MC":
        st.markdown(current_q["question"])
        prev_ans = answers.get(st.session_state.current_index, None)
        default_idx = current_q["choices"].index(prev_ans) if prev_ans in current_q["choices"] else None
        
        user_choice = st.radio("Select one option:", current_q["choices"], index=default_idx, key=f"q_{st.session_state.current_section}_{st.session_state.current_index}")
        if user_choice:
            answers[st.session_state.current_index] = user_choice

    elif current_q["type"] == "NE":
        st.markdown(current_q["question"])
        prev_ans = answers.get(st.session_state.current_index, "")
        
        user_choice = st.text_input("Enter numeric value:", value=prev_ans, key=f"q_{st.session_state.current_section}_{st.session_state.current_index}")
        if user_choice:
            answers[st.session_state.current_index] = user_choice.strip()

    # Μπάρα πλοήγησης στο κάτω μέρος
    st.divider()
    c_prev, _, c_next = st.columns()
    with c_prev:
        if st.session_state.current_index > 0:
            if st.button("⬅️ Back"):
                st.session_state.current_index -= 1
                st.rerun()
    with c_next:
        if st.session_state.current_index < len(questions) - 1:
            if st.button("Next ➡️"):
                st.session_state.current_index += 1
                st.rerun()

# --- ΟΘΟΝΗ ΤΕΛΙΚΩΝ ΑΠΟΤΕΛΕΣΜΑΤΩΝ (130 - 170 SCALE) ---
else:
    st.title("🏁 Official GRE Score Report")
    st.divider()
    
    # Υπολογισμός σωστών απαντήσεων
    sec1_correct = sum(1 for i, q in enumerate(st.session_state.sec1_questions) if st.session_state.sec1_answers.get(i) == q["correct_answer"])
    sec2_correct = sum(1 for i, q in enumerate(st.session_state.sec2_questions) if st.session_state.sec2_answers.get(i) == q["correct_answer"])
    
    total_raw_score = sec1_correct + sec2_correct
    max_raw_score = SEC1_COUNT + SEC2_COUNT  # 27
    
    # Υπολογισμός επίσημης κλίμακας GRE (130 - 170)
    final_scaled_score = 130 + int(round((total_raw_score / max_raw_score) * 40))
    
    st.markdown("### Your Performance")
    col_score, col_raw = st.columns(2)
    with col_score:
        st.metric(label="📊 GRE Quant Scaled Score", value=f"{final_scaled_score} / 170")
    with col_raw:
        st.metric(label="🎯 Total Correct Answers", value=f"{total_raw_score} / {max_raw_score}")
        
    st.progress((final_scaled_score - 130) / 40)
    
    # Αναλυτική ανασκόπηση
    st.subheader("Review Sections")
    tab1, tab2 = st.tabs(["Section 1 (12 Qs)", "Section 2 (15 Qs)"])
    
    with tab1:
        for i, q in enumerate(st.session_state.sec1_questions):
            user_ans = st.session_state.sec1_answers.get(i, "Not Answered")
            is_correct = user_ans == q["correct_answer"]
            with st.expander(f"Question {i+1} — {'✅ Correct' if is_correct else '❌ Incorrect'}"):
                st.markdown(q.get("question", q.get("context", "")))
                if q["type"] == "QC":
                    st.write(f"**Quantity A:** {q['quantity_a']} | **Quantity B:** {q['quantity_b']}")
                st.write(f"Your Answer: `{user_ans}` | Correct Answer: `{q['correct_answer']}`")
                st.info(f"**Explanation:** {q['explanation']}")
                
    with tab2:
        for i, q in enumerate(st.session_state.sec2_questions):
            user_ans = st.session_state.sec2_answers.get(i, "Not Answered")
            is_correct = user_ans == q["correct_answer"]
            with st.expander(f"Question {i+1} — {'✅ Correct' if is_correct else '❌ Incorrect'}"):
                st.markdown(q.get("question", q.get("context", "")))
                if q["type"] == "QC":
                    st.write(f"**Quantity A:** {q['quantity_a']} | **Quantity B:** {q['quantity_b']}")
                st.write(f"Your Answer: `{user_ans}` | Correct Answer: `{q['correct_answer']}`")
                st.info(f"**Explanation:** {q['explanation']}")

    if st.button("🔄 Start New Simulation"):
        st.session_state.clear()
        st.rerun()
