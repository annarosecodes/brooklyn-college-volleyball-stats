import requests
from bs4 import BeautifulSoup 
import csv

url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2009/HTML/TEAMCUME.HTM"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
pre_blocks = soup.find_all("pre")
print(len(pre_blocks))

#print(pre_blocks[0].get_text()), to intitially print information


lines = pre_blocks[0].get_text().splitlines()

#Print each line of the pre block and organize formatting

in_team_stats = False
category = ""
stats_rows = []

for line in lines:
    clean_line = line.strip() 
    parts = clean_line.split()

    if "TEAM STATISTICS" in clean_line:
        in_team_stats = True
        print("Found the team statistics section!")

    if "ATTENDANCE" in clean_line:
        in_team_stats = False

    #Process team statistics lines
    if in_team_stats:
      sections = clean_line.split("..", 1)
      if len(sections) == 2:
        stat_name = sections[0]
        values = sections[1].strip().split()[1:]

       #checking for category headings
        if len(values) == 0:
          category = stat_name
          print("CATEGORY:", category)
        else:
            if len(values) == 2:
                brooklyn = values[0]
                opponents = values[1]
                if stat_name == "BALL HANDLING ERRORS":
                    category = "BALL HANDLING"
                print(category, "|", stat_name, "|", brooklyn, "|", opponents)
                stats_rows.append([2009, "Men's Volleyball", category, stat_name, brooklyn, opponents])

print("Total rows collected:", len(stats_rows))
print("First row:", stats_rows[0])

with open("brooklyn_mens_volleyball_2009_team_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Season","Team","Category", "Statistic", "Brooklyn", "Opponents"])
    writer.writerows(stats_rows)

individual_lines = pre_blocks[1].get_text().splitlines()

for index, line in enumerate(individual_lines):
    if "## Name" in line:
        print("Player table header:", index)
    if "BROOKLYN COLLEGE...." in line:
        print("Team totals:", index)

print("\n2009 OFFENSIVE PLAYERS:")
for line in individual_lines[12:25]:
    print(line)

print("\n2009 DEFENSIVE PLAYERS:")
for line in individual_lines[30:44]:
    print(line)

# 2009 INDIVIDUAL STATISTICS

player_rows = []

for line in individual_lines[13:25]:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-12])
    stats = parts[-12:]

    player_rows.append([2009, "Men's Volleyball", jersey_number, player_name] + stats)

print("Offensive player rows:", len(player_rows))

defense_rows = []

for line in individual_lines[31:43]:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-10])
    defense_stats = parts[-10:]

    defense_rows.append([2009, "Men's Volleyball", jersey_number, player_name] + defense_stats)

print("Defensive player rows:", len(defense_rows))
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

# Column headers for individual statistics
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

# Save 2009 individual statistics
with open("brooklyn_mens_volleyball_2009_individual_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(individual_headers)
    writer.writerows(combined_player_rows)

print("2009 individual statistics CSV saved!")

# Inspect 2009 match statistics
match_lines = pre_blocks[4].get_text().splitlines()

# Extract 2009 match statistics
match_result_lines = match_lines[73:95]

print("Match rows collected:", len(match_result_lines))
print("First match:", match_result_lines[0])
print("Last match:", match_result_lines[-1])
# Clean up formatting differences in the 2009 matches
cleaned_match_lines = []

for line in match_result_lines:
    line = line.replace("L0-3", "L 0-3")
    cleaned_match_lines.append(line)

print("Cleaned first match:", cleaned_match_lines[0])
print("Cleaned last match:", cleaned_match_lines[-1])

# Extract 2009 match statistics
match_rows = []

for line in cleaned_match_lines:
    parts = line.split()

    # Check whether this is a conference match
    is_conference = parts[0] == "*"

    if is_conference:
        parts.pop(0)

    # Extract the date
    if "/" in parts[0]:
        match_date = parts[0]
        remaining = parts[1:]
    else:
        match_date = " ".join(parts[:2])
        remaining = parts[2:]

    # Handle missing attendance
    if remaining[-1] == "-" or remaining[-1].isdigit():
        attendance = remaining[-1]
        remaining = remaining[:-1]
    else:
        attendance = ""

    # Extract results from the end of the line
    set_scores = remaining[-1]
    match_score = remaining[-2]
    result = remaining[-3]

    opponent = " ".join(remaining[:-3])

    match_rows.append([
        2009,
        "Men's Volleyball",
        match_date,
        opponent,
        is_conference,
        result,
        match_score,
        set_scores,
        attendance
    ])

print("Parsed match rows:", len(match_rows))
print("First parsed match:", match_rows[0])
print("Last parsed match:", match_rows[-1])

# Check match data before saving
for row in match_rows:
    if row[5] not in ["W", "L"] or len(row) != 9:
        print("CHECK THIS ROW:", row)

print("Total wins:", sum(row[5] == "W" for row in match_rows))
print("Total losses:", sum(row[5] == "L" for row in match_rows))

# Save 2009 match statistics
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

with open("brooklyn_mens_volleyball_2009_match_stats.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(match_headers)
    writer.writerows(match_rows)

print("2009 match statistics CSV saved!")