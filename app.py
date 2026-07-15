
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Group 2 Quiz", layout="wide")

st.title("📚 AI Group 2: Quiz Mode")

@st.cache_data
def load_data():
    return pd.read_csv('bece_questions_cleaned_pandas.csv')

df = load_data()

# Session State for quiz
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Sidebar for quiz setup
st.sidebar.header("Quiz Settings")
num_questions = st.sidebar.number_input("Number of questions", min_value=1, max_value=20, value=5)
if st.sidebar.button("Start Quiz"):
    st.session_state.quiz_data = df.sample(num_questions)
    st.session_state.submitted = False
    st.session_state.score = 0

# Quiz Display
if st.session_state.quiz_data is not None and not st.session_state.submitted:
    st.write(f"Answer the following {len(st.session_state.quiz_data)} questions:")
    user_answers = {}
    
    for idx, row in enumerate(st.session_state.quiz_data.itertuples()):
        st.write(f"**Q{idx+1}:** {row.Question}") # Assuming column 4 is Question
        user_answers[idx] = st.text_input(f"Your answer for Q{idx+1}:", key=f"q{idx}")
    
    if st.button("Submit Quiz"):
        score = 0
        for idx, row in enumerate(st.session_state.quiz_data.itertuples()):
            # Assuming last column is Answer
            if user_answers[idx].strip().lower() == str(row[-1]).strip().lower():
                score += 1
        st.session_state.score = score
        st.session_state.submitted = True
        st.rerun()

elif st.session_state.submitted:
    st.success(f"Quiz Completed! Your score: {st.session_state.score} / {len(st.session_state.quiz_data)}")
    if st.button("Retake Quiz"):
        st.session_state.quiz_data = None
        st.session_state.submitted = False
        st.rerun()
