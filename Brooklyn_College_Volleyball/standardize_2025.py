import csv
from pathlib import Path

FOLDER = Path(__file__).resolve().parent

FILES = {
    "brooklyn_mens_volleyball_2025_complete.csv":
        "brooklyn_mens_volleyball_2025_individual_stats.csv",

    "brooklyn_mens_volleyball_2025_matches.csv":
        "brooklyn_mens_volleyball_2025_match_stats.csv",

    "brooklyn_mens_team_stats_2025.csv":
        "brooklyn_mens_volleyball_2025_team_stats.csv",
}

for source_name, output_name in FILES.items():
    source = FOLDER / source_name
    output = FOLDER / output_name

    with source.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        original_columns = reader.fieldnames
        rows = list(reader)

    if not original_columns:
        raise ValueError(f"No columns found in {source_name}")

    # Preserve original statistics and add season identifiers
    columns = ["Season", "Team"] + original_columns

    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for row in rows:
            writer.writerow({
                "Season": 2025,
                "Team": "Men's Volleyball",
                **row
            })

    print(f"Saved {output_name}: {len(rows)} rows")

print("\n2025 standardization complete!")