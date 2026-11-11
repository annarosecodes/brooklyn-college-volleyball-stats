import requests
from bs4 import BeautifulSoup 
import csv

url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2008/HTML/TEAMCUME.HTM"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
pre_blocks = soup.find_all("pre")
print(len(pre_blocks))
for index, block in enumerate(pre_blocks):
    print("Block", index, ":", block.get_text()[:100])

individual_lines = pre_blocks[1].get_text().splitlines()

for index, line in enumerate(individual_lines):
    if "## Name" in line:
        print("Player table header found at line:", index)
        print(line)
for index in range(13, 28):
    print(index, individual_lines[index])
player_rows = []

for line in individual_lines[13:24]:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-12])
    stats = parts[-12:]

    player_rows.append([2008, "Men's Volleyball", jersey_number, player_name] + stats)

print("Player rows collected:", len(player_rows))
print("First player row:", player_rows[0])

defense_rows = []

for line in individual_lines[30:41]:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-10])
    defense_stats = parts[-10:]

    defense_rows.append([2008, "Men's Volleyball", jersey_number, player_name] + defense_stats)

print("Defense player rows:", len(defense_rows))
print("First defense player:", defense_rows[0])
combined_player_rows = []

for player in player_rows:
    for defender in defense_rows:
        if player[2] == defender[2]:
            combined_player_rows.append(player + defender[4:])
            break

print("Combined player rows:", len(combined_player_rows))
print("First combined row:", combined_player_rows[0])
for player in combined_player_rows:
    print(player[3], ":", len(player), "columns")
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

with open("brooklyn_mens_volleyball_2008_individual_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(individual_headers)
    writer.writerows(combined_player_rows)

print("2008 individual statistics CSV saved!")
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
                stats_rows.append([2008, "Men's Volleyball", category, stat_name, brooklyn, opponents])

print("Total rows collected:", len(stats_rows))
print("First row:", stats_rows[0])

with open("brooklyn_mens_volleyball_2008_team_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Season","Team","Category", "Statistic", "Brooklyn", "Opponents"])
    writer.writerows(stats_rows)

match_lines = pre_blocks[4].get_text().splitlines()

print("Total match statistics lines:", len(match_lines))

match_result_lines = match_lines[72:95]

print("Match rows collected:", len(match_result_lines))
print("First match:", match_result_lines[0])
print("Last match:", match_result_lines[-1])
first_match_parts = match_result_lines[0].split()
last_match_parts = match_result_lines[-1].split()

print("First match split:", first_match_parts)
print("Last match split:", last_match_parts)
match_rows = []

for line in match_result_lines:
    parts = line.split()
    is_conference = parts[0] == "*"

    if is_conference:
        parts.pop(0)

    if "/" in parts[0]:
        match_date = parts[0]
        opponent = " ".join(parts[1:-4])
    else:
        match_date = " ".join(parts[:2])
        opponent = " ".join(parts[2:-4])

    result = parts[-4]
    match_score = parts[-3]
    set_scores = parts[-2]
    attendance = parts[-1]

    match_rows.append([
        2008,
        "Men's Volleyball",
        match_date,
        opponent,
        is_conference,
        result,
        match_score,
        set_scores,
        attendance
    ])

print("Match rows saved:", len(match_rows))
print("First match row:", match_rows[0])
print("Last match row:", match_rows[-1])
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

with open("brooklyn_mens_volleyball_2008_match_stats.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(match_headers)
    writer.writerows(match_rows)

print("2008 match statistics CSV saved!")
with open("brooklyn_mens_volleyball_2008_match_stats.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    saved_rows = list(reader)

print("Total CSV rows:", len(saved_rows))
print("CSV headers:", saved_rows[0])
print("First saved match:", saved_rows[1])
print("Last saved match:", saved_rows[-1])