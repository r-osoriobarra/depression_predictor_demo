# pages/5_FeatureContribution.py
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils import set_page_style, check_login, check_data, categorize_risk
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

st.set_page_config(page_title="Feature Contributions", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>Feature Importance for Selected Student</h1>",
            unsafe_allow_html=True)

# Require login
if not check_login():
    st.stop()

# Ensure selection and data availability
if not check_data():
    st.stop()

if "selected_student_index" not in st.session_state:
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


try:
    model, preprocessor, feature_columns = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Get selected student data
df = st.session_state["latest_df"]
student_index = st.session_state["selected_student_index"]
X_student = df.loc[[student_index]][feature_columns]

# Student risk score
risk_score = df.loc[student_index]["Depression Risk (%)"]
risk_category, risk_color = categorize_risk(risk_score)

# Display student header
st.markdown(f"""
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="margin: 0;">Student {student_index} - Depression Risk: 
        <span style="color: {risk_color};">{round(risk_score, 1)}%</span></h2>
    </div>
""", unsafe_allow_html=True)

# Check for feature importances
if hasattr(model, "feature_importances_"):
    importances = model.feature_importances_

    # Get student values and compare with average values
    student_values = X_student.values[0]
    avg_values = df[feature_columns].mean().values

    # Calculate relative values (how far from average)
    # Avoid division by zero or NaN
    std_values = df[feature_columns].std().values
    # Replace zeros with ones
    std_values = np.where(std_values == 0, 1, std_values)
    relative_values = np.divide(student_values - avg_values, std_values,
                                out=np.zeros_like(student_values),
                                where=std_values != 0)

    # Create dataframe with feature importances and values
    contribution_df = pd.DataFrame({
        "Feature": feature_columns,
        "Student Value": student_values,
        "Avg Value": avg_values,
        "Relative Value": relative_values,
        "Feature Importance": importances,
        # Estimate individual contribution (importance * relative deviation)
        "Estimated Impact": importances * np.abs(relative_values)
    }).sort_values("Estimated Impact", ascending=False)

    # Display tabs for different visualizations
    tab1, tab2 = st.tabs(["Feature Impact", "Comparison with Average"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            # Create a horizontal bar chart for feature impact
            fig, ax = plt.subplots(figsize=(12, 8))

            # Create bars with colors based on whether the feature is higher or lower than average
            colors = [
                '#D32F2F' if rv > 0 else '#388E3C' for rv in contribution_df['Relative Value']]

            # Plot horizontal bar chart of estimated impact
            bars = ax.barh(
                contribution_df["Feature"],
                contribution_df["Estimated Impact"],
                color=colors
            )

            # Add student values as text
            for i, bar in enumerate(bars):
                width = bar.get_width()
                label_pos = width + 0.01
                rel_val = contribution_df['Relative Value'].iloc[i]
                direction = "higher" if rel_val > 0 else "lower"

                ax.text(
                    label_pos,
                    bar.get_y() + bar.get_height()/2,
                    f"{contribution_df['Student Value'].iloc[i]:.2f} ({direction} than avg)",
                    va='center'
                )

            # Add labels and title
            ax.set_xlabel('Estimated Impact on Depression Risk')
            ax.set_title('Estimated Impact of Each Feature on Depression Risk')

            # Sort bars by impact
            ax.invert_yaxis()  # To match the sort order in the dataframe

            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.markdown(
                "<h3 class='sub-header'>Top Contributing Factors</h3>", unsafe_allow_html=True)

            # Top 5 contributing factors
            top_factors = contribution_df.head(5)

            for i, (_, row) in enumerate(top_factors.iterrows()):
                direction = "higher" if row["Relative Value"] > 0 else "lower"
                color = '#D32F2F' if row['Relative Value'] > 0 else '#388E3C'

                st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin: 0; color: {color};">
                            {i+1}. {row['Feature']}
                        </h4>
                        <p>Student value: <b>{row['Student Value']:.2f}</b> ({direction} than average: {row['Avg Value']:.2f})</p>
                        <div style="width: 100%; background-color: #e0e0e0; height: 10px; border-radius: 5px;">
                            <div style="width: {row['Estimated Impact']/contribution_df['Estimated Impact'].max()*100}%; 
                                 background-color: {color}; 
                                 height: 10px; border-radius: 5px;">
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    with tab2:
        # Create radar chart data visualization
        st.markdown(
            "<h3 class='sub-header'>Student vs Average Comparison</h3>", unsafe_allow_html=True)

        # Select top features for readability
        top_n_features = st.slider("Number of features to display:",
                                   min_value=3, max_value=len(feature_columns), value=8)

        # Get top n features by importance
        top_features = contribution_df.nlargest(
            top_n_features, "Feature Importance")

        # Create radar chart
        categories = top_features["Feature"].tolist()
        N = len(categories)

        # Create angles for each axis
        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        angles += angles[:1]  # Close the loop

        # Create student values and average values
        student_vals = top_features["Student Value"].tolist()
        student_vals += student_vals[:1]  # Close the loop

        avg_vals = top_features["Avg Value"].tolist()
        avg_vals += avg_vals[:1]  # Close the loop

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

        # Plot student values
        ax.plot(angles, student_vals, 'o-', linewidth=2,
                color=risk_color, label='Student')
        ax.fill(angles, student_vals, alpha=0.25, color=risk_color)

        # Plot average values
        ax.plot(angles, avg_vals, 'o-', linewidth=2,
                color='#1E88E5', label='Average')
        ax.fill(angles, avg_vals, alpha=0.1, color='#1E88E5')

        # Set categories
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        # Add legend and title
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        plt.title('Student vs. Average Values', size=14)

        st.pyplot(fig)

        # Also display comparison table
        st.markdown(
            "<h3 class='sub-header'>Detailed Feature Comparison</h3>", unsafe_allow_html=True)

        # Format the dataframe for display
        display_df = contribution_df[[
            "Feature", "Student Value", "Avg Value", "Relative Value", "Feature Importance"]]

        # Function to color cells based on relative value
        def highlight_cells(val):
            if isinstance(val, (int, float)):
                if isinstance(val, float) and pd.isna(val):
                    return ''
                if 'Relative Value' in display_df.columns:
                    feature = display_df.loc[display_df.index[0], 'Feature']
                    rel_val = display_df.loc[display_df['Feature']
                                             == feature, 'Relative Value'].values[0]
                    if rel_val > 0:
                        # Red scale for values higher than average
                        color = f'background-color: rgba(211, 47, 47, {min(abs(rel_val) * 0.3, 0.3)})'
                    else:
                        # Green scale for values lower than average
                        color = f'background-color: rgba(56, 142, 60, {min(abs(rel_val) * 0.3, 0.3)})'
                    return color
            return ''

        # Display styled dataframe
        st.dataframe(display_df.style.applymap(highlight_cells))

else:
    st.warning("This model does not support feature importances.")

    # Show alternative message
    st.info("""
    The model doesn't provide direct feature importance information. 
    
    In a complete implementation, we could use:
    1. Permutation importance
    2. SHAP values
    3. Partial dependence plots
    
    These methods would help identify which features most strongly influence the prediction for this student.
    """)
