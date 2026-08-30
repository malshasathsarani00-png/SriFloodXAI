import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from utils.background import set_background

set_background()

st.title("Model Development Analytics")

st.markdown("""
Analysis of the controlled dataset used for SriFloodXAI model development
and initial evaluation.
""")

st.info(
    "These visualisations describe the model-development dataset only. "
    "They do not represent historical flood frequency or district-level "
    "flood risk across Sri Lanka."
)

# =====================================
# LOAD DATA
# =====================================

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "historical_flood_events.csv"
)

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error("Model-development dataset could not be found.")
    st.stop()
except Exception as exc:
    st.error(f"Could not load the model-development dataset: {exc}")
    st.stop()

required_columns = {
    "rainfall_mm",
    "river_level_m",
    "flood_occurred",
    "dmc_alert",
}

missing = required_columns.difference(df.columns)

if missing:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(sorted(missing))
    )
    st.stop()

if df.empty:
    st.warning("The model-development dataset is empty.")
    st.stop()

# Ensure core numeric fields are numeric
for column in [
    "rainfall_mm",
    "river_level_m",
    "flood_occurred",
    "dmc_alert",
]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

analysis_df = df.dropna(
    subset=[
        "rainfall_mm",
        "river_level_m",
        "flood_occurred",
        "dmc_alert",
    ]
).copy()

if analysis_df.empty:
    st.warning("No valid records are available for analysis.")
    st.stop()

analysis_df["Flood Class"] = analysis_df["flood_occurred"].map(
    {0: "Non-Flood", 1: "Flood"}
).fillna("Other")

analysis_df["DMC Indicator"] = analysis_df["dmc_alert"].map(
    {0: "No Alert", 1: "Alert"}
).fillna("Other")

# =====================================
# DATASET OVERVIEW
# =====================================

st.divider()
st.subheader("Dataset Overview")

total_records = len(analysis_df)
flood_records = int((analysis_df["flood_occurred"] == 1).sum())
non_flood_records = int((analysis_df["flood_occurred"] == 0).sum())
flood_share = (
    flood_records / total_records * 100
    if total_records else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{total_records:,}")

with col2:
    st.metric("Flood-labelled", f"{flood_records:,}")

with col3:
    st.metric("Non-flood-labelled", f"{non_flood_records:,}")

with col4:
    st.metric("Flood Class Share", f"{flood_share:.1f}%")

# =====================================
# CLASS DISTRIBUTION
# =====================================

st.divider()
st.subheader("Target Class Distribution")

class_counts = (
    analysis_df["Flood Class"]
    .value_counts()
    .rename_axis("Class")
    .reset_index(name="Records")
)

fig1 = px.bar(
    class_counts,
    x="Class",
    y="Records",
    text="Records",
    title="Flood vs Non-Flood Records",
)

st.plotly_chart(fig1, use_container_width=True)

st.caption(
    "This chart shows the class balance used in the model-development "
    "dataset. It is not a measure of real-world flood frequency."
)

# =====================================
# RAINFALL DISTRIBUTION
# =====================================

st.divider()
st.subheader("Rainfall Distribution")

fig2 = px.histogram(
    analysis_df,
    x="rainfall_mm",
    nbins=25,
    title="Distribution of Rainfall Values",
    labels={"rainfall_mm": "Rainfall (mm)"},
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================
# RIVER LEVEL DISTRIBUTION
# =====================================

st.subheader("River-Level Distribution")

fig3 = px.histogram(
    analysis_df,
    x="river_level_m",
    nbins=25,
    title="Distribution of River-Level Values",
    labels={"river_level_m": "River Level (m)"},
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================
# RAINFALL VS RIVER LEVEL
# =====================================

st.divider()
st.subheader("Rainfall and River-Level Relationship")

fig4 = px.scatter(
    analysis_df,
    x="rainfall_mm",
    y="river_level_m",
    color="Flood Class",
    title="Rainfall vs River Level by Flood Class",
    labels={
        "rainfall_mm": "Rainfall (mm)",
        "river_level_m": "River Level (m)",
    },
)

st.plotly_chart(fig4, use_container_width=True)

st.caption(
    "The scatter plot shows how rainfall and river-level values are "
    "distributed between flood-labelled and non-flood-labelled records "
    "within the controlled dataset."
)

# =====================================
# FEATURE COMPARISON
# =====================================

st.divider()
st.subheader("Feature Comparison by Flood Class")

comparison = (
    analysis_df.groupby("Flood Class", as_index=False)
    .agg(
        Average_Rainfall=("rainfall_mm", "mean"),
        Average_River_Level=("river_level_m", "mean"),
    )
)

col_left, col_right = st.columns(2)

with col_left:
    fig5 = px.bar(
        comparison,
        x="Flood Class",
        y="Average_Rainfall",
        text_auto=".2f",
        title="Average Rainfall by Flood Class",
        labels={"Average_Rainfall": "Average Rainfall (mm)"},
    )
    st.plotly_chart(fig5, use_container_width=True)

with col_right:
    fig6 = px.bar(
        comparison,
        x="Flood Class",
        y="Average_River_Level",
        text_auto=".2f",
        title="Average River Level by Flood Class",
        labels={"Average_River_Level": "Average River Level (m)"},
    )
    st.plotly_chart(fig6, use_container_width=True)

# =====================================
# DMC INDICATOR
# =====================================

st.divider()
st.subheader("DMC Alert Indicator Distribution")

dmc_counts = (
    analysis_df["DMC Indicator"]
    .value_counts()
    .rename_axis("DMC Indicator")
    .reset_index(name="Records")
)

fig7 = px.bar(
    dmc_counts,
    x="DMC Indicator",
    y="Records",
    text="Records",
    title="DMC Alert Indicator in the Model-Development Dataset",
)

st.plotly_chart(fig7, use_container_width=True)

st.caption(
    "This visualisation represents the DMC alert indicator encoded in "
    "the model-development dataset. It is not a summary of current DMC warnings."
)

# =====================================
# SAMPLE
# =====================================

st.divider()

with st.expander("View Model-Development Dataset Sample"):
    st.dataframe(
        analysis_df.head(20),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "SriFloodXAI uses this controlled dataset for prototype model development "
    "and initial evaluation. Independent real-world data would be required "
    "for operational validation."
)
