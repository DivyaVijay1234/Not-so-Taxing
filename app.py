import streamlit as st

# ✅ Move set_page_config to the top before any Streamlit command
st.set_page_config(page_title="Tax App", layout="wide")

from home import show_home
from tax_app import show_tax_app
from forecast import show_forecast
from tax_advice import show_tax_advice

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');
    body {
        background: linear-gradient(135deg, #0a192f 0%, #000000 100%);
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #000000 100%);
        color: white;
    }
    .header h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 600;
        color: #64ffda;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for page if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Sidebar navigation
st.sidebar.markdown("<h2 style='color: black;'>Navigation</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Home", "Introduction to Taxes", "Calculate Your Tax", "Tax Advice"], index=0)

# Update session state with selected page
st.session_state.page = page

# Load pages dynamically
if st.session_state.page == "Home":
    with st.spinner("Loading application..."):
        show_home()
elif page == "Introduction to Taxes":
    with st.spinner("Loading Introduction to Taxes..."):
        show_forecast()
elif page == "Calculate Your Tax":
    with st.spinner("Loading Calculate Your Tax..."):
        show_tax_app()
elif page == "Tax Advice":
    with st.spinner("Loading Tax Advice..."):
        show_tax_advice()
