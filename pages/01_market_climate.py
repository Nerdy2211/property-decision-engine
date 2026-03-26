import sys
import os
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from core.data_loader import (
    load_market_data, get_national_values, get_city_data,
    get_recent_shifts, get_meta, load_historical_series,
)
from core.scoring import run_full_scoring
from core.config import FACTOR_GROUPS, FACTOR_LABELS, WEIGHTS
from core.charts import factor_bar_chart, historical_line_chart
from core.reporting import (
    get_national_summary,
    get_tailwinds_and_risks,
    get_methodology_rows,
    FACTOR_DESCRIPTIONS,
)
from core.styles import get_common_css, sidebar_branding, gauge_svg, sparkline_svg, score_color, badge_class

st.set_page_config(
    page_title="Market Climate | Property Decision Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data loading — unchanged
# ---------------------------------------------------------------------------
data            = load_market_data()
national_values = get_national_values(data)
city_data_raw   = get_city_data(data)
recent_shifts   = get_recent_shifts(data)
meta            = get_meta(data)
results         = run_full_scoring(national_values)

sub_scores     = results["sub_scores"]
national_score = results["national_score"]
band_label     = results["band_label"]
band_color     = results["color"]
city_scores    = results["city_scores"]

# ---------------------------------------------------------------------------
# Page-specific CSS only (shared classes now in core/styles.py)
# ---------------------------------------------------------------------------
st.markdown("""
<style>

/* ── Global ──────────────────────────────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1400px;
}

/* ── Factor card row ─────────────────────────────────────────────── */
.factor-row {
    display: flex;
    gap: 10px;
    align-items: stretch;
    margin-bottom: 0;
}

/* ── Factor cards ────────────────────────────────────────────────── */
.factor-card {
    background: #111827;
    border: 1px solid rgba(0,191,165,0.06);
    border-radius: 12px;
    padding: 16px 18px 14px;
    margin-bottom: 8px;
    border-left: 3px solid #2A2D33;
    flex: 1;
    box-sizing: border-box;
}
.factor-card.green { border-left-color: #00BFA5; }
.factor-card.amber { border-left-color: #F59E0B; }
.factor-card.red   { border-left-color: #EF4444; }
.factor-name {
    font-size: 10px;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.25);
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 8px;
}
.factor-wt {
    font-size: 10px;
    color: rgba(255,255,255,0.18);
    text-transform: none;
    font-weight: 400;
}
.factor-num {
    font-size: 26px;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.5px;
}
.factor-denom {
    font-size: 12px;
    color: rgba(255,255,255,0.22);
    font-weight: 400;
    margin-left: 1px;
}
.factor-desc {
    font-size: 11px;
    color: rgba(255,255,255,0.37);
    line-height: 1.55;
    min-height: calc(11px * 1.55 * 3);
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ── Group label ─────────────────────────────────────────────────── */
.group-label {
    font-size: 10px;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.22);
    text-transform: uppercase;
    font-weight: 600;
    margin: 20px 0 10px;
}

/* ── Shift rows ──────────────────────────────────────────────────── */
.shift-card {
    background: #111827;
    border: 1px solid rgba(0,191,165,0.06);
    border-radius: 12px;
    padding: 14px 18px 12px;
    margin-bottom: 8px;
}
.shift-body { font-size: 12px; color: rgba(255,255,255,0.42); line-height: 1.55; margin-top: 4px; }

/* ── City rank rows ──────────────────────────────────────────────── */
.rank-row {
    background: #111827;
    border: 1px solid rgba(0,191,165,0.06);
    border-radius: 12px;
    padding: 14px 20px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.rank-row.rank-top { border-left: 3px solid #00BFA5; }
.rank-num   { font-size: 18px; font-weight: 800; color: rgba(255,255,255,0.25);
              min-width: 40px; font-variant-numeric: tabular-nums; }
.rank-city  { font-size: 15px; font-weight: 700; color: #F1F5F9; }
.rank-state { font-size: 11px; color: rgba(255,255,255,0.25); margin-top: 2px; }
.rank-right { margin-left: auto; text-align: right; }
.rank-score { font-size: 20px; font-weight: 800; line-height: 1; }
.rank-denom { font-size: 11px; color: rgba(255,255,255,0.22); font-weight: 400; }
.rank-band  { font-size: 11px; color: rgba(255,255,255,0.25); margin-top: 3px; }

/* ── Signal items ────────────────────────────────────────────────── */
.signal-head {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    display: block;
    margin-bottom: 14px;
}
.signal-card {
    background: #111827;
    border: 1px solid rgba(0,191,165,0.06);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
}
.signal-factor { font-size: 13px; font-weight: 700; margin-bottom: 3px; }
.signal-desc   { font-size: 12px; color: rgba(255,255,255,0.40); line-height: 1.55; }

</style>
""", unsafe_allow_html=True)


# ============================================================================
# PAGE HEADER — native Streamlit
# ============================================================================
data_as_of = meta.get("data_as_of", "")

st.markdown("## Market Climate Dashboard")
st.caption(
    f"Australia · Property Investment Climate · Baseline v2 · "
    f"Data as of {data_as_of} · Indicative only · Not financial advice"
)


# ============================================================================
# SECTION 1 — Hero: gauge + summary
# Streamlit-native layout; gauge is one self-contained SVG block
# ============================================================================
summary_text = get_national_summary(national_score, band_label)

col_gauge, col_summary = st.columns([1, 2.2], gap="large")

with col_gauge:
    st.markdown(
        f'<div style="text-align:center;margin-top:8px;">'
        f'{gauge_svg(national_score, band_color, size=200, label=band_label)}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="text-align:center;font-size:10px;letter-spacing:2px;'
        'color:rgba(255,255,255,0.22);text-transform:uppercase;'
        'font-weight:600;margin-top:2px;">Overall Climate Score</p>',
        unsafe_allow_html=True,
    )

with col_summary:
    st.markdown(
        '<p style="font-size:10px;letter-spacing:2px;color:rgba(255,255,255,0.25);'
        'text-transform:uppercase;font-weight:600;margin-bottom:12px;">Market Summary</p>',
        unsafe_allow_html=True,
    )
    st.markdown(summary_text)
    st.caption(f"9-factor weighted model · Score range 0–100 · Updated {data_as_of}")

st.divider()


# ============================================================================
# SECTION 2 — KPI Row
# st.columns layout; one st.markdown per card (no concatenated loops)
# ============================================================================
kpi_items = [
    {
        "label": "RBA Cash Rate",
        "value": f"{national_values['interest_rate']}%",
        "badge_text": "Restrictive",
        "badge_cls": "badge badge-neg",
        "sub": "Current policy rate",
        "sparkline": [0.10, 0.10, 0.35, 1.85, 3.60, 4.35, 4.10],
    },
    {
        "label": "Rental Vacancy",
        "value": f"{national_values['rental_vacancy']}%",
        "badge_text": "Near Record Low",
        "badge_cls": "badge badge-pos",
        "sub": "National average",
        "sparkline": [2.2, 1.8, 1.3, 1.0, 1.1, 1.2, 1.1],
    },
    {
        "label": "Net Migration",
        "value": f"{int(national_values['population_growth'] / 1000)}k",
        "badge_text": "Above Average",
        "badge_cls": "badge badge-pos",
        "sub": "Persons per year",
        "sparkline": [240, 195, -85, 170, 510, 440, 380],
    },
    {
        "label": "Dwelling Approvals",
        "value": f"{int(national_values['housing_supply'] / 1000)}k",
        "badge_text": "Supply Gap",
        "badge_cls": "badge badge-cau",
        "sub": "Annual, below demand",
        "sparkline": [220, 195, 180, 175, 165, 162, 160],
    },
]

kpi_cols = st.columns(4, gap="small")
for col, item in zip(kpi_cols, kpi_items):
    with col:
        spark = sparkline_svg(item["sparkline"], width=80, height=20)
        st.markdown(
            f'<div class="card" style="padding:18px 20px 14px;">'
            f'<div class="lbl">{item["label"]}</div>'
            f'<div class="val">{item["value"]}</div>'
            f'<span class="{item["badge_cls"]}">{item["badge_text"]}</span>'
            f'<div class="sub" style="margin-top:6px;">{item["sub"]}</div>'
            f'{spark}'
            f'</div>',
            unsafe_allow_html=True,
        )

st.divider()


# ============================================================================
# SECTION 3 — Factor Scores
# st.columns per group; one st.markdown per factor card
# ============================================================================
st.subheader("Factor Scores")
st.caption(
    "Each factor scored 0–100 and weighted by its estimated influence on Australian "
    "property market conditions. Grouped by theme."
)

def _score_class(score):
    if score >= 65: return "green"
    elif score >= 40: return "amber"
    return "red"

def _build_card_html(key):
    """Return the inner HTML string for a single factor card."""
    score      = round(sub_scores[key])
    card_cls   = _score_class(score)
    color      = score_color(score)
    desc       = FACTOR_DESCRIPTIONS.get(key, "")
    label      = FACTOR_LABELS[key]
    weight_pct = int(WEIGHTS.get(key, 0) * 100)
    return (
        f'<div class="factor-card {card_cls}">'
        f'<div class="factor-name">'
        f'{label} <span class="factor-wt">({weight_pct}% wt)</span>'
        f'</div>'
        f'<div class="factor-num" style="color:{color};">'
        f'{score}<span class="factor-denom">/100</span>'
        f'</div>'
        f'<div class="prog-track" style="margin:10px 0 9px;">'
        f'<div class="prog-fill" style="width:{score}%;background:{color};"></div>'
        f'</div>'
        f'<div class="factor-desc">{desc}</div>'
        f'</div>'
    )

for group_name, factor_keys in FACTOR_GROUPS.items():
    st.markdown(
        f'<div class="group-label">{group_name}</div>',
        unsafe_allow_html=True,
    )

    present_keys = [k for k in factor_keys if k in sub_scores]

    if len(present_keys) == 1:
        # Single full-width card — no flex row needed
        st.markdown(_build_card_html(present_keys[0]), unsafe_allow_html=True)
    else:
        # Render all cards for this group in one flex row so align-items:stretch
        # guarantees equal height without relying on Streamlit column internals.
        row_html = '<div class="factor-row">'
        for key in present_keys:
            row_html += _build_card_html(key)
        row_html += '</div>'
        st.markdown(row_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.plotly_chart(factor_bar_chart(sub_scores), use_container_width=True)

st.divider()


# ============================================================================
# SECTION 4 — What's Changed Recently?
# st.columns layout; one st.markdown per shift row
# ============================================================================
st.subheader("What's Changed Recently?")
st.caption("Directional context on recent shifts across key factors.")

_shift_icon  = {"positive": "↑", "negative": "↓", "neutral": "→"}
_shift_badge = {
    "positive": "badge badge-pos",
    "negative": "badge badge-neg",
    "neutral":  "badge badge-cau",
}

half = len(recent_shifts) // 2 + len(recent_shifts) % 2
col_a, col_b = st.columns(2, gap="large")

for col, batch in ((col_a, recent_shifts[:half]), (col_b, recent_shifts[half:])):
    with col:
        for s in batch:
            d    = s.get("direction", "neutral")
            bcls = _shift_badge.get(d, "badge badge-cau")
            icon = _shift_icon.get(d, "→")
            st.markdown(
                f'<div class="shift-card">'
                f'<span class="{bcls}">{icon} {s["factor"]}</span>'
                f'<div class="shift-body">{s["text"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

st.divider()


# ============================================================================
# SECTION 5 — Historical Trends
# Unchanged — already stable (native st.columns + st.plotly_chart)
# ============================================================================
st.subheader("Historical Trends")
st.caption(
    "A point-in-time score shows where conditions are today. "
    "Trend context shows whether they are improving, deteriorating, or stuck — "
    "which matters more for timing than any single reading."
)

df_rates = load_historical_series("interest_rates")
df_cpi   = load_historical_series("inflation")
df_unemp = load_historical_series("unemployment")

h_col1, h_col2, h_col3 = st.columns(3, gap="medium")

with h_col1:
    st.plotly_chart(
        historical_line_chart(
            df_rates, title="RBA Cash Rate", yaxis_label="% p.a.",
            line_color="#06B6D4",
            current_value=national_values["interest_rate"],
            reference_label=f"Current: {national_values['interest_rate']}%",
            invert_signal=True,
        ),
        use_container_width=True,
    )

with h_col2:
    st.plotly_chart(
        historical_line_chart(
            df_cpi, title="Inflation (CPI, Annual)", yaxis_label="% annual",
            line_color="#06B6D4",
            current_value=national_values["inflation"],
            reference_label=f"Current: {national_values['inflation']}%",
            invert_signal=True,
        ),
        use_container_width=True,
    )

with h_col3:
    st.plotly_chart(
        historical_line_chart(
            df_unemp, title="Unemployment Rate", yaxis_label="%",
            line_color="#06B6D4",
            current_value=national_values["unemployment"],
            reference_label=f"Current: {national_values['unemployment']}%",
            invert_signal=True,
        ),
        use_container_width=True,
    )

st.divider()


# ============================================================================
# SECTION 6 — City Rankings
# Loop of individual st.markdown calls — one per row, never concatenated
# ============================================================================
st.subheader("Adjusted Investment Score by City")
st.caption(
    "National score adjusted for local structural factors — "
    "migration, supply, vacancy, and market conditions. Indicative, not objective rankings."
)

sorted_cities = sorted(city_scores.items(), key=lambda x: x[1]["score"], reverse=True)

for rank, (city, d) in enumerate(sorted_cities, 1):
    top_cls = " rank-top" if rank == 1 else ""
    st.markdown(
        f'<div class="rank-row{top_cls}">'
        f'<div class="rank-num">{rank:02d}</div>'
        f'<div>'
        f'<div class="rank-city">{city}</div>'
        f'<div class="rank-state">{d["state"]}</div>'
        f'</div>'
        f'<div class="rank-right">'
        f'<div class="rank-score" style="color:#00BFA5;">'
        f'{d["score"]}<span class="rank-denom">/100</span>'
        f'</div>'
        f'<div class="rank-band">{d["offset_direction"]} {d["band_label"]}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.divider()


# ============================================================================
# SECTION 7 — Tailwinds & Risks
# st.columns layout; one st.markdown per signal item
# ============================================================================
st.subheader("Key Tailwinds & Risks")
st.caption("Derived from top and bottom scoring factors under the current model.")

tailwinds, risks = get_tailwinds_and_risks(sub_scores)
col_tw, col_rk = st.columns(2, gap="large")

def _render_signals(col, title, title_color, items, dot_color):
    with col:
        st.markdown(
            f'<span class="signal-head" style="color:{title_color};">{title}</span>',
            unsafe_allow_html=True,
        )
        for factor_label, desc in items:
            st.markdown(
                f'<div class="signal-card">'
                f'<div class="signal-factor" style="color:{dot_color};">'
                f'<span style="font-size:8px;vertical-align:middle;margin-right:6px;">●</span>'
                f'{factor_label}</div>'
                f'<div class="signal-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

_render_signals(col_tw, "Tailwinds",        "#00BFA5", tailwinds, "#00BFA5")
_render_signals(col_rk, "Risks / Headwinds", "#EF4444", risks,     "#EF4444")

st.divider()


# ============================================================================
# SECTION 8 — Methodology expander — content unchanged
# ============================================================================
with st.expander("How scores are calculated"):
    st.markdown(
        "The national score is a weighted average of 9 factor sub-scores. "
        "Each sub-score maps a raw value to a 0–100 scale using documented thresholds.\n\n"
        "**Model priorities:** Interest rates carry the highest weight (28%) because they are the "
        "single largest lever on Australian property affordability and borrowing capacity. "
        "Population growth (16%) and supply conditions — housing approvals (13%) plus rental vacancy (11%) — "
        "together account for 40% of the score, reflecting how structurally supply-constrained the Australian "
        "market has become relative to demand.\n\n"
        "**Inflation (10%)** is weighted below interest rates deliberately, as its main relevance to property "
        "is through its influence on rate expectations — capturing it separately avoids double-counting the same signal.\n\n"
        "**Global macro risk (6%)** acts as a meaningful overlay. Australian property is exposed to external shocks "
        "— particularly China, commodity prices, and global credit conditions — but these are secondary to the "
        "domestic rate and supply cycle.\n\n"
        "**Threshold calibration:** Scoring ranges were set to reflect realistic Australian conditions, "
        "not theoretical extremes. Specifically:\n"
        "- *Interest rates:* the bearish end is 6.0% (not 7.0%). Rates above 6% would be extraordinary in "
        "the modern Australian context. Using 7% as the floor made 4%+ rates look moderate when they are "
        "genuinely restrictive. At 6% as the floor, current rates score just below neutral — a mild headwind.\n"
        "- *Unemployment:* the bullish end is 3.0% (not 3.5%). Australia's all-time low was around 3.4%, "
        "so using 3.5% as 'perfect' compressed too much of the realistic range into the top of the scale. "
        "At 3.0% as the ceiling, a rate of 4%+ scores as good-but-not-excellent, which is a more honest read.\n\n"
        "Weights and thresholds are the author's considered view, documented here for transparency. "
        "This model is baseline v2, locked March 2026."
    )

    rows = get_methodology_rows(sub_scores, national_values)
    df   = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("#### City Offset Rationale")
    city_table = []
    for city, cdata in city_scores.items():
        offset_str = f"{'+' if cdata['offset'] > 0 else ''}{cdata['offset']}"
        rationale  = city_data_raw.get(city, {}).get("rationale", "")
        city_table.append({
            "City":           city,
            "State":          cdata["state"],
            "Offset":         offset_str,
            "Adjusted Score": f"{cdata['score']}/100",
            "Score":          cdata["score"],
            "Rationale":      rationale,
        })
    city_df = (
        pd.DataFrame(city_table)
        .sort_values("Score", ascending=False)
        .drop(columns=["Score"])
    )
    st.dataframe(city_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown(
        "<span style='font-size:12px;color:#888;'>"
        "**Disclaimer:** This tool provides indicative decision-support only. "
        "It is not financial advice, credit advice, or a substitute for professional guidance. "
        "All data is manually updated and represents a point-in-time snapshot. "
        "Time-series history and live data feeds are planned for a future version."
        "</span>",
        unsafe_allow_html=True,
    )
