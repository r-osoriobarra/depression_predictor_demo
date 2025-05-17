# pages/4_StudentDetail.py (continuación)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils import set_page_style, check_login, check_data, categorize_risk

st.set_page_config(page_title="Student Detail", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Student Risk Detail</h1>",
            unsafe_allow_html=True)

# Require login
if not check_login():
    st.stop()

# Ensure student list was loaded and a student was selected
if not check_data():
    st.stop()

if "selected_student_index" not in st.session_state:
    st.info("Please select a student from the Student List page.")
    st.stop()

# Retrieve student information
df = st.session_state["latest_df"]
student_index = st.session_state["selected_student_index"]
student_data = df.loc[student_index]

# Determine risk category and color
risk_score = student_data["Depression Risk (%)"]
risk_category, risk_color = categorize_risk(risk_score)

# Student header with risk indicator
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
         background-color: #f5f5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <div>
            <h2 style="margin: 0;">Student ID: {student_index}</h2>
            <p style="margin: 5px 0 0 0;">{student_data.get("Degree", "Student")}</p>
        </div>
        <div style="text-align: right;">
            <h3 style="margin: 0; color: {risk_color};">{risk_category} Risk</h3>
            <p style="font-size: 24px; font-weight: bold; margin: 0; color: {risk_color};">{round(risk_score, 1)}%</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create tabs for different views of student data
