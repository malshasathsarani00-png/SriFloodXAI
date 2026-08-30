import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


DMC_URL = (
    "https://www.dmc.gov.lk/index.php"
    "?Itemid=279&lang=en&option=com_dmcreports"
    "&report_type_id=8&view=reports"
)


def get_live_dmc_warnings():
    try:
        response = requests.get(DMC_URL, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        return text

    except Exception as e:
        print("DMC error:", e)
        return None


def check_dmc_alert(river_name):
    text = get_live_dmc_warnings()

    if not text:
        return {
            "active": 0,
            "message": "DMC data unavailable"
        }

    river_search = river_name.lower()

    # Allow common river-name variations
    aliases = {
        "kelani ganga": ["kelani ganga", "kelani river"],
        "gin ganga": ["gin ganga", "gin river"],
        "kalu ganga": ["kalu ganga", "kalu river", "kuda ganga"],
        "nilwala ganga": ["nilwala ganga", "nilwala river"],
        "mahaweli ganga": ["mahaweli ganga", "mahaweli river", "mahaweli basin"],
        "deduru oya": ["deduru oya", "deduru oya basin"],
    }

    search_terms = aliases.get(
        river_search,
        [river_search]
    )

    found = any(
        term in text.lower()
        for term in search_terms
    )

    if not found:
        return {
            "active": 0,
            "message": f"No DMC flood warning found for {river_name}"
        }

    # Look for recent dates only
    today = datetime.now().date()

    for days_back in range(0, 4):
        date_to_check = today - timedelta(days=days_back)

        formats = [
            date_to_check.strftime("%Y-%m-%d"),
            date_to_check.strftime("%Y.%m.%d"),
            date_to_check.strftime("%d-%m-%Y"),
        ]

        if any(date in text for date in formats):
            return {
                "active": 1,
                "message": f"Recent DMC flood warning detected for {river_name}"
            }

    return {
        "active": 0,
        "message": (
            f"DMC warning record found for {river_name}, "
            "but no recent warning detected."
        )
    }