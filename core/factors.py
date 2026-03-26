"""
Sub-score calculation for each factor.
All functions return a float 0–100.
"""

from core.config import THRESHOLDS, INFLATION_IDEAL_MIDPOINT, INFLATION_MAX_DEVIATION


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def score_standard(value: float, factor_key: str) -> float:
    """
    Linear clamp scoring for all standard factors.
    Uses thresholds from config.THRESHOLDS.
    """
    bullish, bearish, higher_is_better = THRESHOLDS[factor_key]
    if higher_is_better:
        raw = (value - bearish) / (bullish - bearish) * 100
    else:
        raw = (bearish - value) / (bearish - bullish) * 100
    return _clamp(raw, 0.0, 100.0)


def score_inflation(value: float) -> float:
    """
    Inflation is scored by distance from the ideal midpoint (2.5%).
    At midpoint = 100. Score drops linearly to 0 at max_deviation away.
    """
    deviation = abs(value - INFLATION_IDEAL_MIDPOINT)
    raw = (1 - deviation / INFLATION_MAX_DEVIATION) * 100
    return _clamp(raw, 0.0, 100.0)


def compute_all_sub_scores(national_values: dict) -> dict:
    """
    Given a flat dict of factor_key -> raw_value,
    return a dict of factor_key -> sub_score (0–100).
    """
    scores = {}
    for key, value in national_values.items():
        if key == "inflation":
            scores[key] = score_inflation(value)
        elif key in THRESHOLDS:
            scores[key] = score_standard(value, key)
        # keys not in THRESHOLDS are ignored
    return scores
