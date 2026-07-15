import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("bece_questions_randomized.csv", encoding='utf-8-sig', engine='python')

df = load_data()

st.title("🇬🇭 Macon Digital: BECE Exam Engine")

# 1. Search Bar
search_query = st.text_input("🔍 Search for a topic or question:")
if search_query:
    df = df[df['Question'].str.contains(search_query, case=False) | 
            df['Topic'].str.contains(search_query, case=False)]

# 2. Filtering
type_filter = st.sidebar.selectbox("Filter by Type", ["Objective", "Theory"])
filtered_df = df[df['Type'] == type_filter]

# 3. Quiz Interface
st.subheader(f"Practice: {type_filter} Questions")
user_answers = {}

if type_filter == "Objective":
    for index, row in filtered_df.iterrows():
        st.write(f"**Q: {row['Question']}**")
        options = [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']]
        # Create a radio button for selection
        choice = st.radio(f"Select answer for Q{index}", options, key=f"q_{index}", index=None)
        user_answers[index] = choice

    if st.button("Submit & Mark"):
        score = 0
        total = len(filtered_df)
        for index, row in filtered_df.iterrows():
            # Match the selected text to the correct option letter
            correct_val = row[f"Option_{row['Correct_Answer']}"]
            if user_answers[index] == correct_val:
                score += 1
        
        st.write(f"### Your Score: {score} / {total}")
        if score == total:
            st.balloons()
            st.success("Excellent! You got everything right.")
        else:
            st.info(f"Keep practicing! You scored { (score/total)*100:.1f}%")

else:
    # Theory mode: Reveal guidelines
    for index, row in filtered_df.iterrows():
        with st.expander(f"Question: {row['Question']}"):
            if st.button("Show Guideline", key=f"theory_{index}"):
                st.info(f"Guideline: {row['Theory_Answer']}")

# Footer
st.sidebar.markdown("---")
st.sidebar.text("Developed by Macon Digital")