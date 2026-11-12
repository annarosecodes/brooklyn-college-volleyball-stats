import requests
from bs4 import BeautifulSoup

duplicates = {
    2016: "5",
    2022: "13",
    2023: "11"
}

for year, jersey in duplicates.items():
    url = (
        "https://www.brooklyncollegeathletics.com/"
        f"sports/mens-volleyball/stats/{year}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    print(f"\n===== {year}: JERSEY {jersey} =====")

    for table_index in [1, 2]:
        print(f"\nTABLE {table_index}")

        for row in tables[table_index].find_all("tr")[2:]:
            cells = [
                cell.get_text(" ", strip=True)
                for cell in row.find_all(["th", "td"])
            ]

            if cells and cells[0].strip() == jersey:
                print(cells)