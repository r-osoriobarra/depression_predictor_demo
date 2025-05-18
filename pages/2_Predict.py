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

# Function to clean and validate data
def clean_and_validate_data(df, feature_columns):
    """Clean and validate the dataframe with robust type conversion"""
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Check for missing columns
    missing_cols = [col for col in feature_columns if col not in df_clean.columns]
    if missing_cols:
        return None, f"Missing required columns: {', '.join(missing_cols)}"
    
    # Select only feature columns
    df_clean = df_clean[feature_columns]
    
    # Define expected types for each column based on typical training data
    numeric_columns = [
        'Age', 'Academic Pressure', 'Work Pressure', 'CGPA', 
        'Study Satisfaction', 'Job Satisfaction', 'Work/Study Hours', 
        'Financial Stress'
    ]
    
    categorical_columns = [
        'Gender', 'City', 'Profession', 'Sleep Duration', 
        'Dietary Habits', 'Degree', 'Have you ever had suicidal thoughts ?', 
        'Family History of Mental Illness'
    ]
    
    # Clean each column based on its expected type
    for col in df_clean.columns:
        if col in numeric_columns:
            # Convert to numeric, handling any string values
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
            # Fill missing numeric values with median
            if df_clean[col].isnull().any():
                median_val = df_clean[col].median()
                if pd.isna(median_val):
                    # If all values are NaN, use a default based on the column
                    if col == 'Age':
                        median_val = 21
                    elif col == 'CGPA':
                        median_val = 3.0
                    elif col in ['Academic Pressure', 'Work Pressure', 'Study Satisfaction', 'Job Satisfaction', 'Financial Stress']:
                        median_val = 5
                    elif col == 'Work/Study Hours':
                        median_val = 6
                    else:
                        median_val = 0
                
                df_clean[col] = df_clean[col].fillna(median_val)
            
            # Ensure the column is numeric
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[col] = df_clean[col].fillna(0)
            
        elif col in categorical_columns:
            # For categorical columns, ensure they are strings
            df_clean[col] = df_clean[col].astype(str)
            
            # Clean up Sleep Duration values that might have extra quotes
            if col == 'Sleep Duration':
                df_clean[col] = df_clean[col].str.replace("'", "", regex=False)
                df_clean[col] = df_clean[col].str.strip()
                
                # Standardize sleep duration values
                sleep_mapping = {
                    '5-6 hours': '6-8 hours',
                    '7-8 hours': '6-8 hours', 
                    'Less than 5 hours': 'Less than 6 hours',
                    'More than 8 hours': 'More than 8 hours'
                }
                df_clean[col] = df_clean[col].replace(sleep_mapping)
            
            # Replace NaN and missing values
            df_clean[col] = df_clean[col].replace(['nan', 'NaN', 'None', ''], 'Unknown')
            
            # Fill any remaining null values
            if df_clean[col].isnull().any():
                df_clean[col] = df_clean[col].fillna('Unknown')
            
            # Standardize common variations
            if col == 'Gender':
                gender_mapping = {
                    'male': 'Male', 'female': 'Female', 'other': 'Other',
                    'M': 'Male', 'F': 'Female', 'O': 'Other'
                }
                df_clean[col] = df_clean[col].replace(gender_mapping)
                
            elif col == 'Have you ever had suicidal thoughts ?':
                suicide_mapping = {
                    'yes': 'Yes', 'no': 'No', 'Y': 'Yes', 'N': 'No',
                    'true': 'Yes', 'false': 'No', '1': 'Yes', '0': 'No'
                }
                df_clean[col] = df_clean[col].replace(suicide_mapping)
                
            elif col == 'Family History of Mental Illness':
                family_mapping = {
                    'yes': 'Yes', 'no': 'No', 'Y': 'Yes', 'N': 'No',
                    'true': 'Yes', 'false': 'No', '1': 'Yes', '0': 'No'
                }
                df_clean[col] = df_clean[col].replace(family_mapping)
                
            elif col == 'Dietary Habits':
                dietary_mapping = {
                    'Moderate': 'Average',
                    'Poor': 'Unhealthy'
                }
                df_clean[col] = df_clean[col].replace(dietary_mapping)
    
    # Final validation - check for any remaining issues
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            # Ensure no null values in categorical columns
            df_clean[col] = df_clean[col].fillna('Unknown')
        else:
            # Ensure no null values in numeric columns
            df_clean[col] = df_clean[col].fillna(0)
    
    return df_clean, None

