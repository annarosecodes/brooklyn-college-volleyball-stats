from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "combined_tables"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT = OUTPUT_DIR / "brooklyn_college_team_stats.csv"

pattern = re.compile(
    r"brooklyn_mens_volleyball_(\d{4})_team_stats\.csv$"
)

frames = []

for path in sorted(ROOT.rglob("*.csv")):
    if OUTPUT_DIR in path.parents:
        continue

    match = pattern.fullmatch(path.name)

    if not match:
        continue

    season = int(match.group(1))
    df = pd.read_csv(path, dtype=str)

    required = [
        "Category", "Statistic", "Brooklyn", "Opponents"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        print(f"SKIPPING {path.name}: missing {missing}")
        continue

    df["School"] = "Brooklyn College"
    df["Season"] = season
    df["Gender"] = "Men"
    df["Scope"] = "Unverified"
    df["SourceFile"] = str(path.relative_to(ROOT))

    frames.append(df)

    print(f"Loaded {season}: {len(df)} team-stat rows")

if not frames:
    raise FileNotFoundError("No men's team statistics found.")

combined = pd.concat(frames, ignore_index=True)

metadata = [
    "School", "Season", "Gender", "Scope",
    "Category", "Statistic", "Brooklyn",
    "Opponents", "SourceFile"
]

combined = combined[metadata]

combined.to_csv(OUTPUT, index=False)

print("\nTEAM STATISTICS COMBINED")
print(f"Seasons: {combined['Season'].nunique()}")
print(f"Rows: {len(combined)}")
print(f"Columns: {len(combined.columns)}")
print(f"Saved to: {OUTPUT}")