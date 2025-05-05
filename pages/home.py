import streamlit as st

def show_home():
    # Custom CSS for modern design
    st.markdown("""
    <style>
        .hero {
            background: linear-gradient(rgba(0, 0, 0, 0.5), url('https://images.unsplash.com/photo-1470114186116-87d266e1c77b?ixlib=rb-1.2.1&auto=format&fit=crop&w=2070&q=80');
            background-size: cover;
            background-position: center;
            padding: 8rem 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            margin: 1rem 0;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .metric {
            text-align: center;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 15px;
            margin: 1rem 0;
        }
        .cta-button {
            background: #2c3e50;
            color: white !important;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
            text-align: center;
            display: inline-block;
            margin: 2rem 0;
        }
        .cta-button:hover {
            background: #3498db;
            transform: scale(1.05);
            color: white;
            text-decoration: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">Modern Dairy Farm Management</h1>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">AI-Powered Insights for Smarter Herd Management</p>
        <a href="#features" class="cta-button">Get Started →</a>
    </div>
    """, unsafe_allow_html=True)

    # Value Proposition
    st.markdown("""
    <div style="text-align: center; margin-bottom: 4rem;">
        <h2>Transform Your Dairy Operations</h2>
        <p style="color: #666; max-width: 800px; margin: 0 auto;">
        Leverage cutting-edge technology to optimize milk production, track animal health, 
        and streamline farm operations with real-time data analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric">
            <h3>📈 15% Increase</h3>
            <p>Average production improvement</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric">
            <h3>🐄 1000+ Farms</h3>
            <p>Trusted by dairy professionals</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric">
            <h3>⏱️ 5h Saved</h3>
            <p>Daily administrative work</p>
        </div>
        """, unsafe_allow_html=True)

    # Features Grid
    st.markdown("""<a name="features"></a>""", unsafe_allow_html=True)
    st.header("Key Features", anchor=False)
    
    features = [
        ("📱", "Real-Time Monitoring", "Track herd health and production metrics instantly"),
        ("🤖", "AI Predictions", "Forecast milk yields and detect health issues early"),
        ("📊", "Smart Analytics", "Interactive dashboards with actionable insights"),
        ("📲", "Mobile First", "Manage your farm from anywhere, anytime"),
        ("🔒", "Secure Cloud", "Military-grade data protection"),
        ("🌱", "Sustainable", "Optimize resources for eco-friendly farming")
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, features[i:i+3]):
            with col:
                st.markdown(f"""
                <div class="feature-card">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
                    <h3>{title}</h3>
                    <p style="color: #666;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)


    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0; border-top: 1px solid #eee;">
        <p>© 2024 DairyFarm Pro. All rights reserved.<br>
        Contact: hello@dairyfarmpro.com | +1 (800) 555-1234</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_home()