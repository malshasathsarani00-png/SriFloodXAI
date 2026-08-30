import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

from utils.background import set_background


GAUGE_URL = (
    "https://services3.arcgis.com/J7ZFXmR8rSmQ3FGf/"
    "arcgis/rest/services/gauges_2_view/FeatureServer/0/query"
)


@st.cache_data(ttl=300)
def get_arcgis_river_levels():
    """Retrieve the latest available gauge records from the ArcGIS layer."""
    params = {
        "where": "1=1",
        "outFields": (
            "basin,gauge,water_level,rain_fall,"
            "EditDate,alertpull,minorpull,majorpull"
        ),
        "returnGeometry": "false",
        "orderByFields": "EditDate DESC",
        "resultRecordCount": 2000,
        "f": "json",
    }

    try:
        response = requests.get(GAUGE_URL, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()

        if "error" in payload:
            return []

        rows = []
        for feature in payload.get("features", []):
            a = feature.get("attributes", {})

            updated = ""
            if a.get("EditDate"):
                updated = datetime.fromtimestamp(
                    a["EditDate"] / 1000
                ).strftime("%Y-%m-%d %H:%M:%S")

            rows.append({
                "river_name": a.get("basin"),
                "station_name": a.get("gauge"),
                "water_level": a.get("water_level"),
                "rainfall": a.get("rain_fall"),
                "timestamp": updated,
                "alert_level": a.get("alertpull"),
                "minor_level": a.get("minorpull"),
                "major_level": a.get("majorpull"),
            })

        return rows

    except (requests.RequestException, ValueError, TypeError):
        return []



# --------------------------------------------------
# PAGE BACKGROUND
# --------------------------------------------------

set_background()


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("Sri Lanka River Gauges")

st.markdown("""
Monitor the latest available river-level information for Sri Lankan
river monitoring stations.
""")

st.info(
    "River information is retrieved from the public ArcGIS river-gauge feature service used by the project."
)


# --------------------------------------------------
# GET LIVE DATA
# --------------------------------------------------

with st.spinner("Fetching latest ArcGIS river gauge data..."):
    data = get_arcgis_river_levels()


if not data:
    st.warning(
        "⚠️ Live river gauge data is currently unavailable. "
        "Please try again later."
    )
    st.stop()


# --------------------------------------------------
# NORMALIZE API DATA
# --------------------------------------------------

stations = []

for item in data:

    river = (
        item.get("river_name")
        or item.get("river")
        or item.get("River")
        or "Unknown River"
    )

    station = (
        item.get("station_name")
        or item.get("station")
        or item.get("Station")
        or "Unknown Station"
    )

    level = (
        item.get("water_level")
        or item.get("level")
        or item.get("WaterLevel")
    )

    timestamp = (
        item.get("timestamp")
        or item.get("datetime")
        or item.get("time")
        or ""
    )

    # Only include records that actually contain a water level
    if level is not None:
        try:
            level = float(level)
        except (TypeError, ValueError):
            continue

        stations.append(
            {
                "River": river,
                "Station": station,
                "Water Level (m)": level,
                "Last Updated": timestamp
            }
        )


if not stations:
    st.warning(
        "⚠️ River data was received, but no valid water-level "
        "records were found."
    )
    st.stop()


df = pd.DataFrame(stations)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

st.divider()

st.subheader("📡 Live River Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Monitoring Stations",
        len(df)
    )

with col2:
    st.metric(
        "Rivers Detected",
        df["River"].nunique()
    )

with col3:
    st.metric(
        "Highest Current Level",
        f"{df['Water Level (m)'].max():.2f} m"
    )


# --------------------------------------------------
# STATION TABLE
# --------------------------------------------------

st.divider()

st.subheader("Current River Gauge Readings")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# SELECT STATION
# --------------------------------------------------

st.divider()

st.subheader("📍 Station Details")

station_options = (
    df["Station"]
    .dropna()
    .astype(str)
    .unique()
)

selected_station = st.selectbox(
    "Select River Station",
    station_options
)

selected_rows = df[
    df["Station"].astype(str) == selected_station
]

if not selected_rows.empty:

    selected = selected_rows.iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "River",
            selected["River"]
        )

    with col2:
        st.metric(
            "Current Water Level",
            f"{selected['Water Level (m)']:.2f} m"
        )

    if selected["Last Updated"]:
        st.info(
            f"🕒 Last Updated: {selected['Last Updated']}"
        )


# --------------------------------------------------
# CHART
# --------------------------------------------------

st.divider()

st.subheader("Current River Levels")

chart_df = df.sort_values(
    "Water Level (m)",
    ascending=False
)

fig = px.bar(
    chart_df,
    x="Station",
    y="Water Level (m)",
    color="River",
    title="Latest Available Water Levels by Station"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# DATA NOTE
# --------------------------------------------------

st.caption(
    "River readings are the latest available values returned by the public ArcGIS feature service. "
    "Availability and update timing depend on the upstream monitoring service."
)
