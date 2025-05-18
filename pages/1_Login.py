from utils import set_page_style
import streamlit as st
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Set page title
st.markdown("<h1 class='main-header'>Login</h1>", unsafe_allow_html=True)

# Simple credentials (for demonstration only)
USERS = {
   "admin": "1234",
   "user": "abcd"
}

# Initialize login state
if "logged_in" not in st.session_state:
   st.session_state.logged_in = False
   st.session_state.username = None

# Login form with simplified styling
if not st.session_state.logged_in:
   username = st.text_input("Username")
   password = st.text_input("Password", type="password")

   col1, col2 = st.columns([1, 4])
   with col1:
       if st.button("Login", use_container_width=True):
           if USERS.get(username) == password:
               st.session_state.logged_in = True
               st.session_state.username = username
               st.success(f"Welcome, {username}!")
               st.switch_page("pages/2_Predict.py")
           else:
               st.error("Invalid username or password.")

   # Add some demo credentials info
   with st.expander("Demo Credentials"):
       st.info("""
       For demonstration purposes, you can use:
       - Username: admin, Password: 1234
       - Username: user, Password: abcd
       """)
else:
   st.success(f"You are logged in as {st.session_state.username}.")
   if st.button("Log out"):
       st.session_state.logged_in = False
       st.session_state.username = None
       st.rerun()