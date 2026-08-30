import pandas as pd
import random

districts = [
    ("Colombo", "Kelani Ganga"),
    ("Gampaha", "Attanagalu Oya"),
    ("Ratnapura", "Kalu Ganga"),
    ("Matara", "Nilwala Ganga"),
    ("Galle", "Gin Ganga"),
    ("Kandy", "Mahaweli Ganga"),
    ("Kurunegala", "Deduru Oya"),
    ("Kalutara", "Kalu Ganga"),
    ("Badulla", "Mahaweli Ganga"),
    ("Jaffna", "None")
]

data = []

for _ in range(500):

    district, river = random.choice(districts)

    rainfall = random.randint(0, 250)

    river_level = round(random.uniform(0, 8), 1)

    temperature = random.randint(24, 33)

    humidity = random.randint(60, 95)

    dmc_alert = 1 if rainfall > 100 else 0

    flood_occurred = 1 if (
        rainfall > 120
        or river_level > 5
        or dmc_alert == 1
    ) else 0

    data.append([

        district,
        river,
        rainfall,
        river_level,
        dmc_alert,
        temperature,
        humidity,
        flood_occurred

    ])

df = pd.DataFrame(

    data,

    columns=[

        "district",
        "river",
        "rainfall_mm",
        "river_level_m",
        "dmc_alert",
        "temperature",
        "humidity",
        "flood_occurred"

    ]

)

df.to_csv(

    "data/historical_flood_events.csv",

    index=False

)

print("Dataset Created Successfully!")
print(df.head())