tab1, tab2, tab3 = st.tabs(
    ["Basic Information", "Risk Visualization", "Recommendations"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 class='sub-header'>Student Profile</h3>",
                    unsafe_allow_html=True)

        # Basic attributes that most data will have
        basic_attrs = ["Gender", "Age", "CGPA", "Degree"]

        # Create profile data dictionary with available attributes
        profile_data = {}
        for attr in basic_attrs:
            if attr in student_data.index:
                profile_data[attr] = student_data[attr]

        # Display profile data
        for key, value in profile_data.items():
            st.markdown(f"**{key}:** {value}")

    with col2:
        st.markdown(
            "<h3 class='sub-header'>Mental Health Indicators</h3>", unsafe_allow_html=True)

        # Mental health indicators that might be in the data
        health_attrs = [
            "Academic Pressure", "Study Satisfaction", "Sleep Duration",
            "Financial Stress", "Family History of Mental Illness",
            "Have you ever had suicidal thoughts ?", "Social Support",
            "Substance Use", "Physical Activity", "Stress Level"
        ]

        # Create health data dictionary with available attributes
        health_data = {}
        for attr in health_attrs:
            if attr in student_data.index:
                health_data[attr] = student_data[attr]

        # Display health indicators with warnings for critical values
        if health_data:
            for key, value in health_data.items():
                warning = ""
                if key == "Have you ever had suicidal thoughts ?" and str(value).lower() in ["yes", "sometimes", "1", "true"]:
                    warning = " ⚠️ **URGENT: Requires immediate attention**"
                elif key == "Sleep Duration" and isinstance(value, (int, float)) and value < 6:
                    warning = " ⚠️ **Below recommended levels**"
                elif key == "Stress Level" and isinstance(value, (int, float)) and value > 7:
                    warning = " ⚠️ **High stress detected**"

                st.markdown(f"**{key}:** {value}{warning}")
        else:
            st.info(
                "No detailed mental health indicators available for this student.")

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 class='sub-header'>Risk Meter</h3>",
                    unsafe_allow_html=True)

        # Create a gauge-like visualization using matplotlib
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        # Set the limits
        ax.set_thetamin(0)
        ax.set_thetamax(180)

        # Create the bars
        low = plt.cm.Greens(0.6)
        medium = plt.cm.Oranges(0.6)
        high = plt.cm.Reds(0.6)

        bars = ax.bar(
            x=[np.pi/4, np.pi/4, np.pi/4],  # All at the same angle
            width=[np.pi/2, np.pi/2, np.pi/2],  # Same width
            bottom=[0, 0, 0],  # Start from the center
            height=[30, 30, 40],  # Low: 0-30, Medium: 30-60, High: 60-100
            color=[low, medium, high],
            alpha=0.6
        )

        # Add risk indicator (needle)
        theta = np.pi * risk_score / 100  # Convert to radians
        r = 100  # Length of the needle
        ax.plot([0, theta], [0, r], 'k-', linewidth=3)
        ax.plot([0, theta], [0, r], 'w-', linewidth=1)

        # Add circular marker at the end of the needle
        ax.plot(theta, r, 'ko', markersize=8)
        ax.plot(theta, r, 'wo', markersize=4)

        # Add labels
        ax.text(np.pi/4 - np.pi/8, 15, 'Low',
                fontsize=12, ha='center', va='center')
        ax.text(np.pi/4, 45, 'Medium', fontsize=12, ha='center', va='center')
        ax.text(np.pi/4 + np.pi/8, 75, 'High',
                fontsize=12, ha='center', va='center')

        # Add risk score text
        ax.text(0, -20, f'{round(risk_score, 1)}%', fontsize=24,
                ha='center', va='center', color=risk_color, weight='bold')

        # Clean up the chart
        ax.set_ylim(0, 100)
        ax.set_axis_off()

        st.pyplot(fig)

    with col2:
        st.markdown(
            "<h3 class='sub-header'>Comparison with Average</h3>", unsafe_allow_html=True)

        # Select some key numeric indicators for comparison
        numeric_indicators = ['Age', 'CGPA', 'Depression Risk (%)']

        # Add other available numeric indicators
        for col in df.select_dtypes(include=['float64', 'int64']).columns:
            if col not in numeric_indicators and col in student_data.index:
                numeric_indicators.append(col)

        # Filter to only available indicators
        available_indicators = [
            ind for ind in numeric_indicators if ind in student_data.index]

        if available_indicators:
            # Calculate averages
            avg_values = df[available_indicators].mean()
            student_values = student_data[available_indicators]

            # Create comparison dataframe
            comparison_df = pd.DataFrame({
                'Indicator': available_indicators,
                'Student Value': student_values.values,
                'Average Value': avg_values.values,
                'Difference': student_values.values - avg_values.values
            })

            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 8))

            # Bar positions
            bar_positions = np.arange(len(available_indicators))
            bar_width = 0.35

            # Create bars
            student_bars = ax.bar(
                bar_positions - bar_width/2,
                student_values.values,
                bar_width,
                label='Student',
                color=risk_color
            )

            avg_bars = ax.bar(
                bar_positions + bar_width/2,
                avg_values.values,
                bar_width,
                label='Average',
                color='#1E88E5'
            )

            # Add values on top of bars
            for bar in student_bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{height:.1f}',
                    ha='center',
                    va='bottom',
                    fontsize=9
                )

            for bar in avg_bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{height:.1f}',
                    ha='center',
                    va='bottom',
                    fontsize=9
                )

            # Labels and legend
            ax.set_xlabel('Indicator')
            ax.set_ylabel('Value')
            ax.set_title('Student vs Average: Key Indicators')
            ax.set_xticks(bar_positions)
            ax.set_xticklabels(available_indicators, rotation=45, ha='right')
            ax.legend()

            plt.tight_layout()
            st.pyplot(fig)

            # Also show the comparison table
            st.dataframe(comparison_df.set_index('Indicator').round(2))
        else:
            st.info("No numeric indicators available for comparison.")

