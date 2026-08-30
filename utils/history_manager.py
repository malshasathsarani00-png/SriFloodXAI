import pandas as pd
from datetime import datetime
import os


HISTORY_FILE = "history/predictions.csv"


def save_prediction(
    district,
    river,
    rainfall,
    river_level,
    temperature,
    humidity,
    dmc_alert,
    risk_level,
    confidence
):

    data = {

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "district": district,

        "river": river,

        "rainfall": rainfall,

        "river_level": river_level,

        "temperature": temperature,

        "humidity": humidity,

        "dmc_alert": dmc_alert,

        "risk_level": risk_level,

        "confidence": round(confidence, 2)

    }


    df = pd.DataFrame([data])


    if os.path.exists(HISTORY_FILE):

        old_df = pd.read_csv(HISTORY_FILE)

        df = pd.concat([old_df, df], ignore_index=True)


    df.to_csv(HISTORY_FILE, index=False)


def load_history():

    if os.path.exists(HISTORY_FILE):

        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame()