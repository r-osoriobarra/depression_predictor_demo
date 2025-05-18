# pages/3_StudentList.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import set_page_style, check_login, check_data
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

st.set_page_config(page_title="Student List", layout="wide")
set_page_style()

st.markdown("<h1 class='main-header'>List of Students and Depression Risk</h1>",
           unsafe_allow_html=True)

# Require user login
if not check_login():
   st.stop()

# Ensure data has been loaded
if not check_data():
   st.stop()

# Use the existing DataFrame stored in session_state
df = st.session_state["latest_df"]

# Create risk category if it doesn't exist
if "Risk Category" not in df.columns:
   df["Risk Category"] = pd.cut(
       df["Depression Risk (%)"],
       bins=[0, 30, 70, 100],
       labels=["Low", "Medium", "High"]
   )

# Create filtering options in sidebar
st.sidebar.markdown(
   "<h3 class='sub-header'>Filter Students</h3>", unsafe_allow_html=True)

# Risk filter
risk_filter = st.sidebar.multiselect(
   "Risk Category",
   options=["High", "Medium", "Low"],
   default=["High", "Medium", "Low"]
)

# Gender filter (if available)
if "Gender" in df.columns:
   gender_filter = st.sidebar.multiselect(
       "Gender",
       options=df["Gender"].unique(),
       default=df["Gender"].unique()
   )
else:
   gender_filter = None

# Degree filter (if available)
if "Degree" in df.columns:
   degree_filter = st.sidebar.multiselect(
       "Degree",
       options=df["Degree"].unique(),
       default=[]
   )
else:
   degree_filter = None

# CGPA range filter (if available)
if "CGPA" in df.columns:
   cgpa_range = st.sidebar.slider(
       "CGPA Range",
       min_value=float(df["CGPA"].min()),
       max_value=float(df["CGPA"].max()),
       value=(float(df["CGPA"].min()), float(df["CGPA"].max()))
   )
else:
   cgpa_range = None

# Apply filters
filtered_df = df.copy()

# Filter by risk category
filtered_df = filtered_df[filtered_df["Risk Category"].isin(risk_filter)]

# Filter by gender if selected
if gender_filter is not None and len(gender_filter) > 0:
   filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]

# Filter by degree if selected
if degree_filter is not None and len(degree_filter) > 0:
   filtered_df = filtered_df[filtered_df["Degree"].isin(degree_filter)]

# Filter by CGPA range if selected
if cgpa_range is not None:
   filtered_df = filtered_df[(filtered_df["CGPA"] >= cgpa_range[0]) &
                             (filtered_df["CGPA"] <= cgpa_range[1])]

# Show filter summary
st.markdown(
   f"Showing **{len(filtered_df)}** students out of **{len(df)}** total students.")

# Initialize selected student index in session state
if "selected_student_for_preview" not in st.session_state:
   if len(filtered_df) > 0:
       st.session_state["selected_student_for_preview"] = filtered_df.index[0]
   else:
       st.session_state["selected_student_for_preview"] = None

# Create a table with the specified columns
st.markdown("<h2 class='sub-header'>Student List</h2>", unsafe_allow_html=True)

# Add custom CSS for clickable rows and button styling
st.markdown("""
<style>
.clickable-row {
   cursor: pointer;
}
.student-preview-container {
   border: 2px solid white;
   border-radius: 10px;
   padding: 20px;
   margin-bottom: 20px;
   background-color: transparent;
}
.stButton > button {
   background-color: #1E88E5 !important;
   color: white !important;
   border-radius: 5px !important;
   border: none !important;
   padding: 5px 10px !important;
   font-size: 12px !important;
}
.stButton > button:hover {
   background-color: #0D47A1 !important;
}
</style>
""", unsafe_allow_html=True)

# Create display columns
if 'id' in filtered_df.columns:
   student_id_col = 'id'
elif 'ID' in filtered_df.columns:
   student_id_col = 'ID'
else:
   student_id_col = None

display_cols = []
if student_id_col:
   display_cols.append(student_id_col)
display_cols.extend(["Age", "Degree", "Depression Risk (%)", "Risk Category"])

# Filter to only available columns
available_cols = [col for col in display_cols if col in filtered_df.columns]

