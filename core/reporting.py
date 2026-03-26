"""
Plain-English text generation for the Market Climate Dashboard.
All text is template-based — no LLM in v1.
"""

from core.config import FACTOR_LABELS, WEIGHTS


# ---------------------------------------------------------------------------
# Factor plain-English one-liners (shown on factor cards)
# These are written for the current data values and updated manually.
# ---------------------------------------------------------------------------
FACTOR_DESCRIPTIONS = {
    "interest_rate": (
        "Monetary policy remains restrictive following recent rate increases. Markets and economists see the possibility of further tightening in 2026, though the outlook remains uncertain."
    ),
    "inflation": (
        "Inflation matters here mainly through its influence on rate policy. Persistent above-target CPI keeps the RBA from cutting — or opens the door to further hikes."
    ),
    "unemployment": (
        "The labour market has held up, but unemployment has drifted up from its 3.4% trough. Forward indicators point to possible further softening through 2026."
    ),
    "wages_growth": (
        "Wages are growing in real terms for the first time in several years, though not enough yet to meaningfully improve housing affordability at current price levels."
    ),
    "population_growth": (
        "Migration is running well above the long-run average (~160k/yr), which is a genuine structural support for housing demand. The pace has moderated from the 500k+ post-COVID surge, but supply is not keeping pace regardless."
    ),
    "consumer_sentiment": (
        "Sentiment improved after the first rate cut but remains below 100 — the long-run neutral level. Households are cautious, not confident."
    ),
    "housing_supply": (
        "Dwelling approvals are running well below the level needed to house population growth. The structural supply gap is a persistent feature of the Australian market."
    ),
    "rental_vacancy": (
        "Vacancy rates are near record lows nationally, supporting rental yields and underpinning investor returns in most markets."
    ),
    "global_macro_risk": (
        "A meaningful but secondary overlay. A China shock, commodity price collapse, or global credit event could move Australian property — but the domestic rate and supply cycle remains the primary story."
    ),
}


def get_national_summary(national_score: int, band_label: str) -> str:
    """One-sentence plain-English summary of the national score."""
    if national_score >= 75:
        return (
            f"Structural conditions for Australian property investment are broadly positive — "
            f"tight supply, elevated migration, and low vacancy are the primary supports. "
            f"However, monetary policy remains restrictive following recent rate increases, "
            f"and the rate outlook for 2026 is uncertain."
        )
    elif national_score >= 55:
        return (
            f"Conditions are cautiously positive for property investment — "
            f"structural demand drivers remain intact, but affordability and rate levels still apply headwinds."
        )
    elif national_score >= 40:
        return (
            f"The market is sending mixed signals — some structural tailwinds remain, "
            f"but macro conditions warrant a measured approach."
        )
    elif national_score >= 20:
        return (
            f"Macro conditions are challenging for property investment — "
            f"buyers and investors should proceed cautiously and stress-test assumptions carefully."
        )
    else:
        return (
            f"Market conditions are poor. Significant headwinds across multiple factors "
            f"suggest waiting for a clearer environment before committing capital."
        )


def get_tailwinds_and_risks(sub_scores: dict) -> tuple:
    """
    Returns (tailwinds, risks) — each a list of (factor_label, description) tuples.
    Tailwinds = top 3 scoring factors. Risks = bottom 3.
    """
    sorted_factors = sorted(sub_scores.items(), key=lambda x: x[1], reverse=True)
    tailwinds = [
        (FACTOR_LABELS[k], FACTOR_DESCRIPTIONS.get(k, ""))
        for k, _ in sorted_factors[:3]
    ]
    risks = [
        (FACTOR_LABELS[k], FACTOR_DESCRIPTIONS.get(k, ""))
        for k, _ in sorted_factors[-3:]
    ]
    return tailwinds, risks


def get_methodology_rows(sub_scores: dict, national_values: dict) -> list:
    """
    Returns a list of dicts for the methodology table in the expander.
    """
    rows = []
    for key, weight in WEIGHTS.items():
        raw = national_values.get(key, "—")
        score = sub_scores.get(key, "—")
        rows.append({
            "Factor": FACTOR_LABELS[key],
            "Weight": f"{int(weight * 100)}%",
            "Current Value": _format_raw(key, raw),
            "Sub-Score": f"{round(score)}/100" if isinstance(score, float) else "—",
        })
    return rows


def _format_raw(key: str, value) -> str:
    if value == "—":
        return "—"
    if key == "interest_rate":
        return f"{value}%"
    if key == "inflation":
        return f"{value}%"
    if key == "unemployment":
        return f"{value}%"
    if key == "wages_growth":
        return f"{value}%"
    if key == "population_growth":
        return f"{int(value):,}/yr"
    if key == "housing_supply":
        return f"{int(value):,}/yr"
    if key == "rental_vacancy":
        return f"{value}%"
    if key == "consumer_sentiment":
        return f"{value} (index)"
    if key == "global_macro_risk":
        return f"{value}/5 (manual)"
    return str(value)
