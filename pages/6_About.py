# pages/6_About.py
import streamlit as st
import os
import sys

# Añadir el directorio raíz al path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Importar utils (solo para los estilos)
try:
   from utils import set_page_style
except ImportError:
   # Función básica de estilo si no se puede importar
   def set_page_style():
       pass

# Configuración de la página
st.set_page_config(
   page_title="About the System",
   page_icon="ℹ️",
   layout="wide"
)

# Aplicar estilos personalizados
st.markdown("""
<style>
   .main-header {color:#1E88E5; font-size:42px; font-weight:bold; text-align:center; margin-bottom:30px;}
   .sub-header {color:#0D47A1; font-size:28px; font-weight:bold; margin-top:30px; margin-bottom:20px;}
   .section-text {font-size:18px; margin-bottom:20px;}
   .info-container {
       background-color: #000000; 
       padding: 20px; 
       border-radius: 10px; 
       margin-bottom: 20px;
       border: 2px solid white;
       color: white;
   }
   .feature-container {
       background-color: #f0f0f0;
       padding: 15px;
       border-radius: 8px;
       border-left: 5px solid #1E88E5;
       margin-bottom: 15px;
       color: #333333;
   }
   .tech-badge {
       display: inline-block;
       background-color: #0D47A1;
       color: white;
       padding: 5px 10px;
       border-radius: 15px;
       margin: 3px;
       font-size: 14px;
   }
   .team-member {
       background-color: #f0f0f0;
       padding: 25px;
       border-radius: 8px;
       margin-bottom: 15px;
       color: #333333;
       text-align: center;
   }
   .team-member h3 {
       margin-bottom: 15px;
   }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>About the Depression Risk Prediction System</h1>", unsafe_allow_html=True)

# Crear columnas para centrar el contenido
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
   # Sección de Propósito
   st.markdown("<h2 class='sub-header'>Purpose & Mission</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container">
       <p>The Student Depression Risk Prediction System was developed to address the growing concern of mental health issues among university students. Our mission is to provide educational institutions with tools to identify students who may be at risk of developing depression, enabling timely intervention and support.</p>
       <p>Mental health challenges can significantly impact academic performance, social relationships, and overall well-being. By proactively identifying at-risk students, universities can offer targeted resources and support services before these challenges escalate.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Funcionalidades
   st.markdown("<h2 class='sub-header'>Key Features</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="feature-container">
       <h3>Risk Assessment</h3>
       <p>The system analyzes various factors from student data to calculate a depression risk score, categorizing students into Low, Medium, and High risk groups.</p>
   </div>
   
   <div class="feature-container">
       <h3>Data Visualization</h3>
       <p>Interactive dashboards provide an overview of risk distribution across the student population, helping administrators identify patterns and trends.</p>
   </div>
   
   <div class="feature-container">
       <h3>Individual Student Profiles</h3>
       <p>Detailed profiles for each student showcase specific risk factors and personalized recommendations for support.</p>
   </div>
   
   <div class="feature-container">
       <h3>Factor Analysis</h3>
       <p>The system breaks down which factors contribute most significantly to a student's depression risk, enabling targeted intervention strategies.</p>
   </div>
   
   <div class="feature-container">
       <h3>Secure Access</h3>
       <p>Role-based authentication ensures that sensitive student information is only accessible to authorized personnel.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Metodología
   st.markdown("<h2 class='sub-header'>Methodology</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container">
       <p>The Depression Risk Prediction System employs a machine learning model trained on a comprehensive dataset of student records where depression status was previously assessed. The model identifies patterns and correlations between various factors and depression outcomes.</p>
       <p>Key factors analyzed include:</p>
       <ul>
           <li>Academic performance (CGPA, course load)</li>
           <li>Sleep patterns and duration</li>
           <li>Academic and work pressure</li>
           <li>Financial stress levels</li>
           <li>Social support systems</li>
           <li>Family history of mental health conditions</li>
           <li>Personal health habits</li>
           <li>Past experiences with mental health challenges</li>
       </ul>
       <p>The system uses this information to calculate a risk percentage that indicates the likelihood of a student experiencing depression. This is not a clinical diagnosis but rather a screening tool to identify students who may benefit from further assessment and support.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Tecnologías
   st.markdown("<h2 class='sub-header'>Technologies Used</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <p class="section-text">This system was built using a stack of modern technologies for data analysis and web application development:</p>
   
   <div style="text-align: center; margin: 30px 0;">
       <span class="tech-badge">Python</span>
       <span class="tech-badge">Streamlit</span>
       <span class="tech-badge">Scikit-learn</span>
       <span class="tech-badge">Pandas</span>
       <span class="tech-badge">NumPy</span>
       <span class="tech-badge">Matplotlib</span>
       <span class="tech-badge">Plotly</span>
       <span class="tech-badge">Seaborn</span>
   </div>
   
   <p class="section-text">The machine learning model at the core of the system is a Random Forest classifier, which was selected for its accuracy, interpretability, and ability to handle mixed data types.</p>
   """, unsafe_allow_html=True)
   
   # Sección de Nota Importante
   st.markdown("<h2 class='sub-header'>Important Note</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container" style="border-color: #F44336;">
       <p><strong>This system is a screening tool, not a diagnostic instrument.</strong> High risk scores indicate students who may benefit from further assessment by qualified mental health professionals.</p>
       <p>The predictions made by this system should be used as one factor in a comprehensive approach to student well-being, alongside direct communication, professional clinical assessment, and established mental health protocols.</p>
       <p>Always prioritize student privacy and confidentiality when using this system, and ensure that any interventions are conducted with sensitivity and respect.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Equipo
   st.markdown("<h2 class='sub-header'>Development Team</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="team-member">
       <h3>Team members</h3>
       <h3>Rodrigo Osorio - Murdoch University Student</h3>
       <h3>Mia Song - Murdoch University Student</h3>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Contacto
   st.markdown("<h2 class='sub-header'>Contact & Support</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container">
       <p>For questions, feedback, or support regarding the Depression Risk Prediction System, please contact:</p>
       <p style="text-align: center; font-weight: bold; margin-top: 15px;">support@depressionrisksystem.edu</p>
       <p style="text-align: center;">University Mental Health Services, Office 302</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Añadir un botón para ir al login (opcional)
   st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
   if st.button("Login to Access the System", type="primary"):
       st.switch_page("pages/1_Login.py")
   st.markdown("</div>", unsafe_allow_html=True)