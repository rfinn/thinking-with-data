#!/usr/bin/env python3
"""Build a salary-plus-stats NBA player dataset for DATA 110.

Sources:
- Basketball Reference player contracts:
  https://www.basketball-reference.com/contracts/players.html
  This page lists NBA player contract salary figures by season. The builder
  uses the "Salary 2026-27" column and saves it as "2026 Salary" so it is
  parallel to the existing WNBA classroom file.

- Basketball Reference regular-season per-game player stats:
  https://www.basketball-reference.com/leagues/NBA_2026_per_game.html
  Basketball Reference's NBA_2026 season page represents the 2025-26 NBA
  regular season. The first table is the standard per-game player table.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
import re
import unicodedata
from urllib.request import Request, urlopen

import pandas as pd
from pandas.api.types import is_numeric_dtype


CONTRACTS_URL = "https://www.basketball-reference.com/contracts/players.html"
STATS_URL = "https://www.basketball-reference.com/leagues/NBA_2026_per_game.html"

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


def read_html_tables(url: str) -> list[pd.DataFrame]:
    """Read source HTML with a browser-like user agent."""
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    return pd.read_html(StringIO(html))


def flatten_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Flatten Basketball Reference's two-level contract header."""
    frame = frame.copy()
    if isinstance(frame.columns, pd.MultiIndex):
        frame.columns = [
            lower if str(upper).startswith("Unnamed") else f"{upper} {lower}"
            for upper, lower in frame.columns
        ]
    return frame


def clean_player_name(name: object) -> str:
    """Create a stable key for matching names across Basketball Reference tables."""
    if pd.isna(name):
        return ""
    cleaned = str(name)
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = cleaned.replace("’", "'").replace("‘", "'")
    cleaned = cleaned.replace("`", "'").replace("´", "'")
    cleaned = cleaned.replace("‑", "-").replace("–", "-").replace("—", "-")
    cleaned = re.sub(r"\*+$", "", cleaned).strip()
    cleaned = unicodedata.normalize("NFKD", cleaned)
    cleaned = "".join(char for char in cleaned if not unicodedata.combining(char))
    cleaned = re.sub(r"[^A-Za-z0-9]+", " ", cleaned).lower().strip()
    return re.sub(r"\s+", " ", cleaned)


def parse_money(value: object) -> float:
    if pd.isna(value):
        return float("nan")
    text = re.sub(r"[^0-9.-]", "", str(value))
    return pd.to_numeric(text, errors="coerce")


def print_list(title: str, values: list[str]) -> None:
    print(f"\n{title} ({len(values)}):")
    if values:
        print(", ".join(values))
    else:
        print("None")


