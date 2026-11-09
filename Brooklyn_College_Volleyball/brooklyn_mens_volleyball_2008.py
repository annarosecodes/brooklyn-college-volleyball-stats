import requests
from bs4 import BeautifulSoup 
import csv

url = "https://static.brooklyncollegeathletics.com/custompages/mvball/2008/HTML/TEAMCUME.HTM"

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
                stats_rows.append([2008, "Men's Volleyball", category, stat_name, brooklyn, opponents])

print("Total rows collected:", len(stats_rows))
print("First row:", stats_rows[0])

with open("brooklyn_mens_volleyball_2008_team_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Season","Team","Category", "Statistic", "Brooklyn", "Opponents"])
    writer.writerows(stats_rows)