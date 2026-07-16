
import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate

st.set_page_config(page_title="AI School Performance Agent", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('bece_questions_cleaned_pandas.csv')

df = load_data()

st.title("🎓 Intelligent School Performance Agent")

# Define the Persona/System Prompt
system_prompt = """
You are an expert Educational Consultant AI for a Junior High School. 
Your goal is to analyze academic performance data to help teachers and headteachers.
When answering, always:
1. Identify students or subjects that need intervention.
2. Suggest actionable strategies (e.g., extra classes, peer tutoring).
3. Be professional, supportive, and data-driven.
If the data shows a performance dip, explain it if possible and recommend steps.
"""

def get_refined_agent(dataframe):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create the agent with a custom system prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    return create_pandas_dataframe_agent(
        llm, 
        dataframe, 
        verbose=True, 
        allow_dangerous_code=True,
        prompt=prompt
    )

# Chat Interface
st.subheader("Ask the Agent about student interventions")
user_query = st.text_input("Example: 'Which students are failing in English and how can I support them?'")

if user_query:
    agent = get_refined_agent(df)
    with st.spinner("Analyzing data and formulating intervention strategies..."):
        try:
            response = agent.invoke(user_query)
            st.write("### Agent Advice:")
            st.write(response['output'])
        except Exception as e:
            st.error(f"Analysis error: {e}")

st.divider()
# [Insert your previously refined Quiz portal code here]
