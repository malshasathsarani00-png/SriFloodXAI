import streamlit as st
from utils.background import set_background

from utils.official_warning_service import (
    get_current_official_warning,
    get_warned_areas_from_warning
)

from utils.prediction_engine import predict_flood_risk
from utils.encoders import DISTRICTS, RIVERS
from utils.history_manager import save_prediction
from utils.emergency_alerts import get_emergency_alert
from utils.email_alert import send_email_alert
from utils.sms_alert import send_sms_alert
from utils.weather_api import get_weather
from utils.river_api import get_latest_river_level
from utils.dmc_scraper import check_dmc_alert

set_background()



st.title("AI Flood Prediction")

st.markdown("""
This module predicts flood risks using:

Controlled model-development flood dataset

River levels

DMC alerts

Weather conditions

using a Random Forest Machine Learning model.
""")


# =====================================
# DISTRICT & RIVER
# =====================================

district = st.selectbox(
    "Select District",
    list(DISTRICTS.keys())
)

river_mapping = {
    "Colombo": "Kelani Ganga",
    "Gampaha": "Attanagalu Oya",
    "Ratnapura": "Kalu Ganga",
    "Matara": "Nilwala Ganga",
    "Galle": "Gin Ganga",
    "Kandy": "Mahaweli Ganga",
    "Kurunegala": "Deduru Oya",
    "Kalutara": "Kalu Ganga",
    "Badulla": "Mahaweli Ganga",
    "Jaffna": "None"
}

river_name = river_mapping[district]

st.info(f"Associated River: {river_name}")

district_code = DISTRICTS[district]
river_code = RIVERS[river_name]

# =====================================
# LIVE WEATHER INPUTS
# =====================================

st.subheader("Live Weather Information")

if st.button("Fetch Live Weather"):
    weather = get_weather(district)

    if weather:
        st.session_state["rainfall"] = float(weather["rainfall_1h"])
        st.session_state["temperature"] = float(weather["temperature"])
        st.session_state["humidity"] = int(weather["humidity"])

        st.success(f"Live weather data loaded for {district}")

    else:
        st.error("Could not fetch live weather data.")


# Default values
if "rainfall" not in st.session_state:
    st.session_state["rainfall"] = 0.0

if "temperature" not in st.session_state:
    st.session_state["temperature"] = 29.0

if "humidity" not in st.session_state:
    st.session_state["humidity"] = 85


col1, col2 = st.columns(2)

with col1:

    rainfall = st.number_input(
        "Rainfall - Last Hour (mm)",
        min_value=0.0,
        max_value=500.0,
        value=float(st.session_state["rainfall"]),
        step=0.1
    )

# Default river threshold values
    alert_level = None
    minor_level = None
    major_level = None


    river_data = get_latest_river_level(river_name)

if river_data and river_data["water_level"] is not None:

    river_level = float(river_data["water_level"])

    st.metric(
        "Official Live River Level",
        f"{river_level:.2f} m"
    )

    st.caption(
        f"Station: {river_data['station']} | "
        f"Updated: {river_data['updated']}"
    )

    alert_level = river_data.get("alert_level")
    minor_level = river_data.get("minor_level")
    major_level = river_data.get("major_level")

    if alert_level is not None:
        st.caption(
            f"Alert: {alert_level} m | "
            f"Minor Flood: {minor_level} m | "
            f"Major Flood: {major_level} m"
        )

        # =====================================
# AUTOMATIC RIVER STATUS
# =====================================

if (
    alert_level is not None
    and minor_level is not None
    and major_level is not None
):

    if river_level >= major_level:
        river_status = "MAJOR FLOOD"
        st.error("🔴 River Status: MAJOR FLOOD")

    elif river_level >= minor_level:
        river_status = "MINOR FLOOD"
        st.warning("🟠 River Status: MINOR FLOOD")

    elif river_level >= alert_level:
        river_status = "ALERT"
        st.warning("🟡 River Status: ALERT")

    else:
        river_status = "NORMAL"
        st.success("🟢 River Status: NORMAL")

else:

    st.warning(
        "⚠️ Official river level unavailable. "
        "Please enter the river level manually."
    )

    river_level = st.number_input(
        "River Level (m)",
        min_value=0.0,
        max_value=20.0,
        value=4.0,
        step=0.1
    )
    


with col2:

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=50.0,
        value=float(st.session_state["temperature"]),
        step=0.1
    )

    humidity = st.number_input(
        "Humidity (%)",
        min_value=0,
        max_value=100,
        value=int(st.session_state["humidity"])
    )


# =====================================
# LIVE DMC ALERT
# =====================================

st.subheader("Live DMC Information")

dmc_result = check_dmc_alert(river_name)

dmc_value = dmc_result["active"]

if dmc_value == 1:
    dmc_alert = "Yes"

    st.error(
        f"Active DMC Flood Warning Detected for {river_name}"
    )

    st.warning(
        dmc_result["message"]
    )

else:
    dmc_alert = "No"

    st.success(
        f"No recent DMC flood warning detected for {river_name}"
    )

    st.caption(
        dmc_result["message"]
    )


# =====================================
# NOTIFICATIONS
# =====================================

st.divider()

