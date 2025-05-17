from utils import set_page_style
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure the page
st.set_page_config(
    page_title="Student Depression Risk Predictor",
    page_icon="🧠",
    layout="wide",
)

# Add style from utils.py
set_page_style()

st.markdown("<h1 class='main-header'>Student Depression Risk Dashboard</h1>",
            unsafe_allow_html=True)

# Load model and preprocessor


@st.cache_resource
def load_model():
    with open("model/depression_model.pkl", "rb") as f_model:
        model = pickle.load(f_model)
    with open("model/preprocessor.pkl", "rb") as f_pre:
        preprocessor = pickle.load(f_pre)
    with open("model/feature_columns.pkl", "rb") as f_cols:
        feature_columns = pickle.load(f_cols)
    return model, preprocessor, feature_columns


# Load resources
model, preprocessor, feature_columns = load_model()

st.success("✅ Model, preprocessor, and feature list loaded successfully.")

# Main information
st.markdown("""
## Welcome to the Student Depression Risk Prediction System

This application is designed to help university wellness coordinators identify students who may be at risk of depression. 
The system uses machine learning to analyze student data and provide risk assessments.

### How to use this dashboard:
1. **Login** - Use your credentials to access the system
2. **Overview** - Upload student data and see aggregate statistics
3. **Student List** - View all students and their risk levels
4. **Student Detail** - Analyze individual student risk factors
5. **Feature Contribution** - Understand what factors contribute to risk

""")

# If there is data uploaded, show basic graphs
if "latest_df" in st.session_state:
    st.markdown("<h2 class='sub-header'>Quick Dashboard</h2>",
                unsafe_allow_html=True)

    df = st.session_state["latest_df"]

    col1, col2 = st.columns(2)

    with col1:
        # Risk distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        df['Risk Category'] = pd.cut(df['Depression Risk (%)'],
                                     bins=[0, 30, 60, 100],
                                     labels=['Low', 'Medium', 'High'])
        risk_counts = df['Risk Category'].value_counts()
        colors = ['#388E3C', '#F57C00', '#D32F2F']
        risk_counts.plot(kind='pie', autopct='%1.1f%%', colors=colors, ax=ax)
        plt.title('Distribution of Depression Risk Levels')
        st.pyplot(fig)

    with col2:
        # Avg risk by gender
        fig, ax = plt.subplots(figsize=(10, 6))
        gender_risk = df.groupby(
            'Gender')['Depression Risk (%)'].mean().reset_index()
        sns.barplot(x='Gender', y='Depression Risk (%)',
                    data=gender_risk, ax=ax)
        plt.title('Average Depression Risk by Gender')
        st.pyplot(fig)
