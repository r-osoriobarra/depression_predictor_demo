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
   "user_test": "P@ssw0rd123!"
}

# Initialize login state
if "logged_in" not in st.session_state:
   st.session_state.logged_in = False
   st.session_state.username = None

# Custom CSS for copy buttons and icons
st.markdown("""
<style>
    .copy-button {
        background-color: #1E88E5;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 12px;
        margin-left: 10px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .copy-button:hover {
        background-color: #0D47A1;
    }
    .credential-item {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        padding: 8px;
        background-color: #f5f5f5;
        border-radius: 5px;
        justify-content: space-between;
    }
    .credential-label {
        font-weight: bold;
        color: #333;
    }
    .credential-value {
        font-family: monospace;
        color: #666;
        font-size: 14px;
    }
    .copy-feedback {
        color: #4CAF50;
        font-size: 12px;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

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

   # Add some demo credentials info with copy functionality
   with st.expander("Demo Credentials"):
       st.info("For demonstration purposes, you can use:")
       
       # Create credentials with copy buttons
       for user, pwd in USERS.items():
           st.markdown(f"""
           <div class="credential-item">
               <div>
                   <span class="credential-label">Username:</span>
                   <span class="credential-value">{user}</span>
               </div>
               <div>
                   <button class="copy-button" onclick="copyToClipboard('{user}', 'username_{user}')">
                       📋 Copy Username
                   </button>
                   <span id="copy-feedback-username_{user}" class="copy-feedback" style="display: none;">Copied!</span>
               </div>
           </div>
           <div class="credential-item">
               <div>
                   <span class="credential-label">Password:</span>
                   <span class="credential-value">{pwd}</span>
               </div>
               <div>
                   <button class="copy-button" onclick="copyToClipboard('{pwd}', 'password_{user}')">
                       📋 Copy Password
                   </button>
                   <span id="copy-feedback-password_{user}" class="copy-feedback" style="display: none;">Copied!</span>
               </div>
           </div>
           <hr style="margin: 15px 0; border: 1px solid #e0e0e0;">
           """, unsafe_allow_html=True)
       
       # Add JavaScript for copy functionality
       st.markdown("""
       <script>
       function copyToClipboard(text, elementId) {
           // Create a temporary textarea element
           const textarea = document.createElement('textarea');
           textarea.value = text;
           document.body.appendChild(textarea);
           textarea.select();
           document.execCommand('copy');
           document.body.removeChild(textarea);
           
           // Show feedback
           const feedback = document.getElementById('copy-feedback-' + elementId);
           if (feedback) {
               feedback.style.display = 'inline';
               setTimeout(() => {
                   feedback.style.display = 'none';
               }, 2000);
           }
       }
       </script>
       """, unsafe_allow_html=True)
       
       # Alternative: Create columns with username and password inputs pre-filled
       st.markdown("---")
       st.markdown("**Quick Fill Options:**")
       
       col1, col2 = st.columns(2)
       
       with col1:
           if st.button("Fill Admin Credentials", type="secondary"):
               st.session_state.fill_credentials = ("admin", "1234")
               
       with col2:
           if st.button("Fill User Credentials", type="secondary"):
               st.session_state.fill_credentials = ("user_test", "P@ssw0rd123!")
       
       # Auto-fill functionality
       if hasattr(st.session_state, 'fill_credentials'):
           st.markdown(f"""
           <script>
           setTimeout(() => {{
               const usernameInput = document.querySelector('input[aria-label="Username"]');
               const passwordInput = document.querySelector('input[aria-label="Password"]');
               if (usernameInput) usernameInput.value = '{st.session_state.fill_credentials[0]}';
               if (passwordInput) passwordInput.value = '{st.session_state.fill_credentials[1]}';
               usernameInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
               passwordInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
           }}, 100);
           </script>
           """, unsafe_allow_html=True)
           # Clear the fill state after use
           del st.session_state.fill_credentials

else:
   st.success(f"You are logged in as {st.session_state.username}.")
   if st.button("Log out"):
       st.session_state.logged_in = False
       st.session_state.username = None
       st.rerun()