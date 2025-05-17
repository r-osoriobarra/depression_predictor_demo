# pages/5_FeatureContribution.py
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Añadir el directorio raíz al path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Importar utils
from utils import set_page_style, check_login, check_data, categorize_risk

st.set_page_config(page_title="Feature Contributions", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Feature Contribution Analysis</h1>", unsafe_allow_html=True)

# Require login
if not check_login():
    st.stop()

# Ensure selection and data availability
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

# Get selected student data
df = st.session_state["latest_df"]
student_index = st.session_state["selected_student_index"]
student_data = df.loc[student_index]

# Get depression risk score
risk_score = student_data["Depression Risk (%)"]
risk_category, risk_color = categorize_risk(risk_score)

# Create two columns layout
col1, col2 = st.columns([1, 2])

# Left column - Student details
with col1:
    st.subheader("Student Information")
    
    # Show key student attributes
    info_cards = {
        "Student ID": student_index,
        "Gender": student_data.get("Gender", "N/A"),
        "Age": student_data.get("Age", "N/A"),
        "CGPA": student_data.get("CGPA", "N/A"),
        "Degree": student_data.get("Degree", "N/A")
    }
    
    # Create styled info cards
    for key, value in info_cards.items():
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
            <p style="margin: 0; color: #666;">{key}</p>
            <p style="margin: 0; font-size: 18px; font-weight: bold;">{value}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Create risk meter
    st.subheader("Depression Risk")
    
    # Progress bar style based on risk level
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 10px; background-color: #f9f9f9;">
        <p style="margin: 0; font-size: 24px; font-weight: bold; color: {risk_color};">{risk_category} Risk: {risk_score:.1f}%</p>
        <div style="background-color: #e0e0e0; border-radius: 10px; height: 20px; width: 100%; margin-top: 10px;">
            <div style="background-color: {risk_color}; width: {risk_score}%; height: 20px; border-radius: 10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right column - Feature Contribution
with col2:
    st.subheader("Feature Contribution to Depression Risk")
    
    if hasattr(model, "feature_importances_"):
        # Get feature importances
        importances = model.feature_importances_
        
        # Calculate contribution percentages
        # This is a simplified approach - we're assuming the model's feature importances
        # can be directly converted to percentage contributions
        total_importance = sum(importances)
        contribution_percentages = [(imp / total_importance) * 100 for imp in importances]
        
        # Create feature contribution dataframe
        contribution_data = []
        for i, feature in enumerate(feature_columns):
            value = student_data.get(feature, "N/A")
            contribution = contribution_percentages[i]
            contribution_data.append({
                "Feature": feature,
                "Value": value,
                "Contribution (%)": contribution
            })
        
        # Sort by contribution
        contribution_df = pd.DataFrame(contribution_data)
        contribution_df = contribution_df.sort_values("Contribution (%)", ascending=False)
        
        # Plot horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get top 10 contributors
        top_contributors = contribution_df.head(10)
        
        # Create horizontal bars
        bars = ax.barh(
            top_contributors["Feature"],
            top_contributors["Contribution (%)"],
            color=risk_color,
            alpha=0.7
        )
        
        # Add percentage labels
        for bar in bars:
            width = bar.get_width()
            label_x_pos = width + 0.5
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                   va='center', color='black')
        
        # Set chart properties
        ax.set_xlabel('Contribution to Depression Risk (%)')
        ax.set_title('Top 10 Features Contributing to Depression Risk')
        ax.invert_yaxis()  # Higher percentages at the top
        
        # Display chart
        st.pyplot(fig)
        
        # Display contribution table
        st.subheader("All Features Contribution")
        
        # Format contribution column to show percentages
        contribution_df["Contribution (%)"] = contribution_df["Contribution (%)"].apply(lambda x: f"{x:.1f}%")
        
        # Show table
        st.dataframe(contribution_df, hide_index=True)
        
    else:
        st.warning("This model does not support feature importance analysis.")