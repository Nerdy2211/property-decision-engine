import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import plotly.graph_objects as go
import streamlit as st
from core.data_loader import load_market_data, get_national_values
from core.scoring import run_full_scoring
from core.locations import STATES, get_suburbs_for_state, get_suburb_data, get_market_city
from core.tax import MARGINAL_TAX_RATES
from core.styles import get_common_css, sidebar_branding, gauge_svg, score_color

st.set_page_config(
    page_title="Property Analyser | Property Decision Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Shared CSS + sidebar branding
# ---------------------------------------------------------------------------
st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page-specific CSS (only classes NOT covered by shared styles.py)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* Override pa-card-row bottom margin for tighter spacing */
.pa-card-row { margin-bottom: 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Market climate data (loaded once)
# ---------------------------------------------------------------------------
_data           = load_market_data()
_national_vals  = get_national_values(_data)
_results        = run_full_scoring(_national_vals)
_city_scores    = _results["city_scores"]
_national_score = _results["national_score"]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SIMPLE_EXPENSE_RATE = 0.015  # 1.5 % of property value

# Marginal tax rate options — imported from core/tax.py (single source of truth)
TAX_RATES = MARGINAL_TAX_RATES

# ---------------------------------------------------------------------------
# Calculation helpers
# ---------------------------------------------------------------------------

def _gross_yield(price: float, weekly_rent: float) -> float:
    return (weekly_rent * 52) / price * 100


def _net_yield(price: float, weekly_rent: float, expenses: float) -> float:
    return ((weekly_rent * 52) - expenses) / price * 100


def _calc_expenses_simple(price: float) -> float:
    return price * SIMPLE_EXPENSE_RATE


def _calc_expenses_detailed(
    price: float, weekly_rent: float,
    council_rates: float, insurance: float,
    maintenance_pct: float, mgmt_pct: float,
    vacancy_pct: float, strata: float,
) -> float:
    annual_rent = weekly_rent * 52
    return (
        council_rates
        + insurance
        + price        * (maintenance_pct / 100)
        + annual_rent  * (mgmt_pct        / 100)
        + annual_rent  * (vacancy_pct     / 100)
        + strata
    )


def _net_yield_score(y: float) -> float:
    if y >= 4.0:   return 100.0
    if y >= 2.5:   return 50.0 + (y - 2.5) / 1.5 * 50.0
    return max(0.0, y / 2.5 * 50.0)


def _cf_score(cf: float) -> float:
    if cf >= 5_000:   return 100.0
    if cf >= 0:       return 75.0
    if cf >= -15_000: return 50.0
    if cf >= -30_000: return 25.0
    return 0.0


def _deal_score(ny_score: float, market_city: str, cf: float) -> int:
    m = _city_scores.get(market_city, {}).get("score", _national_score)
    return round(0.55 * ny_score + 0.35 * m + 0.10 * _cf_score(cf))


def _verdict(score: int) -> tuple:
    if score >= 65: return "Strong Deal", "#00BFA5"
    if score >= 45: return "Reasonable",  "#F59E0B"
    return "Avoid", "#EF4444"


def _yield_label(y: float) -> str:
    if y >= 5.5: return "Strong"
    if y >= 4.0: return "Neutral"
    return "Weak"


def _gearing_label(cf: float) -> str:
    return "Positively geared" if cf >= 0 else "Negatively geared"


def _pct_diff(user_val: float, median_val: float) -> float:
    if median_val == 0: return 0.0
    return (user_val - median_val) / median_val * 100


def _diff_badge(diff: float, invert: bool = False) -> str:
    """Return badge class string for a percentage diff."""
    good = diff <= -5 if invert else diff >= 5
    bad  = diff >= 5  if invert else diff <= -5
    if good: return "badge badge-pos"
    if bad:  return "badge badge-neg"
    return "badge badge-cau"


def _arrow(val: float) -> str:
    if abs(val) < 2: return "≈ At median"
    return ("▲ " if val > 0 else "▼ ") + f"{abs(val):.1f}%"


def _yield_arrow(diff: float) -> str:
    if abs(diff) < 0.1: return "≈ At median"
    return ("▲ " if diff > 0 else "▼ ") + f"{abs(diff):.2f}pp"


def _yield_badge(diff: float) -> str:
    """Return badge class for yield diff."""
    if diff >= 0.1: return "badge badge-pos"
    if diff <= -0.1: return "badge badge-neg"
    return "badge badge-cau"


def _signal_badge(val: float, thresholds: tuple = (5.5, 4.0), labels: tuple = None) -> str:
    """Return badge class based on value vs two thresholds (high=pos, mid=cau, low=neg)."""
    high, low = thresholds
    if val >= high: return "badge badge-pos"
    if val >= low:  return "badge badge-cau"
    return "badge badge-neg"


# ---------------------------------------------------------------------------
# Chart helper
# ---------------------------------------------------------------------------

def _history_chart(years, values, title, yaxis_label, line_color,
                   current_value=None, ref_label=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode="lines+markers",
        line=dict(color=line_color, width=2.5),
        marker=dict(size=5),
        hovertemplate="%{x}: %{y:,.0f}<extra></extra>",
    ))
    if current_value is not None:
        fig.add_hline(
            y=current_value,
            line_dash="dot",
            line_color="rgba(255,255,255,0.25)",
            annotation_text=ref_label or f"This property: {current_value:,.0f}",
            annotation_position="top right",
            annotation_font=dict(size=11, color="rgba(255,255,255,0.45)"),
        )
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#F1F5F9"), x=0),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=11, color="#666"), dtick=1),
        yaxis=dict(
            title=dict(text=yaxis_label, font=dict(size=10, color="#666")),
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            zeroline=False, tickfont=dict(size=11, color="#666"),
            tickformat=",.0f",
        ),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F1F5F9"),
        margin=dict(l=10, r=20, t=40, b=10),
        height=220, showlegend=False,
    )
    return fig


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.markdown("## Property Analyser")
st.caption(
    "Estimate yield, cash flow, and a blended deal score for a specific property. "
    "All figures are indicative. Not financial advice."
)
st.divider()

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
st.subheader("Property Details")

