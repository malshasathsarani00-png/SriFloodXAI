import requests
from datetime import datetime

URL = (
    "https://services3.arcgis.com/J7ZFXmR8rSmQ3FGf/"
    "arcgis/rest/services/gauges_2_view/FeatureServer/0/query"
)

params = {
    "where": "1=1",
    "outFields": "basin,gauge,water_level,rain_fall,EditDate",
    "returnGeometry": "false",
    "orderByFields": "EditDate DESC",
    "resultRecordCount": 2000,
    "f": "json"
}

print("Fetching latest official river gauge readings...\n")

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()

features = data.get("features", [])

latest = {}

for feature in features:
    a = feature.get("attributes", {})

    basin = a.get("basin")
    gauge = a.get("gauge")
    edit_date = a.get("EditDate")

    if not basin or not gauge or not edit_date:
        continue

    key = (basin.strip(), gauge.strip())

    if key not in latest:
        latest[key] = a


print(f"Unique river gauge stations: {len(latest)}")
print("=" * 90)

for (basin, gauge), a in sorted(latest.items()):

    level = a.get("water_level")
    rainfall = a.get("rain_fall")
    edit_date = a.get("EditDate")

    updated = datetime.fromtimestamp(
        edit_date / 1000
    ).strftime("%Y-%m-%d %H:%M:%S")

    print(f"River Basin : {basin}")
    print(f"Gauge       : {gauge}")
    print(f"Water Level : {level}")
    print(f"Rainfall    : {rainfall}")
    print(f"Updated     : {updated}")
    print("-" * 90)