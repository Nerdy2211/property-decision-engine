"""
Shared design system — Aurelia Editorial aesthetic.

Playfair Display for headings, DM Sans for body, Cormorant Garamond for data.
Gold (#C5A880) accent, sharp edges (0px radius), generous whitespace.
"""


def get_common_css() -> str:
    return """<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@400;500;600&family=Cormorant+Garamond:wght@400;500;600&display=swap');

:root {
    --color-primary: #C5A880;
    --color-background: #161618;
    --color-surface: #222225;
    --color-text: #F4F4F5;
    --color-muted: #8A8A93;
    --color-border: #333336;
    --color-accent: #3B4A42;
    --color-neg: #C45C5C;
    --color-neg-border: #8B3A3A;
    --color-alt-row: #1C1C1E;
    --font-heading: 'Playfair Display', Georgia, serif;
    --font-body: 'DM Sans', sans-serif;
    --font-data: 'Cormorant Garamond', Georgia, serif;
    --radius: 0px;
}

/* ── Global font ────────────────────────────────────────────────────── */
.main, .main p, .main li, .main span, .main td {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Streamlit overrides ────────────────────────────────────────────── */
.main .block-container { padding: 2.5rem 3rem 4rem; max-width: 1300px; }

/* Section headers — gold top accent line */
.main h2, .main h3,
.main [data-testid="stMarkdown"] h2,
.main [data-testid="stMarkdown"] h3,
[data-testid="stHeading"] h2,
[data-testid="stHeading"] h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #F4F4F5 !important;
}
.main h2::before, .main h3::before,
[data-testid="stHeading"] h2::before,
[data-testid="stHeading"] h3::before {
    content: '';
    display: block;
    width: 50px;
    height: 2px;
    background: #C5A880;
    margin-bottom: 12px;
}
.main h2, .main [data-testid="stMarkdown"] h2, [data-testid="stHeading"] h2 {
    font-size: 28px !important; font-weight: 600 !important;
    margin-bottom: 8px !important;
}
.main h3, .main [data-testid="stMarkdown"] h3, [data-testid="stHeading"] h3 {
    font-size: 22px !important; font-weight: 600 !important;
}

.main hr {
    border: none !important;
    border-top: 1px solid #333336 !important;
    margin: 2.5rem 0 !important;
}
.main .stCaption p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; color: #8A8A93 !important;
}
.main label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; color: #8A8A93 !important;
}
section[data-testid="stSidebar"] {
    background-color: #161618 !important;
    border-right: 1px solid #333336 !important;
}

/* ── Alert / info box overrides ─────────────────────────────────────── */
.stAlert {
    background: transparent !important;
    border: 1px solid #333336 !important;
    border-left: 3px solid #C5A880 !important;
    border-radius: 0px !important;
}
.stAlert p {
    color: #8A8A93 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}

/* ── st.metric overrides ────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 28px !important; font-weight: 500 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important; text-transform: uppercase !important;
    letter-spacing: 0.1em !important; color: #8A8A93 !important;
}

/* ── Expander overrides ─────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #333336 !important;
    border-radius: 0px !important;
    background: #222225 !important;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: #8A8A93 !important;
}

/* ── Base card ──────────────────────────────────────────────────────── */
.card {
    background: #222225;
    border: 1px solid #333336;
    border-radius: 0px;
    padding: 24px;
}
.card-row {
    display: flex;
    gap: 14px;
    align-items: stretch;
}
.card-row > .card { flex: 1; box-sizing: border-box; }

/* ── Typography ─────────────────────────────────────────────────────── */
.lbl {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #8A8A93;
    margin-bottom: 8px;
}
.val {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 28px;
    font-weight: 500;
    color: #F4F4F5;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
    margin-bottom: 8px;
}
.val-lg {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 72px;
    font-weight: 500;
    color: #F4F4F5;
    font-variant-numeric: tabular-nums;
    line-height: 1;
}
.val-sm {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 20px;
    font-weight: 500;
    color: #F4F4F5;
    font-variant-numeric: tabular-nums;
    line-height: 1.15;
    margin-bottom: 4px;
}
.denom {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 16px;
    color: #8A8A93;
    font-weight: 400;
}
.sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #8A8A93;
    line-height: 1.6;
}
.micro {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    letter-spacing: 0.04em;
    color: #8A8A93;
}

/* ── Badges — sharp, outlined, editorial ────────────────────────────── */
.badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 12px;
    border-radius: 0px;
    line-height: 1.5;
    letter-spacing: 0.03em;
    background: transparent !important;
    border: 1px solid #444448;
    color: #8A8A93;
}
.badge-pos { border-color: #3B4A42 !important; color: #6B8F7B !important; background: transparent !important; }
.badge-neg { border-color: #6B3A3A !important; color: #C47070 !important; background: transparent !important; }
.badge-cau { border-color: #8A7A5A !important; color: #C5A880 !important; background: transparent !important; }
.badge-neu { border-color: #444448 !important; color: #8A8A93 !important; background: transparent !important; }

/* ── Math / ledger tables ───────────────────────────────────────────── */
.math-tbl {
    width: 100%;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    color: #F4F4F5;
    border-collapse: collapse;
    margin-top: 8px;
}
.math-tbl td { padding: 6px 0; border-bottom: 1px solid #2A2A2D; }
.math-tbl .mlbl { color: #8A8A93; }
.math-tbl .mval { text-align: right; font-variant-numeric: tabular-nums; }
.math-tbl .sep { border-top: 1px solid #333336; }
.math-tbl .sep td { padding-top: 10px; border-bottom: 1px solid #2A2A2D; }
.math-tbl .total td { font-weight: 600; }

.ledger-head {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8A8A93;
    border-bottom: 1px solid #C5A880;
    padding-bottom: 8px;
    margin-bottom: 4px;
}

/* ── Progress bar — gold fill ───────────────────────────────────────── */
.prog-track {
    width: 100%;
    height: 4px;
    background: #333336;
    border-radius: 0px;
    margin: 12px 0;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    border-radius: 0px;
    background: #C5A880;
}

/* ── Signal colours ─────────────────────────────────────────────────── */
.sig-pos { color: #6B8F7B; }
.sig-neg { color: #C47070; }
.sig-cau { color: #C5A880; }
.sig-neu { color: #8A8A93; }

/* ── Gold hairline divider ──────────────────────────────────────────── */
.gold-line {
    width: 60%;
    height: 1px;
    background: #C5A880;
    margin: 12px auto;
}

/* ── Disclaimer ─────────────────────────────────────────────────────── */
.disclaimer {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    color: #8A8A93;
    font-style: italic;
    margin-top: 8px;
}

/* ── Sidebar branding ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
.sidebar-brand {
    padding: 18px 16px 14px 16px;
    border-bottom: 1px solid #333336;
    margin-bottom: 12px;
}
.sidebar-brand-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 16px;
    font-weight: 600;
    color: #F4F4F5;
    margin-bottom: 3px;
}
.sidebar-brand-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #C5A880;
}
</style>"""


