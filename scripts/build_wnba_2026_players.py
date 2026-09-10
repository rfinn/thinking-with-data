#!/usr/bin/env python3
"""Build the WNBA player dataset for DATA 110.

Source:
- Her Hoop Stats WNBA Salary Cap Database:
  https://herhoopstats.com/salary-cap-sheet/wnba/players/

The source table combines salary information with per-game player statistics.
This script keeps the same classroom columns used by the NBA dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pandas.api.types import is_numeric_dtype


SOURCE_URL = "https://herhoopstats.com/salary-cap-sheet/wnba/players/"

OUTPUT_COLUMNS = [
    "Player",
    "2026 Salary",
    "G",
    "GS",
    "MIN",
    "PTS",
    "FG%",
    "2P%",
    "3P%",
    "TRB",
    "AST",
    "STL",
    "BLK",
    "TOV",
]

NUMERIC_COLUMNS = [col for col in OUTPUT_COLUMNS if col != "Player"]
INTEGER_COLUMNS = ["2026 Salary", "G", "GS"]
ONE_DECIMAL_COLUMNS = ["MIN", "PTS", "FG%", "2P%", "3P%", "TRB", "AST", "STL", "BLK", "TOV"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def clean_player_names(players: pd.Series) -> pd.Series:
    """Remove duplicate abbreviated names embedded in Her Hoop Stats cells."""
    return players.astype("string").str.split(r"\s{2,}", regex=True).str[0].str.strip()


def parse_money(values: pd.Series) -> pd.Series:
    return pd.to_numeric(
        values.astype("string").str.replace("$", "", regex=False).str.replace(",", "", regex=False),
        errors="coerce",
    )


def parse_percent(values: pd.Series) -> pd.Series:
    return pd.to_numeric(values.astype("string").str.replace("%", "", regex=False), errors="coerce")


def build_dataset() -> pd.DataFrame:
    tables = pd.read_html(SOURCE_URL)
    if not tables:
        raise ValueError("No tables found on Her Hoop Stats source page")

    raw = tables[0].copy()
    missing = set(OUTPUT_COLUMNS) - set(raw.columns)
    if missing:
        raise ValueError(f"WNBA source table missing expected columns: {sorted(missing)}")

    wnba = raw.copy()
    wnba["Player"] = clean_player_names(wnba["Player"])

    duplicated = wnba.loc[wnba["Player"].duplicated(keep=False), "Player"].dropna().unique().tolist()
    wnba = wnba.loc[~wnba["Player"].duplicated(keep=False)].copy()

    wnba["2026 Salary"] = parse_money(wnba["2026 Salary"])
    for col in ["FG%", "2P%", "3P%"]:
        wnba[col] = parse_percent(wnba[col])

    final = wnba[OUTPUT_COLUMNS].copy()
    for col in NUMERIC_COLUMNS:
        final[col] = pd.to_numeric(final[col], errors="coerce")
    for col in INTEGER_COLUMNS:
        final[col] = final[col].round().astype("Int64")
    for col in ONE_DECIMAL_COLUMNS:
        final[col] = final[col].round(1)

    print("WNBA source:")
    print(f"- URL: {SOURCE_URL}")
    print("- Represents Her Hoop Stats WNBA player salary and per-game statistic rows.")
    print(f"- Raw rows: {len(raw)}")
    print(f"- Removed duplicate player rows with ambiguous salary/stat rows: {len(raw) - len(wnba)}")
    if duplicated:
        print("- Duplicate players removed: " + ", ".join(duplicated))

    return final.reset_index(drop=True)


def run_sanity_checks(frame: pd.DataFrame) -> None:
    if list(frame.columns) != OUTPUT_COLUMNS:
        raise AssertionError(f"Unexpected output columns: {list(frame.columns)}")
    if frame.empty:
        raise AssertionError("Final dataset has no rows")
    if frame["Player"].isna().any():
        raise AssertionError("Final dataset has missing player names")
    duplicate_players = frame.loc[frame["Player"].duplicated(), "Player"].tolist()
    if duplicate_players:
        raise AssertionError(f"Final dataset has duplicate players: {duplicate_players}")

    non_numeric = [col for col in NUMERIC_COLUMNS if not is_numeric_dtype(frame[col])]
    if non_numeric:
        raise AssertionError(f"Columns are not numeric dtype: {non_numeric}")

    print("\nSanity checks:")
    print(f"- Final rows: {len(frame)}")
    print("- Duplicate players: 0")
    print("- Numeric dtype columns verified: " + ", ".join(NUMERIC_COLUMNS))
    print("- Missing values by column:")
    print(frame.isna().sum().to_string())


def main() -> int:
    root = project_root()
    output_path = root / "data" / "wnba_2026_players.csv"

    wnba = build_dataset()
    run_sanity_checks(wnba)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wnba.to_csv(output_path, index=False)
    print(f"\nSaved {output_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
