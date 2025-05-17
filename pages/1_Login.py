import streamlit as st

# Set page title
st.title("Login")

# Simple credentials (for demonstration only)
USERS = {
    "admin": "1234",
    "user": "abcd"
}

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login form
if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
else:
    st.success("You are already logged in.")
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()
