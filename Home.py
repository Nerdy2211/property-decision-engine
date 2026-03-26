import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from core.styles import get_common_css, sidebar_branding

st.set_page_config(
    page_title="Property Decision Engine",
    page_icon="\U0001f3e0",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Page-specific CSS
# ---------------------------------------------------------------------------
st.markdown("""<style>
.home-hero { text-align: center; padding: 40px 0 20px 0; }
.home-title {
    font-size: 36px; font-weight: 700; color: #F1F5F9;
    margin-bottom: 6px;
}
.home-sub {
    font-size: 15px; color: rgba(255,255,255,0.4);
    margin-bottom: 0;
}
.page-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 24px;
}
.page-tile {
    background: #111827;
    border: 1px solid rgba(0,191,165,0.06);
    border-radius: 12px;
    padding: 22px 24px 18px 24px;
}
.page-tile-cat {
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.1em; color: rgba(255,255,255,0.25);
    margin-bottom: 6px;
}
.page-tile-name {
    font-size: 17px; font-weight: 700; color: #F1F5F9;
    margin-bottom: 4px;
}
.page-tile-desc {
    font-size: 12px; color: rgba(255,255,255,0.45);
    margin-bottom: 8px;
}
.status-dot {
    display: inline-block; width: 7px; height: 7px;
    border-radius: 50%; margin-right: 5px;
    vertical-align: middle;
}
.status-active { background: #00BFA5; }
.status-soon { background: rgba(255,255,255,0.2); }
.status-text {
    font-size: 10px; color: rgba(255,255,255,0.35);
    text-transform: uppercase; letter-spacing: 0.06em;
    vertical-align: middle;
}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="home-hero">'
    '<div class="home-title">Property Decision Engine</div>'
    '<div class="home-sub">Make smarter property investment decisions</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Page tiles
# ---------------------------------------------------------------------------
pages = [
    ("Market Intelligence", "Market Climate",
     "Is now a good time to invest in Australian property?", True),
    ("Financial Capacity", "Borrowing Power",
     "How much can you likely borrow and what can you buy?", True),
    ("Deal Analysis", "Property Analyser",
     "Is this specific property a good investment?", True),
    ("Due Diligence", "Buying Assistant",
     "What do you need to check before buying?", False),
]

tiles_html = '<div class="page-grid">'
for cat, name, desc, active in pages:
    dot_cls = "status-active" if active else "status-soon"
    status = "Active" if active else "Coming Soon"
    tiles_html += (
        '<div class="page-tile">'
        f'<div class="page-tile-cat">{cat}</div>'
        f'<div class="page-tile-name">{name}</div>'
        f'<div class="page-tile-desc">{desc}</div>'
        f'<span class="status-dot {dot_cls}"></span>'
        f'<span class="status-text">{status}</span>'
        '</div>'
    )
tiles_html += '</div>'

st.markdown(tiles_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div class="disclaimer" style="text-align:center">'
    'Indicative decision-support only \u00b7 Not financial advice \u00b7 '
    'Data manually updated and approximate \u00b7 March 2026 baseline</div>',
    unsafe_allow_html=True,
)
