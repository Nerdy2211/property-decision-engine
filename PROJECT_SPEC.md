# Property Decision Engine — Project Spec

## Goal
Build a Streamlit app for Australian property buyers and investors that helps answer four questions:

1. Is now a good time to invest in Australian property?
2. How much can I likely borrow?
3. Is this specific property a good investment?
4. What else do I need to check before buying?

This is a decision-support app, not formal financial or credit advice.

---

## Tech Stack
- Python
- Streamlit
- Pandas / NumPy
- Plotly
- Local CSV / JSON data initially
- Modular architecture for future API integrations

---

## App Pages

### Page 1 — Market Climate Dashboard
Purpose:
- assess whether now is a good time to invest in Australian property

Outputs:
- Australia-wide property investment score out of 100
- state scores
- city scores
- factor breakdown
- AI summary
- charts and report-style output

Factors to consider:
- inflation
- interest rates
- unemployment
- wages
- immigration / population growth
- dwelling approvals / housing supply
- rental vacancy
- consumer sentiment
- global macro risks

### Page 2 — Borrowing Power Estimator
Purpose:
- estimate likely borrowing capacity and buying costs

Inputs:
- income
- partner income
- number of children
- expenses
- debts
- assets
- deposit
- interest rate assumption

Outputs:
- rough borrowing estimate
- indicative repayments
- buying cost estimate
- confidence / caution notes

### Page 3 — Property Analyzer
Purpose:
- assess a specific property as an investment

Inputs:
- address or listing link
- purchase price
- weekly rent or rent estimate
- property type
- suburb / city
- basic costs

Outputs:
- gross yield
- net yield
- cash flow estimate
- growth context
- simple property score
- strengths / weaknesses
- red flags

### Page 4 — Buying Assistant
Purpose:
- support due diligence and buying workflow

Features:
- buying checklist
- due diligence prompts
- flood / infrastructure / risk notes placeholder
- questions to ask the agent
- estimated upfront cash needed
- comparison notes

---

## v1 Scope
Build only Page 1 first:
- national score
- city scores
- factor scores
- charts
- AI-style summary text
- report layout

Do not build Pages 2–4 yet, but scaffold navigation for them.

---

## Architecture
property-decision-engine/
- app/
- core/
- data/
- outputs/
- tests/
- requirements.txt
- README.md

Suggested modules:
- core/data_loader.py
- core/scoring.py
- core/factors.py
- core/charts.py
- core/reporting.py

---

## Key Rules
- keep code modular
- no overengineering
- prioritize clarity and credibility
- make assumptions explicit
- do not present outputs as guaranteed predictions or formal advice

---

## Success Criteria
- app runs locally
- Page 1 works cleanly
- scores update from underlying factor inputs
- charts render properly
- codebase is extendable for later pages