col_a, col_b = st.columns(2, gap="large")

with col_a:
    purchase_price = st.number_input(
        "Purchase price ($)",
        min_value=50_000, max_value=10_000_000,
        value=750_000, step=10_000, format="%d",
    )
    weekly_rent = st.number_input(
        "Weekly rent ($)",
        min_value=0, max_value=10_000,
        value=600, step=10, format="%d",
    )
    deposit = st.number_input(
        "Deposit ($)",
        min_value=0, max_value=5_000_000,
        value=150_000, step=10_000, format="%d",
    )
    interest_rate = st.number_input(
        "Interest rate (%)",
        min_value=0.0, max_value=20.0,
        value=6.0, step=0.1, format="%.1f",
    )

with col_b:
    state = st.selectbox("State", options=STATES,
                         index=STATES.index("NSW"))
    # Suburb list comes from locations.py — swap the backend there to scale nationally.
    # key=f"suburb_{state}" resets the widget when state changes.
    suburb_options = ["— No suburb —"] + get_suburbs_for_state(state)
    suburb = st.selectbox(
        "Suburb",
        options=suburb_options,
        key=f"suburb_{state}",
        help="Type to search. Enables suburb comparison and historical charts.",
    )
    property_type = st.selectbox("Property type",
                                 options=["House", "Unit / Apartment"])
    expense_mode = st.radio(
        "Expenses",
        options=["Simple (1.5% of value)", "Detailed"],
        horizontal=True,
    )
    cf_freq = st.radio("Show cash flow", ["Weekly", "Fortnightly", "Monthly", "Annual"],
                       index=3, horizontal=True)

_FREQ = {"Weekly": (52, "/wk"), "Fortnightly": (26, "/fn"), "Monthly": (12, "/mo"), "Annual": (1, "/yr")}
def _fmt_cf(annual_amount):
    """Convert annual cash flow to selected frequency."""
    periods, suffix = _FREQ[cf_freq]
    v = annual_amount / periods
    return f"+${v:,.0f}{suffix}" if v >= 0 else f"-${abs(v):,.0f}{suffix}"

