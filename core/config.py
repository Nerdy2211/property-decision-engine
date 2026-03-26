"""
Scoring model — baseline v2 (locked March 2026).

All weights, thresholds, city offsets, and score band definitions live here.
Do not change weights or thresholds without an explicit instruction to do so.
The current model produces a national score of 67/100 (Cautiously Favourable)
under March 2026 data. That output is the reference baseline for all future
UI and reporting work.

Weight rationale (v2):
- Interest Rates (28%) is the single largest driver of Australian property affordability,
  borrowing capacity, and investor returns. Rate changes transmit quickly and broadly.
- Population Growth (16%) is the primary structural demand driver. Australia's migration
  intake is large relative to its housing stock and has a direct, persistent effect on prices.
- Housing Supply (13%) + Rental Vacancy (11%) together represent supply-side conditions
  (24% combined). Low approvals and tight vacancy are a defining feature of the current cycle.
- Inflation (10%) matters mainly through its influence on rate expectations. It is deliberately
  weighted below rates to avoid double-counting the same signal.
- Unemployment (8%) and Wages Growth (4%) are labour market indicators that shape buyer
  capacity and confidence, but are secondary to the rate and supply story in Australia.
- Global Macro Risk (6%) is a meaningful overlay. Australian property is not immune to
  external shocks — particularly a China slowdown, commodity price moves, or global credit
  events — but it does not drive the cycle in the same direct way as domestic factors.
- Consumer Sentiment (4%) is a coincident indicator rather than a leading one.
"""

# ---------------------------------------------------------------------------
# Factor weights — must sum to 1.0
# ---------------------------------------------------------------------------
WEIGHTS = {
    "interest_rate":      0.28,
    "population_growth":  0.16,
    "housing_supply":     0.13,
    "rental_vacancy":     0.11,
    "inflation":          0.10,
    "unemployment":       0.08,
    "global_macro_risk":  0.06,
    "wages_growth":       0.04,
    "consumer_sentiment": 0.04,
}

# ---------------------------------------------------------------------------
# Factor groups for UI organisation
# ---------------------------------------------------------------------------
FACTOR_GROUPS = {
    "Macro": ["interest_rate", "inflation", "unemployment", "wages_growth"],
    "Demand": ["population_growth", "consumer_sentiment"],
    "Supply": ["housing_supply", "rental_vacancy"],
    "External": ["global_macro_risk"],
}

# ---------------------------------------------------------------------------
# Factor display names
# ---------------------------------------------------------------------------
FACTOR_LABELS = {
    "interest_rate":      "Interest Rates",
    "inflation":          "Inflation",
    "unemployment":       "Unemployment",
    "wages_growth":       "Wages Growth",
    "population_growth":  "Population Growth",
    "consumer_sentiment": "Consumer Sentiment",
    "housing_supply":     "Housing Supply",
    "rental_vacancy":     "Rental Vacancy",
    "global_macro_risk":  "Global Macro Risk",
}

# ---------------------------------------------------------------------------
# Scoring thresholds
# Each factor: (bullish_value, bearish_value, higher_is_better)
# higher_is_better=True  → raw value closer to bullish_value → score closer to 100
# higher_is_better=False → raw value closer to bullish_value (which is smaller) → score closer to 100
# Inflation is a special case handled separately (distance from midpoint).
# ---------------------------------------------------------------------------
THRESHOLDS = {
    # (bullish, bearish, higher_is_better)
    #
    # interest_rate: bearish set at 6.0% not 7.0% — in Australian conditions, rates above
    # 6% would be extraordinary. Using 7% as the floor made 4.1% look moderate (58/100)
    # when it is genuinely restrictive. With 6.0% as bearish, 4.1% scores ~48 — just below
    # neutral, which correctly represents a mild-to-moderate headwind.
    "interest_rate":      (2.0,   6.0,   False),

    # unemployment: bullish set at 3.0% not 3.5% — 3.5% is near the floor of what Australia
    # has ever achieved. Setting it there made 4.1% score 87/100, implying near-excellent
    # conditions despite forward softening risk. With 3.0% as bullish, 4.1% scores ~78 —
    # good but not nearly perfect, which fits the "drifting up" narrative.
    "unemployment":       (3.0,   8.0,   False),

    "wages_growth":       (4.5,   1.5,   True),   # higher wages = better
    "population_growth":  (400000, 50000, True),  # higher migration = better
    "consumer_sentiment": (110,   70,    True),   # higher sentiment = better
    "housing_supply":     (130000, 250000, False), # lower approvals = tighter supply = better for investors
    "rental_vacancy":     (0.8,   3.5,   False),  # lower vacancy = better
    "global_macro_risk":  (1,     5,     False),  # lower risk score = better
}

# Inflation treated separately: ideal band is 2.0–3.0%, midpoint 2.5%
INFLATION_IDEAL_MIDPOINT = 2.5
INFLATION_MAX_DEVIATION = 3.5  # deviation at which score hits 0 (6.0% or -1.0%)

# ---------------------------------------------------------------------------
# Score bands
# ---------------------------------------------------------------------------
SCORE_BANDS = [
    (75, 100, "Strong Conditions",       "#00BFA5"),
    (55,  74, "Cautiously Favourable",   "#4CAF50"),
    (40,  54, "Neutral — Mixed Signals", "#FFC107"),
    (20,  39, "Caution Advised",         "#FF7043"),
    ( 0,  19, "Poor Conditions",         "#EF5350"),
]

# ---------------------------------------------------------------------------
# City offsets (applied to national score)
# ---------------------------------------------------------------------------
CITY_OFFSETS = {
    "Perth":     8,
    "Brisbane":  6,
    "Adelaide":  5,
    "Sydney":    0,
    "Canberra": -2,
    "Hobart":   -3,
    "Melbourne": -5,
    "Darwin":   -8,
}

CITY_STATES = {
    "Perth":     "WA",
    "Brisbane":  "QLD",
    "Adelaide":  "SA",
    "Sydney":    "NSW",
    "Canberra":  "ACT",
    "Hobart":    "TAS",
    "Melbourne": "VIC",
    "Darwin":    "NT",
}
