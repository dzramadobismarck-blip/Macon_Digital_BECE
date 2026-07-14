import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Macon Digital: JHS GES Revision Agent", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #002366; color: white; }
    [data-testid="stSidebar"] * { color: white; }
    .stButton>button { background-color: #DAA520; color: #002366; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Updated with Group Branding) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Macon Digital</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>JHS Computing - Teacher Portal</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.write("🏠 Dashboard")
    st.write("📊 Topic Analysis")
    st.write("📈 Student Performance")
    st.write("📚 GES Curriculum Sync")
    st.markdown("---")
    st.write(f"**Development Team:** AI Group 2")
    st.write(f"**Lead:** Bismarck")
    if st.button("Log Out"):
        st.warning("Logged Out.")

# --- MAIN CONTENT ---
st.header("Topic Analysis & Strategy Generator")
st.info("Welcome, Bismarck! Let's analyze topic priority for your JHS Class.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Curriculum Strand")
    strands = ["1. Introduction to Computing", "2. Productivity Software", "3. Communication Networks", "4. Computational Thinking"]
    selected_strand = st.selectbox("Select Strand:", strands, label_visibility="collapsed")
    st.subheader("2. Specific Topic")
    topic_name = st.text_input("Enter Sub-Strand/Topic:", placeholder="e.g., Spreadsheet formulas", label_visibility="collapsed")

with col2:
    st.subheader("3. Exam Priority Factors")
    weight = st.slider("Exam Weight/Priority Score:", 0.0, 1.0, 0.9, step=0.05)
    freq = st.number_input("Historical BECE Frequency:", 0, 10, 8)
    difficulty = st.slider("Average Student Difficulty:", 0.0, 1.0, 0.75, step=0.05)

if st.button("GENERATE REVISION STRATEGY", type="primary"):
    st.markdown("---")
    st.subheader("Analysis Result")
    is_high_priority = (weight > 0.8) or (freq > 7)
    
    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        st.error("HIGH PRIORITY") if is_high_priority else st.success("STANDARD")
    with res_col2:
        if is_high_priority:
            st.write("**Strategy: Deep Learning Approach**")
            st.write("Action: Focus on hands-on practical application. Allocate 3 periods.")
        else:
            st.write("**Strategy: Inquiry-Based Approach**")
            st.write("Action: Focus on real-world examples and discussions. Allocate 1-2 periods.")