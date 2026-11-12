import requests
from bs4 import BeautifulSoup

for year in range(2012, 2025):
    url = (
        f"https://static.brooklyncollegeathletics.com/"
        f"custompages/mvball/{year}/HTML/TEAMCUME.HTM"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        print(
            year,
            "| Status:", response.status_code,
            "| Tables:", len(soup.find_all("table")),
            "| PRE blocks:", len(soup.find_all("pre"))
        )

    except requests.RequestException as error:
        print(year, "| ERROR:", error)