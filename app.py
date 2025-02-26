import streamlit as st

# Set page configuration
st.set_page_config(page_title="Tax App", layout="wide")
from tax_app import show_tax_app
from forecast import show_forecast
from tax_advice import show_tax_advice

def apply_common_style():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');
        
        .main {
            background: linear-gradient(135deg, #0a192f 0%, #000000 100%);
            padding: 2rem;
            min-height: 100vh;
        }
        
        /* Header styling */
        .header {
            color: #ffffff;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            background: transparent;
        }
        
        .header h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 600;
            color: #64ffda;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
        }
        
        .header p {
            color: #8892b0;
            font-size: 1.1rem;
        }
        
        /* Grid container */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));  /* Changed to 3 columns */
            gap: 1.5rem;
            padding: 1rem;
            max-width: 1200px;  /* Increased max-width to accommodate 3 columns */
            margin: 0 auto;
        }
        
        /* Feature card styling */
        .feature-card {
            background: rgba(2, 12, 27, 0.7);
            border-radius: 8px;
            padding: 1.2rem;
            color: #8892b0;
            transition: all 0.3s ease;
            border: 1px solid #1e2d3d;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #64ffda;
            box-shadow: 0 4px 20px rgba(100, 255, 218, 0.1);
        }
        
        .feature-icon {
            font-size: 1.8rem;
            margin-bottom: 0.8rem;
            color: #64ffda;
        }
        
        .feature-title {
            font-size: 1.1rem;
            margin-bottom: 0.8rem;
            color: #ccd6f6;
            font-weight: 600;
        }
        
        .feature-list {
            list-style-type: none;
            padding-left: 0;
        }
        
        .feature-list li {
            margin-bottom: 0.4rem;
            color: #8892b0;
            font-size: 0.85rem;
            position: relative;
            padding-left: 1rem;
        }
        
        .feature-list li:before {
            content: "▹";
            position: absolute;
            left: 0;
            color: #64ffda;
        }

        /* Override Streamlit styles */
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #000000 100%);
        }
        
        .stButton button {
            background-color: #64ffda;
            color: #0a192f;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }
        
        .stSelectbox > div > div {
            background-color: rgba(2, 12, 27, 0.7);
            border: 1px solid #1e2d3d;
        }
        
        .stTextInput > div > div {
            background-color: rgba(2, 12, 27, 0.7);
            border: 1px solid #1e2d3d;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a192f;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #64ffda;
            border-radius: 5px;
        }
    </style>
    """

def show_home():
    st.title("Welcome to the Not-so-Taxing- An app that makes managing taxes less 'taxing'!")
    st.markdown("""
    This app helps you with:
    - Understanding the tax filing process
    - Calculating your income tax
    - Checking the required documents for tax filing
    - Uploading and analyzing your expenditure sheet
    - Summarizing tax advice from your favorite financial advisors

    Use the sidebar to navigate to different sections.
    """)

    # Custom CSS for styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');
        
        /* Main container styling */
        .main {
            background: linear-gradient(135deg, #0a192f 0%, #000000 100%);
            padding: 2rem;
            min-height: 100vh;
        }
        
        /* Header styling */
        .header {
            color: #ffffff;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            background: transparent;
        }
        
        .header h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 600;
            color: #64ffda;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
        }
        
        .header p {
            color: #8892b0;
            font-size: 1.1rem;
        }
        
        /* Grid container */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));  /* Changed to 3 columns */
            gap: 1.5rem;
            padding: 1rem;
            max-width: 1200px;  /* Increased max-width to accommodate 3 columns */
            margin: 0 auto;
        }
        
        /* Feature card styling */
        .feature-card {
            background: rgba(2, 12, 27, 0.7);
            border-radius: 8px;
            padding: 1.2rem;
            color: #8892b0;
            transition: all 0.3s ease;
            border: 1px solid #1e2d3d;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #64ffda;
            box-shadow: 0 4px 20px rgba(100, 255, 218, 0.1);
        }
        
        .feature-icon {
            font-size: 1.8rem;
            margin-bottom: 0.8rem;
            color: #64ffda;
        }
        
        .feature-title {
            font-size: 1.1rem;
            margin-bottom: 0.8rem;
            color: #ccd6f6;
            font-weight: 600;
        }
        
        .feature-list {
            list-style-type: none;
            padding-left: 0;
        }
        
        .feature-list li {
            margin-bottom: 0.4rem;
            color: #8892b0;
            font-size: 0.85rem;
            position: relative;
            padding-left: 1rem;
        }
        
        .feature-list li:before {
            content: "▹";
            position: absolute;
            left: 0;
            color: #64ffda;
        }

        /* Override Streamlit styles */
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #000000 100%);
        }
    </style>
    """, unsafe_allow_html=True)

    def create_feature_card(icon, title, features, page):
        feature_items = "".join([f"<li>• {feature}</li>" for feature in features])
        card_html = f"""
        <div class="feature-card" onclick="window.location.href='?page={page}'">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <ul class="feature-list">
                {feature_items}
            </ul>
        </div>
        """
        return card_html

    # Feature cards container
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    # Create feature cards
    st.markdown(create_feature_card("📊", "Introduction to Taxes", ["Learn about taxes", "Understand tax filing process"], "Introduction to Taxes"), unsafe_allow_html=True)
    st.markdown(create_feature_card("🧮", "Calculate Your Tax", ["Calculate your income tax", "Check required documents"], "Calculate Your Tax"), unsafe_allow_html=True)
    st.markdown(create_feature_card("💼", "Tax Advice", ["Get tax advice", "Upload and analyze expenditure sheet"], "Tax Advice"), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Apply common styles
st.markdown(apply_common_style(), unsafe_allow_html=True)

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
elif st.session_state.page == "Introduction to Taxes":
    #from forecast import show_forecast
    with st.spinner("Loading Introduction to Taxes..."):
        show_forecast()
elif st.session_state.page == "Calculate Your Tax":
    #from tax_app import show_tax_app
    with st.spinner("Loading Calculate Your Tax..."):
        show_tax_app()
elif st.session_state.page == "Tax Advice":
    #from tax_advice import show_tax_advice
    with st.spinner("Loading Tax Advice..."):
        show_tax_advice()
else:
    st.write("")