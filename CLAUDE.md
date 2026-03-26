# CLAUDE.md — Property Decision Engine

## What This Project Is
A Streamlit-based decision-support tool for Australian property investors. Four pages, one user flow:

1. **Is it a good time to invest?** → Market Climate Dashboard
2. **How much can I invest?** → Borrowing Power Estimator
3. **What property should I pick?** → Property Analyser
4. **What are the next steps?** → Buying Assistant

**This is NOT financial advice.** Every page must include a disclaimer.

---

## Tech Stack
- Python 3.11+, Streamlit (dark theme, custom CSS)
- Pandas / NumPy, Plotly (dark-themed charts, teal/cyan accent)
- Local CSV/JSON data (hardcoded — live feeds later)

---

## Project Structure
```
property-decision-engine/
├── CLAUDE.md
├── Home.py                        ← Streamlit entry point
├── .streamlit/config.toml
├── core/
│   ├── __init__.py
│   ├── charts.py                  ← Plotly chart builders
│   ├── config.py                  ← weights, thresholds, city offsets (LOCKED)
│   ├── data_loader.py             ← load market_data.json + historical CSVs
│   ├── factors.py                 ← sub-score calculations (0–100)
│   ├── locations.py               ← state/suburb lookups, market city mapping
│   ├── reporting.py               ← template-based summary text
│   ├── scoring.py                 ← national/city/state score aggregation
│   └── tax.py                     ← income tax (2024–25), stamp duty by state
├── pages/
│   ├── 01_market_climate.py       ← Page 1 ✅
│   ├── 02_borrowing_power.py      ← Page 2 ✅
│   ├── 03_property_analyser.py    ← Page 3 ✅
│   └── 04_buying_assistant.py     ← Page 4 (stub)
├── data/
│   ├── market_data.json           ← national factor values (March 2026)
│   ├── suburb_data.json           ← sample suburb medians + 7yr history
│   └── historical/                ← CSV time series (rates, inflation, unemployment)
├── tests/
│   └── test_scoring.py
├── PROJECT_SPEC.md
├── UI_NOTES.md
└── requirements.txt
```

---

## Design System
- **Background:** #0E1117 · **Cards:** #1A1D23 · **Accent:** #00BFA5 (teal)
- **Positive:** #00BFA5 / #4CAF50 · **Negative:** #EF5350 · **Caution:** #FFC107
- **Text:** #FAFAFA primary, rgba(255,255,255,0.45) secondary
- Plotly: `plot_bgcolor="#1A1D23"`, `paper_bgcolor="#1A1D23"`
- Report-style layout, card-based sections, expanders for methodology
- Language: practical, confident, never academic

---

## Build Status

### Page 1 — Market Climate Dashboard ✅
652 lines. Overall climate score (67/100), 9-factor weighted model, factor cards grouped by theme, bar chart sorted by weight, key stat cards, "What's Changed Recently", historical trend charts, city rankings with offsets, tailwinds & risks, methodology expander.

Scoring model locked in `core/config.py` — do not change weights or thresholds without explicit instruction.

### Page 2 — Borrowing Power Estimator ✅
~640 lines. Rebuilt from scratch with clear section hierarchy:
- **Section 1 — Inputs:** Income (per-person tax), HEM (income-scaled), debts, investment properties (up to 3 with equity/gearing), loan settings, repayment frequency toggle (weekly/fortnightly/monthly).
- **Section 2 — Borrowing Power:** Single hero number (pure serviceability), expandable math breakdown.
- **Section 3 — What Can You Buy?:** 4-column LVR comparison table (80/85/90/95%), each showing purchase, loan, deposit, LMI, stamp duty, total upfront, verdict (funded/short). If equity exists, shows "cash only" and "with equity" rows per tier. Best-fit auto-selects lowest fully-funded LVR.
- **Section 4 — Selected Deal:** Financing + upfront costs in two-column layout. Repayment comparison (P&I vs IO). Portfolio aggregate LVR (existing + new properties) with >80% caution warning.
- **Section 5 — Things to Consider:** Dynamic caution notes.
- **Section 6 — Methodology:** Full expander.

