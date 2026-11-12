import requests
from bs4 import BeautifulSoup

url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2010/HTML/TEAMCUME.HTM"

response = requests.get(url)
print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
pre_blocks = soup.find_all("pre")

print("Number of PRE blocks:", len(pre_blocks))

for index, block in enumerate(pre_blocks):
    print("Block", index, ":", block.get_text()[:100])

# Find individual statistics table boundaries
individual_lines = pre_blocks[1].get_text().splitlines()

for index, line in enumerate(individual_lines):
    if "## Name" in line or "BROOKLYN COLLEGE...." in line:
        print("Individual table:", index, line.strip())

# Find match statistics table
match_lines = pre_blocks[4].get_text().splitlines()

for index, line in enumerate(match_lines):
    if "DATE" in line and "OPPONENT" in line:
        print("Match table header:", index, line.strip())

print("Total match block lines:", len(match_lines))

print("\n2010 OFFENSIVE PLAYERS:")

for index in range(13, 29):
    print(index, individual_lines[index])

print("\n2010 DEFENSIVE PLAYERS:")

for index in range(34, 51):
    print(index, individual_lines[index])

# Test offensive player parsing
for line in individual_lines[14:29]:
    parts = line.split()
    stats = parts[-12:]

    print(parts[0], "|", len(stats), "stats |", stats)

# Extract 2010 offensive player statistics
player_rows = []

for line in individual_lines[14:29]:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-12])
    stats = parts[-12:]

    player_rows.append([
        2010,
        "Men's Volleyball",
        jersey_number,
        player_name
    ] + stats)

print("Offensive player rows:", len(player_rows))
print("First offensive player:", player_rows[0])
print("Last offensive player:", player_rows[-1])
# Extract 2010 defensive player statistics
defense_rows = []

for line in individual_lines[35:50]:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-10])
    defense_stats = parts[-10:]

    defense_rows.append([
        2010,
        "Men's Volleyball",
        jersey_number,
        player_name
    ] + defense_stats)

print("Defensive player rows:", len(defense_rows))
print("First defensive player:", defense_rows[0])
print("Last defensive player:", defense_rows[-1])
# Combine offensive and defensive statistics
combined_player_rows = []

for player in player_rows:
    for defender in defense_rows:
        if player[2] == defender[2]:
            combined_player_rows.append(player + defender[4:])
            break

print("Combined player rows:", len(combined_player_rows))

for player in combined_player_rows:
    print(player[3], ":", len(player), "columns")

import csv

# Column headers (same as 2007–2009)
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

with open("brooklyn_mens_volleyball_2010_individual_stats.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(individual_headers)
    writer.writerows(combined_player_rows)

print("2010 individual statistics CSV saved!")
# Inspect the 2010 team statistics
team_lines = pre_blocks[0].get_text().splitlines()

for index, line in enumerate(team_lines):
    if line.strip():
        print(index, line)

# Extract 2010 team statistics
import re

team_rows = []

for line in team_lines[11:37]:
    match = re.match(r"^\s*(.*?)\.{2,}\s+(\S+)\s+(\S+)\s*$", line)

    if match:
        stat_name, bc_value, opp_value = match.groups()

        team_rows.append([
            2010,
            "Men's Volleyball",
            stat_name.strip(),
            bc_value,
            opp_value
        ])

print("Team statistic rows:", len(team_rows))

for row in team_rows:
    print(row)



# Clarify repeated statistic names
team_rows[1][2] = "Attack Errors"
team_rows[8][2] = "Service Errors"
team_rows[10][2] = "Reception Errors"

# Save team statistics
with open("brooklyn_mens_volleyball_2010_team_stats.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Season",
        "Team",
        "Category",
        "Statistic",
        "Brooklyn",
        "Opponents"
    ])

    category = ""

    for row in team_rows:
        if row[2] == "Kills":
            category = "ATTACK"
        elif row[2] == "Assists":
            category = "SET"
        elif row[2] == "Aces":
            category = "SERVE"
        elif row[2] == "Reception Errors":
            category = "SERVE RECEPTIONS"
        elif row[2] == "Digs":
            category = "DEFENSE"
        elif row[2] == "Block Solo":
            category = "BLOCKING"
        elif row[2] == "BALL HANDLING ERRORS":
            category = "BALL HANDLING ERRORS"

        writer.writerow([
            row[0],
            row[1],
            category,
            row[2],
            row[3],
            row[4]
        ])

print("2010 team statistics CSV saved!")

# Inspect 2010 match statistics
print("\n2010 MATCH STATISTICS:")

for index in range(76, len(match_lines)):
    print(index, match_lines[index])

# Test 2010 match parsing
for line in match_lines[78:98]:
    parts = line.split()
    print(parts)

# Extract 2010 match statistics
match_rows = []

for line in match_lines[78:98]:
    parts = line.split()

    # Check whether this is a conference match
    conference = "Yes" if parts[0] == "*" else "No"

    if conference == "Yes":
        parts = parts[1:]

    # Extract the result and scores from the end
    result = parts[-4]
    match_score = parts[-3]
    set_scores = parts[-2]
    attendance = parts[-1]

    # Extract the date
    if "/" in parts[0]:
        date = parts[0]
        opponent_parts = parts[1:-4]
    else:
        date = " ".join(parts[:2]) + " 2010"
        opponent_parts = parts[2:-4]

    opponent = " ".join(opponent_parts)

    match_rows.append([
        2010,
        "Men's Volleyball",
        date,
        opponent,
        conference,
        result,
        match_score,
        set_scores,
        attendance
    ])

print("2010 match rows:", len(match_rows))
print("First match:", match_rows[0])
print("Last match:", match_rows[-1])
# Save 2010 match statistics
match_headers = [
    "Season",
    "Team",
    "Date",
    "Opponent",
    "Conference",
    "Result",
    "Match Score",
    "Set Scores",
    "Attendance"
]

with open("brooklyn_mens_volleyball_2010_match_stats.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(match_headers)
    writer.writerows(match_rows)

print("2010 match statistics CSV saved!")