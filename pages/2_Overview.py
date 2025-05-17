import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Overview", layout="wide")
st.title("Overview Dashboard")

# Check login status
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
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


model, preprocessor, feature_columns = load_model()

# File upload
uploaded_file = st.file_uploader("Upload student data CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    try:
        X = df[feature_columns]
        X_transformed = preprocessor.transform(X)
        df["Depression Risk (%)"] = model.predict_proba(
            X_transformed)[:, 1] * 100

        # Store in session_state for later use
        st.session_state["latest_df"] = df

        st.metric("Number of Students", len(df))
        st.metric("Average Risk (%)", round(
            df["Depression Risk (%)"].mean(), 2))
        st.metric("High Risk Students", (df["Depression Risk (%)"] > 60).sum())

        st.dataframe(df[["Gender", "Age", "CGPA", "Depression Risk (%)"]]
                     .sort_values("Depression Risk (%)", ascending=False))

    except Exception as e:
        st.error(
            "Could not process the file. Check that all required columns are included.")
        st.exception(e)

elif "latest_df" in st.session_state:
    df = st.session_state["latest_df"]
    st.info("Displaying previously uploaded data.")

    st.metric("Number of Students", len(df))
    st.metric("Average Risk (%)", round(df["Depression Risk (%)"].mean(), 2))
    st.metric("High Risk Students", (df["Depression Risk (%)"] > 60).sum())

    st.dataframe(df[["Gender", "Age", "CGPA", "Depression Risk (%)"]]
                 .sort_values("Depression Risk (%)", ascending=False))