if len(available_cols) > 0:
   # Create the display dataframe
   display_df = filtered_df[available_cols].copy()
   display_df = display_df.sort_values("Depression Risk (%)", ascending=False)
   
   # Rename student ID column for display
   if student_id_col in display_df.columns:
       display_df = display_df.rename(columns={student_id_col: "Student ID"})
   
   # Add action button column
   display_df["Actions"] = "View Details"
   
   # Function to highlight risk categories with updated thresholds
   def highlight_risk(val):
       if val == "High":
           return 'background-color: rgba(211, 47, 47, 0.2); color: #D32F2F; font-weight: bold'
       elif val == "Medium":
           return 'background-color: rgba(245, 124, 0, 0.2); color: #F57C00; font-weight: bold'
       elif val == "Low":
           return 'background-color: rgba(56, 142, 60, 0.2); color: #388E3C; font-weight: bold'
       return ''
   
   # Apply styling only to Risk Category column
   styled_df = display_df.style.applymap(highlight_risk, subset=["Risk Category"])
   
   # Display the table
   selected_indices = st.dataframe(
       styled_df,
       height=400,
       use_container_width=True,
       on_select="rerun",
       selection_mode="single-row"
   )
   
   # Handle row selection for preview
   if selected_indices["selection"]["rows"]:
       selected_row_idx = selected_indices["selection"]["rows"][0]
       # Get the actual dataframe index
       actual_index = display_df.iloc[selected_row_idx].name
       st.session_state["selected_student_for_preview"] = actual_index
   
   # Create action buttons for each student
   st.markdown("### Quick Actions")
   cols = st.columns(min(5, len(display_df)))
   
   for idx, (_, row) in enumerate(display_df.iterrows()):
       col_idx = idx % 5
       with cols[col_idx]:
           if st.button(f"View {row.name}", key=f"detail_btn_{row.name}"):
               st.session_state["selected_student_index"] = row.name
               st.switch_page("pages/4_Student_Detail.py")
   
   # Student Preview section
   if st.session_state["selected_student_for_preview"] is not None and st.session_state["selected_student_for_preview"] in filtered_df.index:
       selected_student = filtered_df.loc[st.session_state["selected_student_for_preview"]]
       
       st.markdown("<h3 class='sub-header'>Student Preview</h3>",
                   unsafe_allow_html=True)
       
       # Format based on risk level
       risk_score = selected_student["Depression Risk (%)"]
       if risk_score > 70:
           risk_color = "#D32F2F"
           risk_category = "High"
       elif risk_score > 30:
           risk_color = "#F57C00"
           risk_category = "Medium"
       else:
           risk_color = "#388E3C"
           risk_category = "Low"
       
       # Get student ID for display
       if student_id_col and student_id_col in selected_student.index:
           student_display_id = selected_student[student_id_col]
       else:
           student_display_id = st.session_state["selected_student_for_preview"]
       
       st.markdown(f"""
           <div class="student-preview-container">
               <div style="display: flex; justify-content: space-between; align-items: center;">
                   <div>
                       <h3 style="margin: 0; color: white;">Student {student_display_id}</h3>
                       <p style="margin: 5px 0 0 0; color: #CCCCCC;">{selected_student.get("Degree", "Student")}</p>
                   </div>
                   <div style="text-align: right;">
                       <h3 style="margin: 0; color: {risk_color};">{risk_category} Risk</h3>
                       <p style="font-size: 24px; font-weight: bold; margin: 0; color: {risk_color};">{round(risk_score, 1)}%</p>
                   </div>
               </div>
           </div>
       """, unsafe_allow_html=True)
       
       # Display key student attributes in two columns
       col1, col2 = st.columns(2)
       
       # Basic attributes
       basic_attrs = ["Gender", "Age", "CGPA", "Degree"]
       basic_attrs = [
           attr for attr in basic_attrs if attr in selected_student.index]
       
       with col1:
           st.markdown("<h4>Basic Information</h4>", unsafe_allow_html=True)
           for attr in basic_attrs:
               st.markdown(f"**{attr}:** {selected_student[attr]}")
       
       # Mental health indicators if available
       mh_attrs = ["Academic Pressure", "Study Satisfaction", "Sleep Duration",
                   "Financial Stress", "Family History of Mental Illness"]
       mh_attrs = [attr for attr in mh_attrs if attr in selected_student.index]
       
       with col2:
           if mh_attrs:
               st.markdown("<h4>Mental Health Indicators</h4>",
                           unsafe_allow_html=True)
               for attr in mh_attrs:
                   st.markdown(f"**{attr}:** {selected_student[attr]}")
           else:
               st.info(
                   "No detailed mental health indicators available for this student.")
       
       # Button to view full details
       col1, col2, col3 = st.columns([1, 1, 1])
       with col2:
           if st.button("View Full Student Details", use_container_width=True, type="primary"):
               st.session_state["selected_student_index"] = st.session_state["selected_student_for_preview"]
               st.switch_page("pages/4_Student_Detail.py")
   
else:
   st.warning("No students found with the selected filters or required columns are missing.")