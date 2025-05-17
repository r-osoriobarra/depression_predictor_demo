import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Detail", layout="wide")
st.title("Student Risk Detail")

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

# Ensure student list was loaded and a student was selected
if "latest_df" not in st.session_state or "selected_student_index" not in st.session_state:
    st.info("Please select a student from the Student List page.")
    st.stop()

# Retrieve student information
df = st.session_state["latest_df"]
student_index = st.session_state["selected_student_index"]
student_data = df.loc[student_index]

# Display student details
st.subheader(f"Student ID: {student_index}")
st.metric("Depression Risk (%)", round(student_data["Depression Risk (%)"], 2))

st.markdown("### Basic Information")
st.write({
    "Gender": student_data["Gender"],
    "Age": student_data["Age"],
    "CGPA": student_data["CGPA"],
    "Degree": student_data.get("Degree", "Not specified"),
    "Academic Pressure": student_data.get("Academic Pressure", "N/A"),
    "Study Satisfaction": student_data.get("Study Satisfaction", "N/A"),
    "Sleep Duration": student_data.get("Sleep Duration", "N/A"),
    "Financial Stress": student_data.get("Financial Stress", "N/A"),
    "Family History": student_data.get("Family History of Mental Illness", "N/A"),
    "Suicidal Thoughts": student_data.get("Have you ever had suicidal thoughts ?", "N/A")
})

st.markdown(
    "You can now proceed to view the feature contributions or trend analysis.")