# Function to process and display data
def display_data_visualizations(df):
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

    # Display key metrics in cards with custom container
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

    # Interactive visualizations in tabs
    st.markdown("<h2 class='sub-header'>Data Visualizations</h2>",
                unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Risk Distribution", "Demographics", "Academic Factors", "Mental Health & Lifestyle"])

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
        if 'CGPA' in df.columns:
            col1, col2 = st.columns(2)

            with col1:
                # Interactive scatter plot for risk by CGPA
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
        else:
            st.info("Academic data not available for visualization.")

    with tab4:
        # Mental Health & Lifestyle Factors
        col1, col2 = st.columns(2)

        with col1:
            # Sleep duration distribution - Pie chart
            if 'Sleep Duration' in df.columns:
                sleep_counts = df['Sleep Duration'].value_counts()
                
                fig_sleep = px.pie(
                    values=sleep_counts.values,
                    names=sleep_counts.index,
                    title='Sleep Duration Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_sleep.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_sleep, use_container_width=True)
            else:
                st.info("Sleep Duration data not available for visualization.")

            # Dietary habits vs risk level - Stacked bar
            if 'Dietary Habits' in df.columns:
                # Create cross-tabulation for stacked bar
                dietary_risk = pd.crosstab(df['Dietary Habits'], df['Risk Category'])
                
                fig_dietary = px.bar(
                    dietary_risk,
                    title='Dietary Habits vs Risk Level',
                    color_discrete_map={
                        'Low': '#388E3C',
                        'Medium': '#F57C00',
                        'High': '#D32F2F'
                    },
                    barmode='stack'
                )
                fig_dietary.update_layout(
                    xaxis_title="Dietary Habits",
                    yaxis_title="Number of Students",
                    template="plotly_white"
                )
                st.plotly_chart(fig_dietary, use_container_width=True)
            else:
                st.info("Dietary Habits data not available for visualization.")

        with col2:
            # Financial stress impact visualization
            if 'Financial Stress' in df.columns:
                # Group by financial stress and calculate average risk
                financial_impact = df.groupby('Financial Stress')['Depression Risk (%)'].mean().reset_index()
                
                fig_financial = px.bar(
                    financial_impact,
                    x='Financial Stress',
                    y='Depression Risk (%)',
                    title='Financial Stress Impact on Depression Risk',
                    color='Depression Risk (%)',
                    color_continuous_scale=['#388E3C', '#F57C00', '#D32F2F']
                )
                fig_financial.update_layout(
                    template="plotly_white",
                    showlegend=False
                )
                st.plotly_chart(fig_financial, use_container_width=True)
            else:
                st.info("Financial Stress data not available for visualization.")

            # Gauge chart for suicidal thoughts percentage
            if 'Have you ever had suicidal thoughts ?' in df.columns:
                # Calculate percentage of students with suicidal thoughts
                suicidal_thoughts = df['Have you ever had suicidal thoughts ?'].value_counts()
                if 'Yes' in suicidal_thoughts.index:
                    suicidal_percent = (suicidal_thoughts.get('Yes', 0) / len(df)) * 100
                else:
                    suicidal_percent = 0
                
                # Create gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = suicidal_percent,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Students with Suicidal Thoughts (%)"},
                    delta = {'reference': 10},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 25], 'color': "#388E3C"},
                            {'range': [25, 50], 'color': "#F57C00"},
                            {'range': [50, 100], 'color': "#D32F2F"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(height=400)
                st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                st.info("Suicidal thoughts data not available for visualization.")

    # Button to view student list - centered on the page
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("View Student List", use_container_width=True):
            st.switch_page("pages/3_Student_List.py")

# Main logic
if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Show data info for debugging
        with st.expander("📊 Data Information"):
            st.write(f"**File shape:** {df.shape}")
            st.write(f"**Columns:** {list(df.columns)}")
            
            # Show data types
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Data types:**")
                for col, dtype in df.dtypes.items():
                    st.write(f"- {col}: {dtype}")
            
            with col2:
                st.write("**Sample values for key columns:**")
                if 'Financial Stress' in df.columns:
                    st.write(f"Financial Stress unique values: {df['Financial Stress'].unique()[:10]}")
                if 'Sleep Duration' in df.columns:
                    st.write(f"Sleep Duration unique values: {df['Sleep Duration'].unique()}")
        
        # Clean and validate the data
        df_clean, error_msg = clean_and_validate_data(df, feature_columns)
        
        if error_msg:
            st.error(error_msg)
            st.stop()
        
        # Apply model to predict depression risk
        X_transformed = preprocessor.transform(df_clean)
        risk_probabilities = model.predict_proba(X_transformed)[:, 1] * 100
        
        # Add predictions to original dataframe
        df["Depression Risk (%)"] = risk_probabilities

        # Create risk categories with updated thresholds
        df['Risk Category'] = pd.cut(
            df["Depression Risk (%)"],
            bins=[0, 30, 70, 100],
            labels=["Low", "Medium", "High"]
        )

        # Store in session_state for later use
        st.session_state["latest_df"] = df

        # Show success message
        st.success(
            f"Data loaded successfully. {len(df)} student records processed.")

        # Display visualizations
        display_data_visualizations(df)

    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.write("**Debug information:**")
        st.write(f"Error type: {type(e)}")
        import traceback
        st.code(traceback.format_exc())

elif "latest_df" in st.session_state:
    df = st.session_state["latest_df"]
    st.info("Displaying previously uploaded data. To update, upload a new file.")
    
    # Display visualizations
    display_data_visualizations(df)
else:
    st.warning("Please upload a CSV file to view the dashboard.")