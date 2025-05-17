# pages/1_Login.py
import streamlit as st
from utils import set_page_style

# Aplicar estilos consistentes
set_page_style()

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

# Login form with improved styling
if not st.session_state.logged_in:
    st.markdown("""
    <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px; max-width: 500px;">
        <h2 style="color: #1E88E5; margin-bottom: 20px;">User Authentication</h2>
        <p>Please enter your credentials to access the system.</p>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Login", use_container_width=True):
            if USERS.get(username) == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
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
