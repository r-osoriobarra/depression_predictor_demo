import streamlit as st
import pickle
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="Student Depression Risk Predictor",
    layout="wide",
)

st.title("Student Depression Risk Dashboard")

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
model, preprocessor, feature_columns = load_model()

st.success("Model, preprocessor, and feature list loaded successfully.")

st.markdown("""
Welcome to the **Student Depression Risk Prediction System**.  
Use the navigation menu on the left to move between pages.
""")
