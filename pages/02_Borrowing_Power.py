import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
from core.tax import income_tax, stamp_duty
from core.locations import STATES
from core.styles import get_common_css, sidebar_branding, score_card_html  # noqa: F401

st.set_page_config(
    page_title="Aurelia | Borrowing Power",
    page_icon="\u25C6",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

# ─── Page-specific CSS ───────────────────────────────────────────────────
st.markdown("""<style>
.tier-card{background:#222225;border:1px solid #333336;
           border-radius:0px;padding:12px 14px 10px 14px;
           height:100%;box-sizing:border-box}
.tier-card-best{border-top:3px solid #C5A880}
.tier-title{font-family:'Playfair Display',Georgia,serif;font-size:14px;font-weight:600;color:#F4F4F5;margin-bottom:6px}
.tier-tbl{width:100%;font-family:'DM Sans',sans-serif;font-size:11px;color:#F4F4F5;border-collapse:collapse}
.tier-tbl td{padding:3px 0}
.tier-tbl .lbl{color:#8A8A93;font-size:11px;text-transform:uppercase;letter-spacing:0.08em}
.tier-tbl .val{text-align:right;font-variant-numeric:tabular-nums}
.tier-tbl .sep{border-top:1px solid #333336}
.tier-tbl .bold .val{font-weight:700}
.inv-box{background:#222225;border:1px solid #333336;
         border-radius:0px;padding:10px 14px;margin-top:6px;
         font-family:'DM Sans',sans-serif;font-size:12px;color:#8A8A93}
.inv-box b{color:#F4F4F5}
.bp-hero{background:#222225;border:1px solid #333336;border-top:3px solid #C5A880;
         border-radius:0px;text-align:center;padding:32px 24px;margin-bottom:16px}
.bp-hero .bp-amount{font-family:'Cormorant Garamond',Georgia,serif;font-size:48px;
                    font-weight:500;color:#F4F4F5;font-variant-numeric:tabular-nums;line-height:1}
.bp-hero .bp-badge{display:inline-block;font-family:'DM Sans',sans-serif;font-size:11px;
                   font-weight:500;padding:2px 10px;border-radius:0px;background:transparent;
                   border:1px solid #333336;color:#8A8A93;margin-top:12px}
.bp-hero .bp-sub{font-family:'DM Sans',sans-serif;font-size:13px;color:#8A8A93;margin-top:8px}
.bp-kpi{background:#222225;border:1px solid #333336;border-radius:0px;padding:16px 20px;
        box-sizing:border-box;height:100%}
.bp-kpi .bp-kpi-val{font-family:'Cormorant Garamond',Georgia,serif;font-size:28px;
                    font-weight:500;color:#F4F4F5;font-variant-numeric:tabular-nums;
                    line-height:1.1;margin-bottom:4px}
.bp-kpi .bp-kpi-lbl{font-family:'DM Sans',sans-serif;font-size:11px;text-transform:uppercase;
                    letter-spacing:0.12em;color:#8A8A93}
.repay-card{background:#222225;border:1px solid #333336;border-radius:0px;padding:16px 20px}
.repay-card .repay-val{font-family:'Cormorant Garamond',Georgia,serif;font-size:28px;
                       font-weight:500;color:#F4F4F5;font-variant-numeric:tabular-nums;
                       line-height:1.1;margin-bottom:8px}
.tbl-head{font-family:'DM Sans',sans-serif;font-size:11px;text-transform:uppercase;
          letter-spacing:0.1em;color:#8A8A93;border-bottom:1px solid #C5A880;
          padding-bottom:8px;margin-bottom:4px}
</style>""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────
APRA_BUFFER = 3.0
LEGALS = 2_500
RENTAL_HAIRCUT = 0.80

HEM_BASE = {
    (False, 0): 2_000, (False, 1): 2_500, (False, 2): 2_900, (False, 3): 3_200,
    (True,  0): 3_000, (True,  1): 3_400, (True,  2): 3_800, (True,  3): 4_200,
}
HEM_THRESHOLD = 80_000
HEM_SCALE = 750          # $/mo per $40k above threshold
HEM_BAND = 40_000

HECS = [
    (180_000, .10), (150_000, .08), (135_000, .07), (120_000, .06),
    (105_000, .05), (90_000, .04), (75_000, .03), (65_000, .02),
    (54_435, .01), (0, .00),
]
LMI_RATES = [(95, .040), (90, .028), (85, .018), (80, .008)]
LVR_TIERS = [80, 85, 90, 95]

# ─── Helpers ──────────────────────────────────────────────────────────────

def _hem(has_partner, deps, combined_income):
    b = HEM_BASE.get((has_partner, min(deps, 3)), 3_000)
    if combined_income > HEM_THRESHOLD:
        b += int((combined_income - HEM_THRESHOLD) / HEM_BAND * HEM_SCALE)
    return b

def _hecs(income, balance):
    if balance <= 0 or income < 54_435: return 0.0
    for t, r in HECS:
        if income >= t: return income * r
    return 0.0

def _pv_pi(mo, rate, term):
    if mo <= 0 or rate <= 0: return 0.0
    r = rate / 100 / 12; n = term * 12
    return mo * (1 - (1 + r) ** (-n)) / r

def _pv_io(mo, rate):
    if mo <= 0 or rate <= 0: return 0.0
    return mo * 12 / (rate / 100)

def _repay_pi(loan, rate, term):
    if loan <= 0 or rate <= 0: return 0.0
    r = rate / 100 / 12; n = term * 12
    return loan * r * (1 + r) ** n / ((1 + r) ** n - 1)

def _repay_io(loan, rate):
    return loan * (rate / 100) / 12 if loan > 0 and rate > 0 else 0.0

def _lmi(loan, pv):
    if pv <= 0: return 0.0
    lvr = loan / pv * 100
    for t, r in LMI_RATES:
        if lvr > t: return round(loan * r)
    return 0.0

def _equity(val, owing):
    return max(0.0, val * 0.80 - owing)

def _tier(svc_max, cash, equity, lvr_pct, rate, term, is_pi, st_code, fhb):
    """Compute one LVR-tier row for the comparison table."""
    frac = lvr_pct / 100
    dep_frac = 1 - frac

    # Max purchase capped by serviceability
    svc_purchase = svc_max / frac if frac > 0 else 0.0

    results = {}
    for label, pool in [("cash", cash), ("cash_equity", cash + equity)]:
        funds_purchase = pool / dep_frac if dep_frac > 0 else 0.0
        purchase = max(0.0, min(svc_purchase, funds_purchase))
        loan = purchase * frac
        dep = purchase * dep_frac
        lmi_cost = _lmi(loan, purchase)
        sd = stamp_duty(purchase, st_code, fhb)
        total = dep + sd + LEGALS + lmi_cost
        # Funding allocation
        eq_dep = min(equity if label == "cash_equity" else 0.0, dep)
        eq_rem = (equity if label == "cash_equity" else 0.0) - eq_dep
        eq_cost = min(eq_rem, sd + LEGALS + lmi_cost)
        eq_draw = eq_dep + eq_cost
        cash_req = total - eq_draw
        shortfall = max(0.0, cash_req - cash)
        mo = _repay_pi(loan, rate, term) if is_pi else _repay_io(loan, rate)

        results[label] = {
            "purchase": purchase, "loan": loan, "dep": dep,
            "lmi": lmi_cost, "sd": sd, "total": total,
            "eq_draw": eq_draw, "cash_req": cash_req,
            "shortfall": shortfall, "monthly": mo,
            "binding": "funds" if purchase < svc_purchase - 1 else "serviceability",
        }
    return results


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — INPUTS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="font-family:Playfair Display,Georgia,serif;font-size:36px;'
    'font-weight:600;color:#F4F4F5;margin-bottom:4px">Borrowing Power Estimator</div>',
    unsafe_allow_html=True)
st.caption("Indicative only · Not financial advice.")
st.divider()

st.subheader("Your Situation")
c1, c2 = st.columns(2, gap="large")

with c1:
    gross = st.number_input("Annual gross income ($)",
        min_value=0, max_value=5_000_000, value=100_000, step=5_000, format="%d")
    partner = st.number_input("Partner income ($/yr, 0 if none)",
        min_value=0, max_value=5_000_000, value=0, step=5_000, format="%d")
    deps = st.number_input("Dependants", min_value=0, max_value=10, value=0, step=1)
    state = st.selectbox("State", STATES, index=STATES.index("NSW"))
    fhb = st.toggle("First home buyer", value=False)

combined = gross + partner
has_partner = partner > 0

with c2:
    exp_mode = st.radio("Living expenses",
        ["Use HEM benchmark", "Enter manually"], horizontal=True)
    hem_val = _hem(has_partner, deps, combined)

    if exp_mode == "Enter manually":
        expenses = st.number_input("Monthly living expenses ($)",
            min_value=0, max_value=50_000, value=int(hem_val), step=100, format="%d")
    else:
        expenses = hem_val
        st.info(f"HEM benchmark: **${hem_val:,.0f}/mo** "
                f"({'couple' if has_partner else 'single'}, "
                f"{deps} dep{'s' if deps != 1 else ''})")

    st.markdown("**Existing debts**")
    dd1, dd2 = st.columns(2)
    with dd1:
        cc_limit = st.number_input("Credit card limit ($)",
            min_value=0, max_value=200_000, value=0, step=1_000, format="%d",
            help="Banks count 3% of the limit as a monthly commitment.")
        hecs_bal = st.number_input("HECS/HELP balance ($)",
            min_value=0, max_value=500_000, value=0, step=5_000, format="%d")
    with dd2:
        other_debt = st.number_input("Other debts ($/mo)",
            min_value=0, max_value=50_000, value=0, step=100, format="%d",
            help="Car loans, personal loans, afterpay.")

st.divider()

# ── Investment Properties ─────────────────────────────────────────────────
st.subheader("Investment Properties")
has_inv = st.toggle("I own investment properties", value=False)

inv_repay_mo = 0.0
inv_rent_mo = 0.0
inv_equity = 0.0
inv_total_value = 0.0
inv_total_loan = 0.0

if has_inv:
    n_inv = st.selectbox("How many?", [1, 2, 3], index=0)
    for i in range(n_inv):
        st.markdown(f"**Property {i + 1}**")
        p1, p2, p3, p4 = st.columns(4, gap="medium")
        with p1:
            iv = st.number_input("Value ($)", key=f"iv{i}",
                min_value=0, max_value=10_000_000, value=600_000, step=25_000, format="%d")
        with p2:
            il = st.number_input("Loan owing ($)", key=f"il{i}",
                min_value=0, max_value=10_000_000, value=400_000, step=10_000, format="%d")
        with p3:
            ir = st.number_input("Repayment ($/mo)", key=f"ir{i}",
                min_value=0, max_value=50_000, value=2_500, step=100, format="%d")
        with p4:
            iw = st.number_input("Rent ($/wk)", key=f"iw{i}",
                min_value=0, max_value=10_000, value=500, step=25, format="%d")

        eq = _equity(iv, il)
        rmo = iw * 52 / 12
        gear = "Positive" if rmo >= ir else "Negative"
        gc = "#3B4A42" if rmo >= ir else "#C45C5C"
        inv_repay_mo += ir
        inv_rent_mo += rmo
        inv_equity += eq
        inv_total_value += iv
        inv_total_loan += il

        st.markdown(
            f'<div class="inv-box">Equity: <b>${iv - il:,.0f}</b> '
            f'(available: <b>${eq:,.0f}</b> = ${iv:,.0f} × 80% − ${il:,.0f}) &middot; '
            f'<span style="color:{gc}">{gear}ly geared</span> '
            f'(${rmo:,.0f}/mo rent vs ${ir:,}/mo repay)</div>',
            unsafe_allow_html=True)

    rental_credit = inv_rent_mo * RENTAL_HAIRCUT
    net_inv = rental_credit - inv_repay_mo
    st.markdown(
        f'<div class="inv-box" style="border-left:3px solid #C5A880;margin-top:10px">'
        f'<b>Totals:</b> Available equity (80% LVR) <b>${inv_equity:,.0f}</b> &middot; '
        f'Rental credit (80%) <b>+${rental_credit:,.0f}/mo</b> &middot; '
        f'Repayments <b>−${inv_repay_mo:,.0f}/mo</b> &middot; '
        f'Net <b style="color:{"#3B4A42" if net_inv >= 0 else "#C45C5C"}">'
        f'{"+" if net_inv >= 0 else ""}{net_inv:,.0f}/mo</b></div>',
        unsafe_allow_html=True)
else:
    rental_credit = 0.0

st.divider()

# ── Loan Settings ─────────────────────────────────────────────────────────
st.subheader("Loan Settings")
l1, l2, l3 = st.columns(3, gap="medium")
with l1:
    cash = st.number_input("Available cash for purchase ($)",
        min_value=0, max_value=10_000_000, value=100_000, step=10_000, format="%d")
with l2:
    rate = st.number_input("Interest rate (%)",
        min_value=0.1, max_value=20.0, value=6.2, step=0.1, format="%.1f",
        help=f"Banks assess at this + {APRA_BUFFER:.0f}% buffer.")
    term = st.selectbox("Loan term", [25, 30], index=1,
        format_func=lambda x: f"{x} years")
with l3:
    repay_type = st.radio("Repayment type",
        ["Principal & Interest", "Interest Only"],
        help="P&I for owner-occupied. IO common for investors.")
    freq = st.radio("Show repayments", ["Weekly", "Fortnightly", "Monthly"],
                    index=2, horizontal=True)

_FREQ = {"Weekly": (52, "/wk"), "Fortnightly": (26, "/fn"), "Monthly": (12, "/mo")}
def _fmt_repay(monthly_amount):
    """Convert monthly to selected frequency and return formatted string."""
    periods, suffix = _FREQ[freq]
    return f"${monthly_amount * 12 / periods:,.0f}{suffix}"

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════════

# Per-individual tax
tax_1 = income_tax(gross)
tax_2 = income_tax(partner) if partner > 0 else 0.0
total_tax = tax_1 + tax_2
net_annual = combined - total_tax
net_mo = net_annual / 12

# Debts
cc_mo = cc_limit * 0.03
hecs_yr = _hecs(gross, hecs_bal)
hecs_mo = hecs_yr / 12
personal_debt = cc_mo + hecs_mo + other_debt

# Available for repayments
avail = net_mo + rental_credit - expenses - personal_debt - inv_repay_mo

assess_rate = rate + APRA_BUFFER
is_pi = repay_type == "Principal & Interest"
svc_max = max(0.0, _pv_pi(avail, assess_rate, term) if is_pi else _pv_io(avail, assess_rate))

# Build comparison tiers
tiers = {}
for lvr in LVR_TIERS:
    tiers[lvr] = _tier(svc_max, cash, inv_equity, lvr, rate, term, is_pi, state, fhb)

# Determine best fit: LOWEST LVR where user is fully funded (least LMI)
use_equity = has_inv and inv_equity > 0
funding_key = "cash_equity" if use_equity else "cash"
best_lvr = None
for lvr in LVR_TIERS:  # ascending: 80, 85, 90, 95
    if tiers[lvr][funding_key]["shortfall"] == 0 and tiers[lvr][funding_key]["loan"] > 0:
        best_lvr = lvr
        break
# Fallback: smallest shortfall
if best_lvr is None:
    best_lvr = min(LVR_TIERS, key=lambda x: tiers[x][funding_key]["shortfall"])

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — YOUR BORROWING POWER
# ═══════════════════════════════════════════════════════════════════════════
if combined > 0:

    st.subheader("Your Borrowing Power")

    if avail <= 0:
        st.error("Expenses and debts exceed net income. No borrowing capacity.")

    # Hero number — full-width card
    st.markdown(
        f'<div class="bp-hero">'
        f'<div class="lbl">Maximum Borrowing Power</div>'
        f'<div class="bp-amount">${svc_max:,.0f}</div>'
        f'<div><span class="bp-badge">'
        f'Assessed at {assess_rate:.1f}% ({rate:.1f}% + {APRA_BUFFER:.0f}% buffer) '
        f'&middot; {"P&I" if is_pi else "IO"} &middot; {term}yr</span></div>'
        f'<div class="bp-sub">This is what your income supports. Your deposit and LVR determine what you can buy.</div>'
        f'</div>',
        unsafe_allow_html=True)

    # Math breakdown
    with st.expander("How this is calculated", expanded=False):
        if partner > 0:
            tax_html = (
                f'<tr><td class="mlbl">Your income</td><td class="mval">${gross:,.0f}</td></tr>'
                f'<tr><td class="mlbl">Your tax + Medicare</td><td class="mval">−${tax_1:,.0f}</td></tr>'
                f'<tr><td class="mlbl">Partner income</td><td class="mval">${partner:,.0f}</td></tr>'
                f'<tr><td class="mlbl">Partner tax + Medicare</td><td class="mval">−${tax_2:,.0f}</td></tr>')
        else:
            tax_html = (
                f'<tr><td class="mlbl">Gross income</td><td class="mval">${combined:,.0f}</td></tr>'
                f'<tr><td class="mlbl">Tax + Medicare</td><td class="mval">−${total_tax:,.0f}</td></tr>')

        inv_html = ""
        if has_inv:
            inv_html = (
                f'<tr><td class="mlbl">Rental credit (80%)</td><td class="mval">+${rental_credit:,.0f}</td></tr>'
                f'<tr><td class="mlbl">Investment repayments</td><td class="mval">−${inv_repay_mo:,.0f}</td></tr>')

        avail_color = "#C5A880" if avail > 0 else "#C45C5C"
        st.markdown(
            f'<table class="math-tbl">{tax_html}'
            f'<tr class="sep total"><td class="mlbl">Net monthly income</td>'
            f'<td class="mval">${net_mo:,.0f}</td></tr>'
            f'{inv_html}'
            f'<tr><td class="mlbl">Living expenses (HEM)</td><td class="mval">−${expenses:,.0f}</td></tr>'
            f'<tr><td class="mlbl">Credit card (3% of limit)</td><td class="mval">−${cc_mo:,.0f}</td></tr>'
            f'<tr><td class="mlbl">HECS/HELP</td><td class="mval">−${hecs_mo:,.0f}</td></tr>'
            f'<tr><td class="mlbl">Other debts</td><td class="mval">−${other_debt:,.0f}</td></tr>'
            f'<tr class="sep total"><td class="mlbl">Available for repayments</td>'
            f'<td class="mval" style="color:{avail_color}">${avail:,.0f}/mo</td></tr>'
            f'<tr class="sep total"><td class="mlbl">Max loan at {assess_rate:.1f}%</td>'
            f'<td class="mval" style="color:{avail_color}">${svc_max:,.0f}</td></tr>'
            f'</table>',
            unsafe_allow_html=True)

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 3 — WHAT CAN YOU BUY?
    # ═══════════════════════════════════════════════════════════════════════
    st.subheader("What Can You Buy?")

    cols = st.columns(4, gap="medium")

    for col, lvr in zip(cols, LVR_TIERS):
        t_cash = tiers[lvr]["cash"]
        t_eq = tiers[lvr]["cash_equity"] if use_equity else None
        is_best = (lvr == best_lvr)

        best_cls = " tier-card-best" if is_best else ""
        lmi_badge = ('<span class="badge badge-pos" style="border-color:#3B4A42;color:#3B4A42">No LMI</span>'
                     if lvr <= 80
                     else '<span class="badge badge-cau" style="border-color:#C5A880;color:#C5A880">LMI applies</span>')

        # Cash-only row
        funded_cash = t_cash["shortfall"] == 0 and t_cash["loan"] > 0
        verdict_cash = (
            '<span class="badge badge-pos" style="border-color:#3B4A42;color:#3B4A42">Funded</span>' if funded_cash
            else f'<span class="badge badge-neg" style="font-size:12px">Short ${t_cash["shortfall"]:,.0f}</span>')

        lmi_row = (f'<tr><td class="lbl">LMI</td><td class="val">${t_cash["lmi"]:,.0f}</td></tr>'
                   if t_cash["lmi"] > 0 else "")

        html = (
            f'<div class="tier-card{best_cls}">'
            f'<div class="tier-title">{lvr}% LVR</div>'
            f'<div style="margin-bottom:8px">{lmi_badge}</div>'
            f'<table class="tier-tbl">'
            f'<tr class="bold"><td class="lbl">Purchase</td><td class="val">${t_cash["purchase"]:,.0f}</td></tr>'
            f'<tr><td class="lbl">Loan</td><td class="val">${t_cash["loan"]:,.0f}</td></tr>'
            f'<tr><td class="lbl">Deposit</td><td class="val">${t_cash["dep"]:,.0f}</td></tr>'
            f'{lmi_row}'
            f'<tr><td class="lbl">Stamp duty</td><td class="val">${t_cash["sd"]:,.0f}</td></tr>'
            f'<tr><td class="lbl">Legals</td><td class="val">${LEGALS:,.0f}</td></tr>'
            f'<tr class="sep bold"><td class="lbl">Total upfront</td><td class="val">${t_cash["total"]:,.0f}</td></tr>'
            f'<tr><td class="lbl">Your cash</td><td class="val">${cash:,.0f}</td></tr>'
            f'<tr class="sep bold"><td class="lbl">Verdict</td><td class="val">{verdict_cash}</td></tr>'
            f'<tr><td class="lbl">Repayment</td><td class="val">{_fmt_repay(t_cash["monthly"])}</td></tr>'
            f'</table>')

        # Equity row (if applicable)
        if use_equity and t_eq:
            funded_eq = t_eq["shortfall"] == 0 and t_eq["loan"] > 0
            verdict_eq = (
                '<span class="badge badge-pos" style="border-color:#3B4A42;color:#3B4A42">Funded</span>' if funded_eq
                else f'<span class="badge badge-neg" style="font-size:12px">Short ${t_eq["shortfall"]:,.0f}</span>')

            lmi_eq_row = (f'<tr><td class="lbl">LMI</td><td class="val">${t_eq["lmi"]:,.0f}</td></tr>'
                         if t_eq["lmi"] > 0 else "")

            html += (
                f'<div style="border-top:1px solid #333336;margin:10px 0 6px 0"></div>'
                f'<div style="font-size:10px;color:#C5A880;font-family:DM Sans,sans-serif;'
                f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px">With Equity</div>'
                f'<table class="tier-tbl">'
                f'<tr class="bold"><td class="lbl">Purchase</td><td class="val">${t_eq["purchase"]:,.0f}</td></tr>'
                f'<tr><td class="lbl">Loan</td><td class="val">${t_eq["loan"]:,.0f}</td></tr>'
                f'<tr class="sep bold"><td class="lbl">Total upfront</td><td class="val">${t_eq["total"]:,.0f}</td></tr>'
                f'<tr><td class="lbl">Equity draw</td><td class="val">${t_eq["eq_draw"]:,.0f}</td></tr>'
                f'<tr><td class="lbl">Cash required</td><td class="val">${t_eq["cash_req"]:,.0f}</td></tr>'
                f'{lmi_eq_row}'
                f'<tr class="sep bold"><td class="lbl">Verdict</td><td class="val">{verdict_eq}</td></tr>'
                f'<tr><td class="lbl">Repayment</td><td class="val">{_fmt_repay(t_eq["monthly"])}</td></tr>'
                f'</table>')

        html += '</div>'

        with col:
            st.markdown(html, unsafe_allow_html=True)
            if is_best:
                st.markdown(
                    '<div class="card" style="padding:12px 16px;margin-top:8px">'
                    '<span class="micro">'
                    "Best fit — lowest LVR where you're fully funded. "
                    "Higher LVR tiers let you buy more but cost more in LMI."
                    '</span></div>',
                    unsafe_allow_html=True)

    if use_equity:
        st.caption(
            "**Equity note:** Available equity = property value x 80% - loan owing "
            "(capped at 80% LVR on the existing property). "
            "Released as cash via top-up or line of credit. "
            "Funds deposit and costs on the new purchase — does not change the new loan's LVR. "
            "Assessed separately; may have different terms. Cross-collateralisation has risks."
        )

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 4 — YOUR SELECTED DEAL
    # ═══════════════════════════════════════════════════════════════════════
    st.subheader("Your Selected Deal")

    sel_lvr = st.selectbox(
        "LVR tier",
        LVR_TIERS,
        index=LVR_TIERS.index(best_lvr),
        format_func=lambda x: f"{x}% LVR" + (" — best fit" if x == best_lvr else ""),
    )

    sel = tiers[sel_lvr][funding_key]
    sel_loan = sel["loan"]
    sel_purchase = sel["purchase"]

    fin1, fin2 = st.columns(2, gap="large")

    with fin1:
        annual_int = sel_loan * (rate / 100)
        st.markdown(
            f'<div class="card"><div class="lbl">Financing</div>'
            f'<table class="math-tbl">'
            f'<tr><td class="mlbl">Purchase price</td><td class="mval">${sel_purchase:,.0f}</td></tr>'
            f'<tr><td class="mlbl">Deposit ({100 - sel_lvr}%)</td><td class="mval">-${sel["dep"]:,.0f}</td></tr>'
            f'<tr class="sep total"><td class="mlbl">Loan amount</td><td class="mval">${sel_loan:,.0f}</td></tr>'
            f'<tr><td class="mlbl">LVR</td><td class="mval">{sel_lvr}%</td></tr>'
            f'<tr><td class="mlbl">Rate</td><td class="mval">{rate:.1f}%</td></tr>'
            f'<tr><td class="mlbl">Annual interest</td><td class="mval">${annual_int:,.0f}</td></tr>'
            f'</table></div>',
            unsafe_allow_html=True)

    with fin2:
        lmi_row_html = (f'<tr><td class="mlbl">LMI</td><td class="mval">${sel["lmi"]:,.0f}</td></tr>'
                        if sel["lmi"] > 0 else "")
        eq_row_html = (f'<tr><td class="mlbl">Equity draw</td><td class="mval">-${sel["eq_draw"]:,.0f}</td></tr>'
                       if sel["eq_draw"] > 0 else "")
        cash_color = "#C5A880" if sel["shortfall"] == 0 else "#C45C5C"
        st.markdown(
            f'<div class="card"><div class="lbl">Upfront Costs</div>'
            f'<table class="math-tbl">'
            f'<tr><td class="mlbl">Deposit ({100 - sel_lvr}%)</td><td class="mval">${sel["dep"]:,.0f}</td></tr>'
            f'<tr><td class="mlbl">Stamp duty ({state})</td><td class="mval">${sel["sd"]:,.0f}</td></tr>'
            f'{lmi_row_html}'
            f'<tr><td class="mlbl">Legals</td><td class="mval">${LEGALS:,.0f}</td></tr>'
            f'<tr class="sep total"><td class="mlbl">Total upfront</td><td class="mval">${sel["total"]:,.0f}</td></tr>'
            f'{eq_row_html}'
            f'<tr class="sep total"><td class="mlbl">Cash required</td>'
            f'<td class="mval" style="color:{cash_color}">${sel["cash_req"]:,.0f}</td></tr>'
            f'</table></div>',
            unsafe_allow_html=True)

    # Gold hairline between sections
    st.markdown('<div style="width:60%;height:1px;background:#C5A880;margin:16px auto"></div>',
                unsafe_allow_html=True)

    # Repayment comparison
    pi_mo = _repay_pi(sel_loan, rate, term)
    io_mo = _repay_io(sel_loan, rate)
    rc1, rc2 = st.columns(2, gap="medium")
    with rc1:
        st.markdown(
            f'<div class="repay-card">'
            f'<div class="lbl">P&I Repayment</div>'
            f'<div class="repay-val">{_fmt_repay(pi_mo)}</div>'
            f'<div class="sub">${pi_mo * 12:,.0f}/yr</div>'
            f'</div>',
            unsafe_allow_html=True)
    with rc2:
        st.markdown(
            f'<div class="repay-card">'
            f'<div class="lbl">Interest Only</div>'
            f'<div class="repay-val">{_fmt_repay(io_mo)}</div>'
            f'<div class="sub">${io_mo * 12:,.0f}/yr</div>'
            f'</div>',
            unsafe_allow_html=True)
    st.caption(f"At actual rate {rate:.1f}% (not the {assess_rate:.1f}% assessment rate).")

    # Portfolio LVR (if investment properties exist)
    if has_inv and sel_purchase > 0:
        port_value = inv_total_value + sel_purchase
        port_debt = inv_total_loan + sel_loan
        port_lvr = (port_debt / port_value * 100) if port_value > 0 else 0.0
        new_lvr = sel_lvr

        lc1, lc2 = st.columns(2, gap="medium")
        lc1.metric("New Property LVR", f"{new_lvr}%",
                   delta="No LMI" if new_lvr <= 80 else "LMI applies",
                   delta_color="normal" if new_lvr <= 80 else "off")
        port_color = "normal" if port_lvr <= 80 else "inverse"
        lc2.metric("Aggregate Portfolio LVR", f"{port_lvr:.0f}%",
                   delta=f"${port_debt:,.0f} debt / ${port_value:,.0f} value",
                   delta_color=port_color)

        if port_lvr > 80:
            st.warning(
                f"**Aggregate portfolio LVR is {port_lvr:.0f}%.** "
                "Some lenders cap aggregate LVR at 80% across all properties "
                "— confirm with your broker before proceeding."
            )

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 5 — THINGS TO CONSIDER
    # ═══════════════════════════════════════════════════════════════════════
    st.subheader("Things to Consider")

    notes = []
    if svc_max > 1_500_000:
        notes.append(("\U0001f534", "Large loan. Stress-test affordability at higher rates."))
    if sel_lvr > 80:
        notes.append(("\U0001f7e1", f"LMI of ${sel['lmi']:,.0f} applies at {sel_lvr}% LVR."))
    if hecs_bal > 0:
        notes.append(("\U0001f7e1", f"HECS/HELP repayment of ${hecs_yr:,.0f}/yr reduces capacity."))
    if cc_limit > 0:
        notes.append(("\U0001f7e1", f"${cc_mo:,.0f}/mo counted against your ${cc_limit:,.0f} card limit."))
    if deps >= 3:
        notes.append(("\U0001f7e1", "High dependant count increases the HEM benchmark."))
    if net_mo > 0 and pi_mo / net_mo > 0.30:
        notes.append(("\U0001f7e1", f"Repayments are {pi_mo / net_mo * 100:.0f}% of net income (>30% = stress)."))
    if has_inv:
        notes.append(("\U0001f7e1", "Investment repayments reduce capacity. Banks assess the full portfolio."))
        if inv_equity > 0:
            notes.append(("\u2139\ufe0f", f"${inv_equity:,.0f} equity available via top-up (assessed separately)."))

    notes.append(("\u2139\ufe0f", "Banks use their own HEM tables and may apply additional haircuts."))
    notes.append(("\u2139\ufe0f", "Stamp duty estimates are simplified. Check your state revenue office."))
    notes.append(("\u2139\ufe0f", f"First home buyer: {'concessions applied' if fhb else 'toggle above if applicable'}."))

    for icon, note in notes:
        st.markdown(f"{icon} {note}")

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 6 — METHODOLOGY
    # ═══════════════════════════════════════════════════════════════════════
    with st.expander("Methodology"):
        st.markdown(
            "#### APRA Serviceability\n"
            f"Assessed at actual rate + **{APRA_BUFFER:.0f}% buffer** "
            f"(currently {assess_rate:.1f}%).\n\n"

            "#### Net Income\n"
            "Each person's income taxed **separately**. "
            "2024-25 post-Stage 3 brackets: 0%, 16%, 30%, 37%, 45%. "
            "Medicare levy (2%) included.\n\n"

            "#### HEM (Living Expenses)\n"
            "Scales with income: base + ~$750/mo per $40k above $80k combined.\n\n"

            "#### Investment Properties\n"
            "Rental income counted at **80%** (bank risk haircut). "
            "Loan repayments deducted in full. "
            "Available equity = Property value x 80% - Loan owing.\n\n"
            "Banks assess debt across your **entire portfolio**, not just the new loan. "
            "Aggregate LVR = Total debt / Total property value. "
            "Some lenders cap aggregate LVR at 80% even if individual properties are below that.\n\n"

            "#### Borrowing Power\n"
            "```\nAvailable = Net income + Rental credit"
            "\n          - Expenses - Debts - Inv repayments"
            "\nMax loan  = PV of annuity at assessment rate\n```\n"
            "Pure serviceability. Does not depend on deposit or LVR.\n\n"

            "#### Comparison Table\n"
            "Each LVR tier: `loan = min(serviceability, funds / (1 - LVR) x LVR)`. "
            "Equity supplements cash for deposit and costs but does not change the new loan's LVR.\n\n"

            "#### LMI Estimate\n"
            "| LVR | Rate |\n|---|---|\n"
            "| 80-85% | ~0.8% |\n| 85-90% | ~1.8% |\n"
            "| 90-95% | ~2.8% |\n| 95%+ | ~4.0% |\n\n"

            "---\n"
            "*Indicative only. Every lender has different policies and benchmarks. "
            "Equity release is assessed separately. "
            "Not a pre-approval or credit assessment.*"
        )

    st.markdown(
        '<div class="disclaimer" style="text-align:center;margin-top:32px">'
        'Aurelia &middot; Indicative only &middot; Not financial advice &middot; Data as of March 2026</div>',
        unsafe_allow_html=True,
    )

else:
    st.info("Enter your income above to see your borrowing power.")
