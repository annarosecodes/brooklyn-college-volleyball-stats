from pathlib import Path
import csv
import json
import re
import time

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent

RAW_DIR = ROOT / "raw_all_tables"
AUDIT_DIR = ROOT / "collection_audit"

RAW_DIR.mkdir(exist_ok=True)
AUDIT_DIR.mkdir(exist_ok=True)

# Start with men. Women will use the same script later.
GENDERS = ["women"]

# Completed seasons only. Exclude 2021 and 2026.
MEN_YEARS = list(range(2013, 2021)) + list(range(2022, 2026))

# These will be used when we expand to women.
WOMEN_YEARS = list(range(2012, 2020)) + list(range(2021, 2026))

BASE_URL = "https://www.brooklyncollegeathletics.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AcademicStatsResearch/1.0)"
}

session = requests.Session()
session.headers.update(HEADERS)

audit_rows = []


def get_page(url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_table(table):
    """
    Preserve every HTML table row and cell.

    Each cell retains:
    - text
    - HTML tag type (th or td)
    - colspan
    - rowspan

    This avoids losing grouped headers.
    """
    extracted = []

    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"], recursive=False)

        if not cells:
            continue

        row = []

        for cell in cells:
            row.append({
                "text": cell.get_text(" ", strip=True),
                "tag": cell.name,
                "colspan": cell.get("colspan", "1"),
                "rowspan": cell.get("rowspan", "1"),
            })

        extracted.append(row)

    return extracted


def find_table_context(table):
    """
    Collect nearby headings and text as context.
    The scope remains unverified until we can
    reliably identify Overall vs Conference.
    """
    context = []

    for element in table.find_all_previous(
        ["h1", "h2", "h3", "h4", "h5", "h6"],
        limit=5
    ):
        text = element.get_text(" ", strip=True)

        if text:
            context.append(text)

    return " | ".join(reversed(context))


def save_table_csv(rows, output_path):
    """
    Store each original HTML row as a CSV row.

    Cell metadata is kept as JSON in each column,
    preserving headers and colspan/rowspan.
    """
    max_cells = max((len(row) for row in rows), default=0)

    columns = [
        f"Cell_{i}" for i in range(1, max_cells + 1)
    ]

    with output_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(["HTML_Row"] + columns)

        for index, row in enumerate(rows, start=1):
            encoded = [
                json.dumps(cell, ensure_ascii=False)
                for cell in row
            ]

            writer.writerow(
                [index] + encoded + [""] * (max_cells - len(encoded))
            )


def scrape_season(gender, year):
    sport = "mens-volleyball" if gender == "men" else "womens-volleyball"

    url = f"{BASE_URL}/sports/{sport}/stats/{year}"

    print(f"\nScraping {gender.upper()} {year}")
    print(url)

    try:
        soup = get_page(url)
        tables = soup.find_all("table")

        print(f"Found {len(tables)} HTML tables")

        season_dir = RAW_DIR / gender / str(year)
        season_dir.mkdir(parents=True, exist_ok=True)

        for table_number, table in enumerate(tables, start=1):

            rows = extract_table(table)
            context = find_table_context(table)

            output_name = f"table_{table_number:02d}.csv"
            output_path = season_dir / output_name

            save_table_csv(rows, output_path)

            header_rows = sum(
                1 for row in rows
                if any(cell["tag"] == "th" for cell in row)
            )

            data_rows = sum(
                1 for row in rows
                if any(cell["tag"] == "td" for cell in row)
            )

            audit_rows.append({
                "School": "Brooklyn College",
                "Season": year,
                "Gender": gender,
                "Table_Number": table_number,
                "Context": context,
                "HTML_Rows": len(rows),
                "Header_Rows": header_rows,
                "Data_Rows": data_rows,
                "Scope": "Unverified",
                "SourceURL": url,
                "SavedFile": str(output_path.relative_to(ROOT)),
                "Status": "Saved",
            })

            print(
                f"  Table {table_number:02d}: "
                f"{len(rows)} rows saved"
            )

        if len(tables) != 15:
            print(
                f"  WARNING: Expected 15 HTML tables "
                f"based on earlier inventory; found {len(tables)}"
            )

    except Exception as error:
        print(f"ERROR: {error}")

        audit_rows.append({
            "School": "Brooklyn College",
            "Season": year,
            "Gender": gender,
            "Table_Number": "",
            "Context": "",
            "HTML_Rows": "",
            "Header_Rows": "",
            "Data_Rows": "",
            "Scope": "",
            "SourceURL": url,
            "SavedFile": "",
            "Status": f"ERROR: {error}",
        })


def main():
    for gender in GENDERS:

        years = MEN_YEARS if gender == "men" else WOMEN_YEARS

        for year in years:
            scrape_season(gender, year)
            time.sleep(1)

    audit_path = AUDIT_DIR / "raw_table_collection_audit.csv"

    fields = [
        "School",
        "Season",
        "Gender",
        "Table_Number",
        "Context",
        "HTML_Rows",
        "Header_Rows",
        "Data_Rows",
        "Scope",
        "SourceURL",
        "SavedFile",
        "Status",
    ]

    with audit_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(audit_rows)

    saved = sum(row["Status"] == "Saved" for row in audit_rows)
    errors = sum(row["Status"] != "Saved" for row in audit_rows)

    print("\n" + "=" * 65)
    print("RAW TABLE COLLECTION COMPLETE")
    print(f"Tables saved: {saved}")
    print(f"Errors: {errors}")
    print(f"Audit: {audit_path}")
    print("=" * 65)


if __name__ == "__main__":
    main()