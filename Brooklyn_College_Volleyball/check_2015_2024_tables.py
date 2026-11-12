import requests
from bs4 import BeautifulSoup

for year in range(2015, 2025):
    url = (
        "https://www.brooklyncollegeathletics.com/"
        f"sports/mens-volleyball/stats/{year}"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")

        if len(tables) < 8:
            print(year, "| CHECK MANUALLY | Tables:", len(tables))
            continue

        player_headers = [
            cell.get_text(" ", strip=True)
            for cell in tables[1].find_all("tr")[1].find_all(["th", "td"])
        ]

        defense_headers = [
            cell.get_text(" ", strip=True)
            for cell in tables[2].find_all("tr")[1].find_all(["th", "td"])
        ]

        matches = len(tables[5].find_all("tr")) - 2

        valid = (
            "Player" in player_headers
            and "SP" in player_headers
            and "DIG" in defense_headers
            and matches > 0
        )

        print(
            year,
            "| Tables:", len(tables),
            "| Players:", len(tables[1].find_all("tr")) - 2,
            "| Match rows (approx):", matches,
            "| Structure:", "MATCH" if valid else "REVIEW"
        )

    except (requests.RequestException, IndexError) as error:
        print(year, "| ERROR:", error)