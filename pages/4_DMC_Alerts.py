import streamlit as st

from utils.dmc_scraper import check_dmc_alert
from utils.background import set_background

set_background()

st.title("Disaster Management Centre Alerts")

st.markdown("""
Latest flood-warning information checked from the Sri Lanka
Disaster Management Centre (DMC) public reports page.
""")

st.info(
    "This page checks recent DMC flood-warning information for the "
    "selected river. Official warnings remain independent from the "
    "SriFloodXAI prediction."
)

river_options = [
    "Kelani Ganga",
    "Attanagalu Oya",
    "Kalu Ganga",
    "Nilwala Ganga",
    "Gin Ganga",
    "Mahaweli Ganga",
    "Deduru Oya",
]

river_name = st.selectbox(
    "Select River",
    river_options
)

if st.button("Check Latest DMC Warning", use_container_width=True):
    with st.spinner("Checking latest DMC flood-warning information..."):
        result = check_dmc_alert(river_name)

    st.divider()
    st.subheader(f"📍 {river_name}")

    if result["active"] == 1:
        st.error("Recent DMC Flood Warning Detected")
        st.warning(result["message"])
    else:
        st.success("No recent DMC flood warning detected")
        st.caption(result["message"])

st.divider()

st.caption(
    "Source: Sri Lanka Disaster Management Centre public flood-warning "
    "reports. Availability and detection depend on the structure and "
    "publication timing of the DMC website."
)
