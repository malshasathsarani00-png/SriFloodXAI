import requests
from datetime import datetime

GAUGE_URL = (
    "https://services3.arcgis.com/J7ZFXmR8rSmQ3FGf/"
    "arcgis/rest/services/gauges_2_view/FeatureServer/0/query"
)

RIVER_ALIASES = {
    "Attanagalu Oya": "Aththanagalu Oya"
}
def get_latest_river_level(river, gauge=None):
    river = RIVER_ALIASES.get(river, river)

    where = f"basin='{river}'"

    if gauge:
        where += f" AND gauge='{gauge}'"

    params = {
        "where": where,
        "outFields": (
            "basin,gauge,water_level,rain_fall,"
            "EditDate,alertpull,minorpull,majorpull"
        ),
        "returnGeometry": "false",
        "orderByFields": "EditDate DESC",
        "resultRecordCount": 1,
        "f": "json"
    }

    try:
        response = requests.get(
            GAUGE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            return None

        features = data.get("features", [])

        if not features:
            return None

        a = features[0]["attributes"]

        updated = None

        if a.get("EditDate"):
            updated = datetime.fromtimestamp(
                a["EditDate"] / 1000
            ).strftime("%Y-%m-%d %H:%M:%S")

        return {
            "river": a.get("basin"),
            "station": a.get("gauge"),
            "water_level": a.get("water_level"),
            "rainfall": a.get("rain_fall"),
            "updated": updated,
            "alert_level": a.get("alertpull"),
            "minor_level": a.get("minorpull"),
            "major_level": a.get("majorpull")
        }

    except requests.RequestException:
        return None