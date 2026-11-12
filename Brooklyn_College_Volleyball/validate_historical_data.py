import csv
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
YEARS = [year for year in range(2007, 2026) if year != 2021]
KINDS = ["individual", "match", "team"]

errors = []
total_rows = 0

for year in YEARS:
    for kind in KINDS:
        filename = f"brooklyn_mens_volleyball_{year}_{kind}_stats.csv"
        path = FOLDER / filename

        if not path.exists():
            errors.append(f"MISSING FILE: {filename}")
            continue

        with path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames or []
            rows = list(reader)

        if not rows:
            errors.append(f"EMPTY FILE: {filename}")
            continue

        if not {"Season", "Team"}.issubset(headers):
            errors.append(f"MISSING COLUMNS: {filename}")
            continue

        for row_number, row in enumerate(rows, start=2):
            if row["Season"] != str(year):
                errors.append(
                    f"WRONG SEASON: {filename}, row {row_number}"
                )

            if any(value is None for value in row.values()):
                errors.append(
                    f"MALFORMED ROW: {filename}, row {row_number}"
                )

        total_rows += len(rows)
        print(f"OK: {year} {kind} ({len(rows)} rows)")

print("\n========== VALIDATION SUMMARY ==========")
print(f"Expected files: {len(YEARS) * len(KINDS)}")
print(f"Total data rows checked: {total_rows}")
print(f"Problems found: {len(errors)}")

for error in errors:
    print("ERROR:", error)

if not errors:
    print("PASS: All files exist and basic structural checks passed!")