Key calculations: APRA +3% buffer, per-individual tax, income-scaled HEM ($750/mo per $40k above $80k), 80% rental income haircut, available equity = value×80%−loan.

### Page 3 — Property Analyser ✅
~660 lines. Yield calculations, cash flow, deal scoring, tax estimate, suburb comparison, historical charts.
- State/suburb selection via `core/locations.py` (searchable selectbox)
- Simple (1.5%) or detailed expense mode
- Net yield score (55%) + market score (35%) + cash flow score (10%) = blended deal score
- Tax estimate section with marginal rate selector
- Cash flow frequency toggle (weekly/fortnightly/monthly/annual)
- Suburb comparison against local medians (price, rent, yield)
- Historical context charts (2019–2025) from `suburb_data.json`
- Post–Stage 3 tax brackets (0%, 16%, 30%, 37%, 45%) via `core/tax.py`

### Page 4 — Buying Assistant 📋 STUB — NEXT TO BUILD
10-line placeholder. Planned features:

**Pre-purchase checklist:** Due diligence steps (building inspection, pest, strata report, flood zone, zoning check, title search). Toggleable checklist the user works through.

**Questions for the agent:** Template questions to ask at inspections (body corp fees, current tenancy, reason for sale, days on market, comparable sales).

**Upfront cost summary:** Pull deposit, stamp duty, LMI, legals into one consolidated view. Could link to Borrowing Power page data if user has filled it in.

**Risk flags:** Auto-flag based on property details (high LVR, negative gearing, low yield, high strata).

**Settlement timeline:** Simple visual timeline of typical AU settlement process (contract → cooling off → finance → settlement, ~6 weeks).

**Property comparison notes:** Side-by-side comparison if user is evaluating 2–3 properties.

---

## Data Strategy
**Current (MVP):** All data hardcoded in JSON/CSV. March 2026 values. Sample suburbs only (4 per capital city).
**Future:** RBA, ABS, SQM Research feeds. CoreLogic/PropTrack API. State revenue office stamp duty. Full suburb coverage via `core/locations.py` backend swap.

---

## Key Rules
1. **Keep code modular.** Pages in `pages/`, shared logic in `core/`.
2. **No overengineering.** MVP first.
3. **Match Page 1's design.** Same dark theme, card CSS, colour coding.
4. **Make assumptions explicit.** Show them to the user.
5. **Disclaimers on every page.** "Indicative only · Not financial advice."
6. **Australian context.** AUD, AU tax rates, state-based stamp duty, APRA terminology.
7. **Don't break what works.** Preserve existing functionality.
8. **Test before finishing.** Run `streamlit run Home.py` to verify.

---

## Self-Review Protocol
After building or modifying any feature with calculations or financial logic:

- **Logic:** Challenge hardcoded numbers. Check edge cases ($0 income, $5M property, 0% deposit). Run a worked example.
- **Domain:** Are tax rates, stamp duty, LMI triggers current? Would an experienced AU investor trust it?
- **UI:** Does it match Page 1? Numbers formatted correctly? Clear hierarchy?
- **Output:** ✅ Confident / ⚠️ Assumptions / 🔍 Worth checking

---

## Debug Protocol
Reproduce → Diagnose → Fix (minimum change) → Verify. Common issues: caching (`st.cache_data.clear()`), imports (sys.path hack), CSS (`unsafe_allow_html=True`), annual vs monthly vs gross vs net.

---

## What to Build Next
1. ~~Page 1 — Market Climate~~ ✅
2. ~~Page 2 — Borrowing Power~~ ✅
3. ~~Page 3 — Property Analyser~~ ✅
4. **Page 4 — Buying Assistant** ← CURRENT PRIORITY
5. Data automation + full suburb coverage
6. Cross-page data sharing (pass borrowing power results to property analyser)
