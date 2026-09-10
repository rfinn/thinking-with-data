# Data Notes

This folder has small datasets for DATA 110: Thinking with Data.

## Basketball Player Data

The files `nba_2026_players.csv` and `wnba_2026_players.csv` are meant to be used together. They give students a way to compare NBA and WNBA player salaries and per-game performance statistics without needing to wrangle the original web tables first.

Both files use the same columns, in the same order:

`Player`, `2026 Salary`, `G`, `GS`, `MIN`, `PTS`, `FG%`, `2P%`, `3P%`, `TRB`, `AST`, `STL`, `BLK`, `TOV`

### Column Definitions

* `Player`: Player name.
* `2026 Salary`: Player salary in dollars for the 2026-related season in the source data.
* `G`: Games played.
* `GS`: Games started.
* `MIN`: Minutes played per game.
* `PTS`: Points scored per game.
* `FG%`: Field goal percentage, written as a regular percent instead of a proportion.
* `2P%`: Two-point field goal percentage.
* `3P%`: Three-point field goal percentage.
* `TRB`: Total rebounds per game.
* `AST`: Assists per game.
* `STL`: Steals per game.
* `BLK`: Blocks per game.
* `TOV`: Turnovers per game.

## NBA Player Data

The NBA file is built by `scripts/build_nba_2026_players.py`.

It uses two Basketball Reference pages:

* Player contracts: https://www.basketball-reference.com/contracts/players.html
* Regular-season per-game statistics: https://www.basketball-reference.com/leagues/NBA_2026_per_game.html

Retrieval date for this snapshot: 2026-09-10.

The contracts page lists player salaries by NBA season. The script uses the `Salary 2026-27` column and calls it `2026 Salary` so it lines up with the WNBA file.

The stats page follows Basketball Reference's naming convention: `NBA_2026` means the 2025-26 NBA season. The script uses the regular-season per-game player table. Basketball Reference calls minutes per game `MP`, but the CSV uses `MIN` to match the WNBA file.

### NBA Cleaning Choices

Player names are cleaned behind the scenes so the salary table and stats table can be matched. The cleaning removes things like accent marks, extra punctuation, trailing asterisks, and repeated spaces. The final `Player` names still come from the contracts table.

The contracts table is the starting point for the NBA file because this is mostly a salary-and-stats comparison dataset. Players with a 2026-27 salary stay in the file even if they do not have a 2025-26 regular-season stat line.

Basketball Reference includes repeated header/separator rows in the contracts HTML table. Those are not players, so the script removes them.

Some players show up more than once in the contracts table, usually because of team or contract accounting details. The script removes those players instead of asking students to sort out what happened.

Players who changed teams during the 2025-26 season can show up more than once in the stats table. Basketball Reference often includes a total row such as `2TM` or `3TM`, but for this introductory dataset the script removes those multi-entry players. That keeps the file easier to analyze in a first data class.

Salary values are stored as numeric dollars. Shooting percentages are converted from Basketball Reference proportions, such as `0.476`, into regular percentage values, such as `47.6`.

When you run the script, it prints the players that did not match across the salary and stats tables. Those are reported on purpose so the data cleaning choices are visible.

## WNBA Player Data

The WNBA file is built by `scripts/build_wnba_2026_players.py`.

It uses the Her Hoop Stats WNBA Salary Cap Database:

https://herhoopstats.com/salary-cap-sheet/wnba/players/

Retrieval date for this snapshot: 2026-09-10.

The Her Hoop Stats table already combines WNBA salary information with per-game player statistics. The script keeps the shared classroom columns listed above.

### WNBA Cleaning Choices

Player names are cleaned to remove abbreviated duplicate names that appear inside some HTML table cells.

Players with multiple entries are removed because their salary information is ambiguous, likely because of team changes or related roster movement. This is the same classroom rule used in the NBA file: if a player has multiple source rows, leave that case out of the student-facing dataset.

Salary values are stored as numeric dollars. Shooting percentages are stored as regular percentage values. Games, games started, minutes, points, rebounds, assists, steals, blocks, and turnovers are converted to numeric columns.

## Comparing NBA and WNBA

The two CSV files have the same variables, which makes them convenient for side-by-side analysis. Still, the numbers do not come from identical worlds.

A few things to keep in mind:

* `2026 Salary` does not mean the same labor market in both leagues. NBA and WNBA contracts happen under very different salary systems.
* NBA salary values come from Basketball Reference's 2026-27 contract table. WNBA salary values come from Her Hoop Stats.
* NBA stats are from the 2025-26 NBA regular season. The WNBA file is its own fixed snapshot from Her Hoop Stats.
* NBA and WNBA seasons have different schedules, roster rules, and league contexts.
* Shooting percentage columns are numeric percentage values in both files.

That means these files are good for asking questions, making graphs, and noticing patterns. They are not meant to prove that the leagues are directly equivalent in every way.

## Citation

Basketball Reference, player contracts and 2025-26 per-game statistics.

Her Hoop Stats, WNBA Salary Cap Database.
