import streamlit as st
import time
import random
from questions_pool import ALL_QUESTIONS  # Εισαγωγή της βάσης ερωτήσεων

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="GRE Quant Random Simulator", page_icon="🧮", layout="centered")

# Πόσες ερωτήσεις θέλετε να έχει κάθε τυχαίο τεστ; (Το επίσημο GRE έχει 20)
NUM_TEST_QUESTIONS = 5 

# --- ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE ---
if "test_questions" not in st.session_state:
    # Επιλογή τυχαίων ερωτήσεων χωρίς επαναλήψεις από το pool
    if len(ALL_QUESTIONS) >= NUM_TEST_QUESTIONS:
        st.session_state.test_questions = random.sample(ALL_QUESTIONS, NUM_TEST_QUESTIONS)
    else:
        st.session_state.test_questions = ALL_QUESTIONS
        
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "test_submitted" not in st.session_state:
    st.session_state.test_submitted = False

# Σταθερές επιλογές για Quantitative Comparison (QC)
QC_OPTIONS = [
    "A: Η ποσότητα Α είναι μεγαλύτερη (Quantity A is greater).",
    "B: Η ποσότητα Β είναι μεγαλύτερη (Quantity B is greater).",
    "C: Οι δύο ποσότητες είναι ίσες (The two quantities are equal).",
    "D: Η σχέση δεν μπορεί να προσδιοριστεί (The relationship cannot be determined)."
]
QC_KEYS = ["A", "B", "C", "D"]

# --- ΔΙΑΧΕΙΡΙΣΗ ΧΡΟΝΟΥ (35 Λεπτά) ---
TOTAL_TIME = 35 * 60
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(0, TOTAL_TIME - int(elapsed_time))

if remaining_time == 0 and not st.session_state.test_submitted:
    st.session_state.test_submitted = True
    st.rerun()

# --- SIDEBAR ΠΛΟΗΓΗΣΗΣ ---
st.sidebar.title("GRE Quant Exam")
mins, secs = divmod(remaining_time, 60)
st.sidebar.metric(label="⏱️ Υπολειπόμενος Χρόνος", value=f"{mins:02d}:{secs:02d}")

st.sidebar.subheader("Πλοήγηση")
for i, q in enumerate(st.session_state.test_questions):
    label = "✅" if i in st.session_state.answers else "⚪"
    if st.sidebar.button(f"{label} Ερώτηση {i+1}", key=f"nav_{i}"):
        st.session_state.current_index = i

st.sidebar.divider()
if st.sidebar.button("🚨 Τέλος & Υποβολή", use_container_width=True, type="primary"):
    st.session_state.test_submitted = True
    st.rerun()

# --- ΚΥΡΙΩΣ ΟΘΟΝΗ ΕΞΕΤΑΣΗΣ ---
if not st.session_state.test_submitted:
    current_q = st.session_state.test_questions[st.session_state.current_index]
    
    st.subheader(f"Ερώτηση {st.session_state.current_index + 1} από {len(st.session_state.test_questions)}")
    st.caption(f"Πηγή Ερώτησης: {current_q['book']}")
    st.divider()
    
    # 1. Τύπος Quantitative Comparison (QC)
    if current_q["type"] == "QC":
        st.markdown(current_q["context"])
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Ποσότητα Α (Quantity A)**\n\n### {current_q['quantity_a']}")
        with col2:
            st.success(f"**Ποσότητα Β (Quantity B)**\n\n### {current_q['quantity_b']}")
            
        prev_ans = st.session_state.answers.get(st.session_state.current_index, None)
        default_idx = QC_KEYS.index(prev_ans) if prev_ans in QC_KEYS else None
        
        user_choice = st.radio("Επιλέξτε την ορθή σχέση:", QC_OPTIONS, index=default_idx, key=f"qc_{st.session_state.current_index}")
        if user_choice:
            st.session_state.answers[st.session_state.current_index] = QC_KEYS[QC_OPTIONS.index(user_choice)]

    # 2. Τύπος Multiple Choice (MC)
    elif current_q["type"] == "MC":
        st.markdown(current_q["question"])
        prev_ans = st.session_state.answers.get(st.session_state.current_index, None)
        default_idx = current_q["choices"].index(prev_ans) if prev_ans in current_q["choices"] else None
        
        user_choice = st.radio("Επιλογές απάντησης:", current_q["choices"], index=default_idx, key=f"mc_{st.session_state.current_index}")
        if user_choice:
            st.session_state.answers[st.session_state.current_index] = user_choice

    # 3. Τύπος Numeric Entry (NE)
    elif current_q["type"] == "NE":
        st.markdown(current_q["question"])
        prev_ans = st.session_state.answers.get(st.session_state.current_index, "")
        
        user_choice = st.text_input("Εισάγετε την τιμή (αριθμό):", value=prev_ans, key=f"ne_{st.session_state.current_index}")
        if user_choice:
            st.session_state.answers[st.session_state.current_index] = user_choice.strip()

    # Μπάρα Πλοήγησης Κάτω
    st.divider()
    c_prev, c_space, c_next = st.columns([1, 3, 1])
    with c_prev:
        if st.session_state.current_index > 0:
            if st.button("⬅️ Πίσω"):
                st.session_state.current_index -= 1
                st.rerun()
    with c_next:
        if st.session_state.current_index < len(st.session_state.test_questions) - 1:
            if st.button("Επόμενο ➡️"):
                st.session_state.current_index += 1
                st.rerun()

# --- ΟΘΟΝΗ ΑΝΑΦΟΡΑΣ ΑΠΟΤΕΛΕΣΜΑΤΩΝ (REVIEW SCREEN) ---
else:
    st.title("📊 Αποτελέσματα Εξέτασης")
    st.divider()
    
    score = sum(1 for i, q in enumerate(st.session_state.test_questions) if st.session_state.answers.get(i) == q["correct_answer"])
    st.metric(label="Τελικό Σκορ (Raw Score)", value=f"{score} / {len(st.session_state.test_questions)}")
    
    st.subheader("Αναλυτική Επισκόπηση")
    for i, q in enumerate(st.session_state.test_questions):
        user_ans = st.session_state.answers.get(i, "Δεν απαντήθηκε")
        is_correct = user_ans == q["correct_answer"]
        
        status = "✅ Σωστό" if is_correct else "❌ Λάθος"
        with st.expander(f"Ερώτηση {i+1} ({q['book']}) — {status}"):
            if q["type"] == "QC":
                st.write(f"**Ποσότητα Α:** {q['quantity_a']} | **Ποσότητα Β:** {q['quantity_b']}")
            else:
                st.write(q.get("question", "Question Text"))
                
            st.markdown(f"* **Η απάντησή σας:** `{user_ans}`")
            st.markdown(f"* **Σωστή απάντηση:** `{q['correct_answer']}`")
            st.info(f"**Επεξήγηση:** {q['explanation']}")
            
    if st.button("🔄 Ξεκινήστε Νέο Τεστ (Με Νέες Τυχαίες Ερωτήσεις)"):
        st.session_state.clear()
        st.rerun()
