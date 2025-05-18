# pages/7_FAQs.py
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
   page_title="FAQ - Frequently Asked Questions",
   page_icon="❓",
   layout="wide"
)

# Apply custom styles
st.markdown("""
<style>
   .main-header {color:#1E88E5; font-size:42px; font-weight:bold; text-align:center; margin-bottom:30px;}
   .sub-header {color:#0D47A1; font-size:28px; font-weight:bold; margin-top:30px; margin-bottom:20px;}
   .faq-container {
       background-color: #000000; 
       padding: 20px; 
       border-radius: 10px; 
       margin-bottom: 20px;
       border: 2px solid white;
       color: white;
   }
   .faq-question {
       color: #1E88E5;
       font-size: 18px;
       font-weight: bold;
       margin-bottom: 10px;
   }
   .faq-answer {
       color: white;
       font-size: 16px;
       margin-bottom: 15px;
       line-height: 1.6;
   }
   .category-header {
       background-color: #1E88E5;
       color: white;
       padding: 10px 20px;
       border-radius: 8px;
       font-size: 20px;
       font-weight: bold;
       margin: 25px 0 15px 0;
       text-align: center;
   }
   .navigation-container {
       border: 2px solid white;
       border-radius: 10px;
       padding: 20px;
       margin-bottom: 20px;
       background-color: transparent;
       text-align: center;
   }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("<h1 class='main-header'>Frequently Asked Questions</h1>", unsafe_allow_html=True)

# Create columns to center the content
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    # Introduction
    st.markdown("""
    <div class="faq-container">
        <p>Welcome to the FAQ section for the Student Depression Risk Prediction System. Here you'll find answers to common questions about our demo application, how it works, and its academic purpose.</p>
        <p>This system is developed as part of an academic project for the ICT619 Artificial Intelligence unit at Murdoch University.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # General Questions
    st.markdown("<div class='category-header'>🔍 General Questions</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Q: What is the Student Depression Risk Prediction System?**")
        st.markdown("A: This is an academic demonstration project that uses machine learning to predict depression risk in university students. It's designed as a tool for wellbeing coordinators to identify students who may need mental health support.")
        
        st.markdown("**Q: Is this a real clinical tool?**")
        st.markdown("A: No, this is an academic demonstration project developed for the ICT619 Artificial Intelligence unit at Murdoch University. It is not intended for actual clinical use or real student assessment.")
        
        st.markdown("**Q: Who developed this system?**")
        st.markdown("A: This system was developed by Rodrigo Osorio and Mia Song, both Master of IT students at Murdoch University, Western Australia, as part of their ICT619 coursework.")
    
    # Technical Questions
    st.markdown("<div class='category-header'>⚙️ Technical Questions</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Q: What technology is used in this system?**")
        st.markdown("A: The system is built using Python with Streamlit for the web interface, Scikit-learn for machine learning, and Plotly for interactive visualizations. The prediction model uses Random Forest algorithms.")
        
        st.markdown("**Q: What data does the system analyze?**")
        st.markdown("A: The system analyzes various factors including academic performance (CGPA), lifestyle factors (sleep, diet), stress indicators (academic pressure, financial stress), and health history. All data is processed through a trained machine learning model.")
        
        st.markdown("**Q: How accurate are the predictions?**")
        st.markdown("A: While the model has been trained and validated using standard machine learning techniques, accuracy can vary. Remember, this is an academic demonstration and should not be used for actual mental health assessment.")
    
    # Usage Questions
    st.markdown("<div class='category-header'>💻 Usage Questions</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Q: How do I access the system?**")
        st.markdown("A: You need to log in using the demo credentials provided on the login page. The system requires authentication to access the prediction and analysis features.")
        
        st.markdown("**Q: What format should my data be in?**")
        st.markdown("A: Data should be uploaded as a CSV file containing all required student information fields. The system will validate the data format upon upload and notify you of any missing columns.")
        
        st.markdown("**Q: Can I download or export results?**")
        st.markdown("A: Currently, the demo version focuses on visualization and analysis within the web interface. Export functionality is not available in this academic demonstration version.")
        
        st.markdown("**Q: Why can't I access certain pages without logging in?**")
        st.markdown("A: The prediction and analysis features require login to demonstrate a realistic security model. However, informational pages like About and FAQ are accessible without authentication.")
    
    # Academic Context
    st.markdown("<div class='category-header'>🎓 Academic Context</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Q: What is the purpose of this project?**")
        st.markdown("A: This project demonstrates the application of artificial intelligence and machine learning techniques to mental health screening in educational settings. It's an assignment for the ICT619 unit, showcasing practical implementation of AI concepts.")
        
        st.markdown("**Q: Can this system be used in real universities?**")
        st.markdown("A: While the concept could be adapted for real-world use, this current version is purely for academic demonstration. Real implementation would require extensive validation, ethical approval, and compliance with privacy regulations.")
        
        st.markdown("**Q: What machine learning concepts does this project demonstrate?**")
        st.markdown("A: The project demonstrates supervised learning, classification algorithms (Random Forest), feature engineering, data preprocessing, model evaluation, and interpretation of machine learning results in a healthcare context.")
    
    # Privacy and Ethics
    st.markdown("<div class='category-header'>🔒 Privacy and Ethics</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Q: Is student data kept confidential?**")
        st.markdown("A: Since this is a demonstration system, no real student data should be uploaded. Any data uploaded is processed locally in the session and is not permanently stored or shared.")
        
        st.markdown("**Q: Should this system replace professional mental health assessment?**")
        st.markdown("A: Absolutely not. This is purely an academic demonstration. Real mental health concerns should always be addressed by qualified mental health professionals using validated clinical tools and personal assessment.")
        
        st.markdown("**Q: What are the ethical considerations of such systems?**")
        st.markdown("A: Real implementations would need to consider consent, privacy, potential bias in algorithms, the risk of false positives/negatives, and ensuring human oversight in all decisions. This demo helps students understand these important considerations.")
    
    # Support and Contact
    st.markdown("<div class='category-header'>📞 Support and Contact</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Q: Who can I contact for technical issues?**")
        st.markdown("""
        A: For technical questions or issues with the demo, you can contact the developers:
        - Rodrigo Osorio: 35444036@student.murdoch.edu.au
        - Mia Song: 35473397@student.murdoch.edu.au
        """)
        
        st.markdown("**Q: Can I use this code for my own project?**")
        st.markdown("A: This is an academic project submitted as coursework. Please respect academic integrity policies. If you're interested in similar projects, consider developing your own implementation or properly citing this work according to your institution's guidelines.")
        
        st.markdown("**Q: Where can I learn more about the project?**")
        st.markdown("A: Check the About page for more detailed information about the project's purpose, methodology, and technical implementation.")
    
    # Navigation section
    st.markdown("### Ready to explore the system?")
    st.markdown("Visit other sections to learn more about the project.")
    
    # Navigation buttons
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    
    with col_nav1:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    
    with col_nav2:
        if st.button("ℹ️ About", use_container_width=True):
            st.switch_page("pages/6_About.py")
    
    with col_nav3:
        if st.button("🔐 Login", use_container_width=True):
            st.switch_page("pages/1_Login.py")