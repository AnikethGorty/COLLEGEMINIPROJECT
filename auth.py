#auth.py
import streamlit as st
from db import get_user_by_email, create_user

def login_form():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user_by_email(email)
        if user and user.password == password:
            st.session_state["user_id"] = user.id
            st.session_state["tenant_id"] = user.tenant_id
            st.rerun()
        else:
            st.error("Invalid credentials")

def signup_form():
    st.title("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        user_id, tenant_id = create_user(email, password)
        if user_id:
            st.session_state["user_id"] = user_id
            st.session_state["tenant_id"] = tenant_id
            st.success("Account created and logged in!")
            st.rerun()
        else:
            st.error("User already exists.")
