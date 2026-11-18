
import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.brooklyncollegeathletics.com"
OUTPUT_FILE = "brooklyn_website_table_inventory.csv"

# Checks all the years.
SEASONS = list(range(2007, 2027))
TEAMS = {
    "Men": "mens-volleyball",
    "Women": "womens-volleyball",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchTableAudit/1.0)"
}


def clean_text(element):
    return " ".join(element.stripped_strings)


def get_section_name(table):
    """Find the nearest preceding heading for a table."""
    heading = table.find_previous(
        ["h1", "h2", "h3", "h4", "h5", "h6"]
    )
    return clean_text(heading) if heading else "Unknown"


def audit_page(gender, sport, season):
    url = f"{BASE_URL}/sports/{sport}/stats/{season}"
    print(f"\nChecking {gender} {season}: {url}")

    try:
        response = requests.get(
            url, headers=HEADERS, timeout=30
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print(f"  ERROR: {error}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    if not tables:
        print("  No HTML tables found. Needs review.")
        return [{
            "School": "Brooklyn College",
            "Season": season,
            "Gender": gender,
            "Table_Number": "",
            "Section": "",
            "Column_Headers": "",
            "Column_Count": 0,
            "Row_Count": 0,
            "Source_URL": url,
            "Audit_Status": "Needs review",
        }]

    results = []

    for number, table in enumerate(tables, start=1):
        section = get_section_name(table)

        # Capture every header row, including grouped headers.
        header_rows = table.select("thead tr")
        if not header_rows:
            header_rows = [
                row for row in table.find_all("tr")
                if row.find("th")
            ]

        headers = []
        for row in header_rows:
            cells = row.find_all(
                ["th", "td"], recursive=False
            )
            values = [clean_text(cell) for cell in cells]
            if values:
                headers.append(" | ".join(values))

        body = table.find("tbody")
        if body:
            row_count = len(body.find_all("tr"))
        else:
            row_count = len(table.find_all("tr"))
            row_count -= len(header_rows)

        results.append({
            "School": "Brooklyn College",
            "Season": season,
            "Gender": gender,
            "Table_Number": number,
            "Section": section,
            "Column_Headers": " || ".join(headers),
            "Column_Count": max(
                (
                    len(row.find_all(
                        ["th", "td"], recursive=False
                    ))
                    for row in table.find_all("tr")
                ),
                default=0,
            ),
            "Row_Count": max(row_count, 0),
            "Source_URL": url,
            "Audit_Status": "Found on website",
        })

        print(
            f"  Table {number}: {section} "
            f"({row_count} rows)"
        )

    return results


def main():
    all_results = []

    for season in SEASONS:
        for gender, sport in TEAMS.items():
            all_results.extend(
                audit_page(gender, sport, season)
            )
            time.sleep(1)

    if not all_results:
        print("No results collected.")
        return

    with open(
        OUTPUT_FILE, "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=list(all_results[0].keys())
        )
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nSaved {OUTPUT_FILE}")
    print(f"Inventory entries: {len(all_results)}")


if __name__ == "__main__":
    main()
