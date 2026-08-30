import requests
import streamlit as st

API_KEY = st.secrets["openweather"]["api_key"]


def get_weather(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},LK"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    try:

        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        return {

            "city": city,

            "temperature": data["main"]["temp"],

            "humidity": data["main"]["humidity"],

            "pressure": data["main"]["pressure"],

            "wind_speed": data["wind"]["speed"],

            "condition": data["weather"][0]["main"],

            "description": data["weather"][0]["description"],

            "icon": data["weather"][0]["icon"],

            "rainfall_1h": data.get(
                "rain",
                {}
            ).get(
                "1h",
                0
            )

        }

    except Exception as e:

        print(e)
        return None