import json
import os
import pandas as pd

_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "market_data.json")


def load_market_data() -> dict:
    """Load and return the full market data dict from market_data.json."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_national_values(data: dict) -> dict:
    """Return a flat dict of factor_key -> raw_value for national factors."""
    national = data["national"]
    return {key: entry["value"] for key, entry in national.items()}


def get_city_data(data: dict) -> dict:
    """Return the cities dict with offset and rationale per city."""
    return data["cities"]


def get_recent_shifts(data: dict) -> list:
    """Return the recent_shifts list."""
    return data.get("recent_shifts", [])


def get_meta(data: dict) -> dict:
    """Return metadata (data_as_of date, notes)."""
    return data.get("_meta", {})


_HISTORICAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "historical")


def load_historical_series(series_name: str) -> pd.DataFrame:
    """
    Load a historical time series from data/historical/{series_name}.csv.
    Returns a DataFrame with columns: date (datetime64), value (float).

    To swap to a live or updated source later, replace this function's body
    while keeping the same return signature: DataFrame with 'date' and 'value'.
    """
    path = os.path.join(_HISTORICAL_DIR, f"{series_name}.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df
