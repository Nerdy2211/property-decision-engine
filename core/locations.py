"""
Location data and lookup functions.

This module is the single interface between the UI and suburb/location data.

To later expand to all Australian suburbs:
  1. Replace _load_suburb_data() with a CSV/database loader.
  2. Update get_suburbs_for_state() to query that source.
  3. Update get_suburb_data() to return the same dict structure.
  The UI code in pages/02_property_analyser.py calls only these functions
  and does not need to change.

Suburb data dict structure (must be preserved when swapping backends):
  {
    "median_house_price": int,
    "median_unit_price": int,
    "median_weekly_rent_house": int,
    "median_weekly_rent_unit": int,
    "price_history": [{"year": int, "value": int}, ...],
    "rent_history":  [{"year": int, "value": int}, ...],
  }
"""

import json
import os
import functools

# ---------------------------------------------------------------------------
# State list — all states and territories
# ---------------------------------------------------------------------------
STATES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]

# ---------------------------------------------------------------------------
# State → capital city mapping
# Used to look up market climate scores from the scoring model.
# ---------------------------------------------------------------------------
STATE_TO_MARKET_CITY = {
    "NSW": "Sydney",
    "VIC": "Melbourne",
    "QLD": "Brisbane",
    "WA":  "Perth",
    "SA":  "Adelaide",
    "ACT": "Canberra",
    "TAS": "Hobart",
    "NT":  "Darwin",
}

# ---------------------------------------------------------------------------
# Internal: the suburb_data.json is keyed by capital city name.
# This maps state → that key so the JSON doesn't need restructuring.
# When moving to a full suburb database, this mapping becomes unnecessary.
# ---------------------------------------------------------------------------
_STATE_TO_DATA_KEY = STATE_TO_MARKET_CITY  # currently identical


@functools.lru_cache(maxsize=None)
def _load_suburb_data() -> dict:
    """Load suburb_data.json once and cache it for the process lifetime."""
    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "data", "suburb_data.json")
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_suburbs_for_state(state: str) -> list:
    """
    Return a sorted list of suburb names available for the given state.

    Currently returns suburbs from the mock dataset only.
    To expand: replace the body of this function with a CSV/DB query
    filtered by state — the return type (list of strings) stays the same.
    """
    city_key = _STATE_TO_DATA_KEY.get(state)
    if city_key is None:
        return []
    data = _load_suburb_data()
    return sorted(data.get(city_key, {}).keys())


def get_suburb_data(state: str, suburb: str) -> dict:
    """
    Return the data dict for a suburb, or None if not found.

    To expand: replace with a DB/CSV lookup by (state, suburb).
    The returned dict structure must match the schema above.
    """
    city_key = _STATE_TO_DATA_KEY.get(state)
    if city_key is None:
        return None
    data = _load_suburb_data()
    return data.get(city_key, {}).get(suburb)


def get_market_city(state: str) -> str:
    """
    Return the capital city name used for market climate score lookups.
    Falls back to Sydney if the state is unrecognised.
    """
    return STATE_TO_MARKET_CITY.get(state, "Sydney")
