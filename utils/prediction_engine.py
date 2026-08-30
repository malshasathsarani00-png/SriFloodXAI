import pickle
import pandas as pd


with open("models/sri_flood_model.pkl", "rb") as f:
    model = pickle.load(f)


def predict_flood_risk(
    district,
    river,
    rainfall_mm,
    river_level_m,
    dmc_alert,
    temperature,
    humidity
):

    input_data = pd.DataFrame({

        "district": [district],
        "river": [river],
        "rainfall_mm": [rainfall_mm],
        "river_level_m": [river_level_m],
        "dmc_alert": [dmc_alert],
        "temperature": [temperature],
        "humidity": [humidity]

    })

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    return prediction, probability