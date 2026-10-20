import requests
from bs4 import BeautifulSoup
from io import StringIO

url = url = "https://www.brooklyncollegeathletics.com/sports/womens-volleyball/stats/2025"
response = requests.get(url, timeout=20)

print("HTTP Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")

print("Number of tables found:", len(tables))

for index, table in enumerate(tables):
    print("Table", index, ":", table.get_text(" ", strip=True)[:150])

#Organizing the data
import pandas as pd

team_table = tables[0]

team_df = pd.read_html(StringIO(str(team_table)))[0]

print("\nOverall Team Statistics:")
print(team_df.to_string(index=False))

print("\nColumn names:")
print(team_df.columns.tolist())

categories = ["Attack", "Set", "Serve", "Receptions", "Defense", "Blocking"]

current_category = None
clean_rows = []

for _, row in team_df.iterrows():
    statistic = str(row["Statistic"]).strip()

    if statistic in categories:
        current_category = statistic
        continue

    clean_rows.append({
        "Category": current_category,
        "Statistic": statistic,
        "Brooklyn": row["Brooklyn"],
        "Opponents": row["Opponents OPP"]
    })

clean_df = pd.DataFrame(clean_rows)

print("\nCleaned Overall Team Statistics:")
print(clean_df.to_string(index=False))

print("\nNumber of statistics:", len(clean_df))

#to create a CSV
output_file = "brooklyn_womens_team_stats_2025.csv"

clean_df.to_csv(output_file, index=False)

print("\nCSV saved:", output_file)

check_df = pd.read_csv(output_file)

print("CSV rows:", len(check_df))
print("CSV columns:", check_df.columns.tolist())