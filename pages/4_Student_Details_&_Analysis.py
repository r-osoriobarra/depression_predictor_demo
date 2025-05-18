import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from utils import set_page_style, check_login, check_data, categorize_risk
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

st.set_page_config(page_title="Student Detail", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Student Depression Risk Analysis</h1>",
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

# Load model and preprocessing tools
@st.cache_resource
def load_model():
    with open("model/depression_model.pkl", "rb") as f_model:
        model = pickle.load(f_model)
    with open("model/preprocessor.pkl", "rb") as f_pre:
        preprocessor = pickle.load(f_pre)
    with open("model/feature_columns.pkl", "rb") as f_cols:
        feature_columns = pickle.load(f_cols)
    return model, preprocessor, feature_columns

try:
    model, preprocessor, feature_columns = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Retrieve student information
df = st.session_state["latest_df"]
student_index = st.session_state["selected_student_index"]
student_data = df.loc[student_index]

# Determine risk category and color
risk_score = student_data["Depression Risk (%)"]
risk_category, risk_color = categorize_risk(risk_score)

# Get student ID for display
if 'id' in student_data.index:
    student_display_id = student_data['id']
elif 'ID' in student_data.index:
    student_display_id = student_data['ID']
else:
    student_display_id = student_index

# Custom CSS
st.markdown("""
<style>
.main-container {
    border: 2px solid white;
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    background-color: transparent;
}
.risk-breakdown-container {
    border: 2px solid white;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 30px;
    background-color: transparent;
}
.recommendation-container {
    border: 2px solid white;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    background-color: transparent;
}
.concern-item {
    border: 2px solid;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    background-color: #f8f9fa;
}
.protective-item {
    border: 2px solid #388E3C;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    background-color: #f1f8e9;
}
.recommendation-item {
    border-left: 5px solid;
    padding: 15px;
    margin-bottom: 20px;
    background-color: #f8f9fa;
    border-radius: 0 10px 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ===== SECTION 1: STUDENT OVERVIEW =====
st.markdown(f"""
    <div class="main-container">
        <div style="text-align: center;">
            <h2 style="margin: 0; color: white; font-size: 2.5rem;">Student {student_display_id}</h2>
            <div style="margin: 20px 0;">
                <h3 style="margin: 10px 0; color: {risk_color}; font-size: 2rem;">{risk_category} Risk</h3>
                <p style="font-size: 3.5rem; font-weight: bold; margin: 0; color: {risk_color};">{round(risk_score, 1)}%</p>
                <p style="color: #CCCCCC; margin-top: 10px; font-size: 1.2rem;">Depression Risk Score</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ===== SECTION 2: RISK FACTORS ANALYSIS =====
st.markdown("""
    <div class="risk-breakdown-container">
        <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Risk Factors Assessment</h3>
        <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">Identifying factors that require attention and protective factors</p>
""", unsafe_allow_html=True)

# Define factor analysis rules
def analyze_factor(feature_name, student_value, df):
    """Analyze if a factor needs attention based on student's value compared to population"""
    
    # Skip non-feature columns
    if feature_name in ["id", "ID", "student_id", "Student ID", "Depression Risk (%)", "Risk Category"]:
        return None
    
    # Get population stats for this feature
    if feature_name not in df.columns:
        return None
    
    # Numeric factors analysis
    if pd.api.types.is_numeric_dtype(df[feature_name]):
        avg_value = df[feature_name].mean()
        percentile = (df[feature_name] <= student_value).mean() * 100
        
        # Academic Pressure (higher is worse)
        if feature_name == "Academic Pressure":
            if student_value >= 8:
                return {
                    "concern_level": "high",
                    "explanation": f"Very high academic pressure ({student_value}/10)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "High academic pressure is strongly linked to depression risk",
                    "icon": "📚"
                }
            elif student_value >= 6:
                return {
                    "concern_level": "medium",
                    "explanation": f"Elevated academic pressure ({student_value}/10)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "Moderate academic pressure may affect mental health",
                    "icon": "📝"
                }
            else:
                return {
                    "concern_level": "protective",
                    "explanation": f"Low academic pressure ({student_value}/10)",
                    "comparison": f"Lower than {100-percentile:.0f}% of students",
                    "why_concerning": "Low academic pressure is protective for mental health",
                    "icon": "✅"
                }
        
        # Financial Stress (higher is worse)
        elif feature_name == "Financial Stress":
            if student_value >= 7:
                return {
                    "concern_level": "high",
                    "explanation": f"High financial stress ({student_value}/10)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "Financial stress significantly impacts mental health and academic performance",
                    "icon": "💰"
                }
            elif student_value >= 5:
                return {
                    "concern_level": "medium",
                    "explanation": f"Moderate financial stress ({student_value}/10)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "Financial concerns can contribute to depression risk",
                    "icon": "💳"
                }
        
        # CGPA (lower is worse)
        elif feature_name == "CGPA":
            if student_value < 2.5:
                return {
                    "concern_level": "high",
                    "explanation": f"Low academic performance (CGPA: {student_value})",
                    "comparison": f"Lower than {100-percentile:.0f}% of students",
                    "why_concerning": "Low academic performance often correlates with mental health struggles",
                    "icon": "📉"
                }
            elif student_value < 3.0:
                return {
                    "concern_level": "medium",
                    "explanation": f"Below-average academic performance (CGPA: {student_value})",
                    "comparison": f"Lower than {100-percentile:.0f}% of students",
                    "why_concerning": "Academic difficulties may indicate underlying issues",
                    "icon": "📊"
                }
            elif student_value >= 3.5:
                return {
                    "concern_level": "protective",
                    "explanation": f"Good academic performance (CGPA: {student_value})",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "Strong academic performance is protective for mental health",
                    "icon": "🎓"
                }
        
        # Work/Study Hours (excessive hours are concerning)
        elif feature_name == "Work/Study Hours":
            if student_value >= 10:
                return {
                    "concern_level": "high",
                    "explanation": f"Excessive work/study load ({student_value} hours/day)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "Overcommitment can lead to burnout and mental health issues",
                    "icon": "⏰"
                }
            elif student_value >= 8:
                return {
                    "concern_level": "medium",
                    "explanation": f"Heavy work/study load ({student_value} hours/day)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "High workload may contribute to stress and depression",
                    "icon": "📚"
                }
        
        # Age (no specific concern levels, just informational)
        elif feature_name == "Age":
            return None  # Age is generally not a direct concern factor
        
        # Study Satisfaction (lower is worse)
        elif feature_name == "Study Satisfaction":
            if student_value <= 3:
                return {
                    "concern_level": "high",
                    "explanation": f"Very low study satisfaction ({student_value}/10)",
                    "comparison": f"Lower than {100-percentile:.0f}% of students",
                    "why_concerning": "Low satisfaction with studies strongly predicts depression risk",
                    "icon": "😞"
                }
            elif student_value <= 5:
                return {
                    "concern_level": "medium",
                    "explanation": f"Below-average study satisfaction ({student_value}/10)",
                    "comparison": f"Lower than {100-percentile:.0f}% of students",
                    "why_concerning": "Dissatisfaction with studies can contribute to mental health issues",
                    "icon": "😐"
                }
            elif student_value >= 8:
                return {
                    "concern_level": "protective",
                    "explanation": f"High study satisfaction ({student_value}/10)",
                    "comparison": f"Higher than {percentile:.0f}% of students",
                    "why_concerning": "High satisfaction with studies is protective for mental health",
                    "icon": "😊"
                }
    
    # Categorical factors analysis
    else:
        # Sleep Duration
        if feature_name == "Sleep Duration":
            if "Less than" in str(student_value) or "5" in str(student_value):
                return {
                    "concern_level": "high",
                    "explanation": f"Insufficient sleep ({student_value})",
                    "comparison": "Below recommended 6-8 hours",
                    "why_concerning": "Sleep deprivation is strongly linked to depression and impacts cognitive function",
                    "icon": "😴"
                }
            elif "More than 8" in str(student_value):
                return {
                    "concern_level": "medium",
                    "explanation": f"Excessive sleep ({student_value})",
                    "comparison": "Above typical 6-8 hours",
                    "why_concerning": "Oversleeping can be a sign of depression or other health issues",
                    "icon": "😪"
                }
            else:
                return {
                    "concern_level": "protective",
                    "explanation": f"Adequate sleep ({student_value})",
                    "comparison": "Within recommended range",
                    "why_concerning": "Good sleep patterns support mental health",
                    "icon": "✅"
                }
        
        # Suicidal Thoughts
        elif feature_name == "Have you ever had suicidal thoughts ?":
            if str(student_value).lower() in ["yes", "sometimes", "1", "true"]:
                return {
                    "concern_level": "critical",
                    "explanation": "History of suicidal thoughts",
                    "comparison": "Requires immediate attention",
                    "why_concerning": "Suicidal ideation is a critical risk factor requiring immediate intervention",
                    "icon": "🚨"
                }
            else:
                return {
                    "concern_level": "protective",
                    "explanation": "No history of suicidal thoughts",
                    "comparison": "Positive mental health indicator",
                    "why_concerning": "Absence of suicidal thoughts is protective",
                    "icon": "✅"
                }
        
        # Family History of Mental Illness
        elif feature_name == "Family History of Mental Illness":
            if str(student_value).lower() in ["yes", "1", "true"]:
                return {
                    "concern_level": "medium",
                    "explanation": "Family history of mental illness",
                    "comparison": "Genetic predisposition present",
                    "why_concerning": "Family history increases vulnerability to depression",
                    "icon": "🧬"
                }
            else:
                return {
                    "concern_level": "protective",
                    "explanation": "No family history of mental illness",
                    "comparison": "No known genetic predisposition",
                    "why_concerning": "Absence of family history is protective",
                    "icon": "✅"
                }
        
        # Dietary Habits
        elif feature_name == "Dietary Habits":
            if str(student_value).lower() in ["unhealthy", "poor"]:
                return {
                    "concern_level": "medium",
                    "explanation": "Poor dietary habits",
                    "comparison": "Below optimal nutrition",
                    "why_concerning": "Poor nutrition can affect mood and energy levels",
                    "icon": "🍔"
                }
            elif str(student_value).lower() in ["healthy", "good"]:
                return {
                    "concern_level": "protective",
                    "explanation": "Healthy dietary habits",
                    "comparison": "Good nutritional practices",
                    "why_concerning": "Good nutrition supports mental health",
                    "icon": "🥗"
                }
    
    return None

# Analyze all factors for this student
concern_factors = []
protective_factors = []

for feature in feature_columns:
    if feature in student_data.index:
        analysis = analyze_factor(feature, student_data[feature], df)
        if analysis:
            if analysis["concern_level"] in ["critical", "high", "medium"]:
                concern_factors.append((feature, analysis))
            elif analysis["concern_level"] == "protective":
                protective_factors.append((feature, analysis))

# Sort by concern level (critical first, then high, then medium)
concern_order = {"critical": 0, "high": 1, "medium": 2}
concern_factors.sort(key=lambda x: concern_order[x[1]["concern_level"]])

# Display the analysis in two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h4 style='color: white; margin-bottom: 20px;'>⚠️ Factors Requiring Attention</h4>", unsafe_allow_html=True)
    
    if concern_factors:
        for feature_name, analysis in concern_factors:
            # Define colors and borders based on concern level
            if analysis["concern_level"] == "critical":
                border_color = "#B71C1C"
                bg_color = "#ffebee"
                text_color = "#B71C1C"
            elif analysis["concern_level"] == "high":
                border_color = "#D32F2F"
                bg_color = "#ffebee"
                text_color = "#D32F2F"
            else:  # medium
                border_color = "#F57C00"
                bg_color = "#fff8e1"
                text_color = "#F57C00"
            
            st.markdown(f"""
                <div class="concern-item" style="border-color: {border_color}; background-color: {bg_color};">
                    <h5 style="margin-top: 0; margin-bottom: 8px; color: {text_color};">
                        {analysis['icon']} {feature_name.replace('_', ' ').title()}
                    </h5>
                    <p style="margin-bottom: 6px; font-weight: bold; color: #333;">
                        {analysis['explanation']}
                    </p>
                    <p style="margin-bottom: 6px; color: #666; font-size: 0.9em;">
                        📊 {analysis['comparison']}
                    </p>
                    <p style="margin-bottom: 0; color: #555; font-size: 0.9em; font-style: italic;">
                        💡 {analysis['why_concerning']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="padding: 20px; text-align: center; color: #666; font-style: italic;">
                🎉 No concerning factors identified
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("<h4 style='color: white; margin-bottom: 20px;'>✅ Protective Factors</h4>", unsafe_allow_html=True)
    
    if protective_factors:
        for feature_name, analysis in protective_factors:
            st.markdown(f"""
                <div class="protective-item">
                    <h5 style="margin-top: 0; margin-bottom: 8px; color: #2E7D32;">
                        {analysis['icon']} {feature_name.replace('_', ' ').title()}
                    </h5>
                    <p style="margin-bottom: 6px; font-weight: bold; color: #333;">
                        {analysis['explanation']}
                    </p>
                    <p style="margin-bottom: 6px; color: #666; font-size: 0.9em;">
                        📊 {analysis['comparison']}
                    </p>
                    <p style="margin-bottom: 0; color: #555; font-size: 0.9em; font-style: italic;">
                        💡 {analysis['why_concerning']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="padding: 20px; text-align: center; color: #666; font-style: italic;">
                No clear protective factors identified
            </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ===== SECTION 3: RECOMMENDATIONS =====
st.markdown("""
    <div class="recommendation-container">
        <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Personalized Recommendations</h3>
        <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">Evidence-based interventions based on identified risk factors</p>
""", unsafe_allow_html=True)

# Generate recommendations based on the factors identified
recommendations = []

# Critical recommendations (suicidal thoughts)
for feature_name, analysis in concern_factors:
    if analysis["concern_level"] == "critical":
        recommendations.append({
            "title": "🆘 IMMEDIATE CRISIS INTERVENTION",
            "description": "Student has reported suicidal thoughts - emergency protocol required",
            "actions": [
                "Activate crisis intervention protocol immediately",
                "Ensure student is not left alone",
                "Contact mental health crisis team",
                "Provide 24/7 crisis hotline numbers",
                "Schedule emergency psychiatric evaluation",
                "Follow up within 24 hours"
            ],
            "priority": "CRITICAL",
            "color": "#B71C1C"
        })

# Primary risk-based recommendations
if risk_category == "High":
    recommendations.append({
        "title": "🚨 High-Priority Mental Health Support",
        "description": "High risk score requires immediate professional attention",
        "actions": [
            "Schedule counseling appointment within 24-48 hours",
            "Provide comprehensive mental health resource packet",
            "Implement weekly check-ins with student services",
            "Consider academic accommodations if needed",
            "Ensure emergency contact information is current"
        ],
        "priority": "URGENT",
        "color": "#D32F2F"
    })
elif risk_category == "Medium":
    recommendations.append({
        "title": "⚠️ Proactive Mental Health Support",
        "description": "Moderate risk requires preventive intervention",
        "actions": [
            "Schedule counseling screening within 1-2 weeks",
            "Provide stress management resources",
            "Implement bi-weekly wellness check-ins",
            "Connect with campus support groups",
            "Monitor academic performance closely"
        ],
        "priority": "HIGH",
        "color": "#F57C00"
    })

# Factor-specific recommendations
for feature_name, analysis in concern_factors:
    if analysis["concern_level"] in ["high", "medium"]:
        
        # Sleep-related interventions
        if "Sleep" in feature_name:
            recommendations.append({
                "title": "😴 Sleep Health Intervention",
                "description": f"Addressing sleep concerns: {analysis['explanation']}",
                "actions": [
                    "Provide sleep hygiene education materials",
                    "Recommend 2-week sleep tracking diary",
                    "Assess sleep environment and habits",
                    "Screen for sleep disorders if needed",
                    "Consider referral to sleep specialist"
                ],
                "priority": "MEDIUM",
                "color": "#9C27B0"
            })
        
        # Academic pressure interventions
        elif "Academic Pressure" in feature_name:
            recommendations.append({
                "title": "📚 Academic Stress Management",
                "description": f"High academic pressure intervention: {analysis['explanation']}",
                "actions": [
                    "Schedule academic advisor meeting",
                    "Provide time management workshop resources",
                    "Assess current course load appropriateness",
                    "Connect with tutoring services if needed",
                    "Teach stress reduction techniques",
                    "Consider course load adjustment"
                ],
                "priority": "MEDIUM",
                "color": "#3F51B5"
            })
        
        # Financial stress interventions
        elif "Financial" in feature_name:
            recommendations.append({
                "title": "💰 Financial Support Services",
                "description": f"Financial stress intervention: {analysis['explanation']}",
                "actions": [
                    "Connect with financial aid counselor",
                    "Assess eligibility for emergency assistance",
                    "Provide financial literacy resources",
                    "Explore work-study opportunities",
                    "Connect with food bank/basic needs support",
                    "Financial planning workshop referral"
                ],
                "priority": "MEDIUM",
                "color": "#4CAF50"
            })
        
        # Academic performance interventions
        elif "CGPA" in feature_name:
            recommendations.append({
                "title": "📈 Academic Success Support",
                "description": f"Academic performance intervention: {analysis['explanation']}",
                "actions": [
                    "Academic success center evaluation",
                    "Learning specialist assessment",
                    "Study skills workshop enrollment",
                    "Tutoring services connection",
                    "Learning accommodation screening",
                    "Academic recovery planning"
                ],
                "priority": "MEDIUM",
                "color": "#FF9800"
            })
        
        # Study satisfaction interventions
        elif "Study Satisfaction" in feature_name:
            recommendations.append({
                "title": "🎯 Academic Engagement Enhancement",
                "description": f"Low study satisfaction intervention: {analysis['explanation']}",
                "actions": [
                    "Career counseling consultation",
                    "Academic major/minor exploration",
                    "Connect with faculty mentorship programs",
                    "Explore research opportunities",
                    "Consider campus involvement activities"
                ],
                "priority": "MEDIUM",
                "color": "#795548"
            })
        
        # Work/study hours interventions
        elif "Work/Study Hours" in feature_name and analysis["concern_level"] in ["high", "medium"]:
            recommendations.append({
                "title": "⚖️ Work-Life Balance Support",
                "description": f"Excessive workload intervention: {analysis['explanation']}",
                "actions": [
                    "Time management skills assessment",
                    "Work schedule optimization review",
                    "Stress management workshop participation",
                    "Explore reducing work hours if possible",
                    "Burnout prevention education"
                ],
                "priority": "MEDIUM",
                "color": "#607D8B"
            })

# If no concerning factors but still medium/high risk, add general support
if not any(factor[1]["concern_level"] in ["critical", "high"] for factor in concern_factors) and risk_category in ["Medium", "High"]:
    recommendations.append({
        "title": "🔍 Comprehensive Assessment",
        "description": "Risk score indicates need for evaluation despite no clear individual factors",
        "actions": [
            "Schedule comprehensive mental health assessment",
            "Explore potential underlying factors not captured",
            "Consider recent life events or changes",
            "Assess social support systems",
            "Evaluate coping strategies"
        ],
        "priority": "MEDIUM",
        "color": "#673AB7"
    })

# Low risk general wellness
if risk_category == "Low":
    recommendations.append({
        "title": "✅ Wellness Maintenance",
        "description": "Continue supporting good mental health practices",
        "actions": [
            "Provide general wellness resources",
            "Encourage continued healthy habits",
            "Semi-annual wellness check-ins",
            "Campus activity participation",
            "Stress prevention education"
        ],
        "priority": "STANDARD",
        "color": "#388E3C"
    })

# Display recommendations
for i, rec in enumerate(recommendations):
    st.markdown(f"""
        <div class="recommendation-item" style="border-left-color: {rec['color']};">
            <h4 style="color: {rec['color']}; margin-top: 0; margin-bottom: 8px;">{rec['title']}</h4>
            <p style="margin-bottom: 8px; color: #666;">
                <strong>Priority:</strong> <span style="color: {rec['color']}; font-weight: bold;">{rec['priority']}</span>
            </p>
            <p style="margin-bottom: 12px; color: #333;">{rec['description']}</p>
            <div style="margin-bottom: 0;">
                <strong style="color: #333;">Recommended Actions:</strong>
                <ul style="margin-top: 8px; margin-bottom: 0;">
                    {"".join([f"<li style='margin-bottom: 4px; color: #555;'>{action}</li>" for action in rec['actions']])}
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Navigation buttons
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Student List", use_container_width=True):
        st.switch_page("pages/3_Student_List.py")

with col2:
    if st.button("📊 Overview Dashboard", use_container_width=True):
        st.switch_page("pages/2_Predict.py")

with col3:
    if st.button("📋 Generate Report", use_container_width=True):
        st.info("Report generation feature coming soon!")