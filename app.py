
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Group 2 Revision", layout="wide")
st.title("📚 AI Group 2: Smart Quiz Mode")

@st.cache_data
def load_data():
    return pd.read_csv('bece_questions_cleaned_pandas.csv')

df = load_data()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
    st.session_state.submitted = False

st.sidebar.header("Quiz Settings")
num_questions = st.sidebar.number_input("Number of questions", min_value=1, max_value=20, value=5)
if st.sidebar.button("Start New Quiz"):
    st.session_state.quiz_data = df.sample(num_questions)
    st.session_state.submitted = False
    st.session_state.user_answers = {}

if st.session_state.quiz_data is not None and not st.session_state.submitted:
    user_answers = {}
    for idx, row in enumerate(st.session_state.quiz_data.itertuples()):
        st.write(f"### Q{idx+1}: {row.Question}")
        
        # Check if options exist
        has_options = not pd.isna(row.Option_A) and not pd.isna(row.Option_B)
        
        if has_options:
            options = [f"A: {row.Option_A}", f"B: {row.Option_B}", f"C: {row.Option_C}", f"D: {row.Option_D}"]
            choice = st.radio(f"Select answer for Q{idx+1}:", options, key=f"q{idx}")
            user_answers[idx] = choice.split(":")[0].strip()
        else:
            user_answers[idx] = st.text_area(f"Write your answer for Q{idx+1}:", key=f"q{idx}")

    if st.button("Submit Quiz"):
        st.session_state.user_answers = user_answers
        st.session_state.submitted = True
        st.rerun()

elif st.session_state.submitted:
    st.subheader("Results")
    score = 0
    total = 0
    for idx, row in enumerate(st.session_state.quiz_data.itertuples()):
        st.write(f"**Q{idx+1}:** {row.Question}")
        has_options = not pd.isna(row.Option_A) and not pd.isna(row.Option_B)
        
        if has_options:
            user_ans = st.session_state.user_answers[idx]
            st.write(f"Your Answer: {user_ans} | Correct Answer: {row.Correct_Answer}")
            if user_ans == str(row.Correct_Answer).strip():
                score += 1
            total += 1
        else:
            st.write(f"Your Answer: {st.session_state.user_answers[idx]}")
            st.write(f"Model Answer: {row.Theory_Answer}")
            st.info("Theory answers are for your self-reflection.")
            
    st.success(f"Objective Score: {score} / {total}")
    if st.button("Reset"):
        st.session_state.quiz_data = None
        st.session_state.submitted = False
        st.rerun()
