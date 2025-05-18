import streamlit as st
import pandas as pd
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import set_page_style, check_login
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

st.set_page_config(page_title="Overview", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Overview Dashboard</h1>",
           unsafe_allow_html=True)

# Check login status
if not check_login():
   st.stop()

# Load model, preprocessor and columns


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

# File upload with improved UI
st.markdown("<h2 class='sub-header'>Upload Student Data</h2>",
           unsafe_allow_html=True)
st.markdown("""
Upload a CSV file containing student data with all the required features for depression risk prediction.
""")

# Show required columns in an expander
with st.expander("View Required Columns"):
   st.code(", ".join(feature_columns))

uploaded_file = st.file_uploader("Upload student data CSV", type=["csv"])

if uploaded_file is not None:
   try:
       df = pd.read_csv(uploaded_file)

       # Check if all required columns are present
       missing_cols = [
           col for col in feature_columns if col not in df.columns]
       if missing_cols:
           st.error(f"Missing required columns: {', '.join(missing_cols)}")
           st.stop()

       # Apply model to predict depression risk
       X = df[feature_columns]
       X_transformed = preprocessor.transform(X)
       df["Depression Risk (%)"] = model.predict_proba(
           X_transformed)[:, 1] * 100

       # Create risk categories
       df['Risk Category'] = pd.cut(
           df["Depression Risk (%)"],
           bins=[0, 30, 60, 100],
           labels=["Low", "Medium", "High"]
       )

       # Store in session_state for later use
       st.session_state["latest_df"] = df

       # Show success message
       st.success(
           f"Data loaded successfully. {len(df)} student records processed.")

       # Display key metrics in cards with custom container
       st.markdown("<h2 class='sub-header'>Key Metrics</h2>",
                   unsafe_allow_html=True)

       # Calculate metrics
       high_risk_count = (df["Risk Category"] == "High").sum()
       high_risk_percent = high_risk_count / len(df) * 100
       avg_risk = df["Depression Risk (%)"].mean()
       
       # Determine color for high risk percentage based on new rules
       if high_risk_percent > 70:
           percentage_color = "#D32F2F"  # Red for high
       elif high_risk_percent >= 30:
           percentage_color = "#F57C00"  # Orange for medium
       else:
           percentage_color = "#388E3C"  # Green for low

       # Determine color for average risk
       if avg_risk > 70:
           avg_risk_color = "#D32F2F"  # Red for high
       elif avg_risk >= 30:
           avg_risk_color = "#F57C00"  # Orange for medium
       else:
           avg_risk_color = "#388E3C"  # Green for low

       # Custom container with white border and no background
       st.markdown("""
       <style>
       .metrics-container {
           border: 2px solid white;
           border-radius: 10px;
           padding: 20px;
           margin-bottom: 20px;
           background-color: transparent;
       }
       .custom-metric {
           text-align: center;
           color: white;
       }
       .metric-value {
           font-size: 2rem;
           font-weight: bold;
           margin-bottom: 0.5rem;
       }
       .metric-label {
           font-size: 1.2rem;
           color: #CCCCCC;
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

       col1, col2, col3 = st.columns(3)

       with col1:
           st.markdown(f"""
           <div class="metrics-container">
               <div class="custom-metric">
                   <div class="metric-value" style="color: white;">{len(df)}</div>
                   <div class="metric-label">Number of Students</div>
               </div>
           </div>
           """, unsafe_allow_html=True)

       with col2:
           st.markdown(f"""
           <div class="metrics-container">
               <div class="custom-metric">
                   <div class="metric-value" style="color: {avg_risk_color};">{round(avg_risk, 1)}%</div>
                   <div class="metric-label">Average Risk</div>
               </div>
           </div>
           """, unsafe_allow_html=True)

       with col3:
           st.markdown(f"""
           <div class="metrics-container">
               <div class="custom-metric">
                   <div class="metric-value" style="color: white;">{high_risk_count}</div>
                   <div class="metric-label">Number of High Risk Students <span style="color: {percentage_color};">({high_risk_percent:.1f}%)</span></div>
               </div>
           </div>
           """, unsafe_allow_html=True)

       # Interactive visualizations in tabs
       st.markdown("<h2 class='sub-header'>Data Visualizations</h2>",
                   unsafe_allow_html=True)
       tab1, tab2, tab3, tab4 = st.tabs(
           ["Risk Distribution", "Demographics", "Academic Factors", "Mental Health & Lifestyle Factors"])

       with tab1:
           # Risk distribution visualization
           col1, col2 = st.columns(2)

           with col1:
               # Interactive histogram of risk scores
               fig_hist = px.histogram(
                   df, 
                   x="Depression Risk (%)",
                   nbins=20,
                   title='Distribution of Depression Risk Scores'
               )
               fig_hist.add_vline(x=30, line_dash="dash", line_color="#F57C00", 
                                 annotation_text="Low/Medium threshold")
               fig_hist.add_vline(x=60, line_dash="dash", line_color="#D32F2F", 
                                 annotation_text="Medium/High threshold")
               fig_hist.update_layout(
                   xaxis_title="Risk Score (%)",
                   yaxis_title="Number of Students",
                   template="plotly_white"
               )
               st.plotly_chart(fig_hist, use_container_width=True)

           with col2:
               # Interactive pie chart of risk categories with correct color mapping
               risk_counts = df['Risk Category'].value_counts()
               
               # Create color mapping based on category names
               color_map = {'Low': '#388E3C', 'Medium': '#F57C00', 'High': '#D32F2F'}
               colors = [color_map[category] for category in risk_counts.index]
               
               fig_pie = px.pie(
                   values=risk_counts.values,
                   names=risk_counts.index,
                   title='Distribution of Risk Categories',
                   color=risk_counts.index,
                   color_discrete_map=color_map
               )
               fig_pie.update_traces(textposition='inside', textinfo='percent+label')
               st.plotly_chart(fig_pie, use_container_width=True)

       with tab2:
           # Demographics analysis
           if 'Gender' in df.columns:
               col1, col2 = st.columns(2)

               with col1:
                   # Interactive box plot for risk by gender
                   fig_box = px.box(
                       df, 
                       x='Gender', 
                       y='Depression Risk (%)',
                       title='Depression Risk by Gender'
                   )
                   fig_box.update_layout(template="plotly_white")
                   st.plotly_chart(fig_box, use_container_width=True)

               with col2:
                   # Interactive scatter plot for risk by age (if available)
                   if 'Age' in df.columns:
                       fig_scatter = px.scatter(
                           df, 
                           x='Age', 
                           y='Depression Risk (%)', 
                           color='Risk Category',
                           color_discrete_map={
                               'Low': '#388E3C',
                               'Medium': '#F57C00',
                               'High': '#D32F2F'
                           },
                           title='Depression Risk by Age'
                       )
                       fig_scatter.update_layout(template="plotly_white")
                       st.plotly_chart(fig_scatter, use_container_width=True)
                   else:
                       st.info("Age data not available for visualization.")
           else:
               st.info("Demographic data not available for visualization.")

       with tab3:
           # Academic factors analysis
           col1, col2 = st.columns(2)

           with col1:
               # Interactive scatter plot for risk by CGPA
               if 'CGPA' in df.columns:
                   fig_cgpa = px.scatter(
                       df, 
                       x='CGPA', 
                       y='Depression Risk (%)', 
                       color='Risk Category',
                       color_discrete_map={
                           'Low': '#388E3C',
                           'Medium': '#F57C00',
                           'High': '#D32F2F'
                       },
                       title='Depression Risk by CGPA'
                   )
                   fig_cgpa.update_layout(template="plotly_white")
                   st.plotly_chart(fig_cgpa, use_container_width=True)
               else:
                   st.info("CGPA data not available for visualization.")

           with col2:
               # Interactive bar chart for risk by degree (if available)
               if 'Degree' in df.columns:
                   degree_risk = df.groupby('Degree')['Depression Risk (%)'].mean().sort_values(ascending=False)
                   
                   fig_degree = px.bar(
                       x=degree_risk.index,
                       y=degree_risk.values,
                       title='Average Depression Risk by Degree Program',
                       labels={'x': 'Degree', 'y': 'Average Risk (%)'}
                   )
                   fig_degree.update_layout(
                       template="plotly_white",
                       showlegend=False
                   )
                   st.plotly_chart(fig_degree, use_container_width=True)
               else:
                   st.info("Degree data not available for visualization.")

           # Additional Academic Factors
           col3, col4 = st.columns(2)

           with col3:
               # Scatter plot: CGPA vs Hours of Study colored by risk
               if 'CGPA' in df.columns and 'Work/Study Hours' in df.columns:
                   fig_cgpa_hours = px.scatter(
                       df,
                       x='CGPA',
                       y='Work/Study Hours',
                       color='Risk Category',
                       color_discrete_map={
                           'Low': '#388E3C',
                           'Medium': '#F57C00',
                           'High': '#D32F2F'
                       },
                       title='CGPA vs Study Hours by Risk Level'
                   )
                   fig_cgpa_hours.update_layout(template="plotly_white")
                   st.plotly_chart(fig_cgpa_hours, use_container_width=True)
               else:
                   st.info("CGPA or Work/Study Hours data not available.")

           with col4:
               # Box plot: Risk distribution by degree level
               if 'Degree' in df.columns:
                   fig_degree_box = px.box(
                       df,
                       x='Degree',
                       y='Depression Risk (%)',
                       title='Risk Distribution by Degree Level'
                   )
                   fig_degree_box.update_layout(template="plotly_white")
                   fig_degree_box.update_xaxis(tickangle=45)
                   st.plotly_chart(fig_degree_box, use_container_width=True)
               else:
                   st.info("Degree data not available for visualization.")

       with tab4:
           # Mental Health & Lifestyle Factors
           col1, col2 = st.columns(2)

           with col1:
               # Pie chart: Sleep duration distribution
               if 'Sleep Duration' in df.columns:
                   sleep_counts = df['Sleep Duration'].value_counts()
                   fig_sleep = px.pie(
                       values=sleep_counts.values,
                       names=sleep_counts.index,
                       title='Sleep Duration Distribution'
                   )
                   fig_sleep.update_traces(textposition='inside', textinfo='percent+label')
                   st.plotly_chart(fig_sleep, use_container_width=True)
               else:
                   st.info("Sleep Duration data not available.")

           with col2:
               # Stacked bar: Dietary habits vs risk level
               if 'Dietary Habits' in df.columns:
                   dietary_risk = df.groupby(['Dietary Habits', 'Risk Category']).size().unstack(fill_value=0)
                   fig_dietary = px.bar(
                       dietary_risk,
                       title='Dietary Habits vs Risk Level',
                       color_discrete_map={
                           'Low': '#388E3C',
                           'Medium': '#F57C00',
                           'High': '#D32F2F'
                       }
                   )
                   fig_dietary.update_layout(
                       template="plotly_white",
                       xaxis_title="Dietary Habits",
                       yaxis_title="Number of Students"
                   )
                   st.plotly_chart(fig_dietary, use_container_width=True)
               else:
                   st.info("Dietary Habits data not available.")

           # Financial stress impact visualization
           col3, col4 = st.columns(2)

           with col3:
               # Financial stress impact
               if 'Financial Stress' in df.columns:
                   # Convert financial stress to numeric if it's categorical
                   if df['Financial Stress'].dtype == 'object':
                       # Assume it's in format like 'Low', 'Medium', 'High' or numbers as strings
                       stress_mapping = {'Low': 1, 'Medium': 5, 'High': 10}
                       df['Financial Stress Numeric'] = df['Financial Stress'].map(stress_mapping)
                   else:
                       df['Financial Stress Numeric'] = df['Financial Stress']
                   
                   fig_financial = px.scatter(
                       df,
                       x='Financial Stress Numeric',
                       y='Depression Risk (%)',
                       color='Risk Category',
                       color_discrete_map={
                           'Low': '#388E3C',
                           'Medium': '#F57C00',
                           'High': '#D32F2F'
                       },
                       title='Financial Stress vs Depression Risk'
                   )
                   fig_financial.update_layout(
                       template="plotly_white",
                       xaxis_title="Financial Stress Level"
                   )
                   st.plotly_chart(fig_financial, use_container_width=True)
               else:
                   st.info("Financial Stress data not available.")

           with col4:
               # Academic pressure impact
               if 'Academic Pressure' in df.columns:
                   # Convert academic pressure to numeric if it's categorical
                   if df['Academic Pressure'].dtype == 'object':
                       pressure_mapping = {'Low': 1, 'Medium': 5, 'High': 10}
                       df['Academic Pressure Numeric'] = df['Academic Pressure'].map(pressure_mapping)
                   else:
                       df['Academic Pressure Numeric'] = df['Academic Pressure']
                   
                   fig_academic = px.scatter(
                       df,
                       x='Academic Pressure Numeric',
                       y='Depression Risk (%)',
                       color='Risk Category',
                       color_discrete_map={
                           'Low': '#388E3C',
                           'Medium': '#F57C00',
                           'High': '#D32F2F'
                       },
                       title='Academic Pressure vs Depression Risk'
                   )
                   fig_academic.update_layout(
                       template="plotly_white",
                       xaxis_title="Academic Pressure Level"
                   )
                   st.plotly_chart(fig_academic, use_container_width=True)
               else:
                   st.info("Academic Pressure data not available.")

           # Gauge charts for critical indicators
           st.markdown("### Critical Mental Health Indicators")
           col5, col6 = st.columns(2)

           with col5:
               # Gauge chart: Percentage of students with suicidal thoughts
               if 'Have you ever had suicidal thoughts ?' in df.columns:
                   suicidal_thoughts_yes = df[df['Have you ever had suicidal thoughts ?'] == 'Yes'].shape[0]
                   suicidal_thoughts_percent = (suicidal_thoughts_yes / len(df)) * 100
                   
                   fig_suicidal = go.Figure(go.Indicator(
                       mode = "gauge+number",
                       value = suicidal_thoughts_percent,
                       domain = {'x': [0, 1], 'y': [0, 1]},
                       title = {'text': "Students with Suicidal Thoughts (%)"},
                       gauge = {
                           'axis': {'range': [None, 100]},
                           'bar': {'color': "#D32F2F"},
                           'steps': [
                               {'range': [0, 10], 'color': "#E8F5E9"},
                               {'range': [10, 25], 'color': "#FFF3E0"},
                               {'range': [25, 100], 'color': "#FFEBEE"}
                           ],
                           'threshold': {
                               'line': {'color': "red", 'width': 4},
                               'thickness': 0.75,
                               'value': 25
                           }
                       }
                   ))
                   fig_suicidal.update_layout(height=300)
                   st.plotly_chart(fig_suicidal, use_container_width=True)
               else:
                   st.info("Suicidal thoughts data not available.")

           with col6:
               # Gauge chart: Percentage of students with low study satisfaction
               if 'Study Satisfaction' in df.columns:
                   # Assume low satisfaction is 4 or below on a 1-10 scale
                   if df['Study Satisfaction'].dtype == 'object':
                       # If it's categorical, map to numbers
                       satisfaction_mapping = {'Very Low': 1, 'Low': 3, 'Medium': 5, 'High': 8, 'Very High': 10}
                       df['Study Satisfaction Numeric'] = df['Study Satisfaction'].map(satisfaction_mapping)
                   else:
                       df['Study Satisfaction Numeric'] = df['Study Satisfaction']
                   
                   low_satisfaction = df[df['Study Satisfaction Numeric'] <= 4].shape[0]
                   low_satisfaction_percent = (low_satisfaction / len(df)) * 100
                   
                   fig_satisfaction = go.Figure(go.Indicator(
                       mode = "gauge+number",
                       value = low_satisfaction_percent,
                       domain = {'x': [0, 1], 'y': [0, 1]},
                       title = {'text': "Students with Low Study Satisfaction (%)"},
                       gauge = {
                           'axis': {'range': [None, 100]},
                           'bar': {'color': "#F57C00"},
                           'steps': [
                               {'range': [0, 30], 'color': "#E8F5E9"},
                               {'range': [30, 50], 'color': "#FFF3E0"},
                               {'range': [50, 100], 'color': "#FFEBEE"}
                           ],
                           'threshold': {
                               'line': {'color': "orange", 'width': 4},
                               'thickness': 0.75,
                               'value': 50
                           }
                       }
                   ))
                   fig_satisfaction.update_layout(height=300)
                   st.plotly_chart(fig_satisfaction, use_container_width=True)
               else:
                   st.info("Study Satisfaction data not available.")

       # Button to view student list - centered on the page
       col1, col2, col3 = st.columns([1, 1, 1])
       with col2:
           if st.button("View Student List", use_container_width=True, type="primary"):
               st.switch_page("pages/3_Student_List.py")

   except Exception as e:
       st.error(f"Error processing data: {e}")
       st.exception(e)

elif "latest_df" in st.session_state:
   df = st.session_state["latest_df"]
   st.info("Displaying previously uploaded data. To update, upload a new file.")

   # Calculate metrics
   high_risk_count = (df["Risk Category"] == "High").sum()
   high_risk_percent = high_risk_count / len(df) * 100
   avg_risk = df["Depression Risk (%)"].mean()
   
   # Determine color for high risk percentage based on new rules
   if high_risk_percent > 70:
       percentage_color = "#D32F2F"  # Red for high
   elif high_risk_percent >= 30:
       percentage_color = "#F57C00"  # Orange for medium
   else:
       percentage_color = "#388E3C"  # Green for low

   # Determine color for average risk
   if avg_risk > 70:
       avg_risk_color = "#D32F2F"  # Red for high
   elif avg_risk >= 30:
       avg_risk_color = "#F57C00"  # Orange for medium
   else:
       avg_risk_color = "#388E3C"  # Green for low

   # Display key metrics
   st.markdown("<h2 class='sub-header'>Key Metrics</h2>",
               unsafe_allow_html=True)

   col1, col2, col3 = st.columns(3)

   with col1:
       st.markdown(f"""
       <div class="metrics-container">
           <div class="custom-metric">
               <div class="metric-value" style="color: white;">{len(df)}</div>
               <div class="metric-label">Number of Students</div>
           </div>
       </div>
       """, unsafe_allow_html=True)

   with col2:
       st.markdown(f"""
       <div class="metrics-container">
           <div class="custom-metric">
               <div class="metric-value" style="color: {avg_risk_color};">{round(avg_risk, 1)}%</div>
               <div class="metric-label">Average Risk</div>
           </div>
       </div>
       """, unsafe_allow_html=True)

   with col3:
       st.markdown(f"""
       <div class="metrics-container">
           <div class="custom-metric">
               <div class="metric-value" style="color: white;">{high_risk_count}</div>
               <div class="metric-label">Number of High Risk Students <span style="color: {percentage_color};">({high_risk_percent:.1f}%)</span></div>
           </div>
       </div>
       """, unsafe_allow_html=True)

   # Button to view student list - centered on the page
   col1, col2, col3 = st.columns([1, 1, 1])
   with col2:
       if st.button("View Student List", use_container_width=True, type="primary"):
           st.switch_page("pages/3_Student_List.py")