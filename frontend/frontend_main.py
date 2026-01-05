import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL")
EXTERNAL_BACKEND_URL = os.getenv("EXTERNAL_BACKEND_URL")

st.set_page_config(
    page_title="Random Character Generator",
    layout="centered"
)

# Sidebar / Header
st.title("Character Generator Frontend")
st.subheader("System Status & API Gateway")

st.info("""
**Note:** The Frontend UI is currently under construction. 
The Backend API is fully operational.
""")

# --- Connectivity Check ---
st.markdown("### Backend Connectivity")

try:
    # Attempt to ping the root of your FastAPI app
    response = requests.get(f"{BACKEND_URL}/", timeout=2)
    if response.status_code == 200:
        st.success(f"Connected to Backend at `{EXTERNAL_BACKEND_URL}` successfully!")
    else:
        st.warning("Backend reached but returned an error.")
except Exception:
    st.error(f"Cannot reach Backend at `{EXTERNAL_BACKEND_URL}`. Ensure the Docker containers are running.")
# --- Developer Links ---
st.divider()
st.markdown("### Developer Resources")
st.write("While the UI is being built, you can interact with the API directly via the interactive documentation:")
col1, col2 = st.columns(2)

with col1:
    st.link_button("Swagger UI (Docs)", f"{EXTERNAL_BACKEND_URL}/docs", type="primary", use_container_width=True)

with col2:
    st.link_button("Redoc", f"{EXTERNAL_BACKEND_URL}/redoc", use_container_width=True)