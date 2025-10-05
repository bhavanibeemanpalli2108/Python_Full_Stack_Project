import streamlit as st
import bcrypt
from src.db import create_user, get_user_by_email
from supabase import Client
import os
from dotenv import load_dotenv

# Load Supabase client
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
from supabase import create_client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# Session management
# -------------------------
def get_current_user():
    return st.session_state.get("current_user")

def logout():
    st.session_state["current_user"] = None
    st.success("Logged out successfully!")

# -------------------------
# Signup
# -------------------------
def signup():
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone (optional)")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            # Check if user already exists
            existing_user = get_user_by_email(email, supabase)
            if existing_user:
                st.error("Email already exists. Please login.")
                return None

            # Create user with hashed password
            create_user(name, email, phone, password)
            st.success("Account created successfully! Please login.")
            return {"name": name, "email": email}

# -------------------------
# Login
# -------------------------
def login():
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            user = get_user_by_email(email, supabase)
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                st.session_state["current_user"] = user
                st.success(f"Welcome {user['name']}!")
                return user
            else:
                st.error("Invalid email or password")
                return None
