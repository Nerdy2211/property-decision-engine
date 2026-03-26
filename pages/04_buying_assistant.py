import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
from core.styles import get_common_css, sidebar_branding

st.set_page_config(
    page_title="Buying Assistant | Property Decision Engine",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_common_css(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_branding(), unsafe_allow_html=True)

st.markdown("## Buying Assistant")
st.caption("Indicative only \u00b7 Not financial advice.")
st.divider()

st.markdown("""
<div class="card" style="max-width:700px">
  <div class="lbl">Coming Soon</div>
  <div style="font-size:15px;color:#F1F5F9;font-weight:600;margin-bottom:12px">
    Due diligence and buying workflow support
  </div>
  <div style="font-size:12px;color:rgba(255,255,255,0.45);line-height:1.7">
    <strong style="color:rgba(255,255,255,0.6)">Pre-purchase checklist</strong>
    &mdash; Building inspection, pest, strata report, flood zone, zoning, title search<br>
    <strong style="color:rgba(255,255,255,0.6)">Questions for the agent</strong>
    &mdash; Body corp fees, tenancy, reason for sale, days on market, comparables<br>
    <strong style="color:rgba(255,255,255,0.6)">Upfront cost summary</strong>
    &mdash; Deposit, stamp duty, LMI, legals in one view<br>
    <strong style="color:rgba(255,255,255,0.6)">Risk flags</strong>
    &mdash; Auto-flag high LVR, negative gearing, low yield, high strata<br>
    <strong style="color:rgba(255,255,255,0.6)">Settlement timeline</strong>
    &mdash; Contract &rarr; cooling off &rarr; finance &rarr; settlement (~6 weeks)<br>
    <strong style="color:rgba(255,255,255,0.6)">Property comparison</strong>
    &mdash; Side-by-side notes for 2&ndash;3 properties
  </div>
</div>
""", unsafe_allow_html=True)
