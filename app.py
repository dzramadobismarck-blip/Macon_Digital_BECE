import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="AI Group 2 | Revision Portal", page_icon="🎓", layout="wide")

# Load Data with error handling for malformed CSV lines
@st.cache_data
def load_data():
    try:
        # on_bad_lines='skip' ensures the app doesn't crash on corrupted rows
        return pd.read_csv('bece_questions_randomized.csv', on_bad_lines='skip')
    except Exception:
        return None

df = load_data()

# Session State
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

# Sidebar
with st.sidebar:
    st.title("🎓 Revision Settings")
    if df is not None:
        subject_filter = st.selectbox("Select Subject", ["All"] + df['Subject'].unique().tolist())
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10)
        
        if st.button("Generate New Quiz"):
            filtered_df = df if subject_filter == "All" else df[df['Subject'] == subject_filter]
            st.session_state.selected_questions = filtered_df.sample(min(num_questions, len(filtered_df)))
            st.session_state.submitted = False
            st.session_state.score = 0
            st.session_state.user_answers = {}
            st.rerun()
    else:
        st.error("Could not load CSV data.")

# Main
st.title("AI Group 2 | Revision Portal")

if st.session_state.selected_questions is not None:
    sample_df = st.session_state.selected_questions
    
    for idx, row in sample_df.iterrows():
        st.write(f"### Q: {row['Question']}")
        options = [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']]
        
        # User Selection
        choice = st.radio(f"Select Answer for Q{idx}:", options, key=f"radio_{idx}", index=None)
        st.session_state.user_answers[idx] = choice
        
    if st.button("Submit Quiz"):
        score = 0
        for idx, row in sample_df.iterrows():
            # Clean and map correct answer
            ans = str(row['Correct_Answer']).strip()
            correct_key = f"Option_{ans}"
            
            # Use .get() to avoid KeyErrors
            if st.session_state.user_answers.get(idx) == row.get(correct_key):
                score += 1
        st.session_state.score = score
        st.session_state.submitted = True
        st.rerun()

    if st.session_state.submitted:
        st.success(f"Final Score: {st.session_state.score} / {len(sample_df)}")
else:
    st.info("Use the sidebar to filter by subject and generate your quiz.")