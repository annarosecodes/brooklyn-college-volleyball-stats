# Brooklyn College - Mens Volleyball

# Import the libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Save the webpage URL
url = "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/2025"

# Request the webpage
response = requests.get(url, timeout=20)

# Display the HTTP status code
print("HTTP Status Code:", response.status_code)

# Step 4: Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Step 5: Find the webpage title
page_title = soup.title

# Step 6: Display the title
print("Webpage Title:", page_title.get_text(strip=True) if page_title else "Not found")

# Step 7: Find all HTML tables
tables = soup.find_all("table")

# Step 8: Count the tables
print("Number of HTML tables found:", len(tables))

# Step 7: Inspect each HTML table

for index, table in enumerate(tables):

    print("\n-------------------------")
    print("TABLE NUMBER:", index)
    print("-------------------------")

    headers = table.find_all("th")

    header_text = [
        header.get_text(" ", strip=True)
        for header in headers
    ]

    print("Headers:", header_text[:20])

    first_row = table.find("tr")

    if first_row:
        print(
            "First row:",
            first_row.get_text(" ", strip=True)[:250]
        )
# Step 8A: Inspect player statistics in Table 1

player_table = tables[1]

# Find all rows in the table
rows = player_table.find_all("tr")

print("\nPLAYER STATISTICS - TABLE 1")
print("Number of rows found:", len(rows))

# Display the first five rows
for index, row in enumerate(rows[:5]):

    # Find all header and data cells
    cells = row.find_all(["th", "td"])

    # Extract text from each cell
    cell_text = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print("\nRow:", index)
    print(cell_text)
# Step 9A: Create a pandas DataFrame

# Get the actual column names from Row 1
header_cells = rows[1].find_all(["th", "td"])

column_names = [
    cell.get_text(" ", strip=True)
    for cell in header_cells
]

# Add a column for jersey number
column_names.insert(0, "Jersey")

# Add a column for the biography link text
column_names.append("Bio Link")

# Create an empty list for player data
player_data = []

