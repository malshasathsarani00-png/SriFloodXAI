import streamlit as st
from utils.background import set_background

st.set_page_config(
    page_title="SriFloodXAI",
    layout="wide",
    initial_sidebar_state="expanded"
)

set_background()

st.markdown("""
<style>

/* Metric cards */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: 16px;
    padding: 18px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 15px rgba(0, 70, 120, 0.10);
}

/* Info / module cards */
div[data-testid="stAlert"] {
    background: rgba(235, 247, 255, 0.78);
    border-radius: 16px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 15px rgba(0, 70, 120, 0.10);
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}

/* Main content */
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: rgba(245, 249, 253, 0.94);
    border-right: 1px solid rgba(20, 80, 140, 0.12);
}

/* Sidebar inner spacing */
section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

/* Navigation links */
section[data-testid="stSidebar"] a {
    border-radius: 10px;
    margin: 4px 10px;
    padding: 8px 10px;
    font-weight: 500;
}

/* Hover effect */
section[data-testid="stSidebar"] a:hover {
    background: rgba(40, 120, 200, 0.10);
}

/* Selected page */
section[data-testid="stSidebar"] a[aria-current="page"] {
    background: rgba(40, 120, 200, 0.16);
    font-weight: 700;
}

/* Hide default app label if present */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] > ul {
    padding-top: 0.5rem;
}

/* Module cards equal height */
div[data-testid="stAlert"] {
    min-height: 180px;
    display: flex;
    align-items: center;
}

/* Page links */
a[data-testid="stPageLink-NavLink"] {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(0, 90, 160, 0.12);
    border-radius: 10px;
    padding: 8px 12px;
    margin-top: 6px;
    text-decoration: none;
    font-weight: 600;
}

/* Page link hover */
a[data-testid="stPageLink-NavLink"]:hover {
    background: rgba(220, 240, 255, 0.95);
    border-color: rgba(0, 110, 190, 0.30);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# SriFloodXAI

### Real Flood Intelligence System

**Predict • Monitor • Alert • Protect**

An Explainable and Context-Aware Real-Time Flood Prediction
and Early Warning System for Sri Lanka.
""")

st.divider()

st.subheader("🧠 SriFloodXAI Intelligence Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 🌦️ Live Weather
    Real-time weather conditions and rainfall monitoring.
    """)
    st.page_link(
        "pages/2_Live_Weather.py",
        label="🌦️ Open Live Weather",
        use_container_width=True
    )

with col2:
    st.info("""
    ### 🌊 River Gauges
    Monitor river levels and current river conditions.
    """)
    st.page_link(
        "pages/3_River_Gauges.py",
        label="🌊 Open River Gauges",
        use_container_width=True
    )

with col3:
    st.info("""
    ### 🤖 Flood Prediction
    AI-powered flood risk prediction using multiple data sources.
    """)
    st.page_link(
        "pages/5_Flood_Prediction.py",
        label="🤖 Predict Flood Risk",
        use_container_width=True
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.info("""
    ### 🚨 DMC Alerts
    Monitor official flood warnings and emergency information.
    """)
    st.page_link(
        "pages/4_DMC_Alerts.py",
        label="🚨 View DMC Alerts",
        use_container_width=True
    )

with col5:
    st.info("""
    ### 📊 Analytics & History
    Explore flood information, analytics and previous predictions.
    """)
    st.page_link(
        "pages/7_Analytics.py",
        label="📊 Open Analytics",
        use_container_width=True
    )

    st.page_link(
        "pages/8_History.py",
        label="🕘 View History",
        use_container_width=True
    )

with col6:
    st.info("""
    ### 🧠 Explainable AI
    Understand the factors influencing AI flood predictions.
    """)
    st.page_link(
        "pages/6_Explainable_AI.py",
        label="🧠 Open Explainable AI",
        use_container_width=True
    )

st.divider()

st.caption(
    "🌊 SriFloodXAI — Early Warning Today, Safer Tomorrow"
)