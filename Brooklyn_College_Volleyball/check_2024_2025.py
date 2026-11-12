import requests
from bs4 import BeautifulSoup

for year in [2024, 2025]:
    url = (
        "https://www.brooklyncollegeathletics.com/"
        f"sports/mens-volleyball/stats/{year}"
    )

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    print(f"\nYEAR: {year}")
    print("Tables:", len(tables))

    for index, table in enumerate(tables):
        rows = table.find_all("tr")

        print(
            f"Table {index}:",
            len(rows),
            "rows"
        )

        if len(rows) > 1:
            headers = [
                cell.get_text(" ", strip=True)
                for cell in rows[1].find_all(["th", "td"])
            ]
            print("Headers:", headers[:12])