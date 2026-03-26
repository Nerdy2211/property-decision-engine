import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
from core.styles import get_common_css, sidebar_branding

st.set_page_config(
    page_title="Aurelia | Buying Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

st.markdown(
    '<div style="font-family:Playfair Display,Georgia,serif;font-size:36px;'
    'font-weight:600;color:#F4F4F5;margin-bottom:4px">Buying Assistant</div>',
    unsafe_allow_html=True,
)
st.caption("Indicative only \u00b7 Not financial advice.")
st.divider()

st.markdown("""
<div class="card" style="max-width:700px;margin:0 auto;border-left:3px solid #C5A880">
  <div class="lbl" style="color:#C5A880">Coming Soon</div>
  <div style="font-family:Playfair Display,Georgia,serif;font-size:18px;
       color:#F4F4F5;font-weight:600;margin-bottom:16px">
    Due diligence and buying workflow support
  </div>
  <div style="font-family:DM Sans,sans-serif;font-size:13px;color:#8A8A93;line-height:1.8">
    <strong style="color:#F4F4F5;font-weight:500">Pre-purchase checklist</strong>
    &mdash; Building inspection, pest, strata report, flood zone, zoning, title search<br>
    <strong style="color:#F4F4F5;font-weight:500">Questions for the agent</strong>
    &mdash; Body corp fees, tenancy, reason for sale, days on market, comparables<br>
    <strong style="color:#F4F4F5;font-weight:500">Upfront cost summary</strong>
    &mdash; Deposit, stamp duty, LMI, legals in one view<br>
    <strong style="color:#F4F4F5;font-weight:500">Risk flags</strong>
    &mdash; Auto-flag high LVR, negative gearing, low yield, high strata<br>
    <strong style="color:#F4F4F5;font-weight:500">Settlement timeline</strong>
    &mdash; Contract &rarr; cooling off &rarr; finance &rarr; settlement (~6 weeks)<br>
    <strong style="color:#F4F4F5;font-weight:500">Property comparison</strong>
    &mdash; Side-by-side notes for 2&ndash;3 properties
  </div>
</div>
<div class="micro" style="text-align:center;margin-top:16px">This page is under development</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="disclaimer" style="text-align:center;margin-top:32px">'
    'Indicative only \u00b7 Not financial advice \u00b7 Data as of March 2026</div>',
    unsafe_allow_html=True,
)
