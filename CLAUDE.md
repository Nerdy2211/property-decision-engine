# CLAUDE.md — Aurelia

## What This Is
**Aurelia** — institutional-grade property investment intelligence for the Australian market. Streamlit app, four pages:

1. **Market Climate** → 9-factor scoring model, city rankings, historical trends
2. **Borrowing Power** → APRA serviceability, LVR comparison table, equity analysis
3. **Property Analyser** → Yield, cash flow, deal score, suburb comparison
4. **Buying Assistant** → Due diligence workflow (stub — next to build)

**Not financial advice.** Every page includes a disclaimer.

---

## Tech Stack
- Python 3.11+, Streamlit, Pandas/NumPy, Plotly
- Google Fonts: Playfair Display, DM Sans, Cormorant Garamond
- Local CSV/JSON data (March 2026 baseline)

---

## Project Structure
```
property-decision-engine/
├── Home.py                          ← Landing page ("Aurelia")
├── .streamlit/config.toml           ← Dark theme, gold primary
├── core/
│   ├── styles.py                    ← Shared design system + CSS
│   ├── charts.py                    ← Plotly builders (gold palette)
│   ├── config.py                    ← Scoring weights/thresholds (LOCKED)
│   ├── tax.py                       ← Income tax (2024–25), stamp duty
│   ├── locations.py                 ← State/suburb lookups
│   ├── scoring.py                   ← National/city score aggregation
│   ├── factors.py                   ← Sub-score calculations (0–100)
│   ├── data_loader.py               ← Load market_data.json + CSVs
│   └── reporting.py                 ← Summary text templates
├── pages/
│   ├── 01_Market_Climate.py         ← Page 1 ✅
│   ├── 02_Borrowing_Power.py        ← Page 2 ✅
│   ├── 03_Property_Analyser.py      ← Page 3 ✅
│   └── 04_Buying_Assistant.py       ← Page 4 (styled stub)
├── data/
│   ├── market_data.json, suburb_data.json
│   └── historical/*.csv
└── requirements.txt
```

---

## Design System — Editorial Luxury
**Fonts:** Playfair Display (headings), DM Sans (body/labels), Cormorant Garamond (data numbers)
**Palette:** Gold `#C5A880` primary, charcoal `#161618` background, `#222225` surface, `#333336` borders, `#8A8A93` muted text, `#F4F4F5` primary text. Positive `#3B4A42`/`#6B8F7B`, negative `#6B3A3A`/`#C47070`.
**Cards:** Sharp edges (0px radius), 1px solid `#333336` border, no shadows. Padding 24px.
**Badges:** Outlined only — transparent bg, 1px border, 0px radius, 3px 12px padding.
**Section headers:** Gold left border (4px solid `#C5A880`), Playfair Display.
**Score display:** Cormorant Garamond 72px (hero) or 28px (cards), with gold hairline divider.
**Charts:** Gold `#C5A880` lines, transparent backgrounds, `#8A8A93` axis text.

All styles in `core/styles.py`. Pages import `get_common_css()` and `sidebar_branding()`.

---

## Build Status

### Page 1 — Market Climate ✅
Score card hero (67/100), 4 KPI cards with absolute-positioned badges, factor cards with gold progress bars, ledger-style city rankings with header row and inline score bars, tailwinds/risks with coloured dots, historical trend charts, methodology expander. Scoring model locked in `core/config.py`.

### Page 2 — Borrowing Power ✅
Hero borrowing amount (Cormorant 48px), serviceability math breakdown, 4-column LVR comparison (80/85/90/95%) with cash-only and cash+equity rows, best-fit auto-selection (lowest fully-funded LVR), selected deal with financing/upfront costs, repayment frequency toggle, portfolio aggregate LVR. Per-individual tax, income-scaled HEM, APRA +3% buffer.

### Page 3 — Property Analyser ✅
Yield/cash flow/deal score KPIs, financing breakdown tables, tax estimate with marginal rate selector, deal score gauge (medium), suburb comparison with editorial badges, historical price/rent charts, cash flow frequency toggle. State/suburb via `core/locations.py`.

### Page 4 — Buying Assistant (styled stub)
Gold left-border card with planned features: pre-purchase checklist, agent questions, upfront cost summary, risk flags, settlement timeline, property comparison.

---

## Key Rules
1. Pages in `pages/`, shared logic in `core/`. Keep modular.
2. MVP first. No overengineering.
3. Match the editorial design system. Gold accents, sharp edges, Playfair headings.
4. Disclaimers on every page. Australian context (AUD, APRA, state-based).
5. Don't break what works. Test with `streamlit run Home.py`.

---

## Self-Review Protocol
After modifying calculations: challenge hardcoded numbers, check edge cases ($0 income, $5M property), run a worked example. Verify tax rates and stamp duty are current. Check UI matches design system. Output: ✅ Confident / ⚠️ Assumptions / 🔍 Worth checking.

## Debug Protocol
Reproduce → Diagnose → Fix (minimum change) → Verify. Common issues: caching, sys.path imports, `unsafe_allow_html=True`, annual vs monthly vs gross vs net.

---

## What to Build Next
1. ~~Page 1 — Market Climate~~ ✅
2. ~~Page 2 — Borrowing Power~~ ✅
3. ~~Page 3 — Property Analyser~~ ✅
4. **Page 4 — Buying Assistant** ← CURRENT PRIORITY
5. Live data feeds (RBA, ABS, CoreLogic)
6. Full suburb coverage via `core/locations.py` backend swap
7. Cross-page data sharing (borrowing power → property analyser)
