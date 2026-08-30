import streamlit as st
from utils.background import set_background

set_background()

st.title("About SriFloodXAI")
st.caption("Explainable • Context-Aware • Real-Time Flood Prediction")

st.markdown("""
<style>
.about-hero {
    padding: 1.4rem 1.5rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(13, 110, 253, 0.88), rgba(0, 150, 136, 0.82));
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.16);
}
.about-hero h2 { margin: 0 0 0.4rem 0; color: white; }
.about-hero p { margin: 0; font-size: 1.02rem; }
.info-card {
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(120,120,120,0.18);
    border-radius: 16px;
    padding: 1.05rem 1.1rem;
    min-height: 190px;
    margin-bottom: 0.8rem;
    box-shadow: 0 5px 18px rgba(0,0,0,0.10);
}
.info-card h3 {
    margin-top: 0;
    color: #17345f;
    border-bottom: 2px solid #d7e8f8;
    padding-bottom: 0.45rem;
}
h3 {
    color: #17345f;
}
.small-card {
    background: rgba(255,255,255,0.90);
    border-radius: 14px;
    padding: 0.9rem 1rem;
    border-left: 5px solid #0d6efd;
    margin-bottom: 0.7rem;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
</style>

<div class="about-hero">
  <h2>SriFloodXAI</h2>
  <p><b>An Explainable and Context-Aware Real-Time Flood Prediction System Using Edge Intelligence</b></p>
  <p style="margin-top:.55rem;">A final-year research prototype supporting flood monitoring,
  explainable AI predictions, multi-source data integration and context-aware disaster alerts in Sri Lanka.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
      <h3>Weather</h3>
      <b>OpenWeather API</b><br><br>
      • Temperature<br>
      • Humidity<br>
      • Rainfall<br>
      • Wind speed<br>
      • Atmospheric pressure
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
      <h3>River Monitoring</h3>
      <b>ArcGIS Feature Service</b><br><br>
      • River gauge monitoring<br>
      • Water-level information<br>
      • Flood-risk context<br>
      • Irrigation Department GIS workflow
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
      <h3>Official Warnings</h3>
      <b>Disaster Management Centre</b><br><br>
      • Flood warnings<br>
      • Disaster advisories<br>
      • Official warned areas<br>
      • Independent warning context
    </div>
    """, unsafe_allow_html=True)

st.markdown("### AI Prediction & Explainability")

ai1, ai2 = st.columns(2)

with ai1:
    st.markdown("""
    <div class="info-card">
      <h3>Random Forest</h3>
      <b>Prediction inputs</b><br><br>
      • Rainfall and river level<br>
      • DMC alert status<br>
      • Temperature and humidity<br>
      • District and river information<br><br>
      <b>Outputs:</b> LOW • MODERATE • HIGH • CRITICAL
    </div>
    """, unsafe_allow_html=True)

with ai2:
    st.markdown("""
    <div class="info-card">
      <h3>SHAP Explainable AI</h3>
      SHAP is used to show how input features influence the model's output and to
      provide human-readable explanations of the latest prediction.<br><br>
      <b>Note:</b> SHAP explains model behaviour; it does not prove that a prediction is correct.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Emergency Notification Methods")

n1, n2, n3 = st.columns(3)

with n1:
    st.markdown("""
    <div class="small-card">
      <b>Email Alerts</b><br>
      Gmail SMTP is used for higher-risk email notifications when an address is provided.
    </div>
    """, unsafe_allow_html=True)

with n2:
    st.markdown("""
    <div class="small-card">
      <b>SMS Alerts</b><br>
      Twilio SMS was implemented and successfully tested during development.
      Live SMS delivery is not maintained in the current prototype.
    </div>
    """, unsafe_allow_html=True)

with n3:
    st.markdown("""
    <div class="small-card">
      <b>Sound Alerts</b><br>
      An emergency alarm is presented for CRITICAL-risk predictions.
      Playback depends on browser media permissions.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Research Prototype")
st.info(
    "The Random Forest model was developed and evaluated using a controlled "
    "model-development flood dataset. SriFloodXAI is a research prototype and "
    "should not be interpreted as a fully validated national flood-warning system."
)

st.markdown("### Technology Stack")
st.markdown(
    "`Python`  •  `Streamlit`  •  `Scikit-Learn`  •  `SHAP`  •  `Pandas`  •  "
    "`Plotly`  •  `OpenWeather API`  •  `ArcGIS Feature Service`  •  `Requests`"
)

st.markdown("### Future Improvements")
f1, f2 = st.columns(2)

with f1:
    st.markdown("""
    <div class="info-card">
      <h3>Coverage & Validation</h3>
      • Extend prediction-model coverage to all 25 districts<br>
      • Validate with larger independent real-world datasets<br>
      • Strengthen official river and warning integrations
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="info-card">
      <h3>Platform Development</h3>
      • Persistent cloud-based prediction history<br>
      • Mobile application support<br>
      • Additional rainfall/geospatial sources<br>
      • Local-versus-cloud performance benchmarking
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Project Information")
st.markdown("""
<div class="small-card">
<b>Student:</b> T. K. M. Sathsarani &nbsp; | &nbsp; <b>Index:</b> 11434<br>
<b>Module:</b> COM4901 &nbsp; | &nbsp; <b>Programme:</b> B.Sc. (Hons) Management Information Systems<br>
<b>Supervisor:</b> Mr. Ravindu Saluwadana<br>
<b>Faculty:</b> Faculty of Computer Science and Engineering, KIU
</div>
""", unsafe_allow_html=True)

st.success("SriFloodXAI Version 1.0 — Final Year Research Prototype")
