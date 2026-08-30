import requests
import pandas as pd


API_URL = "https://lk-flood-api.vercel.app/levels/latest"


def get_live_river_levels():
    try:
        response = requests.get(API_URL, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        if isinstance(data, dict):
            if "data" in data:
                data = data["data"]
            elif "levels" in data:
                data = data["levels"]

        if not isinstance(data, list):
            return None

        return data

    except Exception as e:
        print("River API error:", e)
        return None


def get_river_level(river_name):
    data = get_live_river_levels()

    if not data:
        return None

    for item in data:

        river = (
            item.get("river_name")
            or item.get("river")
            or item.get("River")
            or ""
        )

        if river_name.lower() in river.lower():

            level = (
                item.get("water_level")
                or item.get("level")
                or item.get("WaterLevel")
            )

            station = (
                item.get("station_name")
                or item.get("station")
                or "Unknown"
            )

            timestamp = (
                item.get("timestamp")
                or item.get("datetime")
                or ""
            )

            if level is not None:
                return {
                    "river": river,
                    "station": station,
                    "water_level": float(level),
                    "timestamp": timestamp
                }

    return None


def get_river_stations():
    data = get_live_river_levels()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)