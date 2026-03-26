"""
Australian income tax calculations (2024–25, post Stage 3 cuts).

Used by Borrowing Power and Property Analyser pages.
Does not include Medicare levy, LMITO offsets, or HELP/HECS repayments.
"""

# (threshold, rate) — each band applies to income ABOVE the threshold
AU_TAX_BRACKETS = [
    (190_000, 0.45),
    (135_000, 0.37),
    (45_000,  0.30),
    (18_200,  0.16),
    (0,       0.00),
]

MEDICARE_LEVY_RATE = 0.02

# Marginal tax rate selector options (used by Property Analyser tax estimate).
# Derived from AU_TAX_BRACKETS above — keep in sync if brackets change.
MARGINAL_TAX_RATES = {
    "0%  — Under $18k":   0.00,
    "16% — $18k–$45k":    0.16,
    "30% — $45k–$135k":   0.30,
    "37% — $135k–$190k":  0.37,
    "45% — $190k+":       0.45,
}


def income_tax(gross_income: float, include_medicare: bool = True) -> float:
    """
    Calculate annual income tax on gross_income using 2024–25 brackets.
    Optionally includes Medicare levy (2%).
    """
    tax = 0.0
    remaining = gross_income

    for threshold, rate in AU_TAX_BRACKETS:
        if remaining > threshold:
            taxable = remaining - threshold
            tax += taxable * rate
            remaining = threshold

    if include_medicare:
        tax += gross_income * MEDICARE_LEVY_RATE

    return max(0.0, tax)


def net_income(gross_income: float, include_medicare: bool = True) -> float:
    """Annual net income after tax."""
    return gross_income - income_tax(gross_income, include_medicare)


def effective_tax_rate(gross_income: float) -> float:
    """Effective tax rate as a decimal (0–1)."""
    if gross_income <= 0:
        return 0.0
    return income_tax(gross_income) / gross_income


# ---------------------------------------------------------------------------
# Stamp duty by state (simplified — owner-occupied, non-first-home-buyer)
# These are approximations of current rates. Real stamp duty has complex
# tiered thresholds. This uses a simplified bracket approach per state.
# ---------------------------------------------------------------------------
# Format: list of (threshold, base_amount, marginal_rate_above_threshold)
# Applied cumulatively from lowest to highest.

STAMP_DUTY_TABLES = {
    "NSW": [
        (0,         0,       0.0150),  # $0–$100k
        (100_000,   1_500,   0.0200),  # $100k–$300k
        (300_000,   5_500,   0.0350),  # $300k–$1M
        (1_000_000, 30_000,  0.0450),  # $1M–$3M
        (3_000_000, 120_000, 0.0550),  # $3M+
    ],
    "VIC": [
        (0,         0,       0.0140),
        (25_000,    350,     0.0240),
        (130_000,   2_870,   0.0500),
        (960_000,   44_370,  0.0550),
        (2_000_000, 101_570, 0.0650),
    ],
    "QLD": [
        (0,         0,       0.0),     # $0–$5k (nil)
        (5_000,     0,       0.0150),
        (75_000,    1_050,   0.0250),
        (540_000,   12_675,  0.0350),
        (1_000_000, 28_775,  0.0450),
    ],
    "WA": [
        (0,         0,       0.0190),
        (120_000,   2_280,   0.0285),
        (150_000,   3_135,   0.0380),
        (360_000,   11_115,  0.0475),
        (725_000,   28_453,  0.0515),
    ],
    "SA": [
        (0,         0,       0.0100),
        (12_000,    120,     0.0200),
        (50_000,    880,     0.0300),
        (100_000,   2_380,   0.0350),
        (200_000,   5_880,   0.0400),
        (250_000,   7_880,   0.0425),
        (300_000,   10_005,  0.0475),
        (500_000,   19_505,  0.0500),
    ],
    "TAS": [
        (0,         0,       0.0175),
        (3_000,     50,      0.0225),
        (25_000,    545,     0.0350),
        (75_000,    2_295,   0.0400),
        (200_000,   7_295,   0.0425),
        (375_000,   14_733,  0.0450),
        (725_000,   30_483,  0.0450),
    ],
    "ACT": [
        (0,         0,       0.0120),
        (200_000,   2_400,   0.0250),
        (300_000,   4_900,   0.0400),
        (500_000,   12_900,  0.0500),
        (750_000,   25_400,  0.0550),
        (1_000_000, 39_150,  0.0600),
    ],
    "NT": [
        # NT uses a formula-based approach; simplified here.
        (0,         0,       0.0),     # $0–$525k uses a complex formula
        (525_000,   23_928,  0.0495),  # Simplified above $525k
    ],
}

# NT special formula: for values $0–$525k, duty ≈ V^2 × 0.06571441 / 1000
# where V = value in thousands. We'll use that below.

def stamp_duty(purchase_price: float, state: str, first_home_buyer: bool = False) -> float:
    """
    Estimate stamp duty for a given purchase price and state.
    first_home_buyer concessions are simplified approximations.
    """
    if purchase_price <= 0:
        return 0.0

    # NT special formula
    if state == "NT":
        if purchase_price <= 525_000:
            v = purchase_price / 1000
            duty = (v * v * 0.06571441)
            return max(0.0, round(duty))
        else:
            # Above $525k use the table
            duty = 23_928 + (purchase_price - 525_000) * 0.0495
            return round(duty)

    table = STAMP_DUTY_TABLES.get(state)
    if table is None:
        # Fallback — use NSW rates
        table = STAMP_DUTY_TABLES["NSW"]

    duty = 0.0
    for i in range(len(table) - 1, -1, -1):
        threshold = table[i][0]
        if purchase_price > threshold:
            if i == len(table) - 1:
                # Highest bracket — calculate from base + marginal
                duty = table[i][1] + (purchase_price - threshold) * table[i][2]
            else:
                next_threshold = table[i + 1][0]
                if purchase_price <= next_threshold:
                    duty = table[i][1] + (purchase_price - threshold) * table[i][2]
            break

    # First home buyer concessions (simplified)
    if first_home_buyer:
        fhb_exemptions = {
            "NSW":  800_000,   # Exempt up to $800k
            "VIC":  600_000,   # Exempt up to $600k
            "QLD":  700_000,   # Exempt up to $700k (new home) / $500k (existing)
            "WA":   430_000,   # Exempt up to $430k
            "SA":   650_000,   # No stamp duty for FHB on new homes up to $650k
            "TAS":  750_000,   # 50% concession up to $750k
            "ACT":  0,         # ACT abolished stamp duty concessions for FHB (uses rates system)
            "NT":   650_000,   # Concession available
        }
        threshold = fhb_exemptions.get(state, 0)
        if purchase_price <= threshold:
            if state == "TAS":
                duty *= 0.5  # 50% concession
            else:
                duty = 0.0

    return max(0.0, round(duty))
