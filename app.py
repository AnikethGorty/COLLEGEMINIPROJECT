import streamlit as st
from auth import login_form, signup_form
from dashboard import show_dashboard
from db import ensure_default_admin

st.set_page_config(page_title="TradeZone", layout="wide")

# Ensure default admin exists
ensure_default_admin()

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if "user_id" not in st.session_state:
    if choice == "Login":
        login_form()
    elif choice == "Sign Up":
        signup_form()
else:
    show_dashboard()
