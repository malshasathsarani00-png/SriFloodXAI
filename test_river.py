from utils.river_api import get_latest_river_level

data = get_latest_river_level(
    "Attanagalu Oya"
)

print(data)