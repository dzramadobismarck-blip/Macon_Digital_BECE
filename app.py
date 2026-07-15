
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Group 2 Revision Portal", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('bece_questions_cleaned_pandas.csv')

df = load_data()

# Navigation
page = st.sidebar.radio("Navigate", ["Quiz Mode", "Question Search"])

st.title("📚 AI Group 2: Revision Portal")

# Shared State
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
    st.session_state.submitted = False
    st.session_state.user_answers = {}

if page == "Question Search":
    st.subheader("🔍 Custom Search")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        subjects = ["All"] + sorted(df['Subject'].dropna().unique().tolist())
        selected_subject = st.selectbox("Filter by Subject", subjects)
    with col2:
        years = ["All"] + sorted(df['Year'].unique().tolist(), reverse=True)
        selected_year = st.selectbox("Filter by Year", years)
    with col3:
        search_query = st.text_input("Keyword Search:")

    filtered_df = df.copy()
    if selected_subject != "All":
        filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if search_query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    
    st.write(f"Found {len(filtered_df)} questions.")
    
    if not filtered_df.empty:
        st.dataframe(filtered_df)
        if st.button("Take Quiz with these Questions"):
            st.session_state.quiz_data = filtered_df
            st.session_state.submitted = False
            st.session_state.user_answers = {}
            st.rerun() # Switch view logic is handled by session state
    else:
        st.warning("No questions match your search.")

elif page == "Quiz Mode":
    st.subheader("📝 Quiz Mode")
    
    if st.session_state.quiz_data is None:
        st.info("Search for questions first and click 'Take Quiz with these Questions', or start a random quiz below.")
        num_questions = st.number_input("Number of random questions:", min_value=1, max_value=20, value=5)
        if st.button("Start Random Quiz"):
            st.session_state.quiz_data = df.sample(min(num_questions, len(df)))
            st.session_state.submitted = False
            st.session_state.user_answers = {}
            st.rerun()

    if st.session_state.quiz_data is not None and not st.session_state.submitted:
        user_answers = {}
        for idx, row in enumerate(st.session_state.quiz_data.itertuples()):
            st.write(f"### Q{idx+1}: {row.Question}")
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
                st.write(f"Your Answer: {user_ans} | Correct: {row.Correct_Answer}")
                if user_ans == str(row.Correct_Answer).strip():
                    score += 1
                total += 1
            else:
                st.write(f"Your Answer: {st.session_state.user_answers[idx]}")
                st.write(f"Model Answer: {row.Theory_Answer}")
        st.success(f"Objective Score: {score} / {total}")
        if st.button("Reset Quiz"):
            st.session_state.quiz_data = None
            st.session_state.submitted = False
            st.rerun()
