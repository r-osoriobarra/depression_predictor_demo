# app.py
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

# Aplicar estilos personalizados
st.markdown("""
<style>
    .main-header {color:#1E88E5; font-size:42px; font-weight:bold; text-align:center; margin-bottom:30px;}
    .sub-header {color:#0D47A1; font-size:28px; font-weight:bold; margin-top:20px;}
    .welcome-text {font-size:18px; margin-bottom:30px;}
    .banner-container {text-align:center; margin-bottom:30px;}
    .step-container {background-color:#f5f5f5; padding:20px; border-radius:10px; margin-bottom:20px;}
    .step-number {background-color:#1E88E5; color:white; padding:5px 12px; border-radius:50%; margin-right:10px; font-weight:bold;}
    .login-button {text-align:center; margin-top:40px; margin-bottom:30px;}
</style>
""", unsafe_allow_html=True)

# Banner/imagen en la parte superior
st.markdown("""
<div class="banner-container">
    <img src="https://img.freepik.com/free-vector/mental-health-awareness-concept_23-2148527732.jpg?w=1380&t=st=1701290147~exp=1701290747~hmac=d3da4071dfe4d89fc10db9dfa47c9e9bee8eb4a2cc14288d69b66e8e14a49574" alt="Mental Health Banner" style="max-width:800px; width:100%;">
</div>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>Student Depression Risk Prediction System</h1>", unsafe_allow_html=True)

# Texto de bienvenida
st.markdown("<p class='welcome-text'>Welcome to the Student Depression Risk Prediction System, a tool designed to help university wellness coordinators identify students who may be at risk of depression. Early identification allows for timely intervention and support, helping students maintain their mental well-being throughout their academic journey.</p>", unsafe_allow_html=True)

# Pasos para usar la aplicación
st.markdown("<h2 class='sub-header'>How to Use This System</h2>", unsafe_allow_html=True)

# Paso 1
st.markdown("""
<div class="step-container">
    <h3><span class="step-number">1</span> Login</h3>
    <p>Access the system using your provided credentials. Click the "Login" button below or use the navigation menu on the left.</p>
</div>
""", unsafe_allow_html=True)

# Paso 2
st.markdown("""
<div class="step-container">
    <h3><span class="step-number">2</span> Upload Student Data</h3>
    <p>On the Overview page, upload your student data file (CSV format). The system will process this data and calculate depression risk scores for each student.</p>
</div>
""", unsafe_allow_html=True)

# Paso 3
st.markdown("""
<div class="step-container">
    <h3><span class="step-number">3</span> Explore Student Risk Levels</h3>
    <p>View the list of students organized by risk level. The system categorizes students into Low, Medium, and High risk groups based on their calculated risk score.</p>
</div>
""", unsafe_allow_html=True)

# Paso 4
st.markdown("""
<div class="step-container">
    <h3><span class="step-number">4</span> Analyze Individual Students</h3>
    <p>Select any student to view their detailed profile, including specific risk factors and personalized recommendations for support.</p>
</div>
""", unsafe_allow_html=True)

# Paso 5
st.markdown("""
<div class="step-container">
    <h3><span class="step-number">5</span> Understand Contributing Factors</h3>
    <p>For each student, analyze which factors contribute most to their depression risk score. This insight helps in developing targeted intervention strategies.</p>
</div>
""", unsafe_allow_html=True)

# Botón de Login que redirige a la página de login
st.markdown("<div class='login-button'>", unsafe_allow_html=True)
if st.button("Login to Get Started", use_container_width=False, type="primary"):
    # Redireccionar a la página de login
    st.switch_page("pages/1_Login.py")
st.markdown("</div>", unsafe_allow_html=True)

# Información adicional en la parte inferior
with st.expander("About This System"):
    st.markdown("""
    ### About the Depression Risk Prediction System
    
    This system uses machine learning to identify students who may be at risk of depression based on various factors including:
    
    - Academic performance
    - Sleep patterns
    - Study/work pressure
    - Financial stress
    - Social support
    - And many other factors
    
    The model has been trained on a dataset of student records where depression status was known, allowing it to recognize patterns 
    associated with higher risk. This allows university wellness coordinators to proactively reach out to students who might benefit 
    from support services.
    
    **Note:** This system is a screening tool, not a diagnostic instrument. High risk scores indicate students who may benefit from 
    further assessment by qualified mental health professionals.
    """)