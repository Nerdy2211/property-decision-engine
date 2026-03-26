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
from core.styles import get_common_css, sidebar_branding, gauge_svg, score_color, badge_class

st.set_page_config(
    page_title="Aurelia | Market Climate",
    page_icon="\u25C6",
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
# Page-specific CSS — editorial luxury design system
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
    background: #222225;
    border: 1px solid #333336;
    border-radius: 0px;
    padding: 20px 22px 18px 22px;
    margin-bottom: 8px;
    border-left: 3px solid #333336;
    flex: 1;
    box-sizing: border-box;
}
.factor-card.green { border-left-color: #C5A880; }
.factor-card.amber { border-left-color: #8A8A93; }
.factor-card.red   { border-left-color: #C45C5C; }
.factor-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    letter-spacing: 1px;
    color: #8A8A93;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 8px;
}
.factor-wt {
    font-size: 10px;
    color: #8A8A93;
    text-transform: none;
    font-weight: 400;
}
.factor-num {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 28px;
    font-weight: 500;
    color: #F4F4F5;
    line-height: 1;
    letter-spacing: -0.5px;
}
.factor-denom {
    font-size: 12px;
    color: #8A8A93;
    font-weight: 400;
    margin-left: 1px;
}
.factor-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    color: #8A8A93;
    line-height: 1.6;
    margin-top: 10px;
}

/* ── Group label ─────────────────────────────────────────────────── */
.group-label {
    font-size: 10px;
    letter-spacing: 2px;
    color: #C5A880;
    text-transform: uppercase;
    font-weight: 600;
    margin: 28px 0 10px;
}

/* ── Shift rows ──────────────────────────────────────────────────── */
.shift-card {
    background: #222225;
    border: 1px solid #333336;
    border-radius: 0px;
    padding: 16px 20px;
    margin-bottom: 8px;
}
.shift-body { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #8A8A93; line-height: 1.55; margin-top: 4px; }

/* ── City rank rows ──────────────────────────────────────────────── */
.rank-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 20px 10px 20px;
    border-bottom: 1px solid #C5A880;
    margin-bottom: 4px;
}
.rank-header-lbl {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #8A8A93;
    font-weight: 600;
}
.rank-row {
    background: #222225;
    border: 1px solid #333336;
    border-radius: 0px;
    padding: 14px 20px;
    margin-bottom: 0px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.rank-row.rank-top { border-left: 3px solid #C5A880; }
.rank-num   { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 24px; font-weight: 500; color: #8A8A93;
              min-width: 40px; font-variant-numeric: tabular-nums; }
.rank-city  { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 600; color: #F4F4F5; }
.rank-state { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #8A8A93; margin-top: 2px; }
.rank-right { margin-left: auto; text-align: right; display: flex; align-items: center; gap: 16px; }
.rank-score { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 20px; font-weight: 500; color: #C5A880; line-height: 1; }
.rank-denom { font-size: 11px; color: #8A8A93; font-weight: 400; }
.rank-band  { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #8A8A93; opacity: 0.5; margin-top: 3px; }
.rank-bar-track { width: 120px; height: 4px; background: #333336; border-radius: 0px; overflow: hidden; }
.rank-bar-fill  { height: 100%; background: #C5A880; border-radius: 0px; }

/* ── Signal items ────────────────────────────────────────────────── */
.signal-head {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    display: block;
    margin-bottom: 20px;
}
.signal-card {
    background: #222225;
    border: 1px solid #333336;
    border-radius: 0px;
    padding: 16px 20px;
    margin-bottom: 8px;
}
.signal-factor { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 700; margin-bottom: 3px; }
.signal-desc   { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #8A8A93; line-height: 1.55; }

</style>
""", unsafe_allow_html=True)


# ============================================================================
# PAGE HEADER — editorial title
# ============================================================================
data_as_of = meta.get("data_as_of", "")

st.markdown(
    '<div style="font-family:Playfair Display,Georgia,serif;font-size:36px;'
    'font-weight:600;color:#F4F4F5;margin-bottom:4px;">Market Climate Dashboard</div>',
    unsafe_allow_html=True,
)
st.caption(
    f"Australia \u00b7 Property Investment Climate \u00b7 Baseline v2 \u00b7 "
    f"Data as of {data_as_of} \u00b7 Indicative only \u00b7 Not financial advice"
)


# ============================================================================
# SECTION 1 — Hero: score card + summary
# ============================================================================
summary_text = get_national_summary(national_score, band_label)

col_gauge, col_summary = st.columns([1.2, 2], gap="large")

with col_gauge:
    st.markdown(
        f'<div style="text-align:center;margin-top:8px;">'
        f'{gauge_svg(national_score, size=280, label=band_label, show_micro=False)}'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="text-align:center;font-family:DM Sans,sans-serif;font-size:10px;'
        'letter-spacing:3px;color:#8A8A93;text-transform:uppercase;'
        'font-weight:600;margin-top:10px;">Overall Climate Score</p>',
        unsafe_allow_html=True,
    )
    st.caption("9-factor weighted model \u00b7 Score range 0\u2013100 \u00b7 Updated March 2026")

with col_summary:
    st.markdown(
        '<p style="font-family:DM Sans,sans-serif;font-size:10px;letter-spacing:2px;'
        'color:#8A8A93;text-transform:uppercase;font-weight:600;margin-bottom:12px;">'
        'Market Summary</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="border-left:3px solid #C5A880;padding-left:16px;'
        f'color:rgba(255,255,255,0.85);font-family:DM Sans,sans-serif;'
        f'font-size:14px;line-height:1.6;">'
        f'{summary_text}</div>',
        unsafe_allow_html=True,
    )

st.divider()


# ============================================================================
# SECTION 2 — KPI Row (no sparklines)
# ============================================================================
kpi_items = [
    {
        "label": "RBA Cash Rate",
        "value": f"{national_values['interest_rate']}%",
        "badge_text": "Restrictive",
        "badge_cls": "badge badge-neg",
        "sub": "Current policy rate",
    },
    {
        "label": "Rental Vacancy",
        "value": f"{national_values['rental_vacancy']}%",
        "badge_text": "Near Record Low",
        "badge_cls": "badge badge-pos",
        "sub": "National average",
    },
    {
        "label": "Net Migration",
        "value": f"{int(national_values['population_growth'] / 1000)}k",
        "badge_text": "Above Average",
        "badge_cls": "badge badge-pos",
        "sub": "Persons per year",
    },
    {
        "label": "Dwelling Approvals",
        "value": f"{int(national_values['housing_supply'] / 1000)}k",
        "badge_text": "Supply Gap",
        "badge_cls": "badge badge-cau",
        "sub": "Annual, below demand",
    },
]

kpi_cols = st.columns(4, gap="small")
for col, item in zip(kpi_cols, kpi_items):
    with col:
        st.markdown(
            f'<div class="card" style="padding:24px 24px 18px 24px;position:relative">'
            f'<span class="{item["badge_cls"]}" style="position:absolute;top:20px;right:20px">{item["badge_text"]}</span>'
            f'<div class="lbl">{item["label"]}</div>'
            f'<div class="val">{item["value"]}</div>'
            f'<div class="sub">{item["sub"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.divider()


# ============================================================================
# SECTION 3 — Factor Scores
# ============================================================================
st.subheader("Factor Scores")
st.caption(
    "Each factor scored 0\u2013100 and weighted by its estimated influence on Australian "
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
        st.markdown(_build_card_html(present_keys[0]), unsafe_allow_html=True)
    else:
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
# ============================================================================
st.subheader("What\u2019s Changed Recently?")
st.caption("Directional context on recent shifts across key factors.")

_shift_icon  = {"positive": "\u2191", "negative": "\u2193", "neutral": "\u2192"}
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
            icon = _shift_icon.get(d, "\u2192")
            # Badge with gold border for factor name
            st.markdown(
                f'<div class="shift-card">'
                f'<div style="margin-bottom:8px">'
                f'<span class="badge" style="border-color:#C5A880;color:#C5A880;">'
                f'{icon} {s["factor"]}</span></div>'
                f'<div class="shift-body">{s["text"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

st.divider()


# ============================================================================
# SECTION 5 — Historical Trends
# ============================================================================
st.subheader("Historical Trends")
st.caption(
    "A point-in-time score shows where conditions are today. "
    "Trend context shows whether they are improving, deteriorating, or stuck \u2014 "
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
            line_color="#C5A880",
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
            line_color="#C5A880",
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
            line_color="#C5A880",
            current_value=national_values["unemployment"],
            reference_label=f"Current: {national_values['unemployment']}%",
            invert_signal=True,
        ),
        use_container_width=True,
    )

st.divider()


# ============================================================================
# SECTION 6 — City Rankings (ledger style)
# ============================================================================
st.subheader("Adjusted Investment Score by City")
st.caption(
    "National score adjusted for local structural factors \u2014 "
    "migration, supply, vacancy, and market conditions. Indicative, not objective rankings."
)

sorted_cities = sorted(city_scores.items(), key=lambda x: x[1]["score"], reverse=True)

# Header row
st.markdown(
    '<div style="display:flex;align-items:center;gap:12px;padding:8px 20px;border-bottom:1px solid #C5A880;margin-bottom:8px">'
    '<span style="font-family:DM Sans,sans-serif;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:#8A8A93;min-width:40px">Rank</span>'
    '<span style="font-family:DM Sans,sans-serif;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:#8A8A93;flex:1">City</span>'
    '<span style="font-family:DM Sans,sans-serif;font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:#8A8A93;text-align:right;min-width:120px">Score</span>'
    '</div>',
    unsafe_allow_html=True,
)

for i, (city, d) in enumerate(sorted_cities):
    rank = i + 1
    top_cls = " rank-top" if rank == 1 else ""
    alt_style = ' style="background:#1C1C1E"' if i % 2 == 1 else ""
    bar_width = int(d["score"] * 120 / 100)
    st.markdown(
        f'<div class="rank-row{top_cls}"{alt_style}>'
        f'<div class="rank-num">{rank:02d}</div>'
        f'<div style="flex:1;">'
        f'<div class="rank-city">{city}</div>'
        f'<div class="rank-state">{d["state"]}</div>'
        f'</div>'
        f'<div class="rank-right">'
        f'<div>'
        f'<div class="rank-score">'
        f'{d["score"]}<span class="rank-denom">/100</span>'
        f'</div>'
        f'<div class="rank-band">{d["offset_direction"]} {d["band_label"]}</div>'
        f'</div>'
        f'<div class="rank-bar-track">'
        f'<div class="rank-bar-fill" style="width:{bar_width}px;"></div>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.divider()


# ============================================================================
# SECTION 7 — Tailwinds & Risks
# ============================================================================
st.subheader("Key Tailwinds & Risks")
st.caption("Derived from top and bottom scoring factors under the current model.")

tailwinds, risks = get_tailwinds_and_risks(sub_scores)
col_tw, col_rk = st.columns(2, gap="large")

def _render_signals(col, title, title_color, items, dot_color):
    with col:
        st.markdown(
            f'<span class="signal-head" style="color:{title_color};">'
            f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{dot_color};margin-right:6px;vertical-align:middle"></span>'
            f'{title}</span>',
            unsafe_allow_html=True,
        )
        for factor_label, desc in items:
            st.markdown(
                f'<div class="signal-card">'
                f'<div class="signal-factor" style="color:{dot_color};">'
                f'<span style="font-size:8px;vertical-align:middle;margin-right:6px;">\u25cf</span>'
                f'{factor_label}</div>'
                f'<div class="signal-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

_render_signals(col_tw, "Tailwinds",        "#C5A880", tailwinds, "#C5A880")
_render_signals(col_rk, "Risks / Headwinds", "#C45C5C", risks,     "#C45C5C")

st.divider()


# ============================================================================
# SECTION 8 — Methodology expander — content unchanged
# ============================================================================
with st.expander("How scores are calculated"):
    st.markdown(
        "The national score is a weighted average of 9 factor sub-scores. "
        "Each sub-score maps a raw value to a 0\u2013100 scale using documented thresholds.\n\n"
        "**Model priorities:** Interest rates carry the highest weight (28%) because they are the "
        "single largest lever on Australian property affordability and borrowing capacity. "
        "Population growth (16%) and supply conditions \u2014 housing approvals (13%) plus rental vacancy (11%) \u2014 "
        "together account for 40% of the score, reflecting how structurally supply-constrained the Australian "
        "market has become relative to demand.\n\n"
        "**Inflation (10%)** is weighted below interest rates deliberately, as its main relevance to property "
        "is through its influence on rate expectations \u2014 capturing it separately avoids double-counting the same signal.\n\n"
        "**Global macro risk (6%)** acts as a meaningful overlay. Australian property is exposed to external shocks "
        "\u2014 particularly China, commodity prices, and global credit conditions \u2014 but these are secondary to the "
        "domestic rate and supply cycle.\n\n"
        "**Threshold calibration:** Scoring ranges were set to reflect realistic Australian conditions, "
        "not theoretical extremes. Specifically:\n"
        "- *Interest rates:* the bearish end is 6.0% (not 7.0%). Rates above 6% would be extraordinary in "
        "the modern Australian context. Using 7% as the floor made 4%+ rates look moderate when they are "
        "genuinely restrictive. At 6% as the floor, current rates score just below neutral \u2014 a mild headwind.\n"
        "- *Unemployment:* the bullish end is 3.0% (not 3.5%). Australia\u2019s all-time low was around 3.4%, "
        "so using 3.5% as \u2018perfect\u2019 compressed too much of the realistic range into the top of the scale. "
        "At 3.0% as the ceiling, a rate of 4%+ scores as good-but-not-excellent, which is a more honest read.\n\n"
        "Weights and thresholds are the author\u2019s considered view, documented here for transparency. "
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

    st.markdown(
        '<div class="disclaimer" style="text-align:center;margin-top:32px">'
        'Aurelia \u00b7 v1.0 \u00b7 March 2026</div>',
        unsafe_allow_html=True,
    )
