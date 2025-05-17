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
    
    # Show key student attributes, excluding those that shouldn't contribute to the model
    non_feature_columns = ["Depression Risk (%)", "Risk Category", "id", "ID", "student_id", "Student ID"]
    info_columns = ["Gender", "Age", "CGPA", "Degree"]
    
    # Add any additional columns that might be informative but aren't features
    for col in df.columns:
        if col not in feature_columns and col not in non_feature_columns and col not in info_columns:
            info_columns.append(col)
    
    # Display student ID separately
    if "id" in student_data:
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
            <p style="margin: 0; color: #666;">Student ID</p>
            <p style="margin: 0; font-size: 18px; font-weight: bold;">{student_data['id']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
            <p style="margin: 0; color: #666;">Student Index</p>
            <p style="margin: 0; font-size: 18px; font-weight: bold;">{student_index}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display other important info
    for col in info_columns:
        if col in student_data:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <p style="margin: 0; color: #666;">{col}</p>
                <p style="margin: 0; font-size: 18px; font-weight: bold;">{student_data[col]}</p>
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
    
    # Get feature importances
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        
        # Get prediction probability for this student
        X_student = df.loc[[student_index]][feature_columns]
        X_student_transformed = preprocessor.transform(X_student)
        
        # Get probabilities - class 1 is typically the positive class (depression)
        student_prob = model.predict_proba(X_student_transformed)[0, 1]
        
        # Filter out non-feature columns that shouldn't contribute
        non_feature_columns = ["id", "ID", "student_id", "Student ID"]
        valid_features = []
        valid_importances = []
        student_values = []
        
        for i, feature in enumerate(feature_columns):
            if feature not in non_feature_columns:
                valid_features.append(feature)
                valid_importances.append(importances[i])
                student_values.append(student_data.get(feature, "N/A"))
        
        # Calculate contribution percentages
        total_importance = sum(valid_importances)
        contribution_percentages = [(imp / total_importance) * 100 for imp in valid_importances]
        
        # Enhanced method: Consider student values to determine direction of effect
        contribution_effects = []
        
        # Separate features by type
        numeric_features = df[valid_features].select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = [f for f in valid_features if f not in numeric_features]
        
        # For each feature, determine if it likely increases or decreases risk
        for i, feature in enumerate(valid_features):
            feature_value = student_values[i]
            
            if feature in numeric_features:
                # For numeric features, compare to dataset average
                try:
                    avg_value = df[feature].mean()
                    feature_value = float(feature_value)
                    
                    # Check correlation with target (positive correlation means higher value -> higher risk)
                    # We're using the feature importance as a proxy for correlation direction
                    # This is not perfect but gives a reasonable approximation
                    if feature_value > avg_value:
                        effect = "Increases risk"  # Above average value
                    else:
                        effect = "Decreases risk"  # Below average value
                except:
                    effect = "Unknown effect"  # Can't determine
            else:
                # For categorical features, look at conditional probability
                try:
                    # Group by this feature and calculate average risk
                    grouped = df.groupby(feature)["Depression Risk (%)"].mean()
                    
                    # If this category has above average risk, it increases risk
                    avg_risk = df["Depression Risk (%)"].mean()
                    cat_risk = grouped.get(feature_value, avg_risk)
                    
                    if cat_risk > avg_risk:
                        effect = "Increases risk"
                    else:
                        effect = "Decreases risk"
                except:
                    effect = "Unknown effect"
            
            contribution_effects.append(effect)
        
        # Create feature contribution dataframe
        contribution_data = []
        for i, feature in enumerate(valid_features):
            contribution_data.append({
                "Feature": feature,
                "Value": student_values[i],
                "Contribution (%)": contribution_percentages[i],
                "Effect": contribution_effects[i]
            })
        
        # Sort by contribution
        contribution_df = pd.DataFrame(contribution_data)
        contribution_df = contribution_df.sort_values("Contribution (%)", ascending=False)
        
        # Add explanation about the analysis
        st.info("""
        **Understanding Feature Contributions:** 
        
        This analysis shows how much each feature contributes to this student's depression risk prediction, based on:
        
        1. How important each feature is in the prediction model
        2. This student's specific values compared to population averages
        
        - **"Increases risk"** means this feature likely pushes the prediction higher
        - **"Decreases risk"** means this feature likely reduces the predicted risk  
        - **Larger percentages** indicate features with stronger influence on the prediction
        """)
        
        # Plot horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get top 10 contributors
        top_contributors = contribution_df.head(10)
        
        # Create colors based on effect
        colors = ['#D32F2F' if effect == "Increases risk" else '#388E3C' 
                 for effect in top_contributors["Effect"]]
        
        # Create horizontal bars
        bars = ax.barh(
            top_contributors["Feature"],
            top_contributors["Contribution (%)"],
            color=colors,
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
        
        # Add a legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#D32F2F', alpha=0.7, label='Increases Risk'),
            Patch(facecolor='#388E3C', alpha=0.7, label='Decreases Risk')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        # Display chart
        st.pyplot(fig)
        
        # Display contribution table
        st.subheader("All Features Contribution")
        
        # Format contribution column to show percentages with 1 decimal place
        formatted_df = contribution_df.copy()
        formatted_df["Contribution (%)"] = formatted_df["Contribution (%)"].apply(lambda x: f"{x:.1f}%")
        
        # Show table
        st.dataframe(formatted_df, hide_index=True)
        
        # Add explanation about interpretation
        st.markdown("""
        ### Interpreting These Results
        
        The percentages above show how much each feature contributes to this student's overall depression risk prediction. Features with higher percentages have a stronger influence on the prediction.
        
        - **Values marked "Increases risk"** (red bars) are pushing this student's risk prediction higher
        - **Values marked "Decreases risk"** (green bars) are helping reduce their risk prediction
        
        For example, if "Academic Pressure" shows 30% contribution with "Increases risk" effect, it means this factor is a significant contributor to this student's depression risk.
        """)
    else:
        st.warning("This model does not support feature importance analysis.")