def sidebar_branding() -> str:
    return (
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-title">Aurelia</div>'
        '<div class="sidebar-brand-sub">Institutional Brief</div>'
        '</div>'
    )


def score_card_html(score, label: str = "", size: str = "large",
                    prefix: str = "", suffix: str = "/100") -> str:
    fs = {"large": 72, "medium": 48, "small": 28}[size]
    suf_fs = {"large": 18, "medium": 14, "small": 12}[size]
    label_html = ""
    if label:
        label_html = (
            f'<div class="gold-line"></div>'
            f'<div style="font-family:DM Sans,sans-serif;font-size:13px;'
            f'color:#8A8A93;margin-top:4px">{label}</div>'
        )
    return (
        f'<div class="card" style="text-align:center;padding:32px 24px">'
        f'<div style="font-family:Cormorant Garamond,Georgia,serif;'
        f'font-size:{fs}px;font-weight:500;color:#F4F4F5;'
        f'font-variant-numeric:tabular-nums;line-height:1">'
        f'{prefix}{score}'
        f'<span style="font-size:{suf_fs}px;color:#8A8A93;font-weight:400;'
        f'margin-left:2px">{suffix}</span>'
        f'</div>'
        + label_html +
        f'</div>'
    )


def sparkline_svg(values: list, width: int = 80, height: int = 28,
                  color: str = "#C5A880") -> str:
    if not values or len(values) < 2:
        return ""
    mn, mx = min(values), max(values)
    rng = mx - mn if mx != mn else 1
    n = len(values)
    pad = 2
    points = []
    for i, v in enumerate(values):
        x = pad + i * (width - 2 * pad) / (n - 1)
        y = height - pad - (v - mn) / rng * (height - 2 * pad)
        points.append(f"{x:.1f},{y:.1f}")
    return (
        f'<svg width="{width}" height="{height}" style="display:block">'
        f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg>'
    )


def score_color(score: int) -> str:
    if score >= 65:
        return "#C5A880"
    if score >= 40:
        return "#8A7A5A"
    return "#6B3A3A"


def badge_class(score_or_value, thresholds=(65, 40), invert=False):
    high, low = thresholds
    if invert:
        if score_or_value <= low:
            return "badge badge-pos"
        if score_or_value <= high:
            return "badge badge-cau"
        return "badge badge-neg"
    if score_or_value >= high:
        return "badge badge-pos"
    if score_or_value >= low:
        return "badge badge-cau"
    return "badge badge-neg"


def gauge_svg(score: int, color: str = "#C5A880", size: int = 280,
              label: str = "", show_micro: bool = False) -> str:
    sz = "large" if size >= 200 else "medium" if size >= 120 else "small"
    return score_card_html(score, label=label, size=sz)