st.subheader("Emergency Notifications")

email = st.text_input(
    "Email Address (Optional)"
)

phone = st.text_input(
    "Mobile Number (Optional)"
)



# =====================================
# PREDICT BUTTON
# =====================================

if st.button("Predict Flood Risk"):

    prediction, probability = predict_flood_risk(
        district_code,
        river_code,
        rainfall,
        river_level,
        dmc_value,
        temperature,
        humidity
    )

    confidence = probability * 100

    # =====================================
    # DETERMINE RISK LEVEL
    # =====================================

    if confidence < 25:
        risk_level = "LOW"
    elif confidence < 50:
        risk_level = "MODERATE"
    elif confidence < 75:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    # =====================================
    # SAVE LATEST PREDICTION FOR XAI
    # =====================================

    st.session_state["xai_input"] = {
        "district": district_code,
        "river": river_code,
        "rainfall_mm": rainfall,
        "river_level_m": river_level,
        "dmc_alert": dmc_value,
        "temperature": temperature,
        "humidity": humidity
    }

    st.session_state["xai_probability"] = float(probability)
    st.session_state["xai_district"] = district
    st.session_state["xai_river"] = river_name
    st.session_state["risk_level"] = risk_level

    # =====================================
    # PREDICTION RESULTS
    # =====================================

    st.divider()
    st.subheader("Prediction Results")

    if risk_level == "LOW":
        st.success(
            f"""
🟢 LOW FLOOD RISK

Flood Probability: {confidence:.2f}%
"""
        )

    elif risk_level == "MODERATE":
        st.warning(
            f"""
🟡 MODERATE FLOOD RISK

Flood Probability: {confidence:.2f}%
"""
        )

    elif risk_level == "HIGH":
        st.error(
            f"""
🟠 HIGH FLOOD RISK

Flood Probability: {confidence:.2f}%
"""
        )

    else:
        st.error(
            f"""
🔴 CRITICAL FLOOD RISK

Flood Probability: {confidence:.2f}%
"""
        )

    # =====================================
    # SAVE HISTORY
    # =====================================

    save_prediction(
        district,
        river_name,
        rainfall,
        river_level,
        temperature,
        humidity,
        dmc_alert,
        risk_level,
        confidence
    )

    st.success("Prediction saved to history.")

    # =====================================
    # EMERGENCY ALERTS
    # =====================================

    st.divider()
    st.subheader("Emergency Alert System")

    alert = get_emergency_alert(
        risk_level,
        district=district,
        river_name=river_name,
        river_level=river_level,
        rainfall=rainfall,
        dmc_alert=dmc_value
    )

    # =====================================
    # CURRENT OFFICIAL WARNED AREAS
    # =====================================

    official_warning = get_current_official_warning(
        river_name
    )

    if official_warning["active"]:

        warning_data = official_warning.get("warning")

        warned_areas = get_warned_areas_from_warning(
            warning_data
        )

        st.warning("CURRENT OFFICIAL FLOOD WARNING DETECTED")

        if warning_data:
            st.write(
                f"**Official Warning:** "
                f"{warning_data.get('title', 'Flood Warning')}"
            )

        if warned_areas:
            st.write("### Current Official Warned Areas")

            for area in warned_areas:
                st.write(f"• {area}")

        else:
            st.info(
                "A current official flood warning was detected, "
                "but specific affected areas could not be extracted."
            )

    else:
        st.info(
            f"No current official DMC warned areas detected "
            f"for {river_name}."
        )

    # =====================================
    # RISK-SPECIFIC ALERT + NOTIFICATIONS
    # =====================================

    if risk_level == "LOW":

        st.success(alert["message"])

    elif risk_level == "MODERATE":

        st.warning(alert["message"])

    elif risk_level == "HIGH":

        st.error(alert["message"])

        if email:
            success = send_email_alert(
                email,
                district,
                river_name,
                risk_level,
                confidence
            )

            if success:
                st.success("Email alert sent.")
            else:
                st.error("Email sending failed.")

        # SMS
        if phone:
            send_sms_alert(
                phone,
                district,
                risk_level
            )
            st.success("SMS alert sent.")


    elif risk_level == "CRITICAL":

        st.error(alert["message"])
        st.balloons()

        try:
            st.audio(
                "assets/emergency_alarm.mp3",
                autoplay=True
        )

        except Exception:
            st.warning("⚠ Emergency sound file not found")

        if email:
            success = send_email_alert(
                email,
                district,
                river_name,
                risk_level,
                confidence
            )

            if success:
                st.success("Emergency email sent.")
            else:
                st.error("Email sending failed.")

        # SMS
        if phone:
            send_sms_alert(
                phone,
                district,
                risk_level
            )
            st.success("Emergency SMS sent.")


    # =====================================
    # INPUT SUMMARY
    # =====================================

    st.divider()
    st.subheader("Prediction Summary")

    st.write({
        "District": district,
        "River": river_name,
        "Rainfall (mm)": rainfall,
        "River Level (m)": river_level,
        "Temperature (°C)": temperature,
        "Humidity (%)": humidity,
        "DMC Alert": dmc_alert,
        "Risk Level": risk_level,
        "Confidence (%)": round(confidence, 2)
    })
