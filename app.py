import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Group 2 | Macon Digital", page_icon="🎓", layout="wide")

# Initialize session state variables
if 'search_fulfilled' not in st.session_state:
    st.session_state.search_fulfilled = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

# Load data at startup with caching for efficiency
@st.cache_data
def load_data():
    try:
        return pd.read_csv('bece_questions_randomized.csv')
    except Exception as e:
        return None

df = load_data()

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("AI Group 2")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=50, value=5)
    
    if st.button("Generate Quiz"):
        if df is not None:
            # Store a sample in session state
            st.session_state.selected_questions = df.sample(min(num_questions, len(df)))
            st.session_state.search_fulfilled = True
            st.session_state.submitted = False
            st.session_state.score = 0
            st.session_state.user_answers = {} # Reset answers
            st.rerun()
        else:
            st.error("CSV file not found.")

# --- MAIN INTERFACE ---
st.title("🎓 Intelligent Revision Portal")
st.subheader("Artificial Intelligence Group Two Assignment")

if st.session_state.search_fulfilled and 'selected_questions' in st.session_state:
    sample_df = st.session_state.selected_questions
    
    st.write("---")
    # Display each question
    for index, row in sample_df.iterrows():
        st.write(f"**Question:** {row['Question']}")
        
        # Options list
        options = [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']]
        
        # Radio button: Updates session state directly on change
        ans = st.radio(
            f"Select your answer for Q{index}:", 
            options, 
            key=f"q_{index}", 
            index=None
        )
        st.session_state.user_answers[index] = ans
    
    if st.button("Submit Answers"):
        score = 0
        all_answered = True
        
        # Check if all questions were answered
        for index in sample_df.index:
            if st.session_state.user_answers.get(index) is None:
                all_answered = False
                break
        
        if not all_answered:
            st.warning("Please answer all questions before submitting!")
        else:
            # Calculate score
            for index, row in sample_df.iterrows():
                ans = str(row['Correct_Answer']).strip()
                correct_col = f"Option_{ans}"
                
                if st.session_state.user_answers.get(index) == row.get(correct_col):
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