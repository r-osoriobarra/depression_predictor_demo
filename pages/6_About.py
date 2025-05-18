import streamlit as st
import os
import sys

# Add the root directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import utils (only for styles)
try:
   from utils import set_page_style
except ImportError:
   # Basic style function if import fails
   def set_page_style():
       pass

# Page configuration
st.set_page_config(
   page_title="About the System",
   page_icon="ℹ️",
   layout="wide"
)

# Apply custom styles
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

# Main title
st.markdown("<h1 class='main-header'>About the Depression Risk Prediction System <span class='version-badge'>v2.0</span></h1>", unsafe_allow_html=True)

# Create columns to center the content
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
   # Purpose section
   st.markdown("<h2 class='sub-header'>Purpose</h2>", unsafe_allow_html=True)
   
   st.markdown("""
   <div class="info-container">
       <p>This project is developed as an assignment for the ICT619 Artificial Intelligence unit, Semester 1, 2025, at Murdoch University, Western Australia, Australia.</p>
       <p>The purpose of this web application is to demonstrate a comprehensive depression risk prediction system for university students. This demo is specifically designed for wellbeing services coordinators who seek to proactively address early signs of depression in students through data-driven insights.</p>
       <p>The system allows coordinators to upload survey data from students, which is then processed by our machine learning model to predict depression risk percentages. By identifying at-risk students early, institutions can implement preventive interventions and provide targeted support before mental health challenges become more severe, ultimately improving student wellbeing and academic success.</p>
   </div>
   """, unsafe_allow_html=True)
   
   # Key features section
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
   
   # Scientific methodology section
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
   
   st.markdown("*The system uses this comprehensive information to calculate a risk percentage that indicates the likelihood of a student experiencing depression. This serves as a screening tool to identify students who may benefit from further assessment and support.*")
   
   # Technology stack section
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
      
   # Contact and support section
   st.markdown("<h2 class='sub-header'>Contact & Support</h2>", unsafe_allow_html=True)
   
   col1_team, col2_team = st.columns(2)
   
   with col1_team:
       st.markdown("""
       <div class="team-member">
           <h3>Rodrigo Osorio</h3>
           <p><strong>Master of IT Student</strong></p>
           <p>Murdoch University</p>
           <p>📧 35444036@student.murdoch.edu.au</p>
       </div>
       """, unsafe_allow_html=True)
   
   with col2_team:
       st.markdown("""
       <div class="team-member">
           <h3>Mia Song</h3>
           <p><strong>Master of IT Student</strong></p>
           <p>Murdoch University</p>
           <p>📧 35473397@student.murdoch.edu.au</p>
       </div>
       """, unsafe_allow_html=True)