def load_contracts() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = flatten_columns(read_html_tables(CONTRACTS_URL)[0])
    required = {"Rk", "Player", "Tm", "Salary 2026-27"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Contracts table missing expected columns: {sorted(missing)}")

    non_player = raw["Player"].isna() | raw["Player"].astype(str).eq("Player")
    contracts = raw.loc[~non_player].copy()
    contracts["2026 Salary"] = contracts["Salary 2026-27"].map(parse_money)
    contracts["player_key"] = contracts["Player"].map(clean_player_name)

    if contracts["player_key"].eq("").any():
        bad = contracts.loc[contracts["player_key"].eq(""), "Player"].tolist()
        raise ValueError(f"Blank player names after cleaning: {bad}")
    if contracts["2026 Salary"].isna().any():
        bad = contracts.loc[contracts["2026 Salary"].isna(), "Player"].tolist()
        raise ValueError(f"Missing 2026-27 salary values: {bad}")

    duplicate_rows = contracts.loc[contracts.duplicated("player_key", keep=False)].copy()
    contracts_one = contracts.loc[~contracts["player_key"].duplicated(keep=False)].copy()

    print("Contracts source:")
    print(f"- URL: {CONTRACTS_URL}")
    print("- Represents Basketball Reference player contract salary rows by NBA season.")
    print(f"- Raw rows: {len(raw)}")
    print(f"- Removed non-player/repeated-header rows: {int(non_player.sum())}")
    print(f"- Player salary rows after filtering: {len(contracts)}")
    print(f"- Removed duplicate player salary rows: {len(contracts) - len(contracts_one)}")

    if not duplicate_rows.empty:
        duplicate_summary = (
            duplicate_rows.sort_values(["Player", "Tm"])[
                ["Player", "Tm", "Salary 2026-27", "Guaranteed"]
            ]
            .to_string(index=False)
        )
        print("\nDuplicate contract rows removed:")
        print(duplicate_summary)

    return contracts_one, duplicate_rows


def load_stats() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = read_html_tables(STATS_URL)[0]
    required = {"Player", "Team", "G", "GS", "MP", "PTS", "FG%", "2P%", "3P%", "TRB", "AST", "STL", "BLK", "TOV"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Stats table missing expected columns: {sorted(missing)}")

    non_player = raw["Player"].isna() | raw["Player"].astype(str).isin(["Player", "League Average"])
    stats = raw.loc[~non_player].copy()
    stats["player_key"] = stats["Player"].map(clean_player_name)

    duplicated = stats.loc[stats.duplicated("player_key", keep=False)].copy()
    stats_one = stats.loc[~stats["player_key"].duplicated(keep=False)].copy()

    keep = {
        "Player": "stats_Player",
        "Team": "stats_Team",
        "G": "G",
        "GS": "GS",
        "MP": "MIN",
        "PTS": "PTS",
        "FG%": "FG%",
        "2P%": "2P%",
        "3P%": "3P%",
        "TRB": "TRB",
        "AST": "AST",
        "STL": "STL",
        "BLK": "BLK",
        "TOV": "TOV",
        "player_key": "player_key",
    }
    stats_one = stats_one[list(keep)].rename(columns=keep)

    for col in ["G", "GS", "MIN", "PTS", "FG%", "2P%", "3P%", "TRB", "AST", "STL", "BLK", "TOV"]:
        stats_one[col] = pd.to_numeric(stats_one[col], errors="coerce")
    for col in ["FG%", "2P%", "3P%"]:
        stats_one[col] = stats_one[col] * 100

    print("\nStats source:")
    print(f"- URL: {STATS_URL}")
    print("- Represents Basketball Reference 2025-26 NBA regular-season per-game player statistics.")
    print(f"- Raw rows: {len(raw)}")
    print(f"- Removed non-player rows, including League Average: {int(non_player.sum())}")
    print(f"- Player stat rows after filtering: {len(stats)}")
    print(f"- Removed duplicate player stat rows: {len(stats) - len(stats_one)}")
    if not duplicated.empty:
        duplicate_names = sorted(duplicated["Player"].dropna().unique())
        print("- Duplicate-stat players removed: " + ", ".join(duplicate_names))

    return stats_one, duplicated


def build_dataset() -> pd.DataFrame:
    contracts, _duplicate_contracts = load_contracts()
    stats, duplicate_stats = load_stats()

    salary = contracts[["Player", "2026 Salary", "player_key"]].copy()
    duplicate_stat_keys = set(duplicate_stats["player_key"])
    removed_for_duplicate_stats = salary.loc[
        salary["player_key"].isin(duplicate_stat_keys),
        "Player",
    ].tolist()
    salary = salary.loc[~salary["player_key"].isin(duplicate_stat_keys)].copy()

    merged = salary.merge(stats, how="left", on="player_key", indicator=True)

    salary_only = merged.loc[merged["_merge"].eq("left_only"), "Player"].tolist()
    stats_only = stats.loc[~stats["player_key"].isin(salary["player_key"]), "stats_Player"].tolist()

    print_list("Players removed from final output because they had multiple stat rows", removed_for_duplicate_stats)
    print_list("Players in contracts table but not in 2025-26 per-game stats", salary_only)
    print_list("Players in 2025-26 per-game stats but not in contracts table", stats_only)

    final = merged[OUTPUT_COLUMNS].copy()
    for col in NUMERIC_COLUMNS:
        final[col] = pd.to_numeric(final[col], errors="coerce")
    for col in INTEGER_COLUMNS:
        final[col] = final[col].round().astype("Int64")
    for col in ONE_DECIMAL_COLUMNS:
        final[col] = final[col].round(1)

    return final


def compare_to_wnba_schema(root: Path, nba: pd.DataFrame) -> None:
    wnba_path = root / "data" / "wnba_2026_players.csv"
    if not wnba_path.exists():
        print("\nWNBA schema comparison skipped: data/wnba_2026_players.csv not found.")
        return

    wnba = pd.read_csv(wnba_path, nrows=5)
    nba_cols = list(nba.columns)
    wnba_cols = list(wnba.columns)
    shared = [col for col in nba_cols if col in wnba_cols]
    wnba_only = [col for col in wnba_cols if col not in nba_cols]
    nba_only = [col for col in nba_cols if col not in wnba_cols]

    print("\nNBA/WNBA schema comparison:")
    print(f"- NBA columns: {nba_cols}")
    print(f"- WNBA columns: {wnba_cols}")
    print(f"- Shared columns: {shared}")
    print(f"- WNBA-only columns: {wnba_only}")
    print(f"- NBA-only columns: {nba_only}")
    print("- Comparability caveats:")
    print("  * NBA salary is Basketball Reference 2026-27 salary; WNBA salary is the existing file's 2026 salary.")
    print("  * NBA stats are Basketball Reference 2025-26 regular-season per-game stats.")
    print("  * Shooting percentages are numeric percent points in the NBA output, not proportions.")
    print("  * The CSV schemas now match, but salary sources, season lengths, and league contexts still differ.")


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
    if frame["2026 Salary"].isna().any():
        bad = frame.loc[frame["2026 Salary"].isna(), "Player"].tolist()
        raise AssertionError(f"Missing salary values in final output: {bad}")

    missing_counts = frame.isna().sum()
    print("\nSanity checks:")
    print(f"- Final rows: {len(frame)}")
    print("- Duplicate players: 0")
    print("- Numeric dtype columns verified: " + ", ".join(NUMERIC_COLUMNS))
    print("- Missing values by column:")
    print(missing_counts.to_string())


def main() -> int:
    root = project_root()
    output_path = root / "data" / "nba_2026_players.csv"

    nba = build_dataset()
    run_sanity_checks(nba)
    compare_to_wnba_schema(root, nba)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    nba.to_csv(output_path, index=False)
    print(f"\nSaved {output_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
