import streamlit as st
import os
import sys

# Configure the page
st.set_page_config(
    page_title="Student Depression Risk Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
st.markdown("""
<style>
    .main-header {color:#1E88E5; font-size:42px; font-weight:bold; text-align:center; margin-bottom:30px;}
    .sub-header {color:#0D47A1; font-size:28px; font-weight:bold; margin-top:20px; text-align:center; margin-bottom:20px;}
    .welcome-text {font-size:18px; margin-bottom:30px; text-align:center;}
    .step-container {
        background-color: #000000; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        border: 2px solid white;
        color: white;
    }
    .step-number {
        background-color: #1E88E5; 
        color: white; 
        padding: 5px 12px; 
        border-radius: 50%; 
        margin-right: 10px; 
        font-weight: bold;
    }
    .stButton>button {
        background-color: #1E88E5 !important;
        color: white !important;
        font-size: 18px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #0D47A1 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("<h1 class='main-header'>Student Depression Risk Prediction System</h1>", unsafe_allow_html=True)

# Welcome text (centered and same width as steps)
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    st.markdown("<p class='welcome-text'>Welcome to the Student Depression Risk Prediction System, a tool designed to help university wellness coordinators identify students who may be at risk of depression. Early identification allows for timely intervention and support, helping students maintain their mental well-being throughout their academic journey.</p>", unsafe_allow_html=True)

# Steps for using the application (centered title)
st.markdown("<h2 class='sub-header'>How to Use This System</h2>", unsafe_allow_html=True)

# Create a central column to limit the width of the steps and center them
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    # Step 1
    st.markdown("""
    <div class="step-container">
        <h3><span class="step-number">1</span> Login</h3>
        <p>Access the system using your provided credentials. Click the "Login" button below or use the navigation menu on the left.</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 2
    st.markdown("""
    <div class="step-container">
        <h3><span class="step-number">2</span> Upload Student Data</h3>
        <p>On the Predict page, upload your student data file (CSV format). The system will process this data and calculate depression risk scores for each student.</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 3
    st.markdown("""
    <div class="step-container">
        <h3><span class="step-number">3</span> Explore Student Risk Levels</h3>
        <p>View the list of students organized by risk level. The system categorizes students into Low, Medium, and High risk groups based on their calculated risk score.</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 4
    st.markdown("""
    <div class="step-container">
        <h3><span class="step-number">4</span> Analyze Individual Students</h3>
        <p>Select any student to view their detailed profile, including specific risk factors and personalized recommendations for support.</p>
    </div>
    """, unsafe_allow_html=True)

    # Step 5
    st.markdown("""
    <div class="step-container">
        <h3><span class="step-number">5</span> Understand Contributing Factors</h3>
        <p>For each student, analyze which factors contribute most to their depression risk score. This insight helps in developing targeted intervention strategies.</p>
    </div>
    """, unsafe_allow_html=True)

# Login button that redirects to the login page - centered on the page
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Login to Get Started", use_container_width=True, type="primary"):
        # Redirect to the login page
        st.switch_page("pages/1_Login.py")