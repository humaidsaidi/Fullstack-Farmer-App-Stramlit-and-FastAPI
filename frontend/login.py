import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager
import re

# URL backend for login
LOGIN_URL = "http://127.0.0.1:8000/login/"  # Change the url from your backend
SIGNUP_URL = "http://127.0.0.1:8000/users/"


# This should be on top of your script
cookies = EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    # prefix="ktosiek/streamlit-cookies-manager/",
    # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
    password="humaid123"
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.spinner()
    st.stop()

# Function for verifying valid email
def is_valid_email(email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_pattern, email):
            return True
        else:
            return False

# Function for doing http request to backend for login
def login(username, password):
    data = {"username": username, "password": password}
    response = requests.post(LOGIN_URL, data=data)
    if response.status_code == 200:
        response_data = response.json()
        if "access_token" in response_data:
            access_token = response_data["access_token"]
            # Set the cookie (secure and with an appropriate expiration)
            cookies["jwt-token"] = access_token
            # "jwt-token" is cookie name
            cookies.save()
            return True
   
    return False

def signup(username, password):
    data = {"email": username, "password": password} # depend on the key (email, password)
    response = requests.post(SIGNUP_URL, json=data)
    if response.status_code == 201:
        return True
    if response.status_code == 409:
        return False

# Login and Sign Up page
def login_page():
    choice = st.selectbox("Login/Signup", ['Login', 'Signup'])
    if choice == 'Login':
        email = st.text_input("Email Adress")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(email, password):
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")
    
    if choice == 'Signup':
        email = st.text_input("Email Adress")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Signup"):
            if is_valid_email(email):
                if password != "" and confirm_password != "":
                    if password == confirm_password:
                        data = {"username": email, "password": password}
                        response = requests.post(SIGNUP_URL, json=data)
                        if signup(email, password):
                            st.success("Account succesfully created!")
                        else:
                            st.error("Email already registered")
                else:
                    st.error("Please enter your password and confirm the password!!!")
            else:
                st.error("Your email is not a valid email!!")
            
