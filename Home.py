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

st.markdown("""<style>
.home-hero { text-align: center; padding: 48px 0 0 0; }
.home-title {
    font-size: 44px; font-weight: 700; color: #F1F5F9;
    margin-bottom: 0;
}
.home-accent {
    width: 80px; height: 2px; background: #00BFA5;
    margin: 16px auto 12px auto; border-radius: 1px;
}
.home-sub {
    font-size: 15px; color: rgba(255,255,255,0.35);
    margin-bottom: 0;
}
.page-row {
    display: flex;
    gap: 14px;
    margin-top: 48px;
}
.page-tile {
    flex: 1;
    background: #111827;
    border: 1px solid rgba(0,191,165,0.06);
    border-radius: 12px;
    padding: 28px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
    transition: border-color 0.2s;
    box-sizing: border-box;
}
.page-tile:hover { border-color: rgba(0,191,165,0.2); }
.page-tile-active { border-bottom: 2px solid #00BFA5; }
.page-tile-cat {
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.1em; color: rgba(255,255,255,0.25);
    margin-bottom: 8px;
}
.page-tile-name {
    font-size: 16px; font-weight: 700; color: #F1F5F9;
    margin-bottom: 5px;
}
.page-tile-desc {
    font-size: 12px; color: rgba(255,255,255,0.4);
    line-height: 1.6; margin-bottom: 12px;
}
.status-dot {
    display: inline-block; width: 7px; height: 7px;
    border-radius: 50%; margin-right: 5px;
    vertical-align: middle;
}
.status-active { background: #00BFA5; }
.status-soon { background: rgba(255,255,255,0.2); }
.status-text {
    font-size: 10px; color: rgba(255,255,255,0.3);
    text-transform: uppercase; letter-spacing: 0.06em;
    vertical-align: middle;
}
</style>""", unsafe_allow_html=True)

# ── Hero ──
st.markdown(
    '<div class="home-hero">'
    '<div class="home-title">Property Decision Engine</div>'
    '<div class="home-accent"></div>'
    '<div class="home-sub">Make smarter property investment decisions</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Page tiles — single row ──
pages = [
    ("Market Intelligence", "Market Climate",
     "Is now a good time to invest in Australian property?", True),
    ("Financial Capacity", "Borrowing Power",
     "How much can you borrow and what can you buy?", True),
    ("Deal Analysis", "Property Analyser",
     "Is this specific property a good investment?", True),
    ("Due Diligence", "Buying Assistant",
     "What do you need to check before buying?", False),
]

tiles = '<div class="page-row">'
for cat, name, desc, active in pages:
    dot = "status-active" if active else "status-soon"
    status = "Active" if active else "Coming Soon"
    cls = "page-tile page-tile-active" if active else "page-tile"
    tiles += (
        f'<div class="{cls}">'
        f'<div class="page-tile-cat">{cat}</div>'
        f'<div class="page-tile-name">{name}</div>'
        f'<div class="page-tile-desc">{desc}</div>'
        f'<span class="status-dot {dot}"></span>'
        f'<span class="status-text">{status}</span>'
        '</div>'
    )
tiles += '</div>'
st.markdown(tiles, unsafe_allow_html=True)

st.markdown(
    '<div style="text-align:center;margin-top:20px">'
    '<span class="micro">Use the sidebar to navigate between pages</span>'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align:center;margin-top:8px">'
    '<span class="micro">v1.0 \u00b7 Baseline March 2026 \u00b7 Brisbane, QLD</span>'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="disclaimer" style="text-align:center;margin-top:24px">'
    'Indicative decision-support only \u00b7 Not financial advice \u00b7 '
    'Data manually updated and approximate</div>',
    unsafe_allow_html=True,
)