_detailed = expense_mode == "Detailed"

if _detailed:
    st.markdown("**Expense breakdown**")
    ex1, ex2, ex3 = st.columns(3, gap="medium")
    with ex1:
        council_rates = st.number_input("Council rates ($/yr)", min_value=0, max_value=20_000,
                                         value=2_000, step=100, format="%d")
        insurance     = st.number_input("Insurance ($/yr)",     min_value=0, max_value=10_000,
                                         value=1_500, step=100, format="%d")
        strata        = st.number_input("Strata ($/yr)",        min_value=0, max_value=30_000,
                                         value=0,     step=200, format="%d")
    with ex2:
        maintenance_pct = st.number_input("Maintenance (% of value)", min_value=0.0, max_value=5.0,
                                           value=0.5, step=0.1, format="%.1f")
        mgmt_pct        = st.number_input("Management (%)",           min_value=0.0, max_value=15.0,
                                           value=8.0, step=0.5, format="%.1f")
    with ex3:
        vacancy_pct = st.number_input("Vacancy (%)", min_value=0.0, max_value=20.0,
                                       value=2.0, step=0.5, format="%.1f")

st.divider()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if purchase_price > 0 and weekly_rent > 0:

    # Core financials
    market_city   = get_market_city(state)
    loan_amount   = max(0.0, purchase_price - deposit)
    annual_rent   = weekly_rent * 52
    interest_cost = loan_amount * (interest_rate / 100)

    if _detailed:
        annual_expenses = _calc_expenses_detailed(
            purchase_price, weekly_rent,
            council_rates, insurance, maintenance_pct,
            mgmt_pct, vacancy_pct, strata,
        )
    else:
        annual_expenses = _calc_expenses_simple(purchase_price)

    cash_flow     = annual_rent - annual_expenses - interest_cost
    gross_yld_pct = _gross_yield(purchase_price, weekly_rent)
    net_yld_pct   = _net_yield(purchase_price, weekly_rent, annual_expenses)
    ny_score      = _net_yield_score(net_yld_pct)
    deal          = _deal_score(ny_score, market_city, cash_flow)
    verdict_label, verdict_color = _verdict(deal)
    yield_label   = _yield_label(gross_yld_pct)
    gear_label    = _gearing_label(cash_flow)
    city_score    = _city_scores.get(market_city, {}).get("score", _national_score)
    city_band     = _city_scores.get(market_city, {}).get("band_label", "")
    cf_sub        = _cf_score(cash_flow)
    is_unit       = "Unit" in property_type
    type_label    = "unit" if is_unit else "house"

    # Badge helpers for KPI cards
    _gy_badge = "badge badge-pos" if gross_yld_pct >= 5.5 else ("badge badge-cau" if gross_yld_pct >= 4.0 else "badge badge-neg")
    _ny_badge = "badge badge-pos" if net_yld_pct >= 4.0 else ("badge badge-cau" if net_yld_pct >= 2.5 else "badge badge-neg")
    _cf_badge = "badge badge-pos" if cash_flow >= 0 else "badge badge-neg"
    _deal_badge = "badge badge-pos" if deal >= 65 else ("badge badge-cau" if deal >= 45 else "badge badge-neg")
    _ny_label = "Strong" if net_yld_pct >= 4.0 else ("Neutral" if net_yld_pct >= 2.5 else "Weak")

    # ── Headline KPIs ────────────────────────────────────────────────────
    st.subheader("Analysis")

    st.markdown(f"""
    <div class="card-row">
      <div class="card">
        <div class="lbl">Gross Yield</div>
        <div class="val">{gross_yld_pct:.2f}%</div>
        <span class="{_gy_badge}">{yield_label}</span>
      </div>
      <div class="card">
        <div class="lbl">Net Yield</div>
        <div class="val">{net_yld_pct:.2f}%</div>
        <span class="{_ny_badge}">{_ny_label}</span>
      </div>
      <div class="card">
        <div class="lbl">Cash Flow</div>
        <div class="val">{_fmt_cf(cash_flow)}</div>
        <span class="{_cf_badge}">{gear_label}</span>
      </div>
      <div class="card" style="border-left: 3px solid {verdict_color}">
        <div class="lbl">Deal Score</div>
        <div class="val" style="color:{verdict_color}">{deal} / 100</div>
        <span class="{_deal_badge}">{verdict_label}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Financing & Cash Flow ────────────────────────────────────────────
    st.subheader("Financing & Cash Flow")

    fin1, fin2 = st.columns(2, gap="large")
    expense_note = "Detailed" if _detailed else "1.5% of value"

    with fin1:
        st.markdown(f"""
        <div class="card">
          <div class="lbl">Financing</div>
          <table class="math-tbl">
            <tr><td class="mlbl">Purchase price</td>
                <td class="mval">${purchase_price:,.0f}</td></tr>
            <tr><td class="mlbl">Deposit</td>
                <td class="mval">−${deposit:,.0f}</td></tr>
            <tr class="sep total">
              <td class="mlbl">Loan amount</td>
              <td class="mval">${loan_amount:,.0f}</td>
            </tr>
            <tr><td class="mlbl">LVR</td>
                <td class="mval">{loan_amount / purchase_price * 100:.1f}%</td></tr>
            <tr><td class="mlbl">Rate</td>
                <td class="mval">{interest_rate:.1f}%</td></tr>
            <tr><td class="mlbl">Annual interest</td>
                <td class="mval">−${interest_cost:,.0f}</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with fin2:
        _cf_color = "#00BFA5" if cash_flow >= 0 else "#EF4444"
        st.markdown(f"""
        <div class="card">
          <div class="lbl">Cash Flow</div>
          <table class="math-tbl">
            <tr><td class="mlbl">Annual rent</td>
                <td class="mval">${annual_rent:,.0f}</td></tr>
            <tr><td class="mlbl">Expenses ({expense_note})</td>
                <td class="mval">−${annual_expenses:,.0f}</td></tr>
            <tr><td class="mlbl">Interest</td>
                <td class="mval">−${interest_cost:,.0f}</td></tr>
            <tr class="sep total">
              <td class="mlbl">Net cash flow</td>
              <td class="mval" style="color:{_cf_color}">{_fmt_cf(cash_flow)}</td>
            </tr>
            <tr><td class="mlbl">Gross yield</td>
                <td class="mval">{gross_yld_pct:.2f}%</td></tr>
            <tr><td class="mlbl">Net yield</td>
                <td class="mval">{net_yld_pct:.2f}%</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    lvr = loan_amount / purchase_price * 100
    if lvr > 80:
        st.warning(
            f"⚠️ **LVR is {lvr:.0f}%** — above 80%. Most lenders will require "
            "Lenders Mortgage Insurance (LMI), which can add $5,000–$30,000+ to upfront costs. "
            "Consider increasing your deposit to avoid LMI."
        )

    st.divider()

    # ── Tax Estimate ─────────────────────────────────────────────────────
    st.subheader("Tax Estimate")

    tax_col, _ = st.columns([1, 2], gap="large")
    with tax_col:
        tax_rate_label = st.selectbox(
            "Marginal tax rate",
            options=list(TAX_RATES.keys()),
            index=2,   # defaults to 32.5%
        )
    tax_rate     = TAX_RATES[tax_rate_label]
    prop_loss    = max(0.0, -cash_flow)
    tax_benefit  = prop_loss * tax_rate
    after_tax_cf = cash_flow + tax_benefit

    t1, t2, t3 = st.columns(3, gap="medium")
    t1.metric("Property Loss", f"${prop_loss:,.0f}",
              delta="Deductible against income (if negatively geared)",
              delta_color="off")
    t2.metric("Est. Tax Benefit", f"+${tax_benefit:,.0f}",
              delta=f"@ {tax_rate*100:.1f}% marginal rate",
              delta_color="off" if tax_benefit == 0 else "normal")
    t3.metric("After-tax Cash Flow", _fmt_cf(after_tax_cf),
              delta="Positively geared" if after_tax_cf >= 0 else "Negatively geared (after tax)",
              delta_color="normal" if after_tax_cf >= 0 else "inverse")

    st.markdown(
        "<div class='disclaimer'>Estimate only. Assumes all losses are fully deductible in the year incurred. "
        "Does not account for depreciation, capital works deductions, individual circumstances, or the 50% CGT discount. "
        "Consult a tax adviser before making investment decisions.</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Deal Score Derivation ────────────────────────────────────────────
    st.subheader("Deal Score Derivation")

    ds_gauge, ds_detail = st.columns([1, 3], gap="large")

    with ds_gauge:
        st.markdown(
            f'<div style="text-align:center;padding-top:8px">'
            f'{gauge_svg(deal, verdict_color, size=140, label=verdict_label, show_micro=False)}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with ds_detail:
        ds1, ds2, ds3 = st.columns(3, gap="medium")
        ds1.metric("Net Yield Score (55%)", f"{ny_score:.0f} / 100",
                   delta=f"{net_yld_pct:.2f}% net yield", delta_color="off")
        ds2.metric(f"Market Score — {market_city} (35%)", f"{city_score} / 100",
                   delta=city_band, delta_color="off")
        ds3.metric("Cash Flow Score (10%)", f"{cf_sub:.0f} / 100",
                   delta=gear_label,
                   delta_color="normal" if cash_flow >= 0 else "inverse")

    pt_note = (
        "Units can offer stronger yields but may carry strata fees. "
        "Check levies and by-laws before committing."
        if is_unit else
        "Houses offer more land component and capital growth potential, "
        "but higher prices typically compress yields."
    )
    st.markdown(
        f"<small style='color:rgba(255,255,255,0.45)'>"
        f"<b>{property_type} note:</b> {pt_note}</small>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Suburb Comparison ────────────────────────────────────────────────
    st.subheader("Suburb Comparison")

    suburb_selected = suburb != "— No suburb —"
    if not suburb_selected:
        st.info("Select a suburb above to compare against local medians.")
    else:
        sub_info = get_suburb_data(state, suburb)
        if sub_info is None:
            st.warning(f"No benchmark data found for {suburb}, {state}.")
        else:
            median_price = sub_info["median_unit_price"] if is_unit else sub_info["median_house_price"]
            median_rent  = sub_info["median_weekly_rent_unit"] if is_unit else sub_info["median_weekly_rent_house"]
            median_gy    = _gross_yield(median_price, median_rent)

            price_diff = _pct_diff(purchase_price, median_price)
            rent_diff  = _pct_diff(weekly_rent,    median_rent)
            yield_diff = gross_yld_pct - median_gy

            price_cls = _diff_badge(price_diff, invert=True)
            rent_cls  = _diff_badge(rent_diff)
            yield_cls = _yield_badge(yield_diff)

            st.markdown(f"""
            <div class="card-row">
              <div class="card">
                <div class="lbl">Price vs {suburb} Median {type_label.title()}</div>
                <div class="val-sm">${purchase_price:,.0f}</div>
                <div class="sub">Suburb median: ${median_price:,.0f}</div>
                <span class="{price_cls}">{_arrow(price_diff)} vs median</span>
              </div>
              <div class="card">
                <div class="lbl">Rent vs {suburb} Median</div>
                <div class="val-sm">${weekly_rent:,.0f}/wk</div>
                <div class="sub">Suburb median: ${median_rent:,.0f}/wk</div>
                <span class="{rent_cls}">{_arrow(rent_diff)} vs median</span>
              </div>
              <div class="card">
                <div class="lbl">Gross Yield vs {suburb} Median</div>
                <div class="val-sm">{gross_yld_pct:.2f}%</div>
                <div class="sub">Suburb median: {median_gy:.2f}%</div>
                <span class="{yield_cls}">{_yield_arrow(yield_diff)}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    # ── Historical Context ───────────────────────────────────────────────
    st.subheader("Historical Context")

    if not suburb_selected:
        st.info("Select a suburb above to see historical price and rent trends.")
    else:
        sub_info = get_suburb_data(state, suburb)
        if sub_info:
            ph = sub_info.get("price_history", [])
            rh = sub_info.get("rent_history",  [])

            if ph or rh:
                hc1, hc2 = st.columns(2, gap="large")
                if ph:
                    with hc1:
                        st.plotly_chart(
                            _history_chart(
                                [p["year"] for p in ph],
                                [p["value"] for p in ph],
                                title=f"{suburb} — Median {type_label.title()} Price (2019–2025)",
                                yaxis_label="Price ($)",
                                line_color="#00BFA5",
                                current_value=purchase_price,
                                ref_label=f"This property: ${purchase_price:,.0f}",
                            ),
                            use_container_width=True,
                        )
                if rh:
                    with hc2:
                        st.plotly_chart(
                            _history_chart(
                                [r["year"] for r in rh],
                                [r["value"] for r in rh],
                                title=f"{suburb} — Median Weekly Rent (2019–2025)",
                                yaxis_label="Weekly rent ($)",
                                line_color="#F59E0B",
                                current_value=weekly_rent,
                                ref_label=f"This property: ${weekly_rent:,.0f}/wk",
                            ),
                            use_container_width=True,
                        )
                st.caption(
                    f"Historical data shown is for {suburb} {type_label}s. "
                    "Figures are indicative approximations — not sourced from live data."
                )

    st.divider()

    # ── Methodology ──────────────────────────────────────────────────────
    with st.expander("How this is calculated"):
        st.markdown(
            "#### Gross & Net Yield\n"
            "```\nGross yield = (Weekly rent × 52) / Purchase price × 100"
            "\nNet yield   = (Annual rent − Expenses) / Purchase price × 100\n```\n"
            "Net yield is more meaningful — it strips holding costs before financing.\n\n"

            "#### Expenses\n"
            "**Simple:** 1.5% of purchase price (proxy for rates, insurance, maintenance, management).\n\n"
            "**Detailed:** Council rates + Insurance + Strata + Maintenance (% of value) "
            "+ Management (% of rent) + Vacancy allowance (% of rent).\n\n"

            "#### Interest\n"
            "```\nLoan = Purchase price − Deposit    Interest = Loan × Rate\n```\n"
            "Interest-only basis. Does not include principal repayments.\n\n"

            "#### Tax Estimate\n"
            "```\nProperty loss = max(0, −Cash flow)"
            "\nTax benefit  = Property loss × Marginal rate"
            "\nAfter-tax CF = Cash flow + Tax benefit\n```\n"
            "Simplified estimate only — see disclaimer below the tax section.\n\n"

            "#### Net Yield Score (0–100)\n"
            "| Net Yield | Score |\n|---|---|\n"
            "| ≥ 4.0% | 100 |\n| 2.5–4.0% | 50–100 (linear) |\n| < 2.5% | 0–50 (linear) |\n\n"

            "#### Cash Flow Score (0–100)\n"
            "| Cash Flow | Score |\n|---|---|\n"
            "| ≥ +$5,000 | 100 |\n| $0–$5,000 | 75 |\n"
            "| −$15k–$0 | 50 |\n| −$30k–−$15k | 25 |\n| < −$30,000 | 0 |\n\n"

            "#### Blended Deal Score\n"
            "```\n(Net Yield Score × 55%) + (Market Score × 35%) + (Cash Flow Score × 10%)\n```\n"
            "Market score reflects the national climate adjusted for the state's capital city.\n\n"

            "#### Verdict\n"
            "| Score | Verdict |\n|---|---|\n"
            "| 65–100 | Strong Deal |\n| 45–64 | Reasonable |\n| 0–44 | Avoid |\n\n"

            "---\n"
            "*Simplified model. Does not account for stamp duty, depreciation, capital growth, "
            "tax treatment, or interest rate changes over time. "
            "Suburb benchmarks are indicative approximations. "
            "Treat all outputs as a first-pass screen, not a formal investment analysis.*"
        )

    st.markdown(
        '<div class="disclaimer" style="text-align:center;margin-top:32px">'
        'Indicative only \u00b7 Not financial advice \u00b7 Data as of March 2026</div>',
        unsafe_allow_html=True,
    )

else:
    st.info("Enter a purchase price and weekly rent above to see the analysis.")
