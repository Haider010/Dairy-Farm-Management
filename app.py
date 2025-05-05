import streamlit as st
from sqlalchemy import create_engine
from crud import init_db

# Initialize DB once
init_db()

def inject_navbar():
    # Hide default Streamlit elements
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Custom navbar styling */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            align-items: center;
        }
        .nav-brand {
            font-weight: 700;
            font-size: 1.4rem;
            margin-right: 3rem;
            color: #2c3e50;
        }
        .nav-item {
            margin: 0 1.5rem;
            color: #666;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .nav-item:hover {
            color: #3498db;
            transform: translateY(-2px);
        }
        .nav-active {
            color: #3498db;
            border-bottom: 2px solid #3498db;
        }
        main {
            margin-top: 80px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Get current page from query parameters
    current_page = st.query_params.get("page", "Home")
    
    # Navbar HTML with proper string formatting
    navbar_html = f"""
    <nav class="navbar">
        <div class="nav-brand">🐄 DairyPro</div>
        <a class="nav-item {'nav-active' if current_page == 'Home' else ''}" href="/?page=Home">Home</a>
        <a class="nav-item {'nav-active' if current_page == 'Animals' else ''}" href="/?page=Animals">Animals</a>
        <a class="nav-item {'nav-active' if current_page == 'Milk Production' else ''}" href="/?page=Milk Production">Milk</a>
        <a class="nav-item {'nav-active' if current_page == 'Feeding Logs' else ''}" href="/?page=Feeding Logs">Feeding</a>
        <a class="nav-item {'nav-active' if current_page == 'Medicine Logs' else ''}" href="/?page=Medicine Logs">Medicine</a>
        <a class="nav-item {'nav-active' if current_page == 'Dashboard' else ''}" href="/?page=Dashboard">Analytics</a>
    </nav>
    """
    
    st.markdown(navbar_html, unsafe_allow_html=True)
# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Dairy Farm Management",
    initial_sidebar_state="collapsed"
)

# Inject custom navbar
inject_navbar()

# Get current page from query parameters
page = st.query_params.get("page", "Home")

# Page routing
if page == "Home":
    from pages.home import show_home
    show_home()
elif page == "Animals":
    from pages.animals import show_animals
    show_animals()
elif page == "Milk Production":
    from pages.milk import show_milk
    show_milk()
elif page == "Feeding Logs":
    from pages.feed import show_feed
    show_feed()
elif page == "Medicine Logs":
    from pages.medicine import show_medicine
    show_medicine()
elif page == "Dashboard":
    from pages.reports import show_dashboard
    show_dashboard()

# Hide sidebar completely
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)