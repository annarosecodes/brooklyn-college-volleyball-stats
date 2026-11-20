# Brooklyn College Volleyball Statistics

## Project Overview

This repository contains Python web-scraping scripts and CSV datasets for Brooklyn College men's and women's volleyball teams.

The project contributes to the development of structured, reproducible sports datasets for CUNY sports analytics research.

The goal is to collect, preserve, and organize historical volleyball statistics while making it possible to compare men's and women's performance across seasons.

The project includes statistical records from **2006 through 2026**, covering **39 eligible team-seasons**. Men's and women's data are combined within the same statistical-category CSV files, with separate columns identifying the season and gender.

## Data Sources

Statistics were collected from the official [Brooklyn College Athletics website](https://www.brooklyncollegeathletics.com/).

Official season statistics include:

- [Men's Volleyball — 2026 Statistics](https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/2026)
- [Women's Volleyball — 2026 Statistics](https://www.brooklyncollegeathletics.com/sports/womens-volleyball/stats/2026)
- [Men's Volleyball — 2025 Statistics](https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/2025)
- [Women's Volleyball — 2025 Statistics](https://www.brooklyncollegeathletics.com/sports/womens-volleyball/stats/2025)

Earlier seasons were collected from Brooklyn College Athletics' archived statistics reports and historical season pages.

The source reports vary in structure and terminology depending on the season.

## Season Coverage

### Women's Volleyball (2006–2026)

**Included seasons:** 2006–2019 and 2021–2026.

**Excluded season:** 2020.

The women's collection contains **20 eligible seasons**.

### Men's Volleyball (2007–2026)

**Included seasons:** 2007–2020 and 2022–2026.

**Excluded season:** 2021.

The men's collection contains **19 eligible seasons**.

### COVID-19 Pandemic Cancellations

The Brooklyn College women's volleyball **2020 season** and men's volleyball **2021 season** were canceled due to the COVID-19 pandemic.

These seasons were intentionally excluded from the dataset because the competitions did not take place.

**They are not considered missing, lost, or unsuccessfully collected statistical records.**

The collection therefore contains **39 eligible team-seasons** across both teams.

## Final Datasets

The final submission datasets are located in the `brooklyn_college_volleyball/` folder.

Each CSV combines men's and women's records by statistical category, rather than storing each gender in separate files.

### Primary Analytical Datasets

| File | Description |
|---|---|
| `brooklyn_college_volleyball_team_statistics.csv` | Season-level team statistics, including offensive, defensive, serving, and blocking categories. Preserves Brooklyn College and opponent totals. |
| `brooklyn_college_volleyball_individual_statistics.csv` | Player-level statistics, including kills, assists, hitting percentage, service aces, digs, and blocks. |
| `brooklyn_college_volleyball_category_leaders.csv` | Statistical leaders and rankings across individual performance categories. |
| `brooklyn_college_volleyball_match_statistics.csv` | Match-by-match statistics for Brooklyn College and its opponents where available. |
| `brooklyn_college_volleyball_per_match_statistics.csv` | Team statistical averages reported in modern source tables, primarily per-set measures. |
| `brooklyn_college_volleyball_historical_match_results.csv` | Historical match dates, opponents, wins and losses, match scores, game scores, attendance, and conference indicators. |
| `brooklyn_college_volleyball_historical_game_tables.csv` | Additional historical game-statistics records preserved from older reports. |
| `brooklyn_college_volleyball_dataset_coverage.csv` | Dataset availability by season, gender, and statistical category, including excluded seasons. |

### Original Statistical Table Preservation

The `brooklyn_college_volleyball/combined_by_category/` folder contains **12 additional CSV files** that preserve original statistical tables grouped by category.

These include:

- Team statistics
- Individual statistics
- Match statistics
- Per-match statistical averages
- Match highs
- Category leaders
- Combined team statistics
- Volleyball statistics
- Match wins by sets
- Sets won by set
- Points by set
- Additional match statistics

All 12 files follow the naming convention:

`brooklyn_college_volleyball_TABLE_NAME.csv`

The original-table preservation datasets retain source information such as original row values, table identifiers, and JSON representations of HTML cells where applicable.

These files are intended to preserve the original statistical information and support verification. The primary analytical datasets provide more accessible structures for comparing performance.

## Historical Data and Reporting Differences

Brooklyn College Athletics' statistical reporting formats changed over time.

Older reports may contain different table structures, headings, and statistical categories than newer reports.

Some historical reports measure performance **per game**, while modern reports use **per set**.

These measures are not automatically treated as equivalent.

The collection preserves original statistical values and terminology rather than silently converting historical statistics into modern formats.

Not every eligible season includes every type of statistical table. For example, detailed modern match-by-match statistics are available for fewer seasons than overall team and individual statistics.

These differences are documented in `brooklyn_college_volleyball_dataset_coverage.csv`.

The two canceled COVID-19 seasons are classified separately from unavailable statistical tables within seasons that were played.

## 2026 Data Collection Note

The 2026 statistics reflect the official Brooklyn College Athletics reports available when the data was collected.

They should not automatically be interpreted as finalized season-end totals. The published statistics may change if Brooklyn College Athletics updates its records.

The collection preserves the source records as published, including original player names and other identifying fields. Potential spelling inconsistencies in source records are not silently corrected or merged.

## Data Processing

Python scripts use `requests`, `BeautifulSoup`, and `pandas` where applicable to retrieve statistics tables, extract information, clean and organize records, and export CSV files.

The data collection and processing workflow includes:

1. Retrieving modern HTML statistics tables and historical statistical reports.
2. Preserving original statistical rows, headers, and source information.
3. Extracting team, individual, match, and statistical-leader records.
4. Combining men's and women's records into shared category-based datasets.
5. Retaining historical reporting distinctions and opponent statistics.
6. Checking season coverage and validating dataset structures.

The team-statistics datasets preserve original categories such as Attack, Set, Serve, Receptions, Defense, and Blocking where reported.

Additional scripts support historical season extraction, player-record matching, CSV organization, and data validation.

## Data Validation

The collection was checked for:

- Expected source tables and historical report sections.
- Correct season and gender identifiers.
- Coverage of the eligible men's and women's seasons.
- Presence of records in the final statistical-category datasets.
- Preservation of original statistical values and source references.
- Exclusion of the two canceled COVID-19 seasons from eligible-season counts.

The primary team-statistics, individual-statistics, and category-leaders datasets contain records for all **39 eligible team-seasons**.

Some statistical categories are available for fewer seasons because historical source reports differ from modern reports.

Structural and coverage checks do not constitute independent verification of every statistical value against the original athletics records.

## Comparative Analysis

The combined datasets support comparisons between Brooklyn College men's and women's volleyball teams across available seasons.

Potential areas of analysis include:

- Team offensive and defensive performance.
- Kills, assists, service aces, digs, and blocks.
- Individual player performance and statistical leaders.
- Match results and performance trends where comparable records are available.
- Differences in historical reporting and statistical availability.

Comparisons must account for differences in matches or sets played, historical statistical definitions, and incomplete category-level coverage.

## File Naming Convention

Final submission CSV files follow this pattern:

`brooklyn_college_volleyball_TABLE_NAME.csv`

For example:

`brooklyn_college_volleyball_individual_statistics.csv`

The filenames identify the statistical category, while the records within each file identify the season and gender.

Earlier working files and collection scripts may retain their original filenames to preserve the existing processing workflow.

## Development Notes

The scripts were developed with assistance from ChatGPT for Python programming, HTML table extraction, data cleaning, debugging, and validation.

The resulting datasets were inspected against source table structures and checked for basic structural consistency.

Original statistical records are retained to support traceability and future verification.

## Project Scope

This project covers Brooklyn College men's and women's volleyball statistical records through the 2026 source reports.

The eligible season ranges are:

- **Women:** 2006–2019 and 2021–2026.
- **Men:** 2007–2020 and 2022–2026.

The women's 2020 and men's 2021 seasons are excluded due to COVID-19 cancellations, not missing-data collection failures.

The repository includes both analysis-ready combined datasets and original-table preservation datasets to support reproducible sports analytics research.
