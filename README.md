# Brooklyn College Volleyball Statistics

## Project Overview

This repository contains Python web-scraping scripts and CSV datasets for Brooklyn College men's and women's volleyball teams.

The project contributes to the development of structured, reproducible sports datasets for CUNY sports analytics research.

The repository currently includes historical men's volleyball statistics from 2007–2025 and women's volleyball statistics for 2025.

## Data Sources

Statistics were collected from the official Brooklyn College Athletics website.

- [Men's Volleyball — 2025 Statistics](https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/2025)
- [Women's Volleyball — 2025 Statistics](https://www.brooklyncollegeathletics.com/sports/womens-volleyball/stats/2025)

Historical men's volleyball statistics were collected from Brooklyn College Athletics' archived statistics pages and newer season statistics pages.

## Men's Volleyball — Historical Statistics (2007–2025)

The historical men's volleyball dataset includes:

- **18 available seasons:** 2007–2020 and 2022–2025
- **54 historical CSV files**
- **1,046 data rows**
- **Three datasets per season:** individual, match, and team statistics

The 2021 season is excluded because athletics competitions were canceled during the COVID-19 pandemic.

### Historical Dataset Types

**Individual Statistics:** Player-level offensive and defensive statistics.

**Match Statistics:** Historical match results or match-by-match team performance statistics, depending on the season.

**Team Statistics:** Season-level statistics comparing Brooklyn College with its opponents.

### File Naming Convention

Historical files follow this naming pattern:

`brooklyn_mens_volleyball_YEAR_TYPE_stats.csv`

Where `TYPE` is `individual`, `match`, or `team`.

### Historical Data Notes

The source website's statistics format changed over time.

- **2007–2014:** Historical statistics tables and match results.
- **2015–2020 and 2022–2025:** Newer statistics tables and match-by-match performance data.

Some column names and available statistics differ between these periods. The historical datasets preserve information from their respective sources rather than assuming every season uses an identical schema.

## Women's Volleyball — 2025

The repository includes four original women's volleyball datasets for the 2025 season:

- Individual offensive statistics
- Combined individual offensive and defensive statistics
- Match-by-match Brooklyn team statistics
- Overall team statistics comparing Brooklyn College and its opponents

Historical women's volleyball statistics are planned for future development.

## Data Processing

Python scripts use `requests`, `BeautifulSoup`, and `pandas` where applicable to retrieve HTML statistics tables, extract information, clean and organize records, and export CSV files.

The team-statistics datasets preserve the original categories: Attack, Set, Serve, Receptions, Defense, and Blocking.

Additional scripts support historical season scraping, player-record matching, CSV standardization, and data validation.

## Data Validation

A validation script checks historical men's volleyball datasets for:

- Expected CSV files
- Required season and team columns
- Correct season identifiers
- Malformed rows and empty datasets

**Validation results:** All 54 historical men's volleyball CSV files passed basic structural checks, with zero reported problems.

These checks do not independently verify every statistic against the original athletics records.

## Current Scope and Future Development

- Men's historical volleyball statistics: 2007–2025, excluding 2021
- Women's volleyball statistics: 2025
- Planned: Historical women's volleyball statistics

Conference-specific individual statistics and separate opponent match-by-match datasets are not yet included in the historical collection.

## Development Notes

The scripts were developed with assistance from ChatGPT for Python programming, HTML table extraction, data cleaning, debugging, and validation.

The resulting datasets were inspected against source table structures and checked for basic structural consistency.
