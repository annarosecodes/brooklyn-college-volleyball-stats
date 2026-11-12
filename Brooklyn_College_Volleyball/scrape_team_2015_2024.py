import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024]

OUTPUT = Path(__file__).resolve().parent

for year in YEARS:
    print(f"\nProcessing {year} team statistics...")

    try:
        url = (
            "https://www.brooklyncollegeathletics.com/"
            f"sports/mens-volleyball/stats/{year}"
        )

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")

        if len(tables) != 15:
            raise ValueError(f"Expected 15 tables, found {len(tables)}")

        table = tables[0]
        category = ""
        data = []

        for tr in table.find_all("tr"):
            cells = [
                cell.get_text(" ", strip=True)
                for cell in tr.find_all(["th", "td"])
            ]

            if not cells:
                continue

            # Skip the column header
            if cells[0] == "Statistic":
                continue

            # A single cell identifies a category
            if len(cells) == 1:
                category = cells[0]
                continue

            # Statistic rows contain Brooklyn and opponent values
            if len(cells) == 3:
                statistic, brooklyn, opponents = cells

                if not category:
                    raise ValueError(
                        f"Statistic has no category: {statistic}"
                    )

                data.append([
                    year,
                    "Men's Volleyball",
                    category,
                    statistic,
                    brooklyn,
                    opponents
                ])

            else:
                raise ValueError(
                    f"Unexpected table row: {cells}"
                )

        if not data:
            raise ValueError("No team statistics found")

        filename = (
            OUTPUT /
            f"brooklyn_mens_volleyball_{year}_team_stats.csv"
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Season",
                "Team",
                "Category",
                "Statistic",
                "Brooklyn",
                "Opponents"
            ])

            writer.writerows(data)

        print(f"  Saved team: {len(data)} statistics")

    except (requests.RequestException, ValueError, IndexError) as error:
        print(f"  REVIEW NEEDED: {error}")

print("\nTeam-summary scraping finished!")