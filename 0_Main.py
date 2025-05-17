# app.py
import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import os
import sys

# Añadir el directorio raíz al path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

# Importar utils
from utils import set_page_style

# Configure the page
st.set_page_config(
    page_title="Student Depression Risk Predictor",
    page_icon="🧠",
    layout="wide",
)

# Aplicar estilos consistentes
set_page_style()

st.markdown("<h1 class='main-header'>Student Depression Risk Dashboard</h1>", unsafe_allow_html=True)

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
try:
    model, preprocessor, feature_columns = load_model()
    st.success("✅ Model, preprocessor, and feature list loaded successfully.")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.info("Please ensure the model files are available in the 'model/' directory.")

# Información principal
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

# Si hay datos cargados, mostrar algunos gráficos básicos
if "latest_df" in st.session_state:
    st.markdown("<h2 class='sub-header'>Quick Dashboard</h2>", unsafe_allow_html=True)
    
    df = st.session_state["latest_df"]
    
    # Crear categorías de riesgo si no existen
    if "Risk Category" not in df.columns:
        df['Risk Category'] = pd.cut(df['Depression Risk (%)'], 
                                    bins=[0, 30, 60, 100], 
                                    labels=['Low', 'Medium', 'High'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución de riesgo con gráfico de pastel interactivo de Plotly
        risk_counts = df['Risk Category'].value_counts().reset_index()
        risk_counts.columns = ['Risk Category', 'Count']
        
        # Definir colores para cada categoría
        color_map = {'Low': '#388E3C', 'Medium': '#F57C00', 'High': '#D32F2F'}
        
        # Crear gráfico de pastel interactivo
        fig = px.pie(
            risk_counts, 
            values='Count', 
            names='Risk Category',
            title='Distribution of Depression Risk Levels',
            color='Risk Category',
            color_discrete_map=color_map,
            hole=0.4  # Donut chart
        )
        
        # Mejorar diseño
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            legend_title="Risk Category",
            font=dict(size=14),
            hoverlabel=dict(font_size=14)
        )
        
        # Mostrar gráfico
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Riesgo promedio por género con gráfico de barras interactivo (si está disponible)
        if 'Gender' in df.columns:
            # Calcular promedio por género
            gender_risk = df.groupby('Gender')['Depression Risk (%)'].mean().reset_index()
            
            # Crear gráfico de barras interactivo
            fig = px.bar(
                gender_risk,
                x='Gender',
                y='Depression Risk (%)',
                title='Average Depression Risk by Gender',
                text_auto='.1f',  # Mostrar valores en las barras con 1 decimal
                color='Depression Risk (%)',
                color_continuous_scale=['#4CAF50', '#FFC107', '#F44336']
            )
            
            # Mejorar diseño
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis_title="Gender",
                yaxis_title="Average Depression Risk (%)",
                font=dict(size=14),
                hoverlabel=dict(font_size=14)
            )
            
            # Mostrar gráfico
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Si no hay datos de género, mostrar otra visualización útil
            # Por ejemplo, distribución de edades si está disponible
            if 'Age' in df.columns:
                fig = px.histogram(
                    df, 
                    x='Age',
                    color='Risk Category',
                    color_discrete_map=color_map,
                    title='Age Distribution by Risk Category',
                    nbins=20
                )
                
                fig.update_layout(
                    xaxis_title="Age",
                    yaxis_title="Count",
                    font=dict(size=14),
                    hoverlabel=dict(font_size=14)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Gender and Age data not available for visualization.")
    
    # Añadir un tercer gráfico debajo (opcional)
    if 'CGPA' in df.columns:
        # Gráfico de dispersión para CGPA vs Risk
        fig = px.scatter(
            df,
            x='CGPA',
            y='Depression Risk (%)',
            color='Risk Category',
            color_discrete_map=color_map,
            title='Relationship between CGPA and Depression Risk',
            hover_data=['Gender', 'Age'] if 'Gender' in df.columns and 'Age' in df.columns else None,
            trendline="ols"  # Añadir línea de tendencia
        )
        
        fig.update_layout(
            xaxis_title="CGPA",
            yaxis_title="Depression Risk (%)",
            font=dict(size=14),
            hoverlabel=dict(font_size=14)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    # Añadir una sección con métricas clave si hay suficientes datos
    if len(df) > 0:
        st.markdown("<h2 class='sub-header'>Key Metrics</h2>", unsafe_allow_html=True)
        
        # Crear 3 columnas para métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Total de estudiantes
            st.metric(
                label="Total Students", 
                value=len(df)
            )
        
        with col2:
            # Promedio de riesgo
            avg_risk = df["Depression Risk (%)"].mean()
            st.metric(
                label="Average Risk", 
                value=f"{avg_risk:.1f}%"
            )
        
        with col3:
            # Estudiantes de alto riesgo
            high_risk = (df["Risk Category"] == "High").sum()
            high_risk_pct = (high_risk / len(df)) * 100
            st.metric(
                label="High Risk Students", 
                value=high_risk,
                delta=f"{high_risk_pct:.1f}%"
            )
        
        with col4:
            # Estudiantes de bajo riesgo
            low_risk = (df["Risk Category"] == "Low").sum()
            low_risk_pct = (low_risk / len(df)) * 100
            st.metric(
                label="Low Risk Students", 
                value=low_risk,
                delta=f"{low_risk_pct:.1f}%"
            )
else:
    # Si no hay datos, mostrar información sobre cómo empezar
    st.info("""
    ### Getting Started
    
    To use this system:
    1. **Login** using the provided credentials (see the Login page)
    2. **Upload student data** on the Overview page
    3. **Explore** risk levels and details
    
    The system will populate this dashboard with visualizations once data is loaded.
    """)

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