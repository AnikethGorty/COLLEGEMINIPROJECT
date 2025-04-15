 #app.py#
import streamlit as st
from auth import login_form, signup_form
from dashboard import show_dashboard

st.set_page_config(page_title="TradeZone", layout="wide")

ensure_default_admin()

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if "user_id" in st.session_state:
    show_dashboard()
elif choice == "Login":
    login_form()
elif choice == "Sign Up":
    signup_form()
