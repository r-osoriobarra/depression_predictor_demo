import streamlit as st
import pandas as pd


def set_page_style():
    """Apply consistent styling across all pages"""
    st.markdown("""
    <style>
        .main-header {color:#1E88E5; font-size:40px; font-weight:bold; margin-bottom:30px;}
        .sub-header {color:#0D47A1; font-size:28px; font-weight:bold; margin-top:20px;}
        .risk-high {color: #D32F2F; font-weight: bold;}
        .risk-medium {color: #F57C00; font-weight: bold;}
        .risk-low {color: #388E3C; font-weight: bold;}
        .metric-card {background-color: #f5f5f5; border-radius: 5px; padding: 15px; margin: 10px 0;}
    </style>
    """, unsafe_allow_html=True)


def categorize_risk(risk_score):
    """Categorize risk percentage into Low, Medium, or High"""
    if risk_score > 60:
        return "High", "#D32F2F"
    elif risk_score > 30:
        return "Medium", "#F57C00"
    else:
        return "Low", "#388E3C"


def check_login():
    """Check if user is logged in, show warning if not"""
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in to access this page.")
        return False
    return True


def check_data():
    """Check if data is loaded, show info message if not"""
    if "latest_df" not in st.session_state:
        st.info("Please upload a student dataset in the Overview page first.")
        return False
    return True
