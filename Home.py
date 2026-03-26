import streamlit as st

st.set_page_config(
    page_title="Property Decision Engine",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Property Decision Engine")
st.markdown(
    "A decision-support tool for Australian property buyers and investors."
)
st.markdown("---")

st.markdown(
    """
    ### What this tool does

    This app helps you think through four key property investment questions:

    | Page | Question |
    |------|----------|
    | **Market Climate** | Is now a good time to invest in Australian property? |
    | **Borrowing Power** | How much can I likely borrow? *(coming soon)* |
    | **Property Analyser** | Is this specific property a good investment? *(coming soon)* |
    | **Buying Assistant** | What do I need to check before buying? *(coming soon)* |

    Use the sidebar to navigate between pages.

    ---
    > **Disclaimer:** This tool provides indicative decision-support only.
    > It is not financial advice, credit advice, or a substitute for professional guidance.
    > All data is manually updated and approximate.
    """
)
