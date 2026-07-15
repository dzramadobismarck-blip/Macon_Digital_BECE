import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Make sure your file is named 'bece_questions_full.csv'
    return pd.read_csv("bece_questions_full.csv", encoding='utf-8-sig', engine='python')

df = load_data()

st.title("🇬🇭 Macon Digital: BECE Revision")

# Sidebar
selected_type = st.sidebar.selectbox("Question Type", ["Objective", "Theory"])
filtered_df = df[df['Type'] == selected_type]

# Display
for index, row in filtered_df.iterrows():
    with st.expander(f"{row['Year']} | {row['Topic']}: {row['Question']}"):
        if selected_type == "Objective":
            st.write(f"A) {row['Option_A']}")
            st.write(f"B) {row['Option_B']}")
            st.write(f"C) {row['Option_C']}")
            st.write(f"D) {row['Option_D']}")
            if st.button("Show Answer", key=f"obj_{index}"):
                st.success(f"Correct Answer: {row['Correct_Answer']}")
        else:
            if st.button("Show Answer", key=f"theory_{index}"):
                st.info(f"Guideline: {row['Theory_Answer']}")
