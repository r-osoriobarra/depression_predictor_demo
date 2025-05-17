# pages/3_StudentList.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import set_page_style, check_login, check_data
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

st.set_page_config(page_title="Student List", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>List of Students and Depression Risk</h1>",
            unsafe_allow_html=True)

# Require user login
if not check_login():
    st.stop()

# Ensure data has been loaded
if not check_data():
    st.stop()

# Use the existing DataFrame stored in session_state
df = st.session_state["latest_df"]

# Dashboard at the top
st.markdown("<h2 class='sub-header'>Risk Distribution</h2>",
            unsafe_allow_html=True)

# Create risk category if it doesn't exist
if "Risk Category" not in df.columns:
    df["Risk Category"] = pd.cut(
        df["Depression Risk (%)"],
        bins=[0, 30, 60, 100],
        labels=["Low", "Medium", "High"]
    )

# Create filtering options in sidebar
st.sidebar.markdown(
    "<h3 class='sub-header'>Filter Students</h3>", unsafe_allow_html=True)

# Risk filter
risk_filter = st.sidebar.multiselect(
    "Risk Category",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

# Gender filter (if available)
if "Gender" in df.columns:
    gender_filter = st.sidebar.multiselect(
        "Gender",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
else:
    gender_filter = None

# Degree filter (if available)
if "Degree" in df.columns:
    degree_filter = st.sidebar.multiselect(
        "Degree",
        options=df["Degree"].unique(),
        default=[]
    )
else:
    degree_filter = None

# CGPA range filter (if available)
if "CGPA" in df.columns:
    cgpa_range = st.sidebar.slider(
        "CGPA Range",
        min_value=float(df["CGPA"].min()),
        max_value=float(df["CGPA"].max()),
        value=(float(df["CGPA"].min()), float(df["CGPA"].max()))
    )
else:
    cgpa_range = None

# Apply filters
filtered_df = df.copy()

# Filter by risk category
filtered_df = filtered_df[filtered_df["Risk Category"].isin(risk_filter)]

# Filter by gender if selected
if gender_filter is not None and len(gender_filter) > 0:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]

# Filter by degree if selected
if degree_filter is not None and len(degree_filter) > 0:
    filtered_df = filtered_df[filtered_df["Degree"].isin(degree_filter)]

# Filter by CGPA range if selected
if cgpa_range is not None:
    filtered_df = filtered_df[(filtered_df["CGPA"] >= cgpa_range[0]) &
                              (filtered_df["CGPA"] <= cgpa_range[1])]

# Show filter summary
st.markdown(
    f"Showing **{len(filtered_df)}** students out of **{len(df)}** total students.")

# Display distribution of filtered students
col1, col2 = st.columns(2)

with col1:
    # Bar chart of risk categories
    fig, ax = plt.subplots(figsize=(10, 6))
    risk_counts = filtered_df["Risk Category"].value_counts()
    colors = ['#388E3C', '#F57C00', '#D32F2F']

    # Map colors to actual categories
    category_colors = {cat: col for cat, col in zip(risk_counts.index, colors)}
    bar_colors = [category_colors.get(cat, '#1E88E5')
                  for cat in risk_counts.index]

    sns.barplot(x=risk_counts.index, y=risk_counts.values,
                palette=bar_colors, ax=ax)
    plt.title("Number of Students by Risk Category")
    plt.xlabel("Risk Category")
    plt.ylabel("Count")
    st.pyplot(fig)

with col2:
    # Either show gender distribution or degree distribution based on which is available
    if "Gender" in filtered_df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        gender_risk = filtered_df.groupby(
            "Gender")["Depression Risk (%)"].mean().sort_values(ascending=False)
        sns.barplot(x=gender_risk.index, y=gender_risk.values,
                    palette='Blues_d', ax=ax)
        plt.title("Average Depression Risk by Gender")
        plt.xlabel("Gender")
        plt.ylabel("Average Risk (%)")
        st.pyplot(fig)
    elif "Degree" in filtered_df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        degree_risk = filtered_df.groupby(
            "Degree")["Depression Risk (%)"].mean().sort_values(ascending=False)
        # Show top 10 to avoid overcrowding
        degree_risk_top = degree_risk.head(10)
        sns.barplot(x=degree_risk_top.index,
                    y=degree_risk_top.values, palette='Blues_d', ax=ax)
        plt.title("Average Depression Risk by Degree (Top 10)")
        plt.xlabel("Degree")
        plt.ylabel("Average Risk (%)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

# Create a summarized table and include the index for selection
display_cols = ["Gender", "Age", "CGPA",
                "Depression Risk (%)", "Risk Category"]
display_cols = [col for col in display_cols if col in filtered_df.columns]

df_summary = filtered_df[display_cols].copy()
df_summary["Student Index"] = filtered_df.index

# Function to highlight risk categories


def highlight_risk(val):
    if val == "High":
        return 'background-color: rgba(211, 47, 47, 0.2); color: #D32F2F; font-weight: bold'
    elif val == "Medium":
        return 'background-color: rgba(245, 124, 0, 0.2); color: #F57C00; font-weight: bold'
    elif val == "Low":
        return 'background-color: rgba(56, 142, 60, 0.2); color: #388E3C; font-weight: bold'
    return ''


# Display student table with styling
st.markdown("<h2 class='sub-header'>Student List</h2>", unsafe_allow_html=True)

# Apply styling
styled_df = df_summary.sort_values("Depression Risk (%)", ascending=False)
styled_df = styled_df.style.applymap(highlight_risk, subset=["Risk Category"])

st.dataframe(styled_df, height=400)

# Select a student from the list
student_indices = df_summary["Student Index"].tolist()
if student_indices:
    student_index = st.selectbox(
        "Select a student to view details:", student_indices)

    # Store selected student index for detail view
    st.session_state["selected_student_index"] = student_index

    st.success(
        f"Student {student_index} selected. You can now view their detailed risk analysis.")

    # Preview selected student
    selected_student = filtered_df.loc[student_index]

    st.markdown("<h3 class='sub-header'>Selected Student Preview</h3>",
                unsafe_allow_html=True)

    # Format based on risk level
    risk_score = selected_student["Depression Risk (%)"]
    if risk_score > 60:
        risk_color = "#D32F2F"
        risk_category = "High"
    elif risk_score > 30:
        risk_color = "#F57C00"
        risk_category = "Medium"
    else:
        risk_color = "#388E3C"
        risk_category = "Low"

    st.markdown(f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0;">Student {student_index}</h3>
                    <p style="margin: 5px 0 0 0;">{selected_student.get("Degree", "Student")}</p>
                </div>
                <div style="text-align: right;">
                    <h3 style="margin: 0; color: {risk_color};">{risk_category} Risk</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 0; color: {risk_color};">{round(risk_score, 1)}%</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Display key student attributes in two columns
    col1, col2 = st.columns(2)

    # Basic attributes
    basic_attrs = ["Gender", "Age", "CGPA", "Degree"]
    basic_attrs = [
        attr for attr in basic_attrs if attr in selected_student.index]

    with col1:
        st.markdown("<h4>Basic Information</h4>", unsafe_allow_html=True)
        for attr in basic_attrs:
            st.markdown(f"**{attr}:** {selected_student[attr]}")

    # Mental health indicators if available
    mh_attrs = ["Academic Pressure", "Study Satisfaction", "Sleep Duration",
                "Financial Stress", "Family History of Mental Illness"]
    mh_attrs = [attr for attr in mh_attrs if attr in selected_student.index]

    with col2:
        if mh_attrs:
            st.markdown("<h4>Mental Health Indicators</h4>",
                        unsafe_allow_html=True)
            for attr in mh_attrs:
                st.markdown(f"**{attr}:** {selected_student[attr]}")
        else:
            st.info(
                "No detailed mental health indicators available for this student.")
else:
    st.warning("No students found with the selected filters.")
