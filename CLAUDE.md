# CLAUDE.md — Aurelia

## What This Is
**Aurelia** — institutional-grade property investment intelligence for the Australian market. Streamlit app, four pages:

1. **Market Climate** → 9-factor scoring model, city rankings, historical trends
2. **Borrowing Power** → APRA serviceability, LVR comparison table, equity analysis
3. **Property Analyser** → Yield, cash flow, deal score, suburb comparison
4. **Buying Assistant** → Due diligence workflow (styled stub — next to build)

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
**Fonts:** Playfair Display (headings), DM Sans (body/labels), Cormorant Garamond (data numbers).
**Palette:** Gold `#C5A880` primary, charcoal `#161618` background, `#222225` surface, `#333336` borders, `#8A8A93` muted, `#F4F4F5` text. Positive `#3B4A42`/`#6B8F7B`, negative `#6B3A3A`/`#C47070`.
**Cards:** Sharp edges (0px radius), 1px solid `#333336`, no shadows, 24px padding.
**Badges:** Outlined only — transparent bg, 1px border, 0px radius, 3px 12px padding.
**Section headers:** Gold top accent rule (50px × 2px `#C5A880` via `::before` pseudo-element), Playfair Display.
**Score display:** Cormorant Garamond 72px (hero) or 28px (cards), gold hairline divider below.
**Charts:** Gold `#C5A880` lines, transparent backgrounds, `#8A8A93` axis text.

All styles in `core/styles.py`. Pages import `get_common_css()` and `sidebar_branding()`.

---

## Build Status

### Page 1 — Market Climate ✅
Score card hero (67/100), KPI cards with absolute-positioned badges, factor cards with score-coloured progress bars (gold/amber/red), ledger-style city rankings with alternating rows and inline score bars, tailwinds/risks, historical trend charts, methodology expander. Scoring model locked in `core/config.py`.

### Page 2 — Borrowing Power ✅
Hero borrowing amount (Cormorant 48px, gold top border), serviceability breakdown, 4-column LVR comparison (80/85/90/95%) with cash-only and cash+equity rows, best-fit auto-selection, selected deal financing/upfront costs, custom repayment cards, portfolio aggregate LVR. Per-individual tax, income-scaled HEM, APRA +3% buffer.

### Page 3 — Property Analyser ✅
Yield/cash flow/deal score KPIs with verdict border, editorial financing tables, tax estimate with custom HTML cards (replacing st.metric), deal score derivation with Cormorant score cards, suburb comparison with editorial badges, historical charts, cash flow frequency toggle.

### Page 4 — Buying Assistant (styled stub)
Gold-accented card listing planned features. Under development.

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
1. **Validate hardcoded data** — check `market_data.json` and `suburb_data.json` against current RBA, ABS, SQM Research sources. Owner task, not Claude Code.
2. **Build Page 4 — Buying Assistant** — pre-purchase checklist, due diligence prompts, questions for agent, upfront cost summary, risk flags, settlement timeline, property comparison. Match editorial design.
3. **Live data feeds** — replace hardcoded JSON with API calls (RBA statistical tables, ABS Labour Force, SQM vacancy rates). Start with easiest public APIs.
4. **Expand suburb coverage** — scale beyond sample data via `core/locations.py` backend swap.
5. **UI polish** — iterate based on user testing feedback.
