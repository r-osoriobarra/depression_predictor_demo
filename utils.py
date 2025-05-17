def set_page_style():
    st.markdown("""
    <style>
        .main-header {color:#1E88E5; font-size:40px; font-weight:bold; margin-bottom:30px;}
        .sub-header {color:#0D47A1; font-size:28px; font-weight:bold; margin-top:20px;}
        .risk-high {color: #D32F2F; font-weight: bold;}
        .risk-medium {color: #F57C00; font-weight: bold;}
        .risk-low {color: #388E3C; font-weight: bold;}
        .metric-card {background-color: #f5f5f5; border-radius: 5px; padding: 15px; margin: 10px 0;}
    </style>
    """, unsafe_allow_html=True)
