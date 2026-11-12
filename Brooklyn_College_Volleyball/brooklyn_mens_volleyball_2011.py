import requests
import csv
from bs4 import BeautifulSoup

url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2011/HTML/TEAMCUME.HTM"

response = requests.get(url, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")

def get_rows(table):
    rows = []

    for tr in table.find_all("tr"):
        cells = [
            cell.get_text(" ", strip=True)
            for cell in tr.find_all(["td", "th"], recursive=False)
        ]
        rows.append(cells)

    return rows

offense_rows = get_rows(tables[8])
defense_rows = get_rows(tables[9])

print("Offensive table rows:", len(offense_rows))
print("Defensive table rows:", len(defense_rows))

print("First offensive player:", offense_rows[2])
print("First defensive player:", defense_rows[2])

# Check which rows contain players
print("\nOFFENSIVE ROWS:")
for row in offense_rows[2:]:
    print(row[0], "|", row[1], "|", len(row), "columns")

print("\nDEFENSIVE ROWS:")
for row in defense_rows[2:]:
    print(row[0], "|", row[1], "|", len(row), "columns")

# Keep only actual players
offense_players = {
    row[0]: row
    for row in offense_rows[2:]
    if row[0].isdigit() and len(row) == 14
}

defense_players = {
    row[0]: row
    for row in defense_rows[2:]
    if row[0].isdigit() and len(row) == 12
}

# Combine offensive and defensive statistics
combined_player_rows = []

for number, offense in offense_players.items():
    defense = defense_players.get(number)

    if defense is None:
        print("Missing defensive stats for:", number)
        continue

    combined_player_rows.append([
        2011,
        "Men's Volleyball",
        *offense,
        offense[2],
        *defense[3:]
    ])

print("Combined players:", len(combined_player_rows))
print("Columns per player:", len(combined_player_rows[0]))

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

with open("brooklyn_mens_volleyball_2011_individual_stats.csv",
          "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(individual_headers)
    writer.writerows(combined_player_rows)

print("2011 individual statistics CSV saved!")

# Extract 2011 team statistics
team_table_rows = get_rows(tables[2])

team_rows = []
category = ""

categories = {
    "ATTACK", "SET", "SERVE",
    "SERVE RECEPTIONS", "DEFENSE",
    "BLOCKING", "BALL HANDLING ERRORS"
}

for row in team_table_rows[1:]:
    if row[0].strip() == "ATTENDANCE":
        break
    if not row:
        continue

    stat_name = row[0].strip()

    if stat_name in categories:
        category = stat_name

        if len(row) < 3 or not row[1].strip():
            continue

    if len(row) < 3 or not row[1].strip() or not row[2].strip():
        continue

    if stat_name == "Errors":
        if category == "ATTACK":
            stat_name = "Attack Errors"
        elif category == "SERVE":
            stat_name = "Service Errors"
        elif category == "SERVE RECEPTIONS":
            stat_name = "Reception Errors"

    team_rows.append([
        2011,
        "Men's Volleyball",
        category,
        stat_name,
        row[1],
        row[2]
    ])

print("2011 team statistic rows:", len(team_rows))
print("Last five rows:", team_rows[-5:])

team_headers = [
    "Season", "Team", "Category",
    "Statistic", "Brooklyn", "Opponents"
]

with open("brooklyn_mens_volleyball_2011_team_stats.csv",
          "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(team_headers)
    writer.writerows(team_rows)

print("2011 team statistics CSV saved!")

print("\n2011 PAGE LINKS:")

for link in soup.find_all("a", href=True):
    text = link.get_text(" ", strip=True)
    href = link["href"]

    if text:
        print(text, "|", href)

match_url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2011/HTML/teamgbg.htm"

match_response = requests.get(match_url, timeout=20)
match_response.raise_for_status()

match_soup = BeautifulSoup(match_response.text, "html.parser")
match_tables = match_soup.find_all("table")

print("\nMATCH TABLES:", len(match_tables))

for i, table in enumerate(match_tables):
    rows = get_rows(table)
    print("Table", i, "| Rows:", len(rows))
    print("First rows:", rows[:3])

# Extract 2011 match statistics
match_rows = get_rows(match_tables[2])

match_headers = [
    "Season", "Team", "Date", "Opponent",
    "Conference", "Result", "Match Score",
    "Set Scores", "Attendance"
]

combined_match_rows = []

for row in match_rows[2:]:
    if len(row) != 9:
        continue

    conference = "Yes" if row[0] == "*" else "No"

    combined_match_rows.append([
        2011,
        "Men's Volleyball",
        row[1] if "2011" in row[1] else row[1] + ", 2011",
        row[2],
        conference,
        row[3],
        row[4],
        row[5],
        row[8]
    ])

with open("brooklyn_mens_volleyball_2011_match_stats.csv",
          "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(match_headers)
    writer.writerows(combined_match_rows)

print("2011 match statistics CSV saved!")
print("2011 matches:", len(combined_match_rows))