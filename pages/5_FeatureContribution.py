# pages/5_FeatureContribution.py
from utils import set_page_style, check_login, check_data, categorize_risk
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys

# Añadir el directorio raíz al path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Importar utils

st.set_page_config(page_title="Feature Contributions", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Feature Importance for Selected Student</h1>",
            unsafe_allow_html=True)

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
X_student = df.loc[[student_index]][feature_columns]

# Student risk score
risk_score = df.loc[student_index]["Depression Risk (%)"]
risk_category, risk_color = categorize_risk(risk_score)

# Display student header
st.markdown(f"""
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="margin: 0;">Student {student_index} - Depression Risk: 
        <span style="color: {risk_color};">{round(risk_score, 1)}%</span></h2>
    </div>
""", unsafe_allow_html=True)

# Check for feature importances
if hasattr(model, "feature_importances_"):
    try:
        # Debug output
        st.write("Model feature importances shape:",
                 model.feature_importances_.shape)
        st.write("Feature columns length:", len(feature_columns))

        # Ensure importances match feature columns
        importances = model.feature_importances_
        if len(importances) != len(feature_columns):
            st.error(
                f"Feature importances length ({len(importances)}) doesn't match feature columns length ({len(feature_columns)})")
            st.stop()

        # Get student values, safely convert to strings for display
        student_values_display = []
        for col in feature_columns:
            val = X_student[col].iloc[0]
            student_values_display.append(str(val))

        # Create simplified contribution analysis
        feature_data = []
        for i, col in enumerate(feature_columns):
            # Get numeric value if possible
            try:
                student_val = float(X_student[col].iloc[0])
            except (ValueError, TypeError):
                student_val = 0  # Default for non-numeric

            # Check if feature is numeric
            is_numeric = col in df.select_dtypes(
                include=['int64', 'float64']).columns

            if is_numeric:
                # For numeric features, get mean and std
                avg = df[col].mean()
                std = df[col].std() if df[col].std() > 0 else 1.0
                # Calculate relative value
                rel_val = (student_val - avg) / std
            else:
                # For categorical features
                mode_val = df[col].mode()[0]
                avg = str(mode_val)
                # Set relative value to 1 if different from mode, 0 if same
                rel_val = 1.0 if str(X_student[col].iloc[0]) != str(
                    mode_val) else 0.0

            # Calculate impact (importance × relative difference)
            impact = importances[i] * abs(rel_val)

            # Add to list
            feature_data.append({
                "Feature": col,
                "Student Value": student_values_display[i],
                "Average Value": str(avg) if not is_numeric else avg,
                "Relative Difference": rel_val,
                "Feature Importance": importances[i],
                "Impact": impact
            })

        # Create dataframe
        contribution_df = pd.DataFrame(feature_data)

        # Sort by impact
        contribution_df = contribution_df.sort_values(
            "Impact", ascending=False)

        # Show top features
        st.subheader("Top Contributing Features")
        st.dataframe(contribution_df)

        # Create bar chart of top features
        fig, ax = plt.subplots(figsize=(12, 8))
        top_features = contribution_df.head(10)

        # Create horizontal bar chart
        colors = ['#D32F2F' if v >
                  0 else '#388E3C' for v in top_features['Relative Difference']]
        bars = ax.barh(top_features['Feature'],
                       top_features['Impact'], color=colors)

        # Add labels
        ax.set_xlabel('Impact on Depression Risk')
        ax.set_title('Top 10 Features Contributing to Depression Risk')

        # Invert y-axis to show highest impact at top
        ax.invert_yaxis()

        st.pyplot(fig)

        # Radar chart for numeric features
        st.subheader("Student vs Average (Numeric Features)")

        # Get numeric features
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        numeric_cols = [col for col in numeric_cols if col in feature_columns]

        if len(numeric_cols) >= 3:
            # Create radar chart data
            radar_data = contribution_df[contribution_df['Feature'].isin(
                numeric_cols)].head(6)

            # Convert average and student values to numeric
            radar_data['Student Numeric'] = pd.to_numeric(
                radar_data['Student Value'], errors='coerce')
            radar_data['Average Numeric'] = pd.to_numeric(
                radar_data['Average Value'], errors='coerce')

            # Replace NaN with 0
            radar_data = radar_data.fillna(0)

            # Create radar chart
            categories = radar_data['Feature'].tolist()
            N = len(categories)

            # Create angles for each axis
            angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
            angles += angles[:1]  # Close the loop

            # Get values
            student_vals = radar_data['Student Numeric'].tolist()
            student_vals += student_vals[:1]  # Close the loop

            avg_vals = radar_data['Average Numeric'].tolist()
            avg_vals += avg_vals[:1]  # Close the loop

            # Create plot
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

            # Plot student values
            ax.plot(angles, student_vals, 'o-', linewidth=2,
                    color=risk_color, label='Student')
            ax.fill(angles, student_vals, alpha=0.25, color=risk_color)

            # Plot average values
            ax.plot(angles, avg_vals, 'o-', linewidth=2,
                    color='#1E88E5', label='Average')
            ax.fill(angles, avg_vals, alpha=0.1, color='#1E88E5')

            # Add labels
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)

            # Add legend
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

            st.pyplot(fig)
        else:
            st.info(
                "Not enough numeric features to create a radar chart. Need at least 3 numeric features.")

        # Explanation
        st.markdown("""
        ### Understanding the Analysis
        
        - **Student Value**: The value for this specific student
        - **Average Value**: The average across all students (for numeric) or most common value (for categorical)
        - **Relative Difference**: How different the student's value is from the average (standardized)
        - **Feature Importance**: How important this feature is in the prediction model
        - **Impact**: Estimated contribution to this student's depression risk score
        
        Features with red bars indicate risk factors, while green bars indicate protective factors.
        """)

    except Exception as e:
        st.error(f"Error analyzing feature importances: {e}")
        st.exception(e)
else:
    st.warning("This model does not support feature importances.")

    # Show alternative message
    st.info("""
    The model doesn't provide direct feature importance information. 
    
    In a complete implementation, we could use:
    1. Permutation importance
    2. SHAP values
    3. Partial dependence plots
    
    These methods would help identify which features most strongly influence the prediction for this student.
    """)
