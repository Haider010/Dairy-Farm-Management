import streamlit as st
from crud import init_db

# Initialize DB once
init_db()

def inject_navbar():
    # Custom CSS for modern navbar
    st.markdown("""
    <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Professional navbar styling */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            align-items: center;
        }
        .nav-brand {
            font-weight: 700;
            font-size: 1.5rem;
            margin-right: 3rem;
            color: #2c3e50;
            display: flex;
            align-items: center;
        }
        .nav-item {
            margin: 0 1.2rem;
            color: #555;
            text-decoration: none;
            font-weight: 500;
            font-size: 1rem;
            padding: 0.5rem 0;
            position: relative;
            transition: all 0.3s ease;
        }
        .nav-item:hover {
            color: #3498db;
        }
        .nav-item::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background: #3498db;
            transition: width 0.3s ease;
        }
        .nav-item:hover::after {
            width: 100%;
        }
        .nav-active {
            color: #3498db;
        }
        .nav-active::after {
            width: 100%;
        }
        main {
            margin-top: 80px;
        }
        /* Hide the actual buttons */
        .stButton > button {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Navbar HTML with click handlers
    st.markdown(f"""
    <nav class="navbar">
        <div class="nav-brand">🐄 DairyPro</div>
        <div class="nav-item {'nav-active' if st.session_state.current_page == 'Home' else ''}" 
             onclick="window.parent.document.querySelector('button[id^=nav_home]').click()">Home</div>
        <div class="nav-item {'nav-active' if st.session_state.current_page == 'Animals' else ''}" 
             onclick="window.parent.document.querySelector('button[id^=nav_animals]').click()">Animals</div>
        <div class="nav-item {'nav-active' if st.session_state.current_page == 'Milk Production' else ''}" 
             onclick="window.parent.document.querySelector('button[id^=nav_milk]').click()">Milk</div>
        <div class="nav-item {'nav-active' if st.session_state.current_page == 'Feeding Logs' else ''}" 
             onclick="window.parent.document.querySelector('button[id^=nav_feeding]').click()">Feeding</div>
        <div class="nav-item {'nav-active' if st.session_state.current_page == 'Medicine Logs' else ''}" 
             onclick="window.parent.document.querySelector('button[id^=nav_medicine]').click()">Medicine</div>
        <div class="nav-item {'nav-active' if st.session_state.current_page == 'Dashboard' else ''}" 
             onclick="window.parent.document.querySelector('button[id^=nav_analytics]').click()">Analytics</div>
    </nav>
    """, unsafe_allow_html=True)

    # Create hidden buttons for each nav item
    if st.button("Home", key="nav_home"):
        st.session_state.current_page = "Home"
        st.rerun()
    if st.button("Animals", key="nav_animals"):
        st.session_state.current_page = "Animals"
        st.rerun()
    if st.button("Milk", key="nav_milk"):
        st.session_state.current_page = "Milk Production"
        st.rerun()
    if st.button("Feeding", key="nav_feeding"):
        st.session_state.current_page = "Feeding Logs"
        st.rerun()
    if st.button("Medicine", key="nav_medicine"):
        st.session_state.current_page = "Medicine Logs"
        st.rerun()
    if st.button("Analytics", key="nav_analytics"):
        st.session_state.current_page = "Dashboard"
        st.rerun()

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Dairy Farm Management",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Inject custom navbar
inject_navbar()

# Page routing
if st.session_state.current_page == "Home":
    from pages.home import show_home
    show_home()
elif st.session_state.current_page == "Animals":
    from pages.animals import show_animals
    show_animals()
elif st.session_state.current_page == "Milk Production":
    from pages.milk import show_milk
    show_milk()
elif st.session_state.current_page == "Feeding Logs":
    from pages.feed import show_feed
    show_feed()
elif st.session_state.current_page == "Medicine Logs":
    from pages.medicine import show_medicine
    show_medicine()
elif st.session_state.current_page == "Dashboard":
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