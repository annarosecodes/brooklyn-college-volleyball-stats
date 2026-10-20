#Brooklyn College Womens Volleyball 2025

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.brooklyncollegeathletics.com/sports/womens-volleyball/stats/2025"

# Download the webpage
response = requests.get(url, timeout=20)

print("HTTP STATUS:", response.status_code)

response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all HTML tables
tables = soup.find_all("table")

print("TOTAL TABLES:", len(tables))

# Inspect each table
for index, table in enumerate(tables):
    rows = table.find_all("tr")

    print(f"\nTABLE {index}")
    print("Rows:", len(rows))

    # Preview the first row
    if rows:
        print(
            "First row:",
            rows[0].get_text(" ", strip=True)[:180]
        )
# Step 15A.2: Inspect Women's offensive statistics

offense_table = tables[1]

offense_rows = offense_table.find_all("tr")

print("\nWOMEN'S OFFENSIVE TABLE INSPECTION")
print("Total rows:", len(offense_rows))

# Inspect the first five rows
for index, row in enumerate(offense_rows[:5]):

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print(f"\nRow {index}")
    print("Number of cells:", len(cells))
    print(values)

# Inspect the final three rows
print("\nFINAL THREE OFFENSIVE ROWS")

for row in offense_rows[-3:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print(values)
# Step 15A.3: Extract Women's offensive player statistics

offense_columns = [
    "Jersey", "Player", "SP", "MP", "MS",
    "PTS", "PTS/S", "K", "K/S", "E",
    "TA", "PCT", "A", "A/S",
    "SA", "SA/S", "SE", "Bio Link"
]

offense_data = []

# Skip the first two header rows
for row in offense_rows[2:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    # Only include rows matching the expected structure
    if len(values) != len(offense_columns):
        continue

    # Exclude season summary rows
    if values[1] in ["Total", "Opponents"]:
        continue

    offense_data.append(values)

# Create the DataFrame
df_women_offense = pd.DataFrame(
    offense_data,
    columns=offense_columns
)

print("\nWOMEN'S OFFENSIVE DATA EXTRACTED")

print("Number of players:", len(df_women_offense))
print("Number of columns:", len(df_women_offense.columns))

print("\nFIRST FIVE PLAYERS")
print(df_women_offense.head().to_string(index=False))

print("\nLAST THREE PLAYERS")
print(df_women_offense.tail(3).to_string(index=False))

print("\nCOLUMN NAMES")
print(df_women_offense.columns.tolist())
# Step 15A.4: Clean duplicated player names

import re

def clean_player_name(name, jersey):
    name = str(name).strip()
    jersey = str(jersey).strip()

    # Match duplicated names separated by the jersey number
    pattern = rf"^(.*?)\s+{re.escape(jersey)}\s+\1$"

    match = re.match(pattern, name)

    if match:
        return match.group(1).strip()

    # Keep the original name if it doesn't match
    return name

# Clean the Player column
df_women_offense["Player"] = df_women_offense.apply(
    lambda row: clean_player_name(
        row["Player"],
        row["Jersey"]
    ),
    axis=1
)

print("\nCLEANED WOMEN'S PLAYER NAMES")

print(
    df_women_offense[
        ["Jersey", "Player"]
    ].to_string(index=False)
)

print("\nTOTAL PLAYERS")
print(len(df_women_offense))

print("\nDUPLICATED JERSEY NUMBERS")
print(df_women_offense["Jersey"].duplicated().sum())
# Step 15A.5: Convert Women's offensive statistics to numbers

# List the numeric columns
women_offense_numeric_columns = [
    "SP", "MP", "MS", "PTS", "PTS/S",
    "K", "K/S", "E", "TA", "PCT",
    "A", "A/S", "SA", "SA/S", "SE"
]

# Check empty values before conversion
print("\nEMPTY OFFENSIVE VALUES BEFORE CONVERSION")

print(
    df_women_offense[women_offense_numeric_columns]
    .apply(
        lambda col: col.astype("string").str.strip().eq("").sum()
    )
)

# Convert each column to numeric
for column in women_offense_numeric_columns:

    df_women_offense[column] = pd.to_numeric(
        df_women_offense[column]
        .astype(str)
        .str.replace(",", "", regex=False),
        errors="coerce"
    )

# Display data types
print("\nWOMEN'S OFFENSIVE DATA TYPES")
print(df_women_offense.dtypes)

# Check missing values after conversion
print("\nMISSING OFFENSIVE VALUES AFTER CONVERSION")
print(df_women_offense.isna().sum())

# Preview selected player statistics
print("\nCLEANED WOMEN'S OFFENSIVE STATISTICS")

print(
    df_women_offense[
        ["Jersey", "Player", "SP", "PTS", "K", "PCT", "A", "SA"]
    ].head().to_string(index=False)
)
# Step 15A.6: Save Women's offensive statistics to CSV

from pathlib import Path

# Save in the same folder as this Python script
women_offense_filename = (
    Path(__file__).resolve().parent
    / "brooklyn_womens_volleyball_2025.csv"
)

# Export the offensive DataFrame
df_women_offense.to_csv(
    women_offense_filename,
    index=False
)

print("\nWOMEN'S OFFENSIVE CSV SAVED")
print("File location:", women_offense_filename)

# Read the saved CSV back into pandas
df_women_offense_check = pd.read_csv(
    women_offense_filename,
    dtype={"Jersey": "string"}
)

# Verify dimensions
assert (
    df_women_offense_check.shape
    == df_women_offense.shape
)

# Verify column names and order
assert (
    df_women_offense_check.columns.tolist()
    == df_women_offense.columns.tolist()
)

# Verify player names
assert (
    df_women_offense_check["Player"].tolist()
    == df_women_offense["Player"].tolist()
)

# Verify jersey numbers
assert (
    df_women_offense_check["Jersey"].tolist()
    == df_women_offense["Jersey"].tolist()
)

# Verify numeric statistics
pd.testing.assert_frame_equal(
    df_women_offense_check[
        women_offense_numeric_columns
    ],
    df_women_offense[
        women_offense_numeric_columns
    ],
    check_dtype=False
)

print("\nWOMEN'S OFFENSIVE CSV VERIFICATION PASSED")
print("Rows:", len(df_women_offense_check))
print("Columns:", len(df_women_offense_check.columns))
print(
    "Missing values:",
    df_women_offense_check.isna().sum().sum()
)

# Step 15B.1: Inspect Women's defensive statistics

defense_table = tables[2]

defense_rows = defense_table.find_all("tr")

print("\nWOMEN'S DEFENSIVE TABLE INSPECTION")
print("Total rows:", len(defense_rows))

# Inspect the first five rows
for index, row in enumerate(defense_rows[:5]):

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print(f"\nRow {index}")
    print("Number of cells:", len(cells))
    print(values)

# Inspect the final three rows
print("\nFINAL THREE DEFENSIVE ROWS")

for row in defense_rows[-3:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print(values)
# Step 15B.2: Extract Women's defensive player statistics

defense_columns = [
    "Jersey", "Player", "SP", "DIG", "DIG/S",
    "RE", "TA", "Rec%", "RE/S", "BS",
    "BA", "BLK", "BLK/S", "BE", "BHE",
    "Bio Link"
]

defense_data = []

# Skip the first two header rows
for row in defense_rows[2:]:

    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    # Only include rows matching the expected structure
    if len(values) != len(defense_columns):
        continue

    # Exclude season summary rows
    if values[1] in ["Total", "Opponents"]:
        continue

    defense_data.append(values)

# Create the DataFrame
df_women_defense = pd.DataFrame(
    defense_data,
    columns=defense_columns
)

print("\nWOMEN'S DEFENSIVE DATA EXTRACTED")

print("Number of players:", len(df_women_defense))
print("Number of columns:", len(df_women_defense.columns))

print("\nFIRST FIVE DEFENSIVE PLAYERS")
print(df_women_defense.head().to_string(index=False))

print("\nLAST THREE DEFENSIVE PLAYERS")
print(df_women_defense.tail(3).to_string(index=False))

print("\nDEFENSIVE COLUMN NAMES")
print(df_women_defense.columns.tolist())

# Step 15B.3: Clean Women's defensive player names

df_women_defense["Player"] = df_women_defense.apply(
    lambda row: clean_player_name(
        row["Player"],
        row["Jersey"]
    ),
    axis=1
)

print("\nCLEANED WOMEN'S DEFENSIVE PLAYER NAMES")

print(
    df_women_defense[
        ["Jersey", "Player"]
    ].to_string(index=False)
)

print("\nTOTAL DEFENSIVE PLAYERS")
print(len(df_women_defense))

print("\nDUPLICATED DEFENSIVE JERSEY NUMBERS")
print(df_women_defense["Jersey"].duplicated().sum())

# Check whether offensive and defensive jerseys match
print("\nOFFENSE AND DEFENSE JERSEYS MATCH")

print(
    set(df_women_offense["Jersey"])
    == set(df_women_defense["Jersey"])
)

# Check whether names match for each jersey
offense_names = df_women_offense.set_index("Jersey")["Player"]
defense_names = df_women_defense.set_index("Jersey")["Player"]

print("\nOFFENSE AND DEFENSE PLAYER NAMES MATCH")
print(
    offense_names.sort_index().equals(
        defense_names.sort_index()
    )
)
# Step 15B.4: Convert Women's defensive statistics to numbers

women_defense_numeric_columns = [
    "SP", "DIG", "DIG/S", "RE", "TA",
    "Rec%", "RE/S", "BS", "BA", "BLK",
    "BLK/S", "BE", "BHE"
]

# Check empty values before conversion
print("\nEMPTY DEFENSIVE VALUES BEFORE CONVERSION")

print(
    df_women_defense[women_defense_numeric_columns]
    .apply(
        lambda col: col.astype("string").str.strip().eq("").sum()
    )
)

# Convert numeric columns
for column in women_defense_numeric_columns:

    df_women_defense[column] = pd.to_numeric(
        df_women_defense[column]
        .astype(str)
        .str.replace(",", "", regex=False),
        errors="coerce"
    )

# Display data types
print("\nWOMEN'S DEFENSIVE DATA TYPES")
print(df_women_defense.dtypes)

# Check missing values after conversion
print("\nMISSING DEFENSIVE VALUES AFTER CONVERSION")
print(df_women_defense.isna().sum())

# Preview selected defensive statistics
print("\nCLEANED WOMEN'S DEFENSIVE STATISTICS")

print(
    df_women_defense[
        ["Jersey", "Player", "SP", "DIG", "RE", "Rec%", "BLK"]
    ].head().to_string(index=False)
)
# Step 15B.5: Merge Women's offensive and defensive statistics

# Make copies so the original DataFrames remain unchanged
df_women_offense_merge = df_women_offense.copy()
df_women_defense_merge = df_women_defense.copy()

# Rename TA to distinguish attack and reception attempts
df_women_offense_merge = df_women_offense_merge.rename(
    columns={"TA": "Attack_TA"}
)

df_women_defense_merge = df_women_defense_merge.rename(
    columns={"TA": "Reception_TA"}
)

# Remove duplicate descriptive columns from defense
df_women_defense_merge = df_women_defense_merge.drop(
    columns=["Player", "SP", "Bio Link"]
)

# Merge on Jersey
df_women_combined = pd.merge(
    df_women_offense_merge,
    df_women_defense_merge,
    on="Jersey",
    how="inner",
    validate="one_to_one"
)

print("\nWOMEN'S COMBINED DATASET")

print("Number of players:", len(df_women_combined))
print("Number of columns:", len(df_women_combined.columns))

print("\nCOMBINED COLUMN NAMES")
print(df_women_combined.columns.tolist())

print("\nMISSING VALUES IN COMBINED DATA")
print(df_women_combined.isna().sum())

print("\nFIRST FIVE COMBINED PLAYERS")
print(
    df_women_combined[
        [
            "Jersey", "Player", "K", "A",
            "SA", "DIG", "Rec%", "BLK"
        ]
    ].head().to_string(index=False)
)
# Step 15B.6: Save Women's complete player statistics

from pathlib import Path

# Save in the same folder as this Python script
women_complete_filename = (
    Path(__file__).resolve().parent
    / "brooklyn_womens_volleyball_2025_complete.csv"
)

# Export the combined DataFrame
df_women_combined.to_csv(
    women_complete_filename,
    index=False
)

print("\nWOMEN'S COMPLETE CSV SAVED")
print("File location:", women_complete_filename)

# Read the saved CSV back into pandas
df_women_complete_check = pd.read_csv(
    women_complete_filename,
    dtype={"Jersey": "string"}
)

# Verify dimensions
assert (
    df_women_complete_check.shape
    == df_women_combined.shape
)

# Verify column names and order
assert (
    df_women_complete_check.columns.tolist()
    == df_women_combined.columns.tolist()
)

# Verify all data
pd.testing.assert_frame_equal(
    df_women_complete_check,
    df_women_combined.reset_index(drop=True),
    check_dtype=False
)

print("\nWOMEN'S COMPLETE CSV VERIFICATION PASSED")
print("Rows:", len(df_women_complete_check))
print("Columns:", len(df_women_complete_check.columns))
print(
    "Missing values:",
    df_women_complete_check.isna().sum().sum()
)
# Step 15C.1: Inspect Women's match-by-match table

women_match_table = tables[5]
women_match_rows = women_match_table.find_all("tr")

print("\nWOMEN'S MATCH-BY-MATCH TABLE INSPECTION")
print("Total rows:", len(women_match_rows))

print("\nFIRST FIVE ROWS")

for i, row in enumerate(women_match_rows[:5]):
    cells = row.find_all(["th", "td"])
    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print(f"\nRow {i}")
    print("Number of cells:", len(values))
    print(values)

print("\nLAST FOUR ROWS")

for i, row in enumerate(women_match_rows[-4:]):
    cells = row.find_all(["th", "td"])
    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    print(f"\nRow {len(women_match_rows) - 4 + i}")
    print("Number of cells:", len(values))
    print(values)

# Step 15C.2: Extract Women's match-by-match statistics

women_match_columns = [
    "Date", "Opponent", "W/L", "SP",
    "K", "E", "TA", "PCT", "AST",
    "SA", "SE", "RE", "DIG", "BS",
    "BA", "BE", "TB", "BHE", "PTS"
]

women_match_data = []

# Skip the header row
for row in women_match_rows[1:]:
    cells = row.find_all(["th", "td"])

    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]

    # Skip rows that don't have 19 columns
    if len(values) != len(women_match_columns):
        continue

    # Exclude the season summary rows
    if values[1] in ["Brooklyn", "Opponents"]:
        continue

    women_match_data.append(values)

# Create the DataFrame
df_women_matches = pd.DataFrame(
    women_match_data,
    columns=women_match_columns
)

print("\nWOMEN'S MATCH DATA EXTRACTED")
print("Number of matches:", len(df_women_matches))
print("Number of columns:", len(df_women_matches.columns))

print("\nFIRST FIVE MATCHES")
print(df_women_matches.head().to_string(index=False))

print("\nLAST FIVE MATCHES")
print(df_women_matches.tail().to_string(index=False))

print("\nMATCH COLUMN NAMES")
print(df_women_matches.columns.tolist())

print("\nWIN/LOSS COUNTS")
print(df_women_matches["W/L"].value_counts())

# Step 15C.3: Clean Women's match dates and locations

# Convert dates to a consistent YYYY-MM-DD format
df_women_matches["Date"] = pd.to_datetime(
    df_women_matches["Date"],
    format="%m/%d/%Y",
    errors="raise"
).dt.strftime("%Y-%m-%d")

# Determine match location from the opponent prefix
def get_match_location(opponent):
    opponent = str(opponent).strip()

    if opponent.startswith("at "):
        return "Away"
    elif opponent.startswith("vs "):
        return "Neutral"
    else:
        return "Home"

df_women_matches["Location"] = (
    df_women_matches["Opponent"]
    .apply(get_match_location)
)

# Remove location prefixes from opponent names
df_women_matches["Opponent"] = (
    df_women_matches["Opponent"]
    .str.replace(r"^(at|vs)\s+", "", regex=True)
    .str.strip()
)

print("\nWOMEN'S CLEANED MATCH INFORMATION")

print(
    df_women_matches[
        ["Date", "Opponent", "W/L", "Location"]
    ].head(10).to_string(index=False)
)

print("\nLOCATION COUNTS")
print(df_women_matches["Location"].value_counts())

print("\nTOTAL MATCHES")
print(len(df_women_matches))

print("\nNUMBER OF COLUMNS")
print(len(df_women_matches.columns))

print("\nDATE RANGE")
print("First match:", df_women_matches["Date"].min())
print("Last match:", df_women_matches["Date"].max())
# Step 15C.4: Convert Women's match statistics to numbers

women_match_numeric_columns = [
    "SP", "K", "E", "TA", "PCT",
    "AST", "SA", "SE", "RE", "DIG",
    "BS", "BA", "BE", "TB", "BHE", "PTS"
]

# Check for empty values before conversion
print("\nEMPTY MATCH VALUES BEFORE CONVERSION")

print(
    df_women_matches[women_match_numeric_columns]
    .apply(
        lambda col: col.astype("string").str.strip().eq("").sum()
    )
)

# Convert statistical columns to numeric values
for column in women_match_numeric_columns:
    df_women_matches[column] = pd.to_numeric(
        df_women_matches[column]
        .astype(str)
        .str.replace(",", "", regex=False),
        errors="coerce"
    )

# Check data types
print("\nWOMEN'S MATCH DATA TYPES")
print(df_women_matches.dtypes)

# Check for missing values
print("\nMISSING VALUES AFTER CONVERSION")
print(df_women_matches.isna().sum())

# Preview the converted statistics
print("\nFIRST FIVE CONVERTED MATCHES")

print(
    df_women_matches[
        ["Date", "Opponent", "W/L", "K", "AST", "SA", "DIG", "PTS"]
    ].head().to_string(index=False)
)

print("\nLAST FIVE CONVERTED MATCHES")

print(
    df_women_matches[
        ["Date", "Opponent", "W/L", "K", "AST", "SA", "DIG", "PTS"]
    ].tail().to_string(index=False)
)

print("\nTOTAL MATCHES AFTER CONVERSION")
print(len(df_women_matches))

print("\nTOTAL MISSING VALUES")
print(df_women_matches.isna().sum().sum())
# Step 15C.5: Save Women's match-by-match statistics

from pathlib import Path

women_matches_filename = (
    Path(__file__).resolve().parent
    / "brooklyn_womens_volleyball_2025_matches.csv"
)

# Save the CSV
df_women_matches.to_csv(
    women_matches_filename,
    index=False
)

print("\nWOMEN'S MATCH CSV SAVED")
print("File location:", women_matches_filename)

# Reload the saved file
df_women_matches_check = pd.read_csv(
    women_matches_filename,
    dtype={
        "Date": "string",
        "Opponent": "string",
        "W/L": "string",
        "Location": "string"
    }
)

# Verify rows and columns
assert (
    df_women_matches_check.shape
    == df_women_matches.shape
)

# Verify column names and order
assert (
    df_women_matches_check.columns.tolist()
    == df_women_matches.columns.tolist()
)

# Verify all values
pd.testing.assert_frame_equal(
    df_women_matches_check,
    df_women_matches.reset_index(drop=True),
    check_dtype=False
)

print("\nWOMEN'S MATCH CSV VERIFICATION PASSED")
print("Rows:", len(df_women_matches_check))
print("Columns:", len(df_women_matches_check.columns))
print(
    "Missing values:",
    df_women_matches_check.isna().sum().sum()
)

print("\nFINAL MATCH COLUMN NAMES")
print(df_women_matches_check.columns.tolist())

# Step 16.1: Verify all six Brooklyn College Volleyball CSV files

from pathlib import Path

project_folder = Path(__file__).resolve().parent

expected_csv_files = [
    "brooklyn_mens_volleyball_2025.csv",
    "brooklyn_mens_volleyball_2025_complete.csv",
    "brooklyn_mens_volleyball_2025_matches.csv",
    "brooklyn_womens_volleyball_2025.csv",
    "brooklyn_womens_volleyball_2025_complete.csv",
    "brooklyn_womens_volleyball_2025_matches.csv"
]

print("\nBROOKLYN COLLEGE VOLLEYBALL CSV FILE CHECK")
print("Project folder:", project_folder)

all_files_found = True

for filename in expected_csv_files:
    file_path = project_folder / filename

    if file_path.is_file():
        df_check = pd.read_csv(file_path)

        print(
            f"FOUND: {filename} "
            f"| Rows: {len(df_check)} "
            f"| Columns: {len(df_check.columns)}"
        )
    else:
        print(f"MISSING: {filename}")
        all_files_found = False

print("\nALL SIX CSV FILES FOUND:", all_files_found)

# Step 16.2: Compare Men's and Women's CSV formats

csv_pairs = [
    (
        "OFFENSIVE PLAYER STATISTICS",
        "brooklyn_mens_volleyball_2025.csv",
        "brooklyn_womens_volleyball_2025.csv"
    ),
    (
        "COMPLETE PLAYER STATISTICS",
        "brooklyn_mens_volleyball_2025_complete.csv",
        "brooklyn_womens_volleyball_2025_complete.csv"
    ),
    (
        "MATCH-BY-MATCH STATISTICS",
        "brooklyn_mens_volleyball_2025_matches.csv",
        "brooklyn_womens_volleyball_2025_matches.csv"
    )
]

print("\nMEN'S AND WOMEN'S CSV FORMAT COMPARISON")

for label, mens_filename, womens_filename in csv_pairs:

    mens_df = pd.read_csv(project_folder / mens_filename)
    womens_df = pd.read_csv(project_folder / womens_filename)

    columns_match = (
        mens_df.columns.tolist()
        == womens_df.columns.tolist()
    )

    print(f"\n{label}")
    print("Men's columns:", len(mens_df.columns))
    print("Women's columns:", len(womens_df.columns))
    print("Column names and order match:", columns_match)

    if not columns_match:
        print("Men's column names:", mens_df.columns.tolist())
        print("Women's column names:", womens_df.columns.tolist())
