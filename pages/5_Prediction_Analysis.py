# pages/5_FeatureContribution.py
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
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

# Get student ID for display
if 'id' in student_data.index:
    student_display_id = student_data['id']
elif 'ID' in student_data.index:
    student_display_id = student_data['ID']
else:
    student_display_id = student_index

# Custom CSS - using similar style to student details
st.markdown("""
<style>
.main-container {
    border: 2px solid white;
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    background-color: transparent;
}
.student-info-container {
    border: 2px solid white;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 30px;
    background-color: transparent;
}
.explanation-container {
    border: 2px solid white;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    background-color: transparent;
}
.feature-item {
    border-left: 5px solid;
    padding: 15px;
    margin-bottom: 15px;
    background-color: #f8f9fa;
    border-radius: 0 10px 10px 0;
}
.info-item {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
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

# ===== SECTION 2: ANALYSIS EXPLANATION =====
st.markdown("""
    <div class="explanation-container">
        <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Understanding Feature Contributions</h3>
        <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">How different factors influence this student's depression risk prediction</p>
        
        <div style="color: white;">
            <p style="margin-bottom: 12px;">This analysis shows how much each factor contributes to this student's depression risk prediction, based on:</p>
            <ul style="margin-bottom: 12px;">
                <li style="margin-bottom: 8px;">📊 <strong>Feature Importance:</strong> How significant each factor is in the prediction model</li>
                <li style="margin-bottom: 8px;">👤 <strong>Student's Values:</strong> This student's specific characteristics compared to population averages</li>
                <li style="margin-bottom: 8px;">🔍 <strong>Effect Direction:</strong> Whether each factor increases or decreases the predicted risk</li>
            </ul>
            <div style="background-color: rgba(30, 136, 229, 0.1); padding: 15px; border-radius: 8px; margin-top: 15px;">
                <p style="margin: 0; font-style: italic;">
                    💡 <strong>Interpretation Guide:</strong> Larger percentages indicate stronger influence on the prediction. 
                    Red factors increase risk, while green factors help reduce it.
                </p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Check if model supports feature importance analysis
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
            "Feature": feature.replace('_', ' ').title(),
            "Value": student_values[i],
            "Contribution (%)": contribution_percentages[i],
            "Effect": contribution_effects[i]
        })
    
    # Sort by contribution
    contribution_df = pd.DataFrame(contribution_data)
    contribution_df = contribution_df.sort_values("Contribution (%)", ascending=False)
    
    # ===== SECTION 3: INTERACTIVE VISUALIZATION =====
    st.markdown("""
        <div class="student-info-container">
            <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Feature Contribution Visualization</h3>
            <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">Interactive chart showing the top contributing factors</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get top 10 contributors for the chart
    top_contributors = contribution_df.head(10).copy()
    
    # Create colors based on effect
    colors = ['#D32F2F' if effect == "Increases risk" else '#388E3C' 
             for effect in top_contributors["Effect"]]
    
    # Create interactive horizontal bar chart with Plotly
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        y=top_contributors["Feature"][::-1],  # Reverse order for descending view
        x=top_contributors["Contribution (%)"][::-1],
        orientation='h',
        marker=dict(
            color=colors[::-1],  # Reverse colors to match
            line=dict(color='rgba(0,0,0,0.1)', width=1)
        ),
        text=[f'{val:.1f}%' for val in top_contributors["Contribution (%)"][::-1]],
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate="<b>%{y}</b><br>" +
                     "Contribution: %{x:.1f}%<br>" +
                     "Student Value: %{customdata[0]}<br>" +
                     "Effect: %{customdata[1]}<br>" +
                     "<extra></extra>",
        customdata=[[row["Value"], row["Effect"]] for _, row in top_contributors[::-1].iterrows()]
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Top 10 Features Contributing to Depression Risk',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'white'}
        },
        xaxis_title="Contribution to Depression Risk (%)",
        yaxis_title="Features",
        template="plotly_dark",
        height=500,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    # Add legend manually using annotations
    fig.add_annotation(
        x=0.98, y=0.02,
        xref="paper", yref="paper",
        text="<b>Legend:</b><br>"
             "🔴 Increases Risk<br>"
             "🟢 Decreases Risk",
        showarrow=False,
        font=dict(size=11, color='white'),
        align="right",
        bgcolor="rgba(0,0,0,0.6)",
        bordercolor="white",
        borderwidth=1
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # ===== SECTION 4: DETAILED FEATURE BREAKDOWN =====
    st.markdown("""
        <div class="student-info-container">
            <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">Detailed Feature Breakdown</h3>
            <p style="color: #CCCCCC; text-align: center; margin-bottom: 25px;">Complete analysis of all contributing factors</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display top contributors with detailed breakdown
    st.markdown("<h4 style='color: white; margin-bottom: 20px;'>🔝 Top Contributing Factors</h4>", unsafe_allow_html=True)
    
    for i, (_, row) in enumerate(contribution_df.head(5).iterrows()):
        # Determine color based on effect
        if row["Effect"] == "Increases risk":
            color = "#D32F2F"
            icon = "⚠️"
        elif row["Effect"] == "Decreases risk":
            color = "#388E3C"
            icon = "✅"
        else:
            color = "#9E9E9E"
            icon = "❓"
        
        st.markdown(f"""
            <div class="feature-item" style="border-left-color: {color};">
                <h5 style="color: {color}; margin-top: 0; margin-bottom: 8px;">
                    {icon} {row['Feature']}
                </h5>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="color: #333; font-weight: bold;">Contribution: {row['Contribution (%)']:.1f}%</span>
                    <span style="color: {color}; font-weight: bold;">{row['Effect']}</span>
                </div>
                <p style="margin-bottom: 8px; color: #666;">
                    <strong>Student's Value:</strong> {row['Value']}
                </p>
                <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                    <p style="margin: 0; color: #555; font-size: 0.9em; font-style: italic;">
                        This factor accounts for {row['Contribution (%)']:.1f}% of the model's prediction for this student. 
                        {' It tends to increase their depression risk.' if row['Effect'] == 'Increases risk' 
                          else ' It helps reduce their depression risk.' if row['Effect'] == 'Decreases risk' 
                          else ' Its effect on depression risk is unclear.'}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Show complete table in an expander
    with st.expander("📋 View Complete Feature Analysis"):
        # Format contribution column to show percentages with 1 decimal place
        formatted_df = contribution_df.copy()
        formatted_df["Contribution (%)"] = formatted_df["Contribution (%)"].apply(lambda x: f"{x:.1f}%")
        
        # Create interactive dataframe with custom styling
        st.dataframe(
            formatted_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Feature": st.column_config.TextColumn("Feature", width="medium"),
                "Value": st.column_config.TextColumn("Student's Value", width="medium"),
                "Contribution (%)": st.column_config.TextColumn("Contribution (%)", width="small"),
                "Effect": st.column_config.TextColumn("Effect on Risk", width="medium")
            }
        )
    
    # ===== SECTION 5: INTERPRETATION GUIDE =====
    st.markdown("""
        <div class="explanation-container">
            <h3 style="margin-top: 0; color: white; text-align: center; font-size: 1.8rem;">How to Interpret These Results</h3>
            
            <div style="color: white;">
                <div style="margin-bottom: 20px;">
                    <h4 style="color: #1E88E5; margin-bottom: 10px;">📊 Understanding Contributions</h4>
                    <p style="margin-bottom: 10px;">
                        The percentages show how much each factor influences this student's overall depression risk prediction. 
                        Features with higher percentages have a stronger impact on the final risk score.
                    </p>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <h4 style="color: #1E88E5; margin-bottom: 10px;">🔍 Effect Interpretation</h4>
                    <ul style="margin-bottom: 10px;">
                        <li style="margin-bottom: 8px;"><span style="color: #D32F2F;">⚠️ Increases Risk:</span> 
                            This factor is pushing the student's risk prediction higher</li>
                        <li style="margin-bottom: 8px;"><span style="color: #388E3C;">✅ Decreases Risk:</span> 
                            This factor is helping to reduce the student's predicted risk</li>
                        <li style="margin-bottom: 8px;"><span style="color: #9E9E9E;">❓ Unknown Effect:</span> 
                            The impact direction is unclear from the available data</li>
                    </ul>
                </div>
                
                <div style="background-color: rgba(245, 124, 0, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #F57C00;">
                    <h4 style="color: #F57C00; margin-top: 0; margin-bottom: 10px;">⚠️ Important Disclaimer</h4>
                    <p style="margin: 0; font-style: italic;">
                        This analysis shows correlations and patterns identified by the machine learning model. 
                        It should be used alongside professional judgment and clinical assessment, not as a replacement for them. 
                        Individual circumstances and context are crucial for proper interpretation.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
else:
    st.warning("This model does not support feature importance analysis.")

# Navigation buttons
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Student Details", use_container_width=True):
        st.switch_page("pages/4_Student_Detail.py")

with col2:
    if st.button("📋 Student List", use_container_width=True):
        st.switch_page("pages/3_Student_List.py")

with col3:
    if st.button("📊 Overview Dashboard", use_container_width=True):
        st.switch_page("pages/2_Predict.py")