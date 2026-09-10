# WNBA Player Data

`wnba_2026_players.csv` contains WNBA player salary and performance statistics for use in DATA 110: Thinking with Data.

## Source

Data were retrieved from the **Her Hoop Stats WNBA Salary Cap Database**:

https://herhoopstats.com/salary-cap-sheet/wnba/players/

The original table was imported using `pandas.read_html()` and then simplified for classroom use.

## Data Preparation

The following changes were made to the original table:

* Player names were cleaned to remove abbreviated duplicate names included in the HTML table.
* Players with multiple entries were removed because their salary information was ambiguous, likely reflecting changes in team affiliation.
* Salary values were converted to numeric values by removing `$` and `,`.
* Shooting percentages were converted to numeric values by removing `%`.
* A subset of columns was retained to make the dataset easier to explore in an introductory data science course.

The resulting CSV is a fixed snapshot of the source data so that all students work with the same dataset.

## Citation

Her Hoop Stats, *WNBA Salary Cap Database*.