with tab3:
    st.markdown("<h3 class='sub-header'>Recommended Actions</h3>",
                unsafe_allow_html=True)

    # Generate recommendations based on risk level and specific factors
    recommendations = []

    # High risk recommendations
    if risk_category == "High":
        recommendations.append({
            "title": "Urgent intervention recommended",
            "description": "Student shows high risk of depression and requires immediate attention.",
            "actions": [
                "Schedule an immediate wellness check",
                "Provide information about counseling services",
                "Follow up within 7 days"
            ],
            "priority": "Urgent",
            "color": "#D32F2F"
        })

        # Check for suicidal thoughts
        if "Have you ever had suicidal thoughts ?" in student_data.index:
            if str(student_data["Have you ever had suicidal thoughts ?"]).lower() in ["yes", "sometimes", "1", "true"]:
                recommendations.append({
                    "title": "ALERT: Suicidal thoughts indicated",
                    "description": "Student has reported having suicidal thoughts.",
                    "actions": [
                        "Implement immediate safety protocol",
                        "Refer to mental health professional",
                        "Follow university protocol for crisis intervention"
                    ],
                    "priority": "Emergency",
                    "color": "#B71C1C"
                })

    # Medium risk recommendations
    elif risk_category == "Medium":
        recommendations.append({
            "title": "Regular monitoring recommended",
            "description": "Student shows medium risk of depression.",
            "actions": [
                "Schedule a wellness check within 2 weeks",
                "Provide information about mental health resources",
                "Consider check-in after midterms or high-stress periods"
            ],
            "priority": "Medium",
            "color": "#F57C00"
        })

    # Low risk recommendations
    else:
        recommendations.append({
            "title": "Preventive approach recommended",
            "description": "Student shows low risk of depression.",
            "actions": [
                "Provide general mental health resources",
                "Include in group wellness activities",
                "Regular semester check-ins"
            ],
            "priority": "Standard",
            "color": "#388E3C"
        })

    # Factor-specific recommendations

    # Sleep issues
    if "Sleep Duration" in student_data.index:
        if isinstance(student_data["Sleep Duration"], (int, float)) and student_data["Sleep Duration"] < 6:
            recommendations.append({
                "title": "Sleep improvement needed",
                "description": f"Student reports only {student_data['Sleep Duration']} hours of sleep, below recommended levels.",
                "actions": [
                    "Provide sleep hygiene resources",
                    "Discuss impact of sleep on mental health",
                    "Consider sleep improvement workshop"
                ],
                "priority": "Medium",
                "color": "#F57C00"
            })

    # Academic pressure
    if "Academic Pressure" in student_data.index:
        if str(student_data["Academic Pressure"]).lower() in ["high", "very high", "4", "5"]:
            recommendations.append({
                "title": "Academic pressure management",
                "description": "Student reports high academic pressure.",
                "actions": [
                    "Review course load and deadlines",
                    "Provide time management resources",
                    "Connect with academic support services"
                ],
                "priority": "Medium",
                "color": "#F57C00"
            })

    # Financial stress
    if "Financial Stress" in student_data.index:
        if str(student_data["Financial Stress"]).lower() in ["high", "very high", "4", "5"]:
            recommendations.append({
                "title": "Financial stress support",
                "description": "Student reports high financial stress.",
                "actions": [
                    "Refer to financial aid office",
                    "Provide information about scholarships or work-study",
                    "Consider emergency financial assistance if available"
                ],
                "priority": "Medium",
                "color": "#F57C00"
            })

    # Display recommendations
    for i, rec in enumerate(recommendations):
        st.markdown(f"""
            <div style="border-left: 5px solid {rec['color']}; padding: 10px; margin-bottom: 20px; background-color: #f5f5f5;">
                <h4 style="color: {rec['color']}; margin-top: 0;">{i+1}. {rec['title']}</h4>
                <p><strong>Priority:</strong> {rec['priority']} | {rec['description']}</p>
                <p><strong>Recommended Actions:</strong></p>
                <ul>
                    {"".join([f"<li>{action}</li>" for action in rec['actions']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Action plan
    st.markdown("<h3 class='sub-header'>Action Plan</h3>",
                unsafe_allow_html=True)

    # Simple form to document actions
    action_taken = st.text_area("Document actions taken:", height=100)
    follow_up_date = st.date_input("Schedule follow-up:")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Save Action Plan", use_container_width=True):
            # In a real application, this would save the data to a database
            st.success("Action plan saved successfully.")

            # Here we'll just store it in session state for demonstration
            if "action_plans" not in st.session_state:
                st.session_state.action_plans = {}

            st.session_state.action_plans[student_index] = {
                "action_taken": action_taken,
                "follow_up_date": follow_up_date,
                "date_created": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
