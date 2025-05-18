# Student Depression Risk Prediction System

## 🌟 Live Demo
**Try the system now:** [https://depressionpredictordemo-cphottfvyylzyswdi7zvs2.streamlit.app/](https://depressionpredictordemo-cphottfvyylzyswdi7zvs2.streamlit.app/)

## 📋 Project Overview

This is an academic demonstration project developed for the **ICT619 Artificial Intelligence** unit, Semester 1, 2025, at Murdoch University, Western Australia, Australia.

The Student Depression Risk Prediction System demonstrates the application of machine learning techniques to mental health screening in educational settings. This web application is designed for wellbeing services coordinators who seek to proactively address early signs of depression in students through data-driven insights.

## 🎯 Purpose

- **Academic Objective**: Showcase practical implementation of AI and machine learning concepts
- **Target Users**: University wellbeing coordinators and mental health professionals
- **Functionality**: Predict depression risk scores from student survey data
- **Goal**: Enable early intervention through intelligent risk assessment

## ✨ Key Features

- **🎯 Intelligent Risk Assessment**: ML algorithms analyze multiple student factors to calculate personalized depression risk scores
- **📊 Interactive Data Visualization**: Comprehensive dashboards with interactive charts showing risk distribution and trends
- **👤 Detailed Student Profiles**: In-depth individual analysis with risk factors and evidence-based recommendations
- **🔍 Feature Contribution Analysis**: Advanced tools showing which factors contribute most to depression risk
- **🛡️ Secure Authentication**: Role-based access control for sensitive student information
- **📱 Responsive Design**: Works seamlessly across desktop and mobile devices

## 🔧 Technology Stack

### Core Technologies
- **Python 3.9+**: Main programming language
- **Streamlit**: Web application framework
- **Scikit-learn**: Machine learning algorithms
- **Pandas & NumPy**: Data manipulation and analysis

### Visualization & UI
- **Plotly**: Interactive data visualizations
- **Matplotlib**: Additional plotting capabilities
- **Custom CSS**: Responsive design and styling

### Machine Learning
- **Random Forest**: Primary prediction algorithm
- **Feature Engineering**: Data preprocessing and transformation
- **Cross-Validation**: Model validation techniques

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/depression-prediction-system.git
   cd depression-prediction-system
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`
   - Use demo credentials: `user_test` / `P@ssw0rd123!`

## 📁 Project Structure

```
depression-prediction-system/
├── app.py                          # Main application file
├── utils.py                        # Utility functions
├── requirements.txt                 # Python dependencies
├── pages/
│   ├── 1_Login.py                  # Authentication page
│   ├── 2_Predict.py                # Overview dashboard
│   ├── 3_Student_List.py           # Student list with filters
│   ├── 4_Student_Details_&_Analysis.py  # Individual student analysis
│   ├── 5_Prediction_Analysis.py    # Feature contribution analysis
│   ├── 6_About.py                  # Project information
│   └── 7_FAQs.py                   # Frequently asked questions
├── model/
│   ├── depression_model.pkl        # Trained ML model
│   ├── preprocessor.pkl            # Data preprocessing pipeline
│   └── feature_columns.pkl         # Required feature columns
└── data/
    └── sample_data.csv             # Sample dataset for testing
```

## 📊 How to Use

1. **Login**: Access the system using provided demo credentials
2. **Upload Data**: Navigate to the Predict page and upload a CSV file with student data
3. **View Overview**: Analyze risk distribution and key metrics across all students
4. **Student List**: Browse individual students with filtering options
5. **Student Details**: View detailed risk analysis and personalized recommendations
6. **Feature Analysis**: Understand which factors contribute most to risk predictions

## 📈 Data Requirements

The system expects CSV files with the following columns:
- Student demographics (Age, Gender, Degree)
- Academic information (CGPA, Academic Pressure, Study Satisfaction)
- Lifestyle factors (Sleep Duration, Dietary Habits)
- Stress indicators (Financial Stress, Work/Study Hours)
- Health history (Family History of Mental Illness, Suicidal Thoughts)

## ⚠️ Important Disclaimers

- **Academic Use Only**: This is a demonstration project for educational purposes
- **Not for Clinical Use**: Should not replace professional mental health assessment
- **Ethical Considerations**: Real implementations require ethical approval and privacy compliance
- **No Real Data**: Do not upload actual student personal information

## 👥 Development Team

**Rodrigo Osorio**  
Master of IT Student, Murdoch University  
📧 35444036@student.murdoch.edu.au

**Mia Song**  
Master of IT Student, Murdoch University  
📧 35473397@student.murdoch.edu.au

## 🎓 Academic Context

This project demonstrates several key AI and machine learning concepts:
- Supervised learning and classification algorithms
- Feature engineering and data preprocessing
- Model evaluation and cross-validation
- Interpretation of ML results in healthcare contexts
- Ethical considerations in AI applications

## 📜 License

This project is developed as academic coursework for Murdoch University. Please respect academic integrity policies when referencing or building upon this work.

## 🔗 Links

- **Live Demo**: [https://depressionpredictordemo-cphottfvyylzyswdi7zvs2.streamlit.app/](https://depressionpredictordemo-cphottfvyylzyswdi7zvs2.streamlit.app/)
- **University**: [Murdoch University](https://www.murdoch.edu.au/)
- **Course**: ICT619 Artificial Intelligence

## 📞 Support

For questions about this academic project, please contact the development team using the email addresses provided above.

---

*Last updated: May 2025*  
*ICT619 Artificial Intelligence - Semester 1, 2025*  
*Murdoch University, Western Australia*