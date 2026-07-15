import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Group 2 | Macon Digital", page_icon="🎓", layout="wide")

# Initialize session state
if 'search_fulfilled' not in st.session_state:
    st.session_state.search_fulfilled = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Load data
try:
    df = pd.read_csv('bece_questions_randomized.csv')
except:
    df = None

# Sidebar
with st.sidebar:
    st.title("AI Group 2")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=50, value=5)
    if st.button("Generate Quiz"):
        # Select random questions and store in session state
        st.session_state.selected_questions = df.sample(min(num_questions, len(df)))
        st.session_state.search_fulfilled = True
        st.session_state.submitted = False
        st.session_state.score = 0
        st.rerun()

# Main Interface
st.title("🎓 Intelligent Revision Portal")
st.subheader("Artificial Intelligence Group Two Assignment")

if st.session_state.search_fulfilled and st.session_state.selected_questions is not None:
    sample_df = st.session_state.selected_questions
    user_answers = {}
    
    st.write("---")
    for index, row in sample_df.iterrows():
        st.write(f"**Question:** {row['Question']}")
        options = [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']]
        # Index=None ensures no option is selected by default
        user_answers[index] = st.radio(f"Select your answer:", options, key=f"q_{index}", index=None)
    
    if st.button("Submit Answers"):
        score = 0
        for index, row in sample_df.iterrows():
            # Map the letter in 'Correct_Answer' (e.g., 'A') to the header (e.g., 'Option_A')
            correct_col = f"Option_{row['Correct_Answer']}"
            if user_answers[index] == row[correct_col]:
                score += 1
        
        st.session_state.score = score
        st.session_state.submitted = True
        st.rerun()

    if st.session_state.submitted:
        st.success(f"### Final Score: {st.session_state.score} / {len(sample_df)}")
        if st.session_state.score == len(sample_df):
            st.balloons()
else:
    st.info("👈 Please set the number of questions in the sidebar and click 'Generate Quiz' to begin your session.")