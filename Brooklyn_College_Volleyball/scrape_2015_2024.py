import csv
import re
from pathlib import Path

from numpy import record
import requests
from bs4 import BeautifulSoup

BASE = "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/"
OUTPUT = Path(__file__).resolve().parent

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024]


def get_rows(table):
    return [
        [cell.get_text(" ", strip=True)
         for cell in tr.find_all(["th", "td"])]
        for tr in table.find_all("tr")
    ]


def save_csv(year, kind, headers, rows):
    filename = OUTPUT / f"brooklyn_mens_volleyball_{year}_{kind}_stats.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"  Saved {kind}: {len(rows)} rows")


def scrape_year(year):
    response = requests.get(BASE + str(year), timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    if len(tables) != 15:
        raise ValueError(f"Expected 15 tables, found {len(tables)}")

    # Offensive and defensive player statistics
    offense = get_rows(tables[1])
    defense = get_rows(tables[2])

    offense_headers = ["Jersey"] + offense[1] + ["Bio Link"]
    defense_headers = ["Jersey"] + defense[1] + ["Bio Link"]

    def player_dict(rows, headers):
        players = {}

        for row in rows[2:]:
            if len(row) != len(headers):
                continue

            record = dict(zip(headers, row))
            jersey = record["Jersey"].strip()

            if not jersey.isdigit():
                continue

            key = (
                jersey,
                record["Player"].strip(),
                record["SP"].strip()
            )

            if key in players:
                raise ValueError(f"Duplicate player record: {key}")

            players[key] = record

        return players

    offense_players = player_dict(offense, offense_headers)
    defense_players = player_dict(defense, defense_headers)

    if not offense_players:
        raise ValueError("No players found")

    if set(offense_players) != set(defense_players):
        raise ValueError("Offense and defense player lists differ")

    # Preserve all columns, including the newer statistics
    individual_headers = (
        ["Season", "Team"]
        + offense_headers
        + ["Defense_" + h for h in defense_headers
           if h not in ("Jersey", "Player", "SP", "Bio Link")]
    )

    individual_rows = []

    for key, player in offense_players.items():
        defensive = defense_players[key]
        jersey = key[0]

        name = player["Player"]
        separator = f" {jersey} "

        if separator in name:
            name = name.split(separator, 1)[0]

        player["Player"] = name.strip()

        individual_rows.append(
            [year, "Men's Volleyball"]
            + [player[h] for h in offense_headers]
            + [defensive[h] for h in defense_headers
               if h not in ("Jersey", "Player", "SP", "Bio Link")]
        )

    # Brooklyn match-by-match performance statistics
    matches = get_rows(tables[5])
    match_headers = matches[0]

    if "Date" not in match_headers or "Opponent" not in match_headers:
        raise ValueError("Unexpected match table headers")

    match_rows = []

    for row in matches[1:]:
        if len(row) != len(match_headers):
            continue

        record = dict(zip(match_headers, row))

        # Keep actual matches, not season totals
        if not re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}",
                            record["Date"].strip()):
            continue

        match_rows.append(
            [year, "Men's Volleyball"] + row
        )

    if not match_rows:
        raise ValueError("No matches found")

    # Save only after both datasets pass checks
    save_csv(year, "individual", individual_headers, individual_rows)
    save_csv(
        year, "match",
        ["Season", "Team"] + match_headers,
        match_rows
    )


for year in YEARS:
    print(f"\nProcessing {year}...")

    try:
        scrape_year(year)
    except (requests.RequestException, ValueError, IndexError, KeyError) as error:
        print(f"  REVIEW NEEDED: {error}")

print("\nFinished. 2021 and team-summary CSVs still need separate handling.")