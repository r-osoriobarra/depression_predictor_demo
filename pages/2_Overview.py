import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
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
Upload a CSV file containing student data. The file should include the following columns:
""")

# Display required columns
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

        # Display key metrics in cards with 3 columns
        st.markdown("<h2 class='sub-header'>Key Metrics</h2>",
                    unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Number of Students", len(df))
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Average Risk (%)", round(
                df["Depression Risk (%)"].mean(), 2))
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            high_risk_count = (df["Risk Category"] == "High").sum()
            high_risk_percent = high_risk_count / len(df) * 100
            st.metric("High Risk Students", high_risk_count,
                      f"{high_risk_percent:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)

        # Visualizations in tabs
        st.markdown("<h2 class='sub-header'>Data Visualizations</h2>",
                    unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(
            ["Risk Distribution", "Demographics", "Academic Factors"])

        with tab1:
            # Risk distribution visualization
            col1, col2 = st.columns(2)

            with col1:
                # Histogram of risk scores
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(df["Depression Risk (%)"],
                             bins=20, kde=True, ax=ax)
                plt.axvline(x=30, color='orange', linestyle='--')
                plt.axvline(x=60, color='red', linestyle='--')
                plt.title('Distribution of Depression Risk Scores')
                plt.xlabel('Risk Score (%)')
                plt.ylabel('Number of Students')
                st.pyplot(fig)

            with col2:
                # Pie chart of risk categories
                fig, ax = plt.subplots(figsize=(10, 6))
                risk_counts = df['Risk Category'].value_counts()
                colors = ['#388E3C', '#F57C00', '#D32F2F']
                risk_counts.plot(kind='pie', autopct='%1.1f%%',
                                 colors=colors, ax=ax)
                plt.title('Distribution of Risk Categories')
                st.pyplot(fig)

        with tab2:
            # Demographics analysis
            if 'Gender' in df.columns:
                col1, col2 = st.columns(2)

                with col1:
                    # Risk by gender
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.boxplot(
                        x='Gender', y='Depression Risk (%)', data=df, ax=ax)
                    plt.title('Depression Risk by Gender')
                    st.pyplot(fig)

                with col2:
                    # Risk by age (if available)
                    if 'Age' in df.columns:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.scatterplot(x='Age', y='Depression Risk (%)', hue='Risk Category',
                                        palette=['#388E3C', '#F57C00', '#D32F2F'], data=df, ax=ax)
                        plt.title('Depression Risk by Age')
                        st.pyplot(fig)
                    else:
                        st.info("Age data not available for visualization.")
            else:
                st.info("Demographic data not available for visualization.")

        with tab3:
            # Academic factors analysis
            if 'CGPA' in df.columns:
                col1, col2 = st.columns(2)

                with col1:
                    # Risk by CGPA
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.scatterplot(x='CGPA', y='Depression Risk (%)', hue='Risk Category',
                                    palette=['#388E3C', '#F57C00', '#D32F2F'], data=df, ax=ax)
                    plt.title('Depression Risk by CGPA')
                    st.pyplot(fig)

                with col2:
                    # Risk by degree (if available)
                    if 'Degree' in df.columns:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        degree_risk = df.groupby(
                            'Degree')['Depression Risk (%)'].mean().sort_values(ascending=False)
                        degree_risk.plot(kind='bar', color='#1E88E5', ax=ax)
                        plt.title('Average Depression Risk by Degree Program')
                        plt.xlabel('Degree')
                        plt.ylabel('Average Risk (%)')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                    else:
                        st.info("Degree data not available for visualization.")
            else:
                st.info("Academic data not available for visualization.")

        # Display student data preview
        st.markdown("<h2 class='sub-header'>Student Data Preview</h2>",
                    unsafe_allow_html=True)

        # Format risk column with colors
        def highlight_risk(val):
            if val == "High":
                return 'background-color: rgba(211, 47, 47, 0.2); color: #D32F2F; font-weight: bold'
            elif val == "Medium":
                return 'background-color: rgba(245, 124, 0, 0.2); color: #F57C00; font-weight: bold'
            elif val == "Low":
                return 'background-color: rgba(56, 142, 60, 0.2); color: #388E3C; font-weight: bold'
            return ''

        # Create display columns for better readability
        display_cols = ["Gender", "Age", "CGPA",
                        "Depression Risk (%)", "Risk Category"]
        display_cols = [col for col in display_cols if col in df.columns]

        # Apply styling
        display_df = df[display_cols].sort_values(
            "Depression Risk (%)", ascending=False)
        styled_df = display_df.style.applymap(
            highlight_risk, subset=["Risk Category"])

        st.dataframe(styled_df, height=400)

        # Add download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="student_risk_analysis.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.exception(e)

elif "latest_df" in st.session_state:
    df = st.session_state["latest_df"]
    st.info("Displaying previously uploaded data. To update, upload a new file.")

    # Display key metrics
    st.markdown("<h2 class='sub-header'>Key Metrics</h2>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Number of Students", len(df))
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Average Risk (%)", round(
            df["Depression Risk (%)"].mean(), 2))
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        high_risk_count = (df["Risk Category"] == "High").sum()
        high_risk_percent = high_risk_count / len(df) * 100
        st.metric("High Risk Students", high_risk_count,
                  f"{high_risk_percent:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

    # Display student data preview
    st.markdown("<h2 class='sub-header'>Student Data Preview</h2>",
                unsafe_allow_html=True)

    # Format risk column with colors (same as above)
    def highlight_risk(val):
        if val == "High":
            return 'background-color: rgba(211, 47, 47, 0.2); color: #D32F2F; font-weight: bold'
        elif val == "Medium":
            return 'background-color: rgba(245, 124, 0, 0.2); color: #F57C00; font-weight: bold'
        elif val == "Low":
            return 'background-color: rgba(56, 142, 60, 0.2); color: #388E3C; font-weight: bold'
        return ''

    # Create display columns for better readability
    display_cols = ["Gender", "Age", "CGPA",
                    "Depression Risk (%)", "Risk Category"]
    display_cols = [col for col in display_cols if col in df.columns]

    # Apply styling
    display_df = df[display_cols].sort_values(
        "Depression Risk (%)", ascending=False)
    styled_df = display_df.style.applymap(
        highlight_risk, subset=["Risk Category"])

    st.dataframe(styled_df, height=400)
