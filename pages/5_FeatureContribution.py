import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Feature Contributions", layout="wide")
st.title("Feature Importance for Selected Student")

# Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

# Ensure selection and data availability
if "latest_df" not in st.session_state or "selected_student_index" not in st.session_state:
    st.info("Please select a student from the Student List page.")
    st.stop()

# Load model and preprocessing tools


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

# Get selected student data
df = st.session_state["latest_df"]
student_index = st.session_state["selected_student_index"]
X_student = df.loc[[student_index]][feature_columns]

# Check for feature importances
if hasattr(model, "feature_importances_"):
    importances = model.feature_importances_
    contribution_df = pd.DataFrame({
        "Feature": feature_columns,
        "Student Value": X_student.values[0],
        "Importance": importances
    }).sort_values("Importance", ascending=False)

    st.subheader(f"Feature Contributions for Student {student_index}")
    st.dataframe(contribution_df.reset_index(drop=True))

    st.bar_chart(contribution_df.set_index("Feature")["Importance"])

else:
    st.warning("This model does not support feature importances.")
