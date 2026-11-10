import requests
from bs4 import BeautifulSoup 
import csv

url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2007/HTML/TEAMCUME.HTM"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
pre_blocks = soup.find_all("pre")
individual_lines = pre_blocks[1].get_text().splitlines()

for i, line in enumerate(individual_lines):
    if "Name" in line:
        print("Player table header found at line:", i)
        print(line)

print("Individual statistics lines:", len(individual_lines))
print(len(pre_blocks))

# Get the 12 players from the first statistics table
attack_player_lines = individual_lines[13:25]

individual_stats_rows = []

for line in attack_player_lines:
    parts = line.split()

    jersey_number = parts[0]
    player_name = " ".join(parts[1:-12])
    player_stats = parts[-12:]

    individual_stats_rows.append(
        [2007, "Men's Volleyball", jersey_number, player_name] + player_stats
    )

print("Individual player rows collected:", len(individual_stats_rows))
print("First player row:", individual_stats_rows[0])
defense_player_lines = individual_lines[31:43]

print("Defense player rows:", len(defense_player_lines))
print("First defense player:", defense_player_lines[0])
for i, line in enumerate(defense_player_lines):
    parts = line.split()
    jersey_number = parts[0]
    player_name = " ".join(parts[1:-10])
    defense_stats = parts[-10:]

    
    if individual_stats_rows[i][2] == jersey_number and individual_stats_rows[i][3] == player_name:
        individual_stats_rows[i].extend(defense_stats)
    else:
        print("Player mismatch:", player_name)
        print("Attack record:", individual_stats_rows[i][:4])
        print("Defense record:", jersey_number, player_name)

print("Combined player rows:", len(individual_stats_rows))
print("First combined row:", individual_stats_rows[0])
individual_headers = [
    "Season", "Team", "Jersey Number", "Player Name",
    "Games Played", "Matches Played-Started (Raw)", "Kills", "Kills Per Game",
    "Attack Errors", "Total Attacks", "Attack Percentage",
    "Assists", "Assists Per Game", "Service Aces",
    "Service Aces Per Game", "Service Errors",
    "Defense Games Played", "Reception Errors", "Digs",
    "Digs Per Game", "Block Solos", "Block Assists",
    "Total Blocks", "Blocks Per Game", "Block Errors",
    "Ball Handling Errors"
]

print("Number of headers:", len(individual_headers))
print("Number of values:", len(individual_stats_rows[0]))
for row in individual_stats_rows:
    print(row[3], ":", len(row), "columns")
for row in individual_stats_rows:
    if len(row) != len(individual_headers):
        print("Column mismatch:", row[3])
with open("brooklyn_mens_volleyball_2007_individual_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(individual_headers)
    writer.writerows(individual_stats_rows)

print("Individual statistics CSV saved!")
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
                stats_rows.append([2007, "Men's Volleyball", category, stat_name, brooklyn, opponents])

print("Total rows collected:", len(stats_rows))
print("First row:", stats_rows[0])

with open("brooklyn_mens_volleyball_2007_team_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Season","Team","Category", "Statistic", "Brooklyn", "Opponents"])
    writer.writerows(stats_rows)