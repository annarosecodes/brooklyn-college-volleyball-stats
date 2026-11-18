from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "combined_tables"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "brooklyn_college_individual_stats.csv"

# Older website columns mapped to the newer statistical names.
COLUMN_MAP = {
    "Jersey Number": "Jersey",
    "Number": "Jersey",
    "Player Name": "Player",
    "Name": "Player",
    "Games Played": "SP",
    "GP": "SP",
    "Kills": "K",
    "Kills Per Game": "K/S",
    "Kills/Game": "K/S",
    "Attack Errors": "E",
    "Total Attacks": "Attack_TA",
    "Attack Percentage": "PCT",
    "Attack Pct": "PCT",
    "Assists": "A",
    "Assists Per Game": "A/S",
    "Assists/Game": "A/S",
    "Service Aces": "SA",
    "Service Aces Per Game": "SA/S",
    "Service Aces/Game": "SA/S",
    "Service Errors": "SE",
    "Reception Errors": "RE",
    "Digs": "DIG",
    "Digs Per Game": "DIG/S",
    "Digs/Game": "DIG/S",
    "Block Solos": "BS",
    "Block Solo": "BS",
    "Block Assists": "BA",
    "Block Assist": "BA",
    "Total Blocks": "BLK",
    "Blocks Per Game": "BLK/S",
    "Blocks/Game": "BLK/S",
    "Block Errors": "BE",
    "Ball Handling Errors": "BHE",
    "Defense_DIG": "DIG",
    "Defense_DIG/S": "DIG/S",
    "Defense_RE": "RE",
    "Defense_TA": "Reception_TA",
    "Defense_Rec%": "Rec%",
    "Defense_RE/S": "RE/S",
    "Defense_BS": "BS",
    "Defense_BA": "BA",
    "Defense_BLK": "BLK",
    "Defense_BLK/S": "BLK/S",
    "Defense_BE": "BE",
    "Defense_BHE": "BHE",
    "TA": "Attack_TA",
    "Defense Games Played": "Defense_Games_Played",
    "Games": "Defense_Games_Played",
    "Matches Played-Started (Raw)": "MP_MS_Raw",
    "MP-MS": "MP_MS_Raw",
}

METADATA = [
    "School", "Season", "Gender", "Scope",
    "Jersey", "Player", "SourceFile"
]

all_frames = []

# Exact filenames only: excludes 2025 intermediate files.
pattern = re.compile(
    r"brooklyn_mens_volleyball_(\d{4})_individual_stats\.csv$"
)

for path in sorted(ROOT.rglob("*.csv")):
    if OUTPUT_DIR in path.parents:
        continue

    match = pattern.fullmatch(path.name)
    if not match:
        continue

    season = int(match.group(1))
    df = pd.read_csv(path, dtype=str)

    # Rename first, preserving all other columns.
    df = df.rename(columns=COLUMN_MAP)

    # Avoid duplicate names when aliases coexist.
    if df.columns.duplicated().any():
        raise ValueError(
            f"Duplicate column names after renaming: {path}"
        )

    df["School"] = "Brooklyn College"
    df["Season"] = season
    df["Gender"] = "Men"

    # Existing files do not explicitly identify their scope.
    # Do not label them Overall without verifying the source.
    df["Scope"] = "Unverified"
    df["SourceFile"] = str(path.relative_to(ROOT))

    all_frames.append(df)

    print(f"Loaded {season}: {len(df)} player rows")

if not all_frames:
    raise FileNotFoundError(
        "No men's individual statistics CSVs were found."
    )

combined = pd.concat(
    all_frames,
    ignore_index=True,
    sort=False
)

# Put identifying columns first; keep every other statistic.
remaining = [
    column for column in combined.columns
    if column not in METADATA
]

combined = combined[METADATA + remaining]

# Flag possible duplicate player-season records for review.
duplicates = combined.duplicated(
    subset=["Season", "Gender", "Jersey", "Player"],
    keep=False
)

combined.to_csv(OUTPUT, index=False)

print("\nCOMBINING COMPLETE")
print(f"Seasons: {combined['Season'].nunique()}")
print(f"Player-season rows: {len(combined)}")
print(f"Columns: {len(combined.columns)}")
print(f"Possible duplicate rows: {duplicates.sum()}")
print(f"Saved to: {OUTPUT}")