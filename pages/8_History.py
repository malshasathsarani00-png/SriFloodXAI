import streamlit as st
import pandas as pd

from utils.history_manager import load_history
from utils.background import set_background

set_background()

st.title("Prediction History")

st.markdown("""
Review flood-risk predictions previously generated and saved by SriFloodXAI.
These records represent model outputs from the prototype and are not official
flood-warning records.
""")

# =====================================
# LOAD HISTORY
# =====================================

try:
    history_df = load_history()
except Exception as exc:
    st.error(f"Could not load prediction history: {exc}")
    st.stop()

if history_df is None or history_df.empty:
    st.info(
        "No saved predictions are available yet. "
        "Run a flood-risk prediction to create a history record."
    )
    st.stop()

df = history_df.copy()

# =====================================
# VALIDATE / NORMALIZE
# =====================================

required_columns = {"district", "risk_level", "confidence"}
missing_columns = required_columns.difference(df.columns)

if missing_columns:
    st.error(
        "Prediction history is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

df["district"] = df["district"].fillna("Unknown").astype(str)
df["risk_level"] = df["risk_level"].fillna("Unknown").astype(str).str.upper()
df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")

# Find a likely timestamp column without assuming one exact history schema.
timestamp_column = next(
    (
        col for col in [
            "timestamp",
            "datetime",
            "date_time",
            "created_at",
            "date",
        ]
        if col in df.columns
    ),
    None,
)

if timestamp_column:
    parsed_time = pd.to_datetime(df[timestamp_column], errors="coerce")
    if parsed_time.notna().any():
        df["_parsed_time"] = parsed_time
        df = df.sort_values("_parsed_time", ascending=False)

# =====================================
# FILTERS
# =====================================

st.divider()
st.subheader("Filter Prediction Records")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    district_options = ["All"] + sorted(
        df["district"].dropna().unique().tolist()
    )
    selected_district = st.selectbox(
        "District",
        district_options,
    )

with filter_col2:
    preferred_order = ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    available_risks = df["risk_level"].dropna().unique().tolist()

    ordered_risks = [
        risk for risk in preferred_order
        if risk in available_risks
    ]
    ordered_risks += sorted(
        risk for risk in available_risks
        if risk not in preferred_order
    )

    selected_risk = st.selectbox(
        "Risk Level",
        ["All"] + ordered_risks,
    )

filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[
        filtered_df["district"] == selected_district
    ]

if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["risk_level"] == selected_risk
    ]

# =====================================
# SUMMARY METRICS
# =====================================

st.divider()
st.subheader("History Summary")

total_predictions = len(filtered_df)
critical_count = int(
    (filtered_df["risk_level"] == "CRITICAL").sum()
)
high_count = int(
    (filtered_df["risk_level"] == "HIGH").sum()
)

valid_confidence = filtered_df["confidence"].dropna()
average_confidence = (
    valid_confidence.mean()
    if not valid_confidence.empty
    else None
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Predictions", f"{total_predictions:,}")

with col2:
    st.metric("High Risk", f"{high_count:,}")

with col3:
    st.metric("Critical Risk", f"{critical_count:,}")

with col4:
    if average_confidence is not None:
        st.metric(
            "Average Model Probability",
            f"{average_confidence:.2f}%",
        )
    else:
        st.metric("Average Model Probability", "N/A")

# =====================================
# HISTORY TABLE
# =====================================

st.divider()
st.subheader("Saved Prediction Records")

if filtered_df.empty:
    st.info("No prediction records match the selected filters.")
else:
    display_df = filtered_df.drop(
        columns=["_parsed_time"],
        errors="ignore",
    ).copy()

    # Friendly display names for common history fields.
    display_names = {
        "timestamp": "Timestamp",
        "datetime": "Date & Time",
        "date_time": "Date & Time",
        "created_at": "Created At",
        "date": "Date",
        "district": "District",
        "river": "River",
        "rainfall": "Rainfall (mm)",
        "rainfall_mm": "Rainfall (mm)",
        "river_level": "River Level (m)",
        "river_level_m": "River Level (m)",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "dmc_alert": "DMC Alert",
        "risk_level": "Risk Level",
        "confidence": "Model Probability (%)",
    }

    display_df = display_df.rename(
        columns={
            col: display_names[col]
            for col in display_df.columns
            if col in display_names
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"Showing {len(display_df):,} of "
        f"{len(history_df):,} saved prediction records."
    )

    # =====================================
    # DOWNLOAD
    # =====================================

    export_df = filtered_df.drop(
        columns=["_parsed_time"],
        errors="ignore",
    )

    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered History",
        data=csv,
        file_name="srifloodxai_prediction_history.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.caption(
    "Prediction history is stored for prototype analysis and traceability. "
    "A saved AI prediction should not be interpreted as an official DMC flood warning."
)
