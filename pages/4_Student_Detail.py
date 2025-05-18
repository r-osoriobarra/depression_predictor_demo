import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from utils import set_page_style, check_login, check_data, categorize_risk
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

st.set_page_config(page_title="Student Detail", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Student Risk Detail Analysis</h1>",
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

# Student header with risk indicator
st.markdown("""
<style>
.student-header-container {
    border: 2px solid white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 30px;
    background-color: transparent;
}
.info-container {
    border: 2px solid white;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    background-color: transparent;
}
.recommendation-container {
    border-left: 5px solid;
    padding: 15px;
    margin-bottom: 20px;
    background-color: #f5f5f5;
    border-radius: 0 10px 10px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="student-header-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 0; color: white;">Student {student_display_id}</h2>
                <p style="margin: 5px 0 0 0; color: #CCCCCC;">{student_data.get("Degree", "Student")}</p>
            </div>
            <div style="text-align: right;">
                <h3 style="margin: 0; color: {risk_color};">{risk_category} Risk</h3>
                <p style="font-size: 32px; font-weight: bold; margin: 0; color: {risk_color};">{round(risk_score, 1)}%</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create tabs for different views of student data
tab1, tab2, tab3 = st.tabs(["Student Profile", "Risk Analysis", "Recommendations"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Basic Information Container
        basic_attrs = ["Gender", "Age", "CGPA", "Degree"]
        basic_info_content = "<h4 style='margin-top: 0; color: white;'>Basic Information</h4>"
        
        for attr in basic_attrs:
            if attr in student_data.index:
                basic_info_content += f"<p style='margin: 8px 0; color: white;'><strong>{attr}:</strong> {student_data[attr]}</p>"
        
        st.markdown(f"""
            <div class="info-container">
                {basic_info_content}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Mental Health Indicators Container
        health_attrs = [
            "Academic Pressure", "Study Satisfaction", "Sleep Duration",
            "Financial Stress", "Family History of Mental Illness",
            "Have you ever had suicidal thoughts ?", "Work/Study Hours"
        ]
        
        mh_info_content = "<h4 style='margin-top: 0; color: white;'>Mental Health Indicators</h4>"
        has_indicators = False
        
        for attr in health_attrs:
            if attr in student_data.index:
                has_indicators = True
                value = student_data[attr]
                
                # Add warning indicators for critical values
                warning = ""
                if attr == "Have you ever had suicidal thoughts ?" and str(value).lower() in ["yes", "sometimes", "1", "true"]:
                    warning = " <span style='color: #FF4444;'>⚠️ URGENT</span>"
                elif attr == "Sleep Duration" and "Less than" in str(value):
                    warning = " <span style='color: #FFA500;'>⚠️</span>"
                elif attr == "Academic Pressure" and isinstance(value, (int, float)) and value > 7:
                    warning = " <span style='color: #FFA500;'>⚠️</span>"
                
                mh_info_content += f"<p style='margin: 8px 0; color: white;'><strong>{attr}:</strong> {value}{warning}</p>"
        
        if not has_indicators:
            mh_info_content += "<p style='color: #CCCCCC; font-style: italic;'>No detailed mental health indicators available for this student.</p>"
        
        st.markdown(f"""
            <div class="info-container">
                {mh_info_content}
            </div>
        """, unsafe_allow_html=True)

with tab2:
    # Risk Analysis Section
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<h3 class='sub-header'>Risk Assessment</h3>", unsafe_allow_html=True)
        
        # Risk gauge visualization
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
        ax.set_thetamin(0)
        ax.set_thetamax(180)
        
        # Create colored segments
        low_color = '#388E3C'
        medium_color = '#F57C00'
        high_color = '#D32F2F'
        
        # Draw the gauge segments
        theta = np.linspace(0, np.pi, 100)
        for i, (start, end, color, label) in enumerate([(0, 30, low_color, 'Low'), 
                                                        (30, 70, medium_color, 'Medium'), 
                                                        (70, 100, high_color, 'High')]):
            start_theta = start * np.pi / 100
            end_theta = end * np.pi / 100
            theta_seg = np.linspace(start_theta, end_theta, 50)
            ax.fill_between(theta_seg, 0, 80, color=color, alpha=0.3)
            # Add labels
            mid_theta = (start_theta + end_theta) / 2
            ax.text(mid_theta, 90, label, ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Add the needle
        needle_theta = risk_score * np.pi / 100
        ax.plot([needle_theta, needle_theta], [0, 75], 'k-', linewidth=4)
        ax.plot(needle_theta, 75, 'ko', markersize=8)
        
        # Add risk score text
        ax.text(np.pi/2, -15, f'{round(risk_score, 1)}%', ha='center', va='center', 
                fontsize=20, fontweight='bold', color=risk_color)
        
        ax.set_ylim(0, 100)
        ax.set_rticks([])
        ax.grid(False)
        ax.spines['polar'].set_visible(False)
        
        st.pyplot(fig)
        
        # Comparison with averages
        st.markdown("<h4>Comparison with Averages</h4>", unsafe_allow_html=True)
        
        numeric_attrs = ['Age', 'CGPA', 'Academic Pressure', 'Financial Stress', 'Work/Study Hours']
        for attr in numeric_attrs:
            if attr in student_data.index and attr in df.columns:
                student_val = student_data[attr]
                avg_val = df[attr].mean()
                
                if isinstance(student_val, (int, float)):
                    diff = student_val - avg_val
                    color = "red" if diff > 0 and attr in ['Academic Pressure', 'Financial Stress'] else "green" if diff > 0 else "red"
                    arrow = "↑" if diff > 0 else "↓"
                    st.markdown(f"**{attr}:** {student_val} {arrow} (Avg: {avg_val:.1f})")

    with col2:
        st.markdown("<h3 class='sub-header'>Feature Contribution Analysis</h3>", unsafe_allow_html=True)
        
        # Feature importance analysis
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            
            # Get prediction for this student
            X_student = df.loc[[student_index]][feature_columns]
            X_student_transformed = preprocessor.transform(X_student)
            
            # Calculate feature contributions
            valid_features = []
            valid_importances = []
            student_values = []
            
            for i, feature in enumerate(feature_columns):
                if feature not in ["id", "ID", "student_id", "Student ID"]:
                    valid_features.append(feature)
                    valid_importances.append(importances[i])
                    student_values.append(student_data.get(feature, "N/A"))
            
            # Calculate contribution percentages
            total_importance = sum(valid_importances)
            contribution_percentages = [(imp / total_importance) * 100 for imp in valid_importances]
            
            # Determine effect direction
            contribution_effects = []
            numeric_features = df[valid_features].select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            for i, feature in enumerate(valid_features):
                feature_value = student_values[i]
                
                if feature in numeric_features:
                    try:
                        avg_value = df[feature].mean()
                        feature_value = float(feature_value)
                        effect = "Increases risk" if feature_value > avg_value else "Decreases risk"
                    except:
                        effect = "Unknown effect"
                else:
                    try:
                        grouped = df.groupby(feature)["Depression Risk (%)"].mean()
                        avg_risk = df["Depression Risk (%)"].mean()
                        cat_risk = grouped.get(feature_value, avg_risk)
                        effect = "Increases risk" if cat_risk > avg_risk else "Decreases risk"
                    except:
                        effect = "Unknown effect"
                
                contribution_effects.append(effect)
            
            # Create contribution dataframe
            contribution_data = []
            for i, feature in enumerate(valid_features):
                contribution_data.append({
                    "Feature": feature,
                    "Value": student_values[i],
                    "Contribution (%)": contribution_percentages[i],
                    "Effect": contribution_effects[i]
                })
            
            contribution_df = pd.DataFrame(contribution_data)
            contribution_df = contribution_df.sort_values("Contribution (%)", ascending=False)
            
            # Plot top contributors
            fig, ax = plt.subplots(figsize=(10, 6))
            top_contributors = contribution_df.head(8)
            
            colors = ['#D32F2F' if effect == "Increases risk" else '#388E3C' 
                     for effect in top_contributors["Effect"]]
            
            bars = ax.barh(range(len(top_contributors)), top_contributors["Contribution (%)"], color=colors, alpha=0.7)
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                       f'{width:.1f}%', va='center', ha='left')
            
            ax.set_yticks(range(len(top_contributors)))
            ax.set_yticklabels(top_contributors["Feature"])
            ax.set_xlabel('Contribution to Depression Risk (%)')
            ax.set_title('Top Contributing Factors')
            ax.invert_yaxis()
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#D32F2F', alpha=0.7, label='Increases Risk'),
                Patch(facecolor='#388E3C', alpha=0.7, label='Decreases Risk')
            ]
            ax.legend(handles=legend_elements, loc='lower right')
            
            st.pyplot(fig)
            
            # Show detailed contribution table
            st.markdown("<h4>Detailed Feature Analysis</h4>", unsafe_allow_html=True)
            
            # Format the dataframe for display
            display_df = contribution_df.copy()
            display_df["Contribution (%)"] = display_df["Contribution (%)"].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(display_df.head(10), hide_index=True)

with tab3:
    st.markdown("<h3 class='sub-header'>Personalized Recommendations</h3>", unsafe_allow_html=True)
    
    # Generate recommendations based on risk level and specific factors
    recommendations = []
    
    # Primary risk-based recommendations
    if risk_category == "High":
        recommendations.append({
            "title": "🚨 Urgent Intervention Required",
            "description": "Student shows high risk of depression and requires immediate professional attention.",
            "actions": [
                "Schedule immediate wellness check within 24-48 hours",
                "Provide emergency counseling contact information",
                "Implement daily check-in protocol",
                "Connect with campus mental health services"
            ],
            "priority": "URGENT",
            "color": "#D32F2F"
        })
    elif risk_category == "Medium":
        recommendations.append({
            "title": "⚠️ Active Monitoring Recommended",
            "description": "Student shows moderate risk and would benefit from supportive interventions.",
            "actions": [
                "Schedule wellness check within 1-2 weeks",
                "Provide mental health resource information",
                "Monitor academic performance closely",
                "Encourage participation in stress management workshops"
            ],
            "priority": "MEDIUM",
            "color": "#F57C00"
        })
    else:
        recommendations.append({
            "title": "✅ Preventive Support",
            "description": "Student shows low risk but can benefit from preventive measures.",
            "actions": [
                "Include in general wellness programs",
                "Provide stress management resources",
                "Monitor during high-stress periods (exams, deadlines)",
                "Encourage healthy lifestyle habits"
            ],
            "priority": "STANDARD",
            "color": "#388E3C"
        })
    
    # Factor-specific recommendations
    
    # Suicidal thoughts - highest priority
    if "Have you ever had suicidal thoughts ?" in student_data.index:
        if str(student_data["Have you ever had suicidal thoughts ?"]).lower() in ["yes", "sometimes", "1", "true"]:
            recommendations.insert(0, {
                "title": "🆘 CRITICAL: Suicidal Ideation Detected",
                "description": "Student has reported suicidal thoughts - immediate intervention required.",
                "actions": [
                    "Implement immediate safety protocol",
                    "Contact crisis intervention team",
                    "Refer to mental health professional immediately",
                    "Ensure 24/7 support contact information",
                    "Follow up within 24 hours"
                ],
                "priority": "EMERGENCY",
                "color": "#B71C1C"
            })
    
    # Sleep issues
    if "Sleep Duration" in student_data.index:
        sleep_val = str(student_data["Sleep Duration"])
        if "Less than" in sleep_val or "5" in sleep_val:
            recommendations.append({
                "title": "😴 Sleep Improvement Program",
                "description": f"Student reports insufficient sleep ({sleep_val}), which impacts mental health.",
                "actions": [
                    "Provide sleep hygiene education materials",
                    "Recommend sleep tracking for 1-2 weeks",
                    "Discuss environmental factors affecting sleep",
                    "Consider referral to sleep specialist if needed"
                ],
                "priority": "MEDIUM",
                "color": "#9C27B0"
            })
    
    # Academic pressure
    if "Academic Pressure" in student_data.index:
        pressure_val = student_data["Academic Pressure"]
        if isinstance(pressure_val, (int, float)) and pressure_val > 7:
            recommendations.append({
                "title": "📚 Academic Stress Management",
                "description": f"Student reports high academic pressure (Level {pressure_val}/10).",
                "actions": [
                    "Review current course load and deadlines",
                    "Connect with academic advisor",
                    "Provide time management and study skills resources",
                    "Consider tutoring support if needed",
                    "Discuss realistic goal setting"
                ],
                "priority": "MEDIUM",
                "color": "#3F51B5"
            })
    
    # Financial stress
    if "Financial Stress" in student_data.index:
        financial_val = student_data["Financial Stress"]
        if isinstance(financial_val, (int, float)) and financial_val > 6:
            recommendations.append({
                "title": "💰 Financial Support Services",
                "description": f"Student reports significant financial stress (Level {financial_val}/10).",
                "actions": [
                    "Refer to financial aid office",
                    "Provide information about emergency financial assistance",
                    "Connect with work-study opportunities",
                    "Discuss budgeting and financial literacy resources"
                ],
                "priority": "MEDIUM",
                "color": "#4CAF50"
            })
    
    # Low CGPA
    if "CGPA" in student_data.index:
        cgpa_val = student_data["CGPA"]
        if isinstance(cgpa_val, (int, float)) and cgpa_val < 3.0:
            recommendations.append({
                "title": "📈 Academic Support Services",
                "description": f"Student's CGPA ({cgpa_val}) indicates need for academic support.",
                "actions": [
                    "Connect with academic success center",
                    "Assess for learning difficulties",
                    "Provide study skills training",
                    "Consider reduced course load if appropriate"
                ],
                "priority": "MEDIUM",
                "color": "#FF9800"
            })
    
    # Display recommendations
    for i, rec in enumerate(recommendations):
        st.markdown(f"""
            <div class="recommendation-container" style="border-left-color: {rec['color']};">
                <h4 style="color: {rec['color']}; margin-top: 0;">{rec['title']}</h4>
                <p style="margin-bottom: 10px;"><strong>Priority:</strong> <span style="color: {rec['color']};">{rec['priority']}</span></p>
                <p style="margin-bottom: 15px;">{rec['description']}</p>
                <p style="margin-bottom: 10px;"><strong>Recommended Actions:</strong></p>
                <ul style="margin-bottom: 0;">
                    {"".join([f"<li style='margin-bottom: 5px;'>{action}</li>" for action in rec['actions']])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # Action planning section
    st.markdown("<h3 class='sub-header'>Action Plan Documentation</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        action_taken = st.text_area("Document actions taken:", height=120, 
                                   placeholder="Record any interventions, contacts made, or resources provided...")
        follow_up_date = st.date_input("Schedule follow-up date:", 
                                      value=pd.Timestamp.now().date() + pd.Timedelta(days=7))
    
    with col2:
        priority_level = st.selectbox("Priority Level:", 
                                    ["Low", "Medium", "High", "Urgent", "Emergency"])
        assigned_to = st.text_input("Assigned to:", 
                                  placeholder="Enter name of responsible staff member")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_save, col_export = st.columns(2)
        with col_save:
            if st.button("💾 Save Action Plan", use_container_width=True):
                # Store action plan in session state
                if "action_plans" not in st.session_state:
                    st.session_state.action_plans = {}
                
                st.session_state.action_plans[student_index] = {
                    "student_id": student_display_id,
                    "risk_score": risk_score,
                    "risk_category": risk_category,
                    "action_taken": action_taken,
                    "follow_up_date": follow_up_date,
                    "priority_level": priority_level,
                    "assigned_to": assigned_to,
                    "date_created": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "recommendations_count": len(recommendations)
                }
                
                st.success("✅ Action plan saved successfully!")
        
        with col_export:
            if st.button("📋 Generate Report", use_container_width=True):
                st.info("Report generation feature coming soon!")

# Quick navigation
st.markdown("<br><hr><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Student List", use_container_width=True):
        st.switch_page("pages/3_Student_List.py")

with col2:
    if st.button("🔄 Feature Analysis", use_container_width=True):
        st.switch_page("pages/5_Prediction_Analysis.py")

with col3:
    if st.button("📊 Overview Dashboard", use_container_width=True):
        st.switch_page("pages/2_Predict.py")