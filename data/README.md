# Data Notes

This folder contains small teaching datasets for DATA 110: Thinking with Data.

## Basketball Player Data

`nba_2026_players.csv` and `wnba_2026_players.csv` contain player salary and performance statistics for use in DATA 110: Thinking with Data.

The files have the same columns, column order, and basic units:

`Player`, `2026 Salary`, `G`, `GS`, `MIN`, `PTS`, `FG%`, `2P%`, `3P%`, `TRB`, `AST`, `STL`, `BLK`, `TOV`

### Column Definitions

* `Player`: Player name.
* `2026 Salary`: Player salary in dollars for the 2026-related season in the source data.
* `G`: Games played.
* `GS`: Games started.
* `MIN`: Minutes played per game.
* `PTS`: Points scored per game.
* `FG%`: Field goal percentage, as numeric percentage points.
* `2P%`: Two-point field goal percentage, as numeric percentage points.
* `3P%`: Three-point field goal percentage, as numeric percentage points.
* `TRB`: Total rebounds per game.
* `AST`: Assists per game.
* `STL`: Steals per game.
* `BLK`: Blocks per game.
* `TOV`: Turnovers per game.

## NBA Player Data

### Sources

Data are retrieved by `scripts/build_nba_2026_players.py` from Basketball Reference.

* Contracts: https://www.basketball-reference.com/contracts/players.html
* Regular-season per-game statistics: https://www.basketball-reference.com/leagues/NBA_2026_per_game.html

Retrieval date for the committed snapshot: 2026-09-10.

### Source Tables

The contracts page lists Basketball Reference player contract salary rows by NBA season. The script uses the `Salary 2026-27` column and stores it as `2026 Salary` so the column name parallels `wnba_2026_players.csv`.

The statistics page uses Basketball Reference's season-ending convention: `NBA_2026` is the 2025-26 NBA season. The script uses the first table on that page, which is the regular-season standard per-game player statistics table.

### Cleaning and Merging Decisions

Player names are cleaned only for matching. The matching key removes trailing asterisks, normalizes apostrophes and hyphens, removes accent marks, lowercases names, and collapses punctuation and repeated spaces. The displayed `Player` value in the final CSV comes from the contracts table.

The contracts table is used as the roster base because the WNBA comparison file is salary-list oriented. Players with a 2026-27 salary remain in the NBA output even when they do not have a 2025-26 regular-season stat line. Players who appear in the statistics table but not the contracts table are reported by the script and left out of the salary-based output.

Basketball Reference includes repeated header/separator rows in the contracts HTML table. These rows do not represent players and are explicitly removed by the script.

Some players appear more than once in the contracts table with different team or guaranteed-salary entries. The script removes players with duplicate contract rows so the classroom file does not require students to interpret team-change or contract accounting cases.

Players who changed teams during the 2025-26 season appear more than once in the per-game statistics table. Basketball Reference provides a season-total row labeled with a multi-team code such as `2TM` or `3TM`, but the script removes these duplicate-player cases from the final output to match the WNBA data-building rule and keep the introductory dataset easier to reason about.

Salary values are stored as numeric dollars. Basketball Reference shooting percentages are source proportions, such as `0.476`; the script multiplies them by 100 so `FG%`, `2P%`, and `3P%` use numeric percentage points like the WNBA file. Games, games started, minutes, points, rebounds, assists, steals, blocks, and turnovers are converted to numeric columns.

### NBA and WNBA Comparability

The NBA and WNBA CSV files use the same classroom schema:

`Player`, `2026 Salary`, `G`, `GS`, `MIN`, `PTS`, `FG%`, `2P%`, `3P%`, `TRB`, `AST`, `STL`, `BLK`, `TOV`

In the NBA file, `MP` from Basketball Reference is renamed to `MIN` to match the WNBA file.

Some quantities are not truly comparable:

* `2026 Salary` does not represent the same labor market or salary-cap system. NBA salaries are Basketball Reference 2026-27 salary figures; WNBA salaries come from the existing WNBA salary file.
* The NBA statistics are 2025-26 NBA regular-season per-game statistics. The WNBA file should be treated as its own fixed snapshot from its original source.
* NBA and WNBA seasons have different schedules, roster rules, league contexts, and source providers.
* Shooting percentage columns are numeric percent points in both CSV files.
* The two CSV files contain the same variables, but those variables still come from different source systems and should not be interpreted as perfectly equivalent measures of labor-market value or league performance context.

## WNBA Player Data

### Source

Data are retrieved by `scripts/build_wnba_2026_players.py` from the Her Hoop Stats WNBA Salary Cap Database:

https://herhoopstats.com/salary-cap-sheet/wnba/players/

The original table is imported using `pandas.read_html()` and then simplified for classroom use.

Retrieval date for the committed snapshot: 2026-09-10.

### Source Table

The Her Hoop Stats table combines WNBA player salary information with per-game player statistics. The script keeps the shared classroom columns listed above.

### Cleaning Decisions

Player names are cleaned to remove abbreviated duplicate names included in the HTML table.

Players with multiple entries are removed because their salary information is ambiguous, likely reflecting changes in team affiliation. This matches the NBA file's rule for removing players with duplicate contract or statistics rows.

Salary values are stored as numeric dollars. Shooting percentages are stored as numeric percentage points. Games, games started, minutes, points, rebounds, assists, steals, blocks, and turnovers are converted to numeric columns.

The resulting CSV is a fixed snapshot of the source data so that all students work with the same dataset.

### Citation

Her Hoop Stats, *WNBA Salary Cap Database*.
