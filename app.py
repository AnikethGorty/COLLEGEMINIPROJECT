# app.py
import streamlit as st
from auth import login_form, signup_form
from dashboard import show_dashboard

st.set_page_config(page_title="TradeZone", page_icon="💰")
st.title("💰 TradeZone - Buy & Sell Marketplace")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if "user_id" not in st.session_state:
    if choice == "Login":
        login_form()
    elif choice == "Sign Up":
        signup_form()
else:
    show_dashboard()
