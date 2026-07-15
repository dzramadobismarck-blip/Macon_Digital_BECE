import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Group 2 | Macon Digital",
    page_icon="🎓",
    layout="wide"
)

# --- CUSTOM CSS FOR BETTER UX ---
st.markdown('''
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004a99;
        color: white;
    }
    </style>
''', unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'search_fulfilled' not in st.session_state:
    st.session_state.search_fulfilled = False
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = None
if 'df' not in st.session_state:
    # Load your dataframe once and store in session state
    try:
        st.session_state.df = pd.read_csv('bece_questions.csv')
    except FileNotFoundError:
        st.session_state.df = None

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("AI Group 2")
    st.markdown("---")
    num_questions = st.number_input("Number of questions to practice:", min_value=1, max_value=50, value=5)
    
    if st.button("Generate Quiz"):
        st.session_state.search_fulfilled = True
        st.session_state.selected_questions = num_questions
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🎓 Intelligent Revision Portal")
st.subheader("Welcome to the Bume/Awate Circuit Learning Suite")

if not st.session_state.search_fulfilled:
    st.info("👈 Please set the number of questions in the sidebar and click 'Generate Quiz' to begin your session.")
    st.markdown("### How it works:")
    st.write("1. Set your preferred number of questions.")
    st.write("2. Click the button to load your randomized revision set.")
    st.write("3. Test your knowledge against the BECE curriculum.")
else:
    if st.session_state.df is not None:
        st.success(f"Session Active: {st.session_state.selected_questions} questions loaded.")
        
        # --- DATA FILTERING LOGIC ---
        # Randomly sample the requested number of questions
        sample_df = st.session_state.df.sample(min(st.session_state.selected_questions, len(st.session_state.df)))
        
        st.write("---")
        st.markdown("### Practice Questions")
        
        # Display questions and radio buttons
        for index, row in sample_df.iterrows():
            st.write(f"**Question:** {row['question_text']}") 
            options = [row['option_a'], row['option_b'], row['option_c'], row['option_d']]
            st.radio(f"Select your answer:", options, key=f"q_{index}")
        
        if st.button("Submit Answers"):
            st.balloons()
            st.success("Results processed!")
    else:
        st.error("Error: 'bece_questions.csv' not found. Please ensure the file is in the project directory.")