import streamlit as st

from utils.weather_api import get_weather
from utils.background import set_weather_background

set_weather_background()

st.markdown("""
<style>

/* Live Weather metric glass cards */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.58);
    border: 1px solid rgba(255, 255, 255, 0.65);
    border-radius: 18px;
    padding: 20px 18px;
    min-height: 135px;

    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);

    box-shadow: 0 8px 24px rgba(20, 40, 70, 0.10);
}

/* Metric label */
div[data-testid="stMetric"] label {
    font-weight: 600;
}

/* Metric value */
div[data-testid="stMetricValue"] {
    font-weight: 600;
}

/* Slight hover effect */
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    transition: 0.2s ease;
    box-shadow: 0 10px 28px rgba(20, 40, 70, 0.16);
}

</style>
""", unsafe_allow_html=True)


st.title("Live Weather Dashboard")

st.markdown("""
Real-time weather information for Sri Lanka
using OpenWeather API.
""")


districts = [
    "Ampara",
    "Anuradhapura",
    "Badulla",
    "Batticaloa",
    "Colombo",
    "Galle",
    "Gampaha",
    "Hambantota",
    "Jaffna",
    "Kalutara",
    "Kandy",
    "Kegalle",
    "Kilinochchi",
    "Kurunegala",
    "Mannar",
    "Matale",
    "Matara",
    "Monaragala",
    "Mullaitivu",
    "Nuwara Eliya",
    "Polonnaruwa",
    "Puttalam",
    "Ratnapura",
    "Trincomalee",
    "Vavuniya"
]


selected_city = st.selectbox(

    "Select District",

    districts

)


if st.button("Get Weather Data"):

    weather = get_weather(selected_city)

    if weather:

        st.success(
            f"Weather data loaded for {selected_city}"
        )

        icon_url = (

            f"https://openweathermap.org/img/wn/"
            f"{weather['icon']}@2x.png"

        )

        col_icon, col_info = st.columns([1, 4])

        with col_icon:

            st.image(
                icon_url,
                width=100
            )

        with col_info:

            st.subheader(
                weather["description"].title()
            )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "🌡 Temperature",

                f"{weather['temperature']} °C"

            )

        with col2:

            st.metric(

                "💧 Humidity",

                f"{weather['humidity']} %"

            )

        with col3:

            st.metric(

                "📈 Pressure",

                f"{weather['pressure']} hPa"

            )

        with col4:

            st.metric(

                "💨 Wind Speed",

                f"{weather['wind_speed']} m/s"

            )

        st.divider()

        st.metric(

            "🌧 Rainfall (Last Hour)",

            f"{weather['rainfall_1h']} mm"

        )

    else:

        st.error(
            "Could not fetch weather data."
        )