**Brooklyn College Volleyball Statistics — 2025**

**Project Overview:**
This repository contains Python web-scraping scripts and CSV datasets for Brooklyn College's 2025 men's and women's volleyball teams.
The project contributes to the development of structured, reproducible sports datasets for CUNY sports analytics research.

**Data Sources** - 
Statistics were collected from the official Brooklyn College Athletics website:

**Men's Volleyball — 2025 Statistics**__ (https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/2025)
**Women's Volleyball — 2025 Statistics **__(https://www.brooklyncollegeathletics.com/sports/womens-volleyball/stats/2025)

**Statistics Collected** - 
For each team, the scripts extract three types of information from the website:

Individual → Overall → Offensive and Defensive Statistics: Season-level player statistics, including a combined offensive and defensive dataset.

Match-By-Match → Brooklyn: Team performance for each match during the 2025 season.

Overall Team Statistics: Season-level team statistics comparing Brooklyn College with its opponents.

**Repository Contents** - 
The repository contains:
4 Python scripts: Two original volleyball scrapers and two scripts for Overall Team Statistics.
8 CSV datasets: Four for men's volleyball and four for women's volleyball.

**Each team's datasets include:**
Individual offensive statistics
Combined individual offensive and defensive statistics
Match-by-match Brooklyn team statistics
Overall team statistics comparing Brooklyn and opponents

**Data Processing** - 
The Python scripts use requests, BeautifulSoup, and pandas to retrieve HTML statistics tables, extract relevant information, clean and organize the data, and export it to CSV files.
The Overall Team Statistics datasets preserve the original categories: Attack, Set, Serve, Receptions, Defense, and Blocking.

**Current Scope** - 
This repository currently covers the 2025 season only for Brooklyn College men's and women's volleyball.
Conference-specific individual statistics, separate overall opponent match-by-match datasets, and additional seasons have not yet been collected.

**Development Notes** - 
The scripts were developed with assistance from ChatGPT for Python programming, HTML table extraction, data cleaning, and debugging. The resulting datasets were inspected and checked against the source table structure.
