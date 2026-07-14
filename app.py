import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("bece_questions.csv")

df = load_data()

st.title("🇬🇭 Macon Digital BECE Revision")

# Sidebar filters
st.sidebar.header("Filter Questions")
selected_year = st.sidebar.multiselect("Select Year", df['Year'].unique())
selected_subject = st.sidebar.multiselect("Select Subject", df['Subject'].unique())

# Filtering logic
filtered_df = df.copy()
if selected_year:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_year)]
if selected_subject:
    filtered_df = filtered_df[filtered_df['Subject'].isin(selected_subject)]

# Display questions as interactive items
st.subheader(f"Showing {len(filtered_df)} Questions")

for index, row in filtered_df.iterrows():
    with st.expander(f"{row['Subject']} ({row['Year']}): {row['Question']}"):
        st.write(f"A) {row['Option_A']}")
        st.write(f"B) {row['Option_B']}")
        st.write(f"C) {row['Option_C']}")
        st.write(f"D) {row['Option_D']}")
        
        # Button to reveal the answer
        if st.button(f"Show Answer", key=f"btn_{index}"):
            st.success(f"Correct Answer: {row['Correct_Answer']}")
