# pages/5_FeatureContribution.py
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import shap  # Necesitamos instalar esta biblioteca

# Añadir el directorio raíz al path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Importar utils
from utils import set_page_style, check_login, check_data, categorize_risk

st.set_page_config(page_title="Feature Contributions", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Feature Contribution Analysis with SHAP</h1>", unsafe_allow_html=True)

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

# Mostrar un mensaje de cálculo
with st.spinner("Calculating SHAP values for precise feature contributions..."):
    try:
        # Prepare the data for SHAP
        X = df[feature_columns]
        
        # Transform the data
        X_transformed = preprocessor.transform(X)
        
        # Get the single instance for the selected student
        student_X = X.loc[[student_index]]
        student_X_transformed = preprocessor.transform(student_X)
        
        # Initialize the SHAP explainer based on the model type
        if hasattr(model, "predict_proba"):
            # For classifiers like RandomForest
            explainer = shap.TreeExplainer(model)
            # Get SHAP values for all data points (for background distribution)
            shap_values_all = explainer.shap_values(X_transformed)
            
            # For binary classification, we're interested in class 1 (probability of depression)
            if isinstance(shap_values_all, list) and len(shap_values_all) > 1:
                # This happens for binary classification models
                shap_values_all = shap_values_all[1]  # Class 1 (depression)
            
            # Get SHAP values for the student
            student_shap_values = explainer.shap_values(student_X_transformed)
            
            # For binary classification
            if isinstance(student_shap_values, list) and len(student_shap_values) > 1:
                student_shap_values = student_shap_values[1]  # Class 1 (depression)
            
            # Get the base value (average model output)
            expected_value = explainer.expected_value
            if isinstance(expected_value, list) and len(expected_value) > 1:
                expected_value = expected_value[1]  # For binary classification
        else:
            # For regressors
            explainer = shap.TreeExplainer(model)
            shap_values_all = explainer.shap_values(X_transformed)
            student_shap_values = explainer.shap_values(student_X_transformed)
            expected_value = explainer.expected_value
        
        # Create SHAP summary plot for the student
        # This sometimes causes issues with non-numerical features, so we'll handle that
        try:
            # Get feature names after preprocessing (could be different due to one-hot encoding)
            if hasattr(preprocessor, 'get_feature_names_out'):
                feature_names_out = preprocessor.get_feature_names_out(feature_columns)
            else:
                # Simplified approach if get_feature_names_out isn't available
                feature_names_out = feature_columns
            
            # Flatten SHAP values if they're 2D (only need 1 row for the student)
            if student_shap_values.ndim > 1 and student_shap_values.shape[0] == 1:
                student_shap_values = student_shap_values[0]
            
            # Calculate SHAP contribution to probability
            # For a logistic model, we need to convert log-odds to probability
            base_probability = 1 / (1 + np.exp(-expected_value))
            
            # Calculate contributions as percentages of the total deviation from base
            total_contribution = np.sum(np.abs(student_shap_values))
            contribution_percentages = (np.abs(student_shap_values) / total_contribution) * 100 if total_contribution > 0 else np.zeros_like(student_shap_values)
            
            # Create a DataFrame with contributions
            contributions = []
            for i, feature in enumerate(feature_columns):
                value = student_data.get(feature, "N/A")
                shap_value = student_shap_values[i] if i < len(student_shap_values) else 0
                contribution_pct = contribution_percentages[i] if i < len(contribution_percentages) else 0
                effect = "Increases risk" if shap_value > 0 else "Decreases risk"
                
                contributions.append({
                    "Feature": feature,
                    "Value": value,
                    "SHAP Value": shap_value,
                    "Contribution (%)": contribution_pct,
                    "Effect": effect
                })
            
            # Convert to DataFrame and sort
            contribution_df = pd.DataFrame(contributions)
            contribution_df = contribution_df.sort_values(by="Contribution (%)", ascending=False)
            
            # Success, SHAP values calculated
            st.success("SHAP values calculated successfully!")
        except Exception as e:
            st.error(f"Error creating SHAP summary plot: {e}")
            st.exception(e)
            # Fallback to standard feature importance
            contribution_df = None
    except Exception as e:
        st.error(f"Error calculating SHAP values: {e}")
        st.exception(e)
        # Fallback to standard feature importance
        contribution_df = None

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
    
    if contribution_df is not None:
        # Add explanation about SHAP values
        st.info("""
        **Understanding SHAP Values:** 
        
        SHAP (SHapley Additive exPlanations) values show how much each feature contributes to pushing the prediction higher or lower for this specific student. Unlike general feature importance, SHAP values are personalized to each student's specific data.
        
        - **Positive values (red)** increase the predicted risk of depression
        - **Negative values (green)** decrease the predicted risk of depression  
        - **Larger percentages** indicate features with stronger influence on the prediction
        """)
        
        # Plot horizontal bar chart of SHAP contributions
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get top 10 contributors by absolute contribution
        top_contributors = contribution_df.head(10)
        
        # Create colors based on effect (increases/decreases risk)
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
        ax.set_title('Top 10 Features Contributing to Depression Risk (SHAP Analysis)')
        ax.invert_yaxis()  # Higher percentages at the top
        
        # Display chart
        st.pyplot(fig)
        
        # Display contribution table
        st.subheader("All Features Contribution")
        
        # Format contribution column to show percentages with 1 decimal place
        formatted_df = contribution_df.copy()
        formatted_df["Contribution (%)"] = formatted_df["Contribution (%)"].apply(lambda x: f"{x:.1f}%")
        
        # Select columns to display
        display_df = formatted_df[["Feature", "Value", "Contribution (%)", "Effect"]]
        
        # Show table
        st.dataframe(display_df, hide_index=True)
        
        # Add warning about SHAP interpretation
        st.markdown("""
        ### Interpreting These Results
        
        The percentages above represent how much each feature contributes to this student's depression risk prediction (relative to the average prediction). This is much more specific and accurate than general feature importance, as it takes into account this student's exact values for each feature.
        
        For example, if "Academic Pressure" shows 30% contribution with "Increases risk" effect, it means this student's specific academic pressure level is pushing their risk prediction up significantly compared to the average student.
        """)
    else:
        # Fallback to standard feature importance if SHAP fails
        st.warning("Could not calculate SHAP values. Falling back to standard feature importance.")
        
        if hasattr(model, "feature_importances_"):
            # Get feature importances
            importances = model.feature_importances_
            
            # Filter out non-feature columns that shouldn't contribute
            non_feature_columns = ["id", "ID", "student_id", "Student ID"]
            valid_features = []
            valid_importances = []
            
            for i, feature in enumerate(feature_columns):
                if feature not in non_feature_columns:
                    valid_features.append(feature)
                    valid_importances.append(importances[i])
            
            # Calculate contribution percentages
            total_importance = sum(valid_importances)
            contribution_percentages = [(imp / total_importance) * 100 for imp in valid_importances]
            
            # Create feature contribution dataframe
            contribution_data = []
            for i, feature in enumerate(valid_features):
                value = student_data.get(feature, "N/A")
                contribution = contribution_percentages[i]
                contribution_data.append({
                    "Feature": feature,
                    "Value": value,
                    "Contribution (%)": contribution
                })
            
            # Sort by contribution
            fallback_df = pd.DataFrame(contribution_data)
            fallback_df = fallback_df.sort_values("Contribution (%)", ascending=False)
            
            # Plot horizontal bar chart
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Get top 10 contributors
            top_contributors = fallback_df.head(10)
            
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
            ax.set_title('Top 10 Features Contributing to Depression Risk (General Importance)')
            ax.invert_yaxis()  # Higher percentages at the top
            
            # Display chart
            st.pyplot(fig)
            
            # Display contribution table
            st.subheader("All Features Contribution")
            
            # Format contribution column to show percentages with 1 decimal place
            formatted_df = fallback_df.copy()
            formatted_df["Contribution (%)"] = formatted_df["Contribution (%)"].apply(lambda x: f"{x:.1f}%")
            
            # Show table
            st.dataframe(formatted_df, hide_index=True)
            
            # Add warning about interpretation
            st.info("""
            **Note:** These contributions are based on general feature importance, not specific to this student. 
            They show which features are generally most important in the model, not how this student's specific 
            values affect their prediction.
            """)
        else:
            st.error("This model does not support feature importance analysis.")