# Loop through the player rows
for row in rows[2:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    # Only include rows with matching column counts
    if len(values) == len(column_names):
        player_data.append(values)
    else:
        print("Skipped row with", len(values), "cells")

# Convert the data into a pandas DataFrame
df = pd.DataFrame(player_data, columns=column_names)

# Display the results
print("\nPLAYER DATAFRAME")
print(df.head())

print("\nDataFrame shape:", df.shape)
print("\nColumn names:", df.columns.tolist())

# Step 9C: Verify the player records

print("\nALL PLAYER NAMES AND JERSEY NUMBERS")

# Display every row's jersey number and player name
print(df[["Jersey", "Player"]].to_string(index=False))

# Check for missing values
print("\nMISSING VALUES BY COLUMN")
print(df.isna().sum())

# Check for duplicate jersey numbers
print("\nDUPLICATE JERSEY NUMBERS")
print(df["Jersey"].duplicated().sum())

# Check the DataFrame dimensions
print("\nTOTAL RECORDS:", len(df))
print("TOTAL COLUMNS:", len(df.columns))

# Step 10A: Clean the player statistics

# Make a copy of the original DataFrame
df_clean = df.copy()

# Remove summary rows
df_clean = df_clean[
    ~df_clean["Player"].isin(["Total", "Opponents"])
].copy()

# Clean duplicated player names
def clean_player_name(row):
    name = row["Player"]
    jersey = row["Jersey"]

    # Example:
    # "Seise, Kevin 1 Seise, Kevin"
    # becomes "Seise, Kevin"

    separator = f" {jersey} "

    if separator in name:
        name = name.split(separator, 1)[0]

    return name.strip()

# Apply the cleaning function to each player
df_clean["Player"] = df_clean.apply(
    clean_player_name,
    axis=1
)

# Display cleaned player names
print("\nCLEANED PLAYER NAMES")
print(
    df_clean[["Jersey", "Player"]].to_string(index=False)
)

# Check the number of players
print("\nNumber of players:", len(df_clean))

# Check duplicate jersey numbers
print(
    "Duplicate jersey numbers:",
    df_clean["Jersey"].duplicated().sum()
)

# Step 10B.1: Check for empty values

print("\nEMPTY VALUES BY COLUMN")

# Count empty or whitespace-only cells
empty_counts = df_clean.apply(
    lambda column: column.astype("string")
    .str.strip()
    .eq("")
    .sum()
)

print(empty_counts)

# Check pandas missing values
print("\nMISSING VALUES BY COLUMN")
print(df_clean.isna().sum())
# Step 10B.2: Convert statistics to numeric types

# Identify statistical columns
numeric_columns = [
    "SP", "MP", "MS", "PTS", "PTS/S",
    "K", "K/S", "E", "TA", "PCT",
    "A", "A/S", "SA", "SA/S", "SE"
]

# Convert each statistical column
for column in numeric_columns:
    df_clean[column] = pd.to_numeric(
        df_clean[column],
        errors="coerce"
    )

# Convert jersey numbers to integers
df_clean["Jersey"] = pd.to_numeric(
    df_clean["Jersey"],
    errors="coerce"
)

# Display the updated data types
print("\nDATA TYPES AFTER CONVERSION")
print(df_clean.dtypes)

# Check for missing values after conversion
print("\nMISSING VALUES AFTER CONVERSION")
print(df_clean.isna().sum())

# Display the first five cleaned records
print("\nCLEANED PLAYER STATISTICS")
print(
    df_clean[
        ["Jersey", "Player", "SP", "K", "A", "SA", "PTS"]
    ].head().to_string(index=False)
)
# Step 11A: Export the cleaned dataset to CSV

from pathlib import Path

# Choose the CSV filename
filename = Path(__file__).resolve().parent / "brooklyn_mens_volleyball_2025.csv"

# Save the cleaned DataFrame
df_clean.to_csv(filename, index=False)

# Confirm the file was saved
print("\nCSV FILE SAVED SUCCESSFULLY!")
print("File location:", filename)
print("Number of players exported:", len(df_clean))
print("Number of columns exported:", len(df_clean.columns))

# Step 11C: Verify the saved CSV

# Read the CSV back into pandas
df_check = pd.read_csv(filename)

print("\nCSV VERIFICATION")
print("CSV shape:", df_check.shape)
print("CSV columns:", df_check.columns.tolist())

# Confirm the exported data matches
assert df_check.shape == df_clean.shape
assert df_check["Player"].tolist() == df_clean["Player"].tolist()

print("CSV verification passed!")
# Step 12A: Inspect defensive statistics in Table 2

# Select Table 2
defensive_table = tables[2]

# Find all rows in the defensive table
defensive_rows = defensive_table.find_all("tr")

print("\nDEFENSIVE STATISTICS - TABLE 2")
print("Number of rows found:", len(defensive_rows))

# Inspect the first five rows
for index, row in enumerate(defensive_rows[:5]):

    cells = row.find_all(["th", "td"])

    cell_text = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print("\nRow:", index)
    print("Number of cells:", len(cells))
    print(cell_text)
# Step 12B: Create a defensive statistics DataFrame

# Get column names from Row 1
defensive_header_cells = defensive_rows[1].find_all(
    ["th", "td"]
)

defensive_columns = [
    cell.get_text(" ", strip=True)
    for cell in defensive_header_cells
]

# Add names for the two extra cells
defensive_columns.insert(0, "Jersey")
defensive_columns.append("Bio Link")

# Create an empty list for defensive data
defensive_data = []

# Extract data from rows after the headers
for row in defensive_rows[2:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    if len(values) == len(defensive_columns):
        defensive_data.append(values)
    else:
        print(
            "Skipped defensive row with",
            len(values),
            "cells"
        )

# Create the pandas DataFrame
df_defensive = pd.DataFrame(
    defensive_data,
    columns=defensive_columns
)

# Display the results
print("\nDEFENSIVE DATAFRAME")
print(df_defensive.head())

print("\nDefensive DataFrame shape:", df_defensive.shape)
print("\nDefensive column names:", df_defensive.columns.tolist())

# Step 12C: Clean defensive player records

# Make a copy of the defensive DataFrame
df_defensive_clean = df_defensive.copy()

# Remove team summary rows
df_defensive_clean = df_defensive_clean[
    ~df_defensive_clean["Player"].isin(
        ["Total", "Opponents"]
    )
].copy()

# Reuse our player-name cleaning function from Step 10A
df_defensive_clean["Player"] = df_defensive_clean.apply(
    clean_player_name,
    axis=1
)

# Display cleaned defensive player names
print("\nCLEANED DEFENSIVE PLAYER NAMES")
print(
    df_defensive_clean[
        ["Jersey", "Player"]
    ].to_string(index=False)
)

# Verify the number of players
print(
    "\nNumber of defensive players:",
    len(df_defensive_clean)
)

# Check duplicate jersey numbers
print(
    "Duplicate defensive jersey numbers:",
    df_defensive_clean["Jersey"].duplicated().sum()
)

# Check empty jersey numbers
print(
    "Empty defensive jersey numbers:",
    df_defensive_clean["Jersey"].str.strip().eq("").sum()
)

# Step 12D.1: Check defensive missing values

print("\nDEFENSIVE EMPTY VALUES")

# Count empty or whitespace-only cells
defensive_empty = df_defensive_clean.apply(
    lambda column: column.astype("string")
    .str.strip()
    .eq("")
    .sum()
)

print(defensive_empty)

# Check for missing values
print("\nDEFENSIVE MISSING VALUES")
print(df_defensive_clean.isna().sum())

# Step 12D.2: Convert defensive statistics to numbers

# List of defensive statistical columns
defensive_numeric_columns = [
    "SP", "DIG", "DIG/S", "RE", "TA",
    "Rec%", "RE/S", "BS", "BA",
    "BLK", "BLK/S", "BE", "BHE"
]

# Convert statistical columns
for column in defensive_numeric_columns:
    df_defensive_clean[column] = pd.to_numeric(
        df_defensive_clean[column],
        errors="coerce"
    )

# Convert jersey numbers
df_defensive_clean["Jersey"] = pd.to_numeric(
    df_defensive_clean["Jersey"],
    errors="coerce"
)

# Display data types
print("\nDEFENSIVE DATA TYPES")
print(df_defensive_clean.dtypes)

# Check missing values after conversion
print("\nDEFENSIVE MISSING VALUES AFTER CONVERSION")
print(df_defensive_clean.isna().sum())

# Display selected defensive statistics
print("\nCLEANED DEFENSIVE STATISTICS")
print(
    df_defensive_clean[
        ["Jersey", "Player", "SP", "DIG", "RE", "BS", "BA", "BLK"]
    ].head().to_string(index=False)
)
# Step 13A.1: Prepare DataFrames for merging

# Make copies to preserve the cleaned datasets
df_offense_merge = df_clean.copy()
df_defense_merge = df_defensive_clean.copy()

# Rename columns with different meanings
df_offense_merge = df_offense_merge.rename(
    columns={"TA": "Attack_TA"}
)

df_defense_merge = df_defense_merge.rename(
    columns={"TA": "Reception_TA"}
)

# Remove repeated columns from defensive data
df_defense_merge = df_defense_merge.drop(
    columns=["Player", "SP", "Bio Link"]
)

# Check the prepared column names
print("\nOFFENSIVE COLUMNS FOR MERGE")
print(df_offense_merge.columns.tolist())

print("\nDEFENSIVE COLUMNS FOR MERGE")
print(df_defense_merge.columns.tolist())
# Step 13A.2: Merge offensive and defensive statistics

df_combined = pd.merge(
    df_offense_merge,
    df_defense_merge,
    on="Jersey",
    how="inner",
    validate="one_to_one"
)

# Display the combined DataFrame
print("\nCOMBINED PLAYER STATISTICS")
print(
    df_combined[
        ["Jersey", "Player", "K", "A", "SA", "DIG", "BLK", "PTS"]
    ].head().to_string(index=False)
)

# Verify the merged DataFrame
print("\nCOMBINED DATAFRAME SHAPE")
print(df_combined.shape)

print("\nCOMBINED COLUMN NAMES")
print(df_combined.columns.tolist())

print("\nNUMBER OF COMBINED PLAYERS")
print(len(df_combined))
# Step 13B: Save the combined statistics to CSV

from pathlib import Path

# Save the file in the same folder as this Python script
combined_filename = (
    Path(__file__).resolve().parent
    / "brooklyn_mens_volleyball_2025_complete.csv"
)

# Export the combined DataFrame
df_combined.to_csv(
    combined_filename,
    index=False
)

print("\nCOMBINED CSV SAVED")
print("File location:", combined_filename)

# Read the CSV back into pandas
df_combined_check = pd.read_csv(combined_filename)

# Verify its dimensions and player names
assert df_combined_check.shape == df_combined.shape

assert (
    df_combined_check["Player"].tolist()
    == df_combined["Player"].tolist()
)

assert (
    df_combined_check["Jersey"].tolist()
    == df_combined["Jersey"].tolist()
)

print("\nCOMBINED CSV VERIFICATION PASSED")
print("Rows:", len(df_combined_check))
print("Columns:", len(df_combined_check.columns))
print("Players:", df_combined_check["Player"].nunique())

# Step 14A.1: Reproduce Men's Leaders rankings

leader_categories = {
    "Kills": "K",
    "Assists": "A",
    "Service Aces": "SA",
    "Digs": "DIG",
    "Blocks": "BLK"
}

for category, column in leader_categories.items():

    top_five = df_combined[
        ["Player", column]
    ].sort_values(
        by=column,
        ascending=False
    ).head(5)

    print(f"\nMEN'S LEADERS: {category}")
    print(top_five.to_string(index=False))

# Step 14B.1: Locate the Match-By-Match Team Statistics table

print("\nMATCH-BY-MATCH TABLE SEARCH")

for index, table in enumerate(tables):

    rows = table.find_all("tr")

    # Get a short preview of the first three rows
    preview = []

    for row in rows[:3]:
        cells = row.find_all(["th", "td"])

        values = [
            cell.get_text(" ", strip=True)
            for cell in cells
        ]

        preview.append(values)

    print(f"\nTable {index}")
    print("Number of rows:", len(rows))
    print("First three rows:", preview)
# Step 14B.2: Extract Brooklyn College match-by-match data

# Select Brooklyn College's match-by-match table
match_table = tables[5]

# Find all rows
match_rows = match_table.find_all("tr")

# Extract column names from the first row
match_headers = [
    cell.get_text(" ", strip=True)
    for cell in match_rows[0].find_all(["th", "td"])
]

# Extract the remaining rows
match_data = []

for row in match_rows[1:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    if len(values) == len(match_headers):
        match_data.append(values)
    else:
        print(
            "Skipped match row with",
            len(values),
            "cells"
        )

# Create the DataFrame
df_matches = pd.DataFrame(
    match_data,
    columns=match_headers
)

# Display results
print("\nMATCH-BY-MATCH DATAFRAME")
print(df_matches.head().to_string(index=False))

print("\nMATCH DATAFRAME SHAPE")
print(df_matches.shape)

print("\nMATCH COLUMN NAMES")
print(df_matches.columns.tolist())

# Step 14B.3: Clean match dates and opponent names

# Preserve the original extracted data
df_matches_clean = df_matches.copy()

# Remove season summary rows before cleaning match dates - 

df_matches_clean = df_matches_clean[
    ~df_matches_clean["Opponent"].isin(
        ["Brooklyn", "Opponents"]
    )
].copy()

# Convert dates into a standard date format
df_matches_clean["Date"] = pd.to_datetime(
    df_matches_clean["Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

# Identify match locations using opponent prefixes
def get_match_location(opponent):
    if opponent.startswith("at "):
        return "Away"
    elif opponent.startswith("vs "):
        return "Neutral"
    else:
        return "Home"

df_matches_clean["Location"] = (
    df_matches_clean["Opponent"].apply(get_match_location)
)

# Remove the location prefixes from opponent names
df_matches_clean["Opponent"] = (
    df_matches_clean["Opponent"]
    .str.replace(r"^(at|vs)\s+", "", regex=True)
    .str.strip()
)

# Display cleaned match details
print("\nCLEANED MATCH DETAILS")
print(
    df_matches_clean[
        ["Date", "Opponent", "Location", "W/L"]
    ].head(10).to_string(index=False)
)

# Check for dates that could not be converted
print("\nINVALID MATCH DATES")
print(df_matches_clean["Date"].isna().sum())

# Count matches by location
print("\nMATCHES BY LOCATION")
print(df_matches_clean["Location"].value_counts())

# Confirm the number of matches
print("\nTOTAL MATCHES")
print(len(df_matches_clean))

# Step 14B.3A: Investigate invalid match dates

# Find rows where the converted date is missing
invalid_date_rows = df_matches_clean[
    df_matches_clean["Date"].isna()
]

print("\nROWS WITH INVALID MATCH DATES")

print(
    invalid_date_rows[
        ["Opponent", "Location", "W/L"]
    ].to_string(index=True)
)

# Look up the original date text using the same row indexes
print("\nORIGINAL DATE VALUES")

print(
    df_matches.loc[
        invalid_date_rows.index,
        ["Date", "Opponent", "W/L"]
    ].to_string(index=True)
)
# Step 14B.4: Convert match statistics to numeric values

# List all numeric match statistics
match_numeric_columns = [
    "SP", "K", "E", "TA", "PCT",
    "AST", "SA", "SE", "RE", "DIG",
    "BS", "BA", "BE", "TB", "BHE", "PTS"
]

# Check empty values before conversion
print("\nMATCH EMPTY VALUES BEFORE CONVERSION")

print(
    df_matches_clean[match_numeric_columns]
    .apply(lambda col: col.astype("string").str.strip().eq("").sum())
)

# Convert numeric columns
for column in match_numeric_columns:

    df_matches_clean[column] = pd.to_numeric(
        df_matches_clean[column],
        errors="coerce"
    )

# Display data types
print("\nMATCH DATA TYPES")
print(df_matches_clean.dtypes)

# Check missing values after conversion
print("\nMATCH MISSING VALUES AFTER CONVERSION")
print(df_matches_clean.isna().sum())

# Display selected match statistics
print("\nCLEANED MATCH STATISTICS")
print(
    df_matches_clean[
        ["Date", "Opponent", "W/L", "K", "DIG", "PTS"]
    ].head().to_string(index=False)
)

# Step 14B.5: Save match-by-match statistics to CSV

from pathlib import Path

# Save in the same folder as this Python script
matches_filename = (
    Path(__file__).resolve().parent
    / "brooklyn_mens_volleyball_2025_matches.csv"
)

# Export the cleaned match DataFrame
df_matches_clean.to_csv(
    matches_filename,
    index=False,
    date_format="%Y-%m-%d"
)

print("\nMATCH CSV SAVED")
print("File location:", matches_filename)

# Read the CSV back into pandas
df_matches_check = pd.read_csv(matches_filename)

# Verify dimensions
assert df_matches_check.shape == df_matches_clean.shape

# Verify opponent names
assert (
    df_matches_check["Opponent"].tolist()
    == df_matches_clean["Opponent"].tolist()
)

# Verify match results
assert (
    df_matches_check["W/L"].tolist()
    == df_matches_clean["W/L"].tolist()
)

# Verify dates
assert (
    df_matches_check["Date"].tolist()
    == df_matches_clean["Date"].dt.strftime("%Y-%m-%d").tolist()
)

print("\nMATCH CSV VERIFICATION PASSED")
print("Rows:", len(df_matches_check))
print("Columns:", len(df_matches_check.columns))
print("Unique dates:", df_matches_check["Date"].nunique())