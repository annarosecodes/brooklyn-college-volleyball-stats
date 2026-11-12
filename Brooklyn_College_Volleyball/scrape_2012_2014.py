import csv
import requests
from bs4 import BeautifulSoup

BASE = "https://static.brooklyncollegeathletics.com/custompages/mvball"
TEAM = "Men's Volleyball"

individual_headers = [
    "Season", "Team", "Number", "Name",
    "GP", "MP-MS", "Kills", "Kills/Game",
    "Attack Errors", "Total Attacks", "Attack Pct",
    "Assists", "Assists/Game", "Service Aces",
    "Service Aces/Game", "Service Errors",
    "Games", "Reception Errors", "Digs", "Digs/Game",
    "Block Solo", "Block Assist", "Total Blocks",
    "Blocks/Game", "Block Errors", "Ball Handling Errors"
]

team_headers = [
    "Season", "Team", "Category",
    "Statistic", "Brooklyn", "Opponents"
]

match_headers = [
    "Season", "Team", "Date", "Opponent",
    "Conference", "Result", "Match Score",
    "Set Scores", "Attendance"
]


def get_rows(table):
    rows = []
    for tr in table.find_all("tr"):
        cells = [
            cell.get_text(" ", strip=True)
            for cell in tr.find_all(["td", "th"], recursive=False)
        ]
        rows.append(cells)
    return rows


def fetch_tables(year, filename):
    url = f"{BASE}/{year}/HTML/{filename}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("table")


def save_csv(year, kind, headers, rows):
    filename = f"brooklyn_mens_volleyball_{year}_{kind}_stats.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"  Saved {filename}: {len(rows)} rows")


def scrape_year(year):
    print(f"\nProcessing {year}...")

    tables = fetch_tables(year, "TEAMCUME.HTM")

    if len(tables) < 10:
        raise ValueError("Unexpected cumulative statistics page format")

    # Individual statistics
    offense_rows = get_rows(tables[8])
    defense_rows = get_rows(tables[9])

    offense_players = {
        row[0]: row
        for row in offense_rows[2:]
        if len(row) == 14 and row[0].isdigit()
    }

    defense_players = {
        row[0]: row
        for row in defense_rows[2:]
        if len(row) == 12 and row[0].isdigit()
    }

    if set(offense_players) != set(defense_players):
        raise ValueError("Offensive and defensive player lists differ")

    individual_rows = []

    for number, offense in offense_players.items():
        defense = defense_players[number]

        individual_rows.append([
            year, TEAM,
            *offense,
            offense[2],
            *defense[3:]
        ])

    if not individual_rows or any(len(row) != 26 for row in individual_rows):
        raise ValueError("Invalid individual statistics")

    # Team statistics
    categories = {
        "ATTACK", "SET", "SERVE",
        "SERVE RECEPTIONS", "DEFENSE",
        "BLOCKING", "BALL HANDLING ERRORS"
    }

    team_rows = []
    category = ""

    for row in get_rows(tables[2])[1:]:
        if not row:
            continue

        stat_name = row[0].strip()

        if stat_name == "ATTENDANCE":
            break

        if stat_name in categories:
            category = stat_name

        if len(row) < 3 or not row[1].strip() or not row[2].strip():
            continue

        if not category:
            continue

        if stat_name == "Errors":
            if category == "ATTACK":
                stat_name = "Attack Errors"
            elif category == "SERVE":
                stat_name = "Service Errors"
            elif category == "SERVE RECEPTIONS":
                stat_name = "Reception Errors"

        team_rows.append([
            year, TEAM, category,
            stat_name, row[1], row[2]
        ])

    if not team_rows:
        raise ValueError("No team statistics found")

    # Match statistics
    match_tables = fetch_tables(year, "teamgbg.htm")

    if len(match_tables) < 3:
        raise ValueError("Unexpected match results page format")

    match_rows = []

    for row in get_rows(match_tables[2])[2:]:
        if len(row) != 9:
            continue

        date = row[1].strip()

        if str(year) not in date:
            date += f", {year}"

        match_rows.append([
            year,
            TEAM,
            date,
            row[2],
            "Yes" if row[0] == "*" else "No",
            row[3],
            row[4],
            row[5],
            row[8]
        ])

    if not match_rows:
        raise ValueError("No match results found")

    if any(len(row) != 9 for row in match_rows):
        raise ValueError("Invalid match statistics")

    # Save only after all three datasets pass basic checks
    save_csv(year, "individual", individual_headers, individual_rows)
    save_csv(year, "team", team_headers, team_rows)
    save_csv(year, "match", match_headers, match_rows)


for year in range(2012, 2015):
    try:
        scrape_year(year)
    except (requests.RequestException, ValueError, IndexError) as error:
        print(f"  ERROR for {year}: {error}")