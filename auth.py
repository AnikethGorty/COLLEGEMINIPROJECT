import streamlit as st
from db import get_user_by_email, create_user
import uuid

def login_form():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and user.password == password:
            st.session_state["user_id"] = user.id
            st.session_state["tenant_id"] = user.tenant_id
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

def signup_form():
    st.subheader("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if get_user_by_email(email):
            st.error("Account already exists. Please login instead.")
        else:
            user_id = str(uuid.uuid4())
            tenant_id = str(uuid.uuid4())
            create_user(user_id, tenant_id, email, password)
            st.session_state["user_id"] = user_id
            st.session_state["tenant_id"] = tenant_id
            st.success("Account created and logged in!")
            st.rerun()
