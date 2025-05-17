import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student List", layout="wide")
st.title("List of Students and Depression Risk")

# Require user login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

# Ensure data has been loaded from the Overview page
if "latest_df" not in st.session_state:
    st.info("Please upload a student dataset in the Overview page first.")
    st.stop()

# Use the existing DataFrame stored in session_state
df = st.session_state["latest_df"]

# Create a summarized table and include the index for selection
df_summary = df[["Gender", "Age", "CGPA", "Depression Risk (%)"]].copy()
df_summary["Student Index"] = df_summary.index

# Display student table
st.dataframe(df_summary.sort_values("Depression Risk (%)", ascending=False))

# Select a student from the list
student_index = st.selectbox(
    "Select a student to view details:", df_summary["Student Index"])

# Store selected student index for detail view
st.session_state["selected_student_index"] = student_index

st.success(
    f"Student {student_index} selected. You can now view their detailed risk analysis.")
