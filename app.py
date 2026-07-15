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
    st.selected_questions = None
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv('bece_questions_randomized.csv')
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
st.subheader("Artificial Intelligence Group Two Assignment")

if not st.session_state.search_fulfilled:
    st.info("👈 Please set the number of questions in the sidebar and click 'Generate Quiz' to begin your session.")
else:
    if st.session_state.df is not None:
        st.success(f"Session Active: {st.session_state.selected_questions} questions loaded.")
        
        # --- DATA FILTERING LOGIC ---
        # Sampling from the dataframe
        sample_df = st.session_state.df.sample(min(st.session_state.selected_questions, len(st.session_state.df)))
        
        st.write("---")
        st.markdown("### Practice Questions")
        
        # Display questions using the CORRECT column names
        for index, row in sample_df.iterrows():
            st.write(f"**Question:** {row['Question']}") 
            options = [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']]
            st.radio(f"Select your answer:", options, key=f"q_{index}")
        
        if st.button("Submit Answers"):
            st.balloons()
            st.success("Results processed!")
    else:
        st.error("Error: 'bece_questions_randomized.csv' not found.")