import streamlit as st
import pandas as pd
import plotly.express as px
from utils.background import set_background


from utils.shap_explainer import (
    get_feature_importance,
    generate_shap_plot,
    get_local_shap_explanation
)


set_background()

st.title("Explainable AI (XAI)")
st.caption("Understand the factors influencing SriFloodXAI model predictions")

st.markdown("""
<style>
.xai-hero {
    padding: 1.25rem 1.4rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(13,110,253,0.88), rgba(111,66,193,0.82));
    color: white;
    margin-bottom: 1rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.xai-hero h3 { margin: 0 0 .35rem 0; color: white; }
.xai-card {
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(120,120,120,0.18);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: .9rem;
    box-shadow: 0 5px 18px rgba(0,0,0,0.09);
}
</style>

<div class="xai-hero">
  <h3>🔎 Why did the model make this prediction?</h3>
  <p>SHAP is used to examine global feature importance and explain the latest
  flood-risk prediction in a human-readable way.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="xai-card">
<b>Explanation Framework</b><br><br>
✅ SHAP (SHapley Additive Explanations)<br>
✅ Global Feature Importance Analysis<br>
✅ Local Prediction Explanation<br>
✅ Human-Readable Feature Interpretation
</div>
""", unsafe_allow_html=True)


# =====================================
# FEATURE IMPORTANCE
# =====================================

st.subheader("📊 Global Feature Importance")

importance_df = get_feature_importance()

st.dataframe(

    importance_df,

    use_container_width=True

)


fig = px.bar(

    importance_df,

    x="Importance",

    y="Feature",

    orientation="h",

    text="Importance",

    title="Model Feature Importance"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================
# LATEST PREDICTION SHAP EXPLANATION
# =====================================

st.divider()

st.subheader("Latest Flood Prediction Explanation")

if "xai_input" in st.session_state:

    input_df = pd.DataFrame(
        [st.session_state["xai_input"]]
    )

    if "xai_district" in st.session_state:
        st.write(
            f"📍 **District:** "
            f"{st.session_state['xai_district']}"
        )

    if "xai_river" in st.session_state:
        st.write(
            f"🌊 **River:** "
            f"{st.session_state['xai_river']}"
        )

    if "xai_probability" in st.session_state:
        probability = st.session_state["xai_probability"]

        st.metric(
            "Flood Probability",
            f"{probability * 100:.2f}%"
        )

    st.write("### SHAP Explanation")

    shap_fig = generate_shap_plot(input_df)

    st.pyplot(shap_fig)

else:
    st.info(
        "Make a flood prediction first to view "
        "the SHAP explanation."
    )

# =====================================
# HUMAN EXPLANATION
# =====================================

st.subheader("Human Readable Explanation")

if "xai_input" in st.session_state:

    input_df = pd.DataFrame(
        [st.session_state["xai_input"]]
    )

    local_explanation = get_local_shap_explanation(input_df)

    feature = local_explanation["feature"]
    value = local_explanation["value"]
    contribution = local_explanation["contribution"]
    direction = local_explanation["direction"]

    feature_labels = {
        "district": "District",
        "river": "River",
        "rainfall_mm": "Rainfall",
        "river_level_m": "River Level",
        "dmc_alert": "DMC Alert Status",
        "temperature": "Temperature",
        "humidity": "Humidity"
    }

    readable_feature = feature_labels.get(
        feature,
        feature
    )

    st.success(
        f"""
Most influential factor for this prediction:

🌟 **{readable_feature}**

Current value: **{value}**

This factor **{direction} the predicted flood risk**.

SHAP contribution: **{contribution:+.3f}**
"""
    )

else:

    st.info(
        "Make a flood prediction first to view "
        "the human-readable explanation."
    )

# =====================================
# XAI INFORMATION
# =====================================

st.markdown("""
<div class="xai-card">
<b>ℹ️ Interpreting XAI Results</b><br><br>
• Shows which features influence model behaviour<br>
• Helps users understand the latest model output<br>
• Improves transparency of the prediction process<br>
• Supports interpretation of flood-risk predictions<br><br>
<b>Important:</b> SHAP explains how the model produced an output; it does not prove
that the prediction is correct or replace official DMC flood warnings.
</div>
""", unsafe_allow_html=True)