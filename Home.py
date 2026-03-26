import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from core.styles import get_common_css, sidebar_branding

st.set_page_config(
    page_title="Aurelia",
    page_icon="\u25C6",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

st.markdown("""<style>
.home-hero { text-align: center; padding: 56px 0 0 0; }
.home-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 52px; font-weight: 600; color: #F4F4F5;
    margin-bottom: 0; line-height: 1.2;
}
.home-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px; color: #8A8A93; line-height: 1.7;
    max-width: 600px; margin: 0 auto;
}
.home-accent {
    width: 60px; height: 1px; background: #C5A880;
    margin: 20px auto 16px auto;
}
.page-row {
    display: flex; gap: 20px; margin-top: 48px;
}
.page-tile {
    flex: 1;
    background: #222225;
    border: 1px solid #333336;
    border-radius: 0px;
    padding: 32px 28px 24px 28px;
    box-sizing: border-box;
    transition: border-color 0.2s, border-bottom 0.2s;
}
.page-tile:hover { border-color: #C5A880; }
.page-tile-active { border-bottom: 2px solid #C5A880; }
.page-tile-cat {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.12em; color: #C5A880;
    margin-bottom: 10px;
}
.page-tile-name {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 18px; font-weight: 600; color: #F4F4F5;
    margin-bottom: 6px;
}
.page-tile-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px; color: #8A8A93;
    line-height: 1.6; margin-bottom: 14px;
}
.status-dot {
    display: inline-block; width: 6px; height: 6px;
    border-radius: 50%; margin-right: 6px;
    vertical-align: middle;
}
.status-active { background: #C5A880; }
.status-soon { background: #333336; }
.status-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px; color: #8A8A93;
    text-transform: uppercase; letter-spacing: 0.08em;
    vertical-align: middle;
}
</style>""", unsafe_allow_html=True)

st.markdown(
    '<div class="home-hero">'
    '<div class="home-title">Aurelia</div>'
    '<div class="home-accent"></div>'
    '<div class="home-sub">Property Investment Intelligence</div>'
    '</div>',
    unsafe_allow_html=True,
)

pages = [
    ("Market Intelligence", "Market Climate",
     "Is now a good time to invest in Australian property?", True, "/Market_Climate"),
    ("Financial Capacity", "Borrowing Power",
     "How much can you borrow and what can you buy?", True, "/Borrowing_Power"),
    ("Deal Analysis", "Property Analyser",
     "Is this specific property a good investment?", True, "/Property_Analyser"),
    ("Due Diligence", "Buying Assistant",
     "What do you need to check before buying?", False, "/Buying_Assistant"),
]

tiles = '<div class="page-row">'
for cat, name, desc, active, href in pages:
    dot = "status-active" if active else "status-soon"
    status = "Active" if active else "Coming Soon"
    cls = "page-tile page-tile-active" if active else "page-tile"
    tiles += (
        f'<a href="{href}" target="_self" '
        f'style="text-decoration:none;color:inherit;display:block;flex:1">'
        f'<div class="{cls}" style="cursor:pointer;height:100%">'
        f'<div class="page-tile-cat">{cat}</div>'
        f'<div class="page-tile-name">{name}</div>'
        f'<div class="page-tile-desc">{desc}</div>'
        f'<span class="status-dot {dot}"></span>'
        f'<span class="status-text">{status}</span>'
        '</div></a>'
    )
tiles += '</div>'
st.markdown(tiles, unsafe_allow_html=True)

st.markdown(
    '<div style="text-align:center;margin-top:20px">'
    '<span class="micro">Use the sidebar to navigate between pages</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="disclaimer" style="text-align:center;margin-top:24px">'
    'Aurelia \u00b7 v1.0 \u00b7 March 2026</div>',
    unsafe_allow_html=True,
)
