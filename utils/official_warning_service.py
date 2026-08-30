import requests
import re
from io import BytesIO
from pypdf import PdfReader

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


DMC_URL = (
    "https://www.dmc.gov.lk/index.php"
    "?Itemid=277"
    "&lang=en"
    "&limit=100"
    "&limitstart=0"
    "&option=com_dmcreports"
    "&report_type_id=6"
    "&view=reports"
)

BASE_URL = "https://www.dmc.gov.lk"


RIVER_ALIASES = {
    "Kelani Ganga": [
        "kelani river",
        "kelani ganga",
        "kelani basin",
    ],

    "Kalu Ganga": [
        "kalu river",
        "kalu ganga",
        "kalu river basin",
        "kuda ganga",
    ],

    "Gin Ganga": [
        "gin ganga",
        "gin river",
        "gin ganga basin",
    ],

    "Nilwala Ganga": [
        "nilwala ganga",
        "nilwala river",
        "nilwala basin",
    ],

    "Mahaweli Ganga": [
        "mahaweli river",
        "mahaweli ganga",
        "mahaweli basin",
    ],

    "Deduru Oya": [
        "deduru oya",
        "deduru oya basin",
    ],

    "Attanagalu Oya": [
        "attanagalu oya",
        "aththanagalu oya",
        "attanagalu basin",
        "aththanagalu basin",
    ],
}


def _matches_river(title, river_name):

    title_lower = title.lower()

    search_terms = RIVER_ALIASES.get(
        river_name,
        [river_name.lower()]
    )

    return any(
        term in title_lower
        for term in search_terms
    )


def get_current_official_warning(
    river_name,
    max_age_hours=72
):

    try:

        response = requests.get(
            DMC_URL,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        events = []

        for row in soup.find_all("tr"):

            cells = row.find_all("td")

            if len(cells) < 3:
                continue

            title = cells[0].get_text(
                " ",
                strip=True
            )

            date_text = cells[1].get_text(
                " ",
                strip=True
            )

            time_text = cells[2].get_text(
                " ",
                strip=True
            )

            title_lower = title.lower()

            # We only care about flood warnings
            # and withdrawal notices.
            if (
                "flood warning" not in title_lower
                and "withdrawal" not in title_lower
            ):
                continue

            if not _matches_river(
                title,
                river_name
            ):
                continue

            try:

                published_at = datetime.strptime(
                    f"{date_text} {time_text}",
                    "%Y-%m-%d %H:%M"
                )

            except ValueError:
                continue

            link = None

            a_tag = row.find(
                "a",
                href=True
            )

            if a_tag:
                link = urljoin(
                    BASE_URL,
                    a_tag["href"]
                )

            events.append({
                "title": title,
                "published_at": published_at,
                "url": link
            })


        if not events:

            return {
                "active": False,
                "river": river_name,
                "message": (
                    "No official DMC flood warning "
                    "record was found for this river."
                ),
                "warning": None
            }


        # Newest event first
        events.sort(
            key=lambda x: x["published_at"],
            reverse=True
        )

        latest = events[0]

        age_hours = (
            datetime.now()
            - latest["published_at"]
        ).total_seconds() / 3600


        # Latest event is a withdrawal
        if "withdrawal" in latest["title"].lower():

            return {
                "active": False,
                "river": river_name,
                "message": (
                    "The latest official DMC event "
                    "is a flood-warning withdrawal."
                ),
                "warning": latest
            }


        # Warning is too old to call current
        if age_hours > max_age_hours:

            return {
                "active": False,
                "river": river_name,
                "message": (
                    "An older official flood warning "
                    "exists, but it is not treated "
                    "as a current warning."
                ),
                "warning": latest
            }


        return {
            "active": True,
            "river": river_name,
            "message": (
                "A recent official DMC flood warning "
                "was detected."
            ),
            "warning": latest
        }


    except Exception as e:

        return {
            "active": False,
            "river": river_name,
            "message": (
                "Official DMC warning data "
                f"could not be checked: {e}"
            ),
            "warning": None
        }

def extract_warned_areas_from_text(text):

    if not text:
        return []

    clean_text = " ".join(text.split())

    patterns = [
        r"Divisional Secretariat Divisions?\s*:\s*([^.]+)",
        r"DS Divisions?\s*:\s*([^.]+)",
        r"low[- ]lying areas? (?:associated with .*? )?located within ([^.]+)"
    ]

    found = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            clean_text,
            flags=re.IGNORECASE
        )

        for match in matches:

            parts = re.split(
                r",|\band\b|&",
                match,
                flags=re.IGNORECASE
            )

            for part in parts:

                area = part.strip(" .:-")

                if (
                    area
                    and len(area) > 2
                    and area not in found
                ):
                    found.append(area)

    return found

def extract_text_from_pdf_url(pdf_url):

    if not pdf_url:
        return ""

    try:

        response = requests.get(
            pdf_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        pdf_file = BytesIO(
            response.content
        )

        reader = PdfReader(
            pdf_file
        )

        text_parts = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text_parts.append(
                    page_text
                )

        return "\n".join(
            text_parts
        )

    except Exception as e:

        print(
            "PDF extraction error:",
            e
        )

        return ""


def get_warned_areas_from_warning(warning):

    if not warning:
        return []

    pdf_url = warning.get("url")

    if not pdf_url:
        return []

    text = extract_text_from_pdf_url(
        pdf_url
    )

    areas = extract_warned_areas_from_text(
        text
    )

    return areas

def get_latest_warning_for_testing(river_name):

    try:
        response = requests.get(
            DMC_URL,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for row in soup.find_all("tr"):

            cells = row.find_all("td")

            if len(cells) < 3:
                continue

            title = cells[0].get_text(
                " ",
                strip=True
            )

            if "flood warning" not in title.lower():
                continue

            if not _matches_river(
                title,
                river_name
            ):
                continue

            link_tag = row.find(
                "a",
                href=True
            )

            if not link_tag:
                continue

            return {
                "title": title,
                "url": urljoin(
                    BASE_URL,
                    link_tag["href"]
                )
            }

        return None

    except Exception as e:
        print("Historical warning test error:", e)
        return None