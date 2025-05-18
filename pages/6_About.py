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
   .version-badge {
       display: inline-block;
       background-color: #4CAF50;
       color: white;
       padding: 3px 8px;
       border-radius: 12px;
       font-size: 12px;
       margin-left: 10px;
   }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>About the Depression Risk Prediction System <span class='version-badge'>v2.0</span></h1>", unsafe_allow_html=True)

# Crear columnas para centrar el contenido
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
   # Sección de Propósito
   st.markdown("<h2 class='sub-header'>Purpose & Mission</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container">
       <p>The Student Depression Risk Prediction System is an advanced, evidence-based tool designed to support university wellness coordinators and mental health professionals in identifying students who may be at risk of developing depression.</p>
       <p>Our mission is to enable early intervention through intelligent risk assessment, helping institutions provide timely support and resources to students before mental health challenges escalate into more serious conditions.</p>
       <p>Built with cutting-edge machine learning technology and informed by extensive research in student mental health, this system serves as a bridge between data science and compassionate care in educational environments.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Funcionalidades
   st.markdown("<h2 class='sub-header'>Key Features & Capabilities</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="feature-container">
       <h3>🎯 Intelligent Risk Assessment</h3>
       <p>Advanced machine learning algorithms analyze multiple student factors to calculate personalized depression risk scores, categorizing students into Low, Medium, and High risk groups with remarkable accuracy.</p>
   </div>
   
   <div class="feature-container">
       <h3>📊 Interactive Data Visualization</h3>
       <p>Comprehensive dashboards with interactive charts and graphs provide insights into risk distribution, demographics, academic factors, and mental health trends across the student population.</p>
   </div>
   
   <div class="feature-container">
       <h3>👤 Detailed Student Profiles</h3>
       <p>In-depth individual student analysis featuring specific risk factors, protective factors, and evidence-based recommendations tailored to each student's unique circumstances.</p>
   </div>
   
   <div class="feature-container">
       <h3>🔍 Feature Contribution Analysis</h3>
       <p>Advanced interpretation tools that break down which factors contribute most significantly to a student's depression risk, enabling targeted and effective intervention strategies.</p>
   </div>
   
   <div class="feature-container">
       <h3>🛡️ Enterprise-Grade Security</h3>
       <p>Role-based authentication and secure data handling ensure that sensitive student information is protected and only accessible to authorized personnel with appropriate credentials.</p>
   </div>
   
   <div class="feature-container">
       <h3>📋 Comprehensive Reporting</h3>
       <p>Detailed reports and exportable data for administrative review, compliance documentation, and integration with existing student information systems.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Sección de Metodología
   st.markdown("<h2 class='sub-header'>Scientific Methodology</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container">
       <p>The Depression Risk Prediction System employs a sophisticated Random Forest machine learning model, trained on a comprehensive dataset of student records with validated depression assessments. Our methodology combines multiple data science techniques to ensure accuracy and reliability.</p>
   </div>
   """, unsafe_allow_html=True)
   
   st.markdown("#### Key Assessment Factors:")
   st.markdown("""
   - **Academic Performance:** CGPA, course load, study satisfaction levels
   - **Lifestyle Factors:** Sleep patterns, exercise habits, dietary choices  
   - **Stress Indicators:** Academic pressure, financial stress, work-study balance
   - **Social & Environmental:** Social support systems, living situations
   - **Health History:** Family mental health history, previous mental health experiences
   - **Behavioral Patterns:** Study habits, social engagement, extracurricular participation
   - **Psychological Indicators:** Stress coping mechanisms, emotional regulation
   """)
   
   st.markdown("#### Model Validation:")
   st.info("Our prediction model has been rigorously tested and validated using cross-validation techniques, achieving high accuracy rates while maintaining sensitivity to diverse student populations and backgrounds.")
   
   st.markdown("*The system uses this comprehensive information to calculate a risk percentage that indicates the likelihood of a student experiencing depression. This serves as a screening tool to identify students who may benefit from further assessment and support.*")
   
   # Sección de Tecnologías
   st.markdown("<h2 class='sub-header'>Technology Stack</h2>", unsafe_allow_html=True)
   
   st.markdown("Built with modern, industry-standard technologies for optimal performance, scalability, and maintainability:")
   
   col1_tech, col2_tech, col3_tech = st.columns(3)
   
   with col1_tech:
       st.markdown("#### Core Technologies")
       st.markdown("""
       <div style="text-align: center; margin: 15px 0;">
           <span class="tech-badge">Python 3.9+</span><br>
           <span class="tech-badge">Streamlit</span><br>
           <span class="tech-badge">Scikit-learn</span><br>
           <span class="tech-badge">Pandas</span><br>
           <span class="tech-badge">NumPy</span>
       </div>
       """, unsafe_allow_html=True)
   
   with col2_tech:
       st.markdown("#### Visualization & UI")
       st.markdown("""
       <div style="text-align: center; margin: 15px 0;">
           <span class="tech-badge">Plotly</span><br>
           <span class="tech-badge">Matplotlib</span><br>
           <span class="tech-badge">Custom CSS</span><br>
           <span class="tech-badge">Responsive Design</span>
       </div>
       """, unsafe_allow_html=True)
   
   with col3_tech:
       st.markdown("#### ML & Analytics")
       st.markdown("""
       <div style="text-align: center; margin: 15px 0;">
           <span class="tech-badge">Random Forest</span><br>
           <span class="tech-badge">Feature Engineering</span><br>
           <span class="tech-badge">Cross-Validation</span><br>
           <span class="tech-badge">SHAP Analysis</span>
       </div>
       """, unsafe_allow_html=True)
   
   st.info("The machine learning foundation utilizes Random Forest classifiers, chosen for their excellent performance with mixed data types, interpretability, and robustness against overfitting in healthcare applications.")
   
   # Sección de Nota Importante
   st.markdown("<h2 class='sub-header'>Important Usage Guidelines</h2>", unsafe_allow_html=True)
   
   st.error("**🚨 Critical Disclaimer**\n\nThis system is a screening and assessment tool, not a diagnostic instrument. High risk scores indicate students who may benefit from further evaluation by qualified mental health professionals.")
   
   st.markdown("#### 📋 Best Practices for Implementation")
   st.markdown("""
   - Use predictions as one component of a comprehensive mental health strategy
   - Always combine system insights with direct communication and observation
   - Ensure all interventions are conducted by qualified professionals
   - Maintain strict confidentiality and follow institutional privacy protocols
   - Regularly update and validate the model with new data
   - Provide appropriate training for all staff using the system
   """)
   
   st.warning("**🔒 Privacy & Ethics**\n\nStudent privacy and confidentiality are paramount. All data processing follows established ethical guidelines for educational technology and healthcare applications. Users must adhere to institutional policies and applicable regulations regarding student data protection.")
   
   # Sección de Equipo
   st.markdown("<h2 class='sub-header'>Development Team</h2>", unsafe_allow_html=True)
   
   col1_team, col2_team = st.columns(2)
   
   with col1_team:
       st.markdown("""
       <div class="team-member">
           <h3>Rodrigo Osorio</h3>
           <p><strong>Lead Developer & Data Scientist</strong></p>
           <p>Murdoch University Student</p>
           <p>Specialized in machine learning applications for healthcare and educational technology. Responsible for model development, system architecture, and algorithm optimization.</p>
       </div>
       """, unsafe_allow_html=True)
   
   with col2_team:
       st.markdown("""
       <div class="team-member">
           <h3>Mia Song</h3>
           <p><strong>UI/UX Designer & Frontend Developer</strong></p>
           <p>Murdoch University Student</p>
           <p>Expert in user experience design and interface development. Led the creation of intuitive dashboards and user-friendly interfaces for complex data visualization.</p>
       </div>
       """, unsafe_allow_html=True)
   
   # Acknowledgments
   st.markdown("#### Acknowledgments")
   st.markdown("""
   We extend our gratitude to:
   - **Murdoch University** for providing the educational foundation and research environment
   - **Mental Health Professionals** who provided domain expertise and validation
   - **Student Affairs Departments** for insights into practical implementation needs
   - **Open Source Community** for the excellent tools and libraries that made this project possible
   """)
   
   # Información de versión y actualizaciones
   st.markdown("<h2 class='sub-header'>Version Information</h2>", unsafe_allow_html=True)
   
   col1_version, col2_version = st.columns(2)
   
   with col1_version:
       st.markdown("""
       <div class="feature-container">
           <h4>📦 Current Version</h4>
           <p><strong>Version 2.0</strong> - Released December 2024</p>
           <p>Major update featuring enhanced UI, interactive visualizations, and improved prediction accuracy.</p>
       </div>
       """, unsafe_allow_html=True)
   
   with col2_version:
       st.markdown("""
       <div class="feature-container">
           <h4>🔄 Recent Updates</h4>
           <ul>
               <li>Interactive Plotly charts</li>
               <li>Enhanced feature contribution analysis</li>
               <li>Improved user interface design</li>
               <li>Advanced filtering capabilities</li>
               <li>Comprehensive documentation</li>
           </ul>
       </div>
       """, unsafe_allow_html=True)
   
   # Sección de Contacto y Soporte
   st.markdown("<h2 class='sub-header'>Contact & Support</h2>", unsafe_allow_html=True)
   
   col1_contact, col2_contact = st.columns(2)
   
   with col1_contact:
       st.markdown("#### 📧 Technical Support")
       st.markdown("For technical issues, feature requests, or system support:")
       st.code("support@depressionrisksystem.edu")
       
       st.markdown("#### 🏢 Institutional Inquiries") 
       st.markdown("For implementation guidance, training, or institutional partnerships:")
       st.code("partnerships@depressionrisksystem.edu")
   
   with col2_contact:
       st.markdown("#### 🏛️ Office Location")
       st.markdown("""
       University Mental Health Services  
       Innovation Hub, Building 402  
       Murdoch University, WA 6150
       """)
       
       st.info("💬 **Response Time:** Technical support inquiries are typically addressed within 24-48 hours during business days.")