import streamlit as st
import requests
import os

# Use the service name 'backend' from our docker-compose file
BACKEND_URL = os.getenv("BACKEND_URL")

st.title("Docker Stack Smoke Test")

if st.button('Run System Check'):
    try:
        response = requests.get(f"{BACKEND_URL}/test")
        data = response.json()
        
        st.success("Communication with Backend established!")
        st.json(data) # Displays the result from the API
        
    except Exception as e:
        st.error(f"Could not connect to Backend: {e}")