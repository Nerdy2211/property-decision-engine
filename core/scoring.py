"""
Weighted aggregation of sub-scores into national, city, and state scores.
"""

from core.config import WEIGHTS, SCORE_BANDS, CITY_OFFSETS, CITY_STATES
from core.factors import compute_all_sub_scores


def compute_national_score(sub_scores: dict) -> int:
    """
    Weighted average of all factor sub-scores.
    Returns an integer 0–100.
    """
    total = sum(sub_scores[key] * WEIGHTS[key] for key in WEIGHTS if key in sub_scores)
    return round(total)


def get_score_band(score: int) -> tuple:
    """
    Returns (label, color) for the given score.
    """
    for low, high, label, color in SCORE_BANDS:
        if low <= score <= high:
            return label, color
    return "Unknown", "#888888"


def format_score_display(score: int) -> str:
    """
    Returns the primary display string: 'Band Label (score/100)'.
    """
    label, _ = get_score_band(score)
    return f"{label} ({score}/100)"


def compute_city_scores(national_score: int) -> dict:
    """
    Returns a dict of city -> {score, band_label, color, offset, state, offset_direction}.
    """
    results = {}
    for city, offset in CITY_OFFSETS.items():
        score = max(0, min(100, national_score + offset))
        label, color = get_score_band(score)
        if offset > 0:
            direction = "↑"
        elif offset < 0:
            direction = "↓"
        else:
            direction = "→"
        results[city] = {
            "score": score,
            "band_label": label,
            "color": color,
            "offset": offset,
            "state": CITY_STATES[city],
            "offset_direction": direction,
        }
    return results


def compute_state_scores(city_scores: dict) -> dict:
    """
    Returns a dict of state_code -> average score across cities in that state.
    """
    state_buckets = {}
    for city, data in city_scores.items():
        state = data["state"]
        state_buckets.setdefault(state, []).append(data["score"])
    return {
        state: round(sum(scores) / len(scores))
        for state, scores in state_buckets.items()
    }


def run_full_scoring(national_values: dict) -> dict:
    """
    Run the complete scoring pipeline.
    Returns a dict with sub_scores, national_score, band_label, color,
    city_scores, and state_scores.
    """
    sub_scores = compute_all_sub_scores(national_values)
    national_score = compute_national_score(sub_scores)
    band_label, color = get_score_band(national_score)
    city_scores = compute_city_scores(national_score)
    state_scores = compute_state_scores(city_scores)
    return {
        "sub_scores": sub_scores,
        "national_score": national_score,
        "band_label": band_label,
        "color": color,
        "city_scores": city_scores,
        "state_scores": state_scores,
    }
