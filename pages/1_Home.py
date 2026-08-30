import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="SriFloodXAI | Home",
    page_icon="💧",
    layout="wide"
)

# ---------- Helpers ----------
def image_to_data_uri(path):
    image_bytes = Path(path).read_bytes()
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

MAP_URI = image_to_data_uri(
    Path(__file__).resolve().parents[1] / "sri_lanka_flood_map.png"
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: #f7f9fc;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    /* Hero */
    .hero-wrap {
        display: grid;
        grid-template-columns: 1.45fr 0.85fr;
        gap: 1rem;
        align-items: center;
        padding: 2.2rem 2.4rem;
        background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 58%, #edf6ff 100%);
        border: 1px solid #e1e8f0;
        border-radius: 22px;
        box-shadow: 0 10px 30px rgba(20, 50, 90, 0.06);
        margin-bottom: 1.4rem;
        overflow: hidden;
    }

    .hero-kicker {
        color: #3374b5;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 0.35rem;
    }

    .hero-title {
        font-size: 3.45rem;
        line-height: 1.02;
        font-weight: 800;
        color: #122d5a;
        margin: 0 0 0.55rem 0;
    }

    .hero-subtitle {
        font-size: 1.07rem;
        color: #355f8d;
        font-weight: 650;
        margin-bottom: 0.8rem;
    }

    .hero-copy {
        font-size: 1rem;
        line-height: 1.7;
        color: #59697d;
        max-width: 760px;
    }

    .hero-map {
        width: 100%;
        max-width: 430px;
        margin-left: auto;
        display: block;
    }

    /* Overview cards */
    .overview-card {
        min-height: 128px;
        padding: 1.2rem 1.15rem;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(20, 50, 90, 0.07);
        border: 1px solid rgba(40, 80, 120, 0.10);
        border-top: 4px solid var(--accent);
        background: var(--card-bg);
    }

    .card-blue   { --accent: #2f6fad; --card-bg: #f3f8fd; }
    .card-green  { --accent: #2f8061; --card-bg: #f2f9f6; }
    .card-purple { --accent: #6756a5; --card-bg: #f6f4fb; }
    .card-amber  { --accent: #b17828; --card-bg: #fcf8ef; }

    .overview-value {
        color: #102f61;
        font-size: 1.4rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .overview-label {
        color: #2f425a;
        font-size: 0.92rem;
        font-weight: 700;
        margin-top: 0.28rem;
    }

    .overview-note {
        color: #7a8798;
        font-size: 0.78rem;
        margin-top: 0.25rem;
    }

    .section-title {
        color: #152b4c;
        font-size: 1.55rem;
        font-weight: 800;
        margin: 1.7rem 0 0.2rem 0;
    }

    .section-caption {
        color: #738095;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* Source cards */
    .source-card {
        background: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 4px 14px rgba(20, 50, 90, 0.035);
    }

    .source-head {
        display: flex;
        justify-content: space-between;
        gap: 0.8rem;
        align-items: center;
        margin-bottom: 0.45rem;
    }

    .source-title {
        color: #17345f;
        font-size: 1.03rem;
        font-weight: 800;
    }

    .source-text {
        color: #667589;
        font-size: 0.89rem;
        line-height: 1.55;
    }

    .tag {
        display: inline-block;
        background: #edf8f0;
        color: #2b7a47;
        border-radius: 999px;
        padding: 0.22rem 0.62rem;
        font-size: 0.74rem;
        font-weight: 750;
        white-space: nowrap;
    }

    .mini-tags {
        margin-top: 0.65rem;
    }

    .mini {
        display: inline-block;
        background: #f1f5fa;
        color: #5d6c7f;
        border-radius: 999px;
        padding: 0.18rem 0.5rem;
        font-size: 0.73rem;
        margin: 0 0.25rem 0.25rem 0;
    }

    /* System overview */
    .system-panel {
        background: #ffffff;
        border: 1px solid #e1e8f0;
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 6px 18px rgba(20, 50, 90, 0.04);
    }

    .system-row {
        display: grid;
        grid-template-columns: 42px 1fr auto;
        gap: 0.8rem;
        align-items: center;
        padding: 0.9rem 0;
        border-bottom: 1px solid #edf1f5;
    }

    .system-row:last-child {
        border-bottom: none;
    }

    .system-marker {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #edf4fb;
        color: #2f6fad;
        border: 1px solid #d8e6f3;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.03em;
    }

    .system-title {
        color: #203a60;
        font-size: 0.95rem;
        font-weight: 800;
    }

    .system-sub {
        color: #7a8797;
        font-size: 0.78rem;
        margin-top: 0.1rem;
    }

    .status-ready {
        color: #247a43;
        background: #eef8f1;
        border-radius: 999px;
        padding: 0.2rem 0.55rem;
        font-size: 0.72rem;
        font-weight: 750;
    }

    .notice {
        margin-top: 1rem;
        padding: 1rem 1.15rem;
        background: #f0f6ff;
        border: 1px solid #dfeaf7;
        border-radius: 12px;
        color: #47617e;
        line-height: 1.55;
        font-size: 0.87rem;
    }

    @media (max-width: 900px) {
        .hero-wrap {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 2.55rem;
        }
        .hero-map {
            margin: auto;
            max-width: 330px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown(f"""
<div class="hero-wrap">
    <div>
        <div class="hero-kicker">FLOOD INTELLIGENCE FOR SRI LANKA</div>
        <div class="hero-title">SriFloodXAI</div>
        <div class="hero-subtitle">
            Explainable • Context-Aware • Real-Time Flood Intelligence
        </div>
        <div class="hero-copy">
            SriFloodXAI combines current environmental monitoring, machine-learning
            flood prediction, explainable AI, official warning context and multiple
            notification methods in one research dashboard.
        </div>
    </div>
    <div>
        <img class="hero-map" src="{MAP_URI}" alt="Sri Lanka flood monitoring map"/>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Quick overview ----------
c1, c2, c3, c4 = st.columns(4, gap="medium")

cards = [
    ("card-blue", "3", "Main Data Inputs", "Weather • River • DMC"),
    ("card-green", "Random Forest", "Prediction Model", "Flood-risk classification"),
    ("card-purple", "SHAP", "Explainable AI", "Feature-level explanations"),
    ("card-amber", "3", "Alert Methods", "Email • SMS • Sound"),
]

for col, (card_class, value, label, note) in zip((c1, c2, c3, c4), cards):
    with col:
        st.markdown(f"""
        <div class="overview-card {card_class}">
            <div class="overview-value">{value}</div>
            <div class="overview-label">{label}</div>
            <div class="overview-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- Main content ----------
st.markdown('<div class="section-title">Sri Lankan Data & Monitoring Sources</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">The main information sources used by the SriFloodXAI prototype.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.35, 1], gap="large")

with left:
    st.markdown("""
    <div class="source-card">
        <div class="source-head">
            <div class="source-title">OpenWeather API</div>
            <span class="tag">Integrated</span>
        </div>
        <div class="source-text">
            Current weather data used for monitoring and model inputs.
        </div>
        <div class="mini-tags">
            <span class="mini">Temperature</span>
            <span class="mini">Humidity</span>
            <span class="mini">Rainfall</span>
            <span class="mini">Pressure</span>
            <span class="mini">Wind Speed</span>
        </div>
    </div>

    <div class="source-card">
        <div class="source-head">
            <div class="source-title">River-Level Monitoring</div>
            <span class="tag">Integrated</span>
        </div>
        <div class="source-text">
            Available public river-gauge readings are retrieved for current river-level monitoring.
        </div>
        <div class="mini-tags">
            <span class="mini">Gauge Readings</span>
            <span class="mini">River Levels</span>
            <span class="mini">Major Rivers</span>
        </div>
    </div>

    <div class="source-card">
        <div class="source-head">
            <div class="source-title">Disaster Management Centre (DMC)</div>
            <span class="tag">Integrated</span>
        </div>
        <div class="source-text">
            Official public warning information is presented separately from the AI prediction.
        </div>
        <div class="mini-tags">
            <span class="mini">Flood Warnings</span>
            <span class="mini">Official Context</span>
            <span class="mini">Warning Areas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="system-panel">
        <div style="font-size:1.15rem;font-weight:800;color:#17345f;margin-bottom:.2rem;">
            System Overview
        </div>

        <div class="system-row">
            <div class="system-marker">01</div>
            <div>
                <div class="system-title">Live Monitoring</div>
                <div class="system-sub">Weather and river information</div>
            </div>
            <span class="status-ready">Ready</span>
        </div>

        <div class="system-row">
            <div class="system-marker">02</div>
            <div>
                <div class="system-title">Flood Prediction</div>
                <div class="system-sub">Random Forest risk estimation</div>
            </div>
            <span class="status-ready">Ready</span>
        </div>

        <div class="system-row">
            <div class="system-marker">03</div>
            <div>
                <div class="system-title">Explainable AI</div>
                <div class="system-sub">SHAP-based model explanations</div>
            </div>
            <span class="status-ready">Ready</span>
        </div>

        <div class="system-row">
            <div class="system-marker">04</div>
            <div>
                <div class="system-title">Alerts & Notifications</div>
                <div class="system-sub">Email, SMS and sound alerts</div>
            </div>
            <span class="status-ready">Ready</span>
        </div>

        <div class="system-row">
            <div class="system-marker">05</div>
            <div>
                <div class="system-title">Analytics & History</div>
                <div class="system-sub">Trends and previous predictions</div>
            </div>
            <span class="status-ready">Ready</span>
        </div>
    </div>

    <div class="notice">
        <strong>Decision-support prototype</strong><br>
        AI-generated flood risk and official DMC warning information are kept separate.
        SriFloodXAI does not replace official disaster-management warnings.
    </div>
    """, unsafe_allow_html=True)
