# pages/4_Student_Detail.py
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

# ===== SECTION 2: RISK BREAKDOWN =====
st.markdown("""
   <div class="risk-breakdown-container">
       <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Risk Score Breakdown</h3>
       <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">Understanding which factors contribute most to this student's depression risk</p>
""", unsafe_allow_html=True)

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
   risk_levels = []
   numeric_features = df[valid_features].select_dtypes(include=['int64', 'float64']).columns.tolist()
   
   for i, feature in enumerate(valid_features):
       feature_value = student_values[i]
       
       if feature in numeric_features:
           try:
               avg_value = df[feature].mean()
               feature_value = float(feature_value)
               effect = "Increases risk" if feature_value > avg_value else "Decreases risk"
               
               # Determine risk level for this factor
               percentile = (df[feature] <= feature_value).mean() * 100
               if feature in ['Academic Pressure', 'Financial Stress', 'Work/Study Hours']:
                   # For these, higher is worse
                   if percentile > 75:
                       risk_level = "High concern"
                   elif percentile > 50:
                       risk_level = "Moderate concern"
                   else:
                       risk_level = "Low concern"
               else:
                   # For CGPA, Age, etc., depends on the specific value
                   if feature == 'CGPA' and feature_value < 3.0:
                       risk_level = "High concern"
                   elif feature == 'CGPA' and feature_value < 3.5:
                       risk_level = "Moderate concern"
                   else:
                       risk_level = "Low concern"
                       
           except:
               effect = "Unknown effect"
               risk_level = "Unknown"
       else:
           try:
               grouped = df.groupby(feature)["Depression Risk (%)"].mean()
               avg_risk = df["Depression Risk (%)"].mean()
               cat_risk = grouped.get(feature_value, avg_risk)
               effect = "Increases risk" if cat_risk > avg_risk else "Decreases risk"
               
               # Determine risk level for categorical features
               if cat_risk > avg_risk * 1.5:
                   risk_level = "High concern"
               elif cat_risk > avg_risk * 1.2:
                   risk_level = "Moderate concern"
               else:
                   risk_level = "Low concern"
           except:
               effect = "Unknown effect"
               risk_level = "Unknown"
       
       contribution_effects.append(effect)
       risk_levels.append(risk_level)
   
   # Create contribution dataframe
   contribution_data = []
   for i, feature in enumerate(valid_features):
       contribution_data.append({
           "Feature": feature,
           "Student Value": student_values[i],
           "Contribution (%)": contribution_percentages[i],
           "Effect": contribution_effects[i],
           "Attention Level": risk_levels[i]
       })
   
   contribution_df = pd.DataFrame(contribution_data)
   contribution_df = contribution_df.sort_values("Contribution (%)", ascending=False)
   
   # Display top contributors in two columns
   col1, col2 = st.columns(2)
   
   with col1:
       # Create horizontal bar chart
       fig, ax = plt.subplots(figsize=(10, 8))
       top_contributors = contribution_df.head(10)
       
       # Colors based on effect
       colors = []
       for effect in top_contributors["Effect"]:
           if effect == "Increases risk":
               colors.append('#D32F2F')
           elif effect == "Decreases risk":
               colors.append('#388E3C')
           else:
               colors.append('#757575')
       
       bars = ax.barh(range(len(top_contributors)), 
                     top_contributors["Contribution (%)"], 
                     color=colors, alpha=0.8)
       
       # Add value labels
       for i, bar in enumerate(bars):
           width = bar.get_width()
           ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                  f'{width:.1f}%', va='center', ha='left', fontweight='bold')
       
       ax.set_yticks(range(len(top_contributors)))
       ax.set_yticklabels(top_contributors["Feature"])
       ax.set_xlabel('Contribution to Overall Risk (%)', fontsize=12, fontweight='bold')
       ax.set_title('Top 10 Contributing Factors', fontsize=14, fontweight='bold')
       ax.invert_yaxis()
       ax.grid(axis='x', alpha=0.3)
       
       # Add legend
       from matplotlib.patches import Patch
       legend_elements = [
           Patch(facecolor='#D32F2F', alpha=0.8, label='Increases Risk'),
           Patch(facecolor='#388E3C', alpha=0.8, label='Decreases Risk')
       ]
       ax.legend(handles=legend_elements, loc='lower right')
       
       st.pyplot(fig)
   
   with col2:
       st.markdown("<h4 style='color: white;'>Factors Requiring Attention</h4>", unsafe_allow_html=True)
       
       # Filter and display high/moderate concern factors
       attention_factors = contribution_df[
           contribution_df["Attention Level"].isin(["High concern", "Moderate concern"])
       ].head(8)
       
       if len(attention_factors) > 0:
           for _, factor in attention_factors.iterrows():
               # Color coding for attention level
               if factor["Attention Level"] == "High concern":
                   attention_color = "#D32F2F"
                   attention_icon = "🔴"
               elif factor["Attention Level"] == "Moderate concern":
                   attention_color = "#F57C00"
                   attention_icon = "🟡"
               else:
                   attention_color = "#388E3C"
                   attention_icon = "🟢"
               
               st.markdown(f"""
                   <div style="background-color: rgba(255, 255, 255, 0.1); 
                               padding: 12px; margin-bottom: 10px; border-radius: 8px;
                               border-left: 4px solid {attention_color};">
                       <p style="margin: 0; color: white;">
                           <strong>{attention_icon} {factor['Feature']}</strong><br>
                           Value: {factor['Student Value']}<br>
                           <span style="color: {attention_color};">
                               {factor['Attention Level']} - {factor['Effect']}
                           </span><br>
                           <small style="color: #CCCCCC;">
                               Contributes {factor['Contribution (%)']:.1f}% to risk score
                           </small>
                       </p>
                   </div>
               """, unsafe_allow_html=True)
       else:
           st.markdown("""
               <p style="color: #CCCCCC; font-style: italic;">
                   ✅ No factors requiring immediate attention identified.
               </p>
           """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ===== SECTION 3: RECOMMENDATIONS =====
st.markdown("""
   <div class="recommendation-container">
       <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Personalized Recommendations</h3>
       <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">Evidence-based interventions tailored to this student's risk profile</p>
""", unsafe_allow_html=True)

# Generate recommendations based on risk level and specific factors
recommendations = []

# Primary risk-based recommendations
if risk_category == "High":
   recommendations.append({
       "title": "🚨 Immediate Professional Intervention",
       "description": "High risk score requires urgent mental health support",
       "actions": [
           "Schedule appointment with campus counselor within 48 hours",
           "Provide crisis hotline contact information",
           "Implement weekly check-ins",
           "Consider temporary academic accommodations"
       ],
       "priority": "URGENT",
       "color": "#D32F2F"
   })
elif risk_category == "Medium":
   recommendations.append({
       "title": "⚠️ Enhanced Support & Monitoring",
       "description": "Moderate risk requires proactive support measures",
       "actions": [
           "Schedule counseling appointment within 1-2 weeks",
           "Provide mental health resource packet",
           "Bi-weekly wellness check-ins",
           "Connect with peer support programs"
       ],
       "priority": "HIGH",
       "color": "#F57C00"
   })
else:
   recommendations.append({
       "title": "✅ Preventive Care & Wellness",
       "description": "Maintain current mental health with preventive measures",
       "actions": [
           "Provide general wellness resources",
           "Encourage participation in campus activities",
           "Monthly wellness check-ins",
           "Stress management workshop information"
       ],
       "priority": "STANDARD",
       "color": "#388E3C"
   })

# Factor-specific recommendations based on the analysis above
if 'contribution_df' in locals():
   high_concern_factors = contribution_df[contribution_df["Attention Level"] == "High concern"]
   
   for _, factor in high_concern_factors.iterrows():
       feature_name = factor['Feature']
       
       # Sleep-related recommendations
       if 'Sleep' in feature_name:
           recommendations.append({
               "title": "😴 Sleep Optimization Program",
               "description": f"Addressing sleep issues: {factor['Student Value']}",
               "actions": [
                   "Sleep hygiene education and resources",
                   "Sleep diary tracking for 2 weeks",
                   "Environmental sleep assessment",
                   "Consider referral to sleep specialist"
               ],
               "priority": "MEDIUM",
               "color": "#9C27B0"
           })
       
       # Academic pressure recommendations
       elif 'Academic Pressure' in feature_name:
           recommendations.append({
               "title": "📚 Academic Stress Management",
               "description": f"High academic pressure level: {factor['Student Value']}/10",
               "actions": [
                   "Academic advisor consultation",
                   "Time management skills workshop",
                   "Study skills assessment",
                   "Consider course load adjustment"
               ],
               "priority": "MEDIUM",
               "color": "#3F51B5"
           })
       
       # Financial stress recommendations
       elif 'Financial' in feature_name:
           recommendations.append({
               "title": "💰 Financial Support Services",
               "description": f"Financial stress level: {factor['Student Value']}/10",
               "actions": [
                   "Financial aid office consultation",
                   "Emergency financial assistance assessment",
                   "Work-study opportunity exploration",
                   "Financial literacy workshop"
               ],
               "priority": "MEDIUM",
               "color": "#4CAF50"
           })
       
       # CGPA-related recommendations
       elif 'CGPA' in feature_name:
           recommendations.append({
               "title": "📈 Academic Support Services",
               "description": f"CGPA needs attention: {factor['Student Value']}",
               "actions": [
                   "Academic success center referral",
                   "Tutoring services evaluation",
                   "Learning assessment if needed",
                   "Academic recovery planning"
               ],
               "priority": "MEDIUM",
               "color": "#FF9800"
           })

# Check for critical factors
if "Have you ever had suicidal thoughts ?" in student_data.index:
   if str(student_data["Have you ever had suicidal thoughts ?"]).lower() in ["yes", "sometimes", "1", "true"]:
       recommendations.insert(0, {
           "title": "🆘 CRITICAL: Suicide Risk Protocol",
           "description": "Student has reported suicidal thoughts - immediate action required",
           "actions": [
               "Activate crisis intervention protocol immediately",
               "Do not leave student alone",
               "Contact crisis team/911 if necessary",
               "Ensure 24/7 support contact information",
               "Mandatory follow-up within 24 hours"
           ],
           "priority": "EMERGENCY",
           "color": "#B71C1C"
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
   if st.button("📋 Save Assessment", use_container_width=True):
       # Store assessment in session state
       if "assessments" not in st.session_state:
           st.session_state.assessments = {}
       
       st.session_state.assessments[student_index] = {
           "student_id": student_display_id,
           "risk_score": risk_score,
           "risk_category": risk_category,
           "date_assessed": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
           "recommendations_count": len(recommendations),
           "top_risk_factors": contribution_df.head(5)["Feature"].tolist() if 'contribution_df' in locals() else []
       }
       
       st.success("✅ Assessment saved successfully!")