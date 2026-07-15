
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Group 2 Search", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('bece_questions_cleaned_pandas.csv')

df = load_data()

st.title("🔍 Question Search & Quiz Portal")

# Sidebar for Filters
st.sidebar.header("Search Filters")
subjects = ["All"] + sorted(df['Subject'].dropna().unique().tolist())
selected_subject = st.sidebar.selectbox("Filter by Subject", subjects)
years = ["All"] + sorted(df['Year'].unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Filter by Year", years)
search_query = st.sidebar.text_input("Keyword Search:")

# Determine if a search is active
search_active = (selected_subject != "All") or (selected_year != "All") or (search_query != "")

# Apply Filters
filtered_df = df.copy()
if selected_subject != "All":
    filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
if search_query:
    filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

# Show results only if a search is active
if search_active:
    if not filtered_df.empty:
        st.write(f"### Found {len(filtered_df)} results.")
        
        # User selection for type and number
        test_type = st.radio("Select Test Type:", ["Objective", "Subjective"], key="search_type")
        
        # Filter dataframe based on test type
        if test_type == "Objective":
            quiz_df = filtered_df[filtered_df['Option_A'].notna()]
        else:
            quiz_df = filtered_df[filtered_df['Option_A'].isna()]
            
        if not quiz_df.empty:
            limit = st.number_input("Number of questions to quiz on:", min_value=1, max_value=len(quiz_df), value=min(5, len(quiz_df)), key="search_limit")
            if st.button(f"Take {test_type} Quiz"):
                st.session_state.quiz_data = quiz_df.sample(limit)
                st.session_state.submitted = False
                st.session_state.user_answers = {}
                st.rerun()
        else:
            st.warning(f"No {test_type} questions found for this search.")
    else:
        st.warning("No results found.")

# Add "Quick Start" option
st.divider()
st.write("### Or take a random quiz:")
quick_type = st.radio("Select Test Type:", ["Objective", "Subjective"], key="quick_type")

# Filter random data by type
if quick_type == "Objective":
    random_df = df[df['Option_A'].notna()]
else:
    random_df = df[df['Option_A'].isna()]

if not random_df.empty:
    num_rand = st.number_input("Number of random questions:", min_value=1, max_value=min(20, len(random_df)), value=min(5, len(random_df)), key="quick_limit")
    if st.button("Start Random Quiz"):
        st.session_state.quiz_data = random_df.sample(min(num_rand, len(random_df)))
        st.session_state.submitted = False
        st.session_state.user_answers = {}
        st.rerun()
else:
    st.warning(f"No {quick_type} questions available.")

# Quiz Mode (Only shown if quiz_data is active)
if 'quiz_data' in st.session_state and st.session_state.quiz_data is not None:
    st.divider()
    st.subheader("📝 Active Quiz")
    if not st.session_state.submitted:
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
    else:
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
        if st.button("Start New Search"):
            st.session_state.quiz_data = None
            st.session_state.submitted = False
            st.rerun()
