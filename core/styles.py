"""
Shared design system — Editorial / Luxury aesthetic.

Inspired by Monocle Magazine and Bloomberg Terminal.
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
    --color-alt-row: #1A1A1C;
    --font-heading: 'Playfair Display', Georgia, serif;
    --font-body: 'DM Sans', sans-serif;
    --font-data: 'Cormorant Garamond', Georgia, serif;
    --radius: 0px;
}

/* ── Streamlit overrides ────────────────────────────────────────────── */
.main .block-container { padding: 2.5rem 3rem 4rem; max-width: 1300px; }
.main [data-testid="stMarkdown"] h2 {
    font-family: var(--font-heading) !important;
    font-size: 28px !important; font-weight: 600 !important;
    color: var(--color-text) !important;
    border-left: 4px solid var(--color-primary);
    padding-left: 16px;
    margin-bottom: 8px !important;
}
.main [data-testid="stMarkdown"] h3 {
    font-family: var(--font-heading) !important;
    font-size: 22px !important; font-weight: 600 !important;
    color: var(--color-text) !important;
}
.main hr {
    border: none !important;
    border-top: 1px solid var(--color-border) !important;
    margin: 2rem 0 !important;
}
.main .stCaption p {
    font-family: var(--font-body) !important;
    font-size: 13px !important; color: var(--color-muted) !important;
}
.main label {
    font-family: var(--font-body) !important;
    font-size: 13px !important; color: var(--color-muted) !important;
}
section[data-testid="stSidebar"] {
    background-color: #161618 !important;
    border-right: 1px solid var(--color-border) !important;
}

/* ── Base card ──────────────────────────────────────────────────────── */
.card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius);
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
    font-family: var(--font-body);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--color-muted);
    margin-bottom: 8px;
}
.val {
    font-family: var(--font-data);
    font-size: 28px;
    font-weight: 500;
    color: var(--color-text);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
    margin-bottom: 8px;
}
.val-lg {
    font-family: var(--font-data);
    font-size: 72px;
    font-weight: 500;
    color: var(--color-text);
    font-variant-numeric: tabular-nums;
    line-height: 1;
}
.val-sm {
    font-family: var(--font-data);
    font-size: 20px;
    font-weight: 500;
    color: var(--color-text);
    font-variant-numeric: tabular-nums;
    line-height: 1.15;
    margin-bottom: 4px;
}
.denom {
    font-family: var(--font-data);
    font-size: 16px;
    color: var(--color-muted);
    font-weight: 400;
}
.sub {
    font-family: var(--font-body);
    font-size: 13px;
    color: var(--color-muted);
    line-height: 1.6;
}
.micro {
    font-family: var(--font-body);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--color-muted);
}

/* ── Badges — sharp, outlined ───────────────────────────────────────── */
.badge {
    display: inline-block;
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 500;
    padding: 2px 10px;
    border-radius: var(--radius);
    line-height: 1.5;
    background: transparent;
    border: 1px solid var(--color-border);
    color: var(--color-muted);
}
.badge-pos { border-color: var(--color-accent); color: var(--color-accent); }
.badge-neg { border-color: var(--color-neg-border); color: var(--color-neg); }
.badge-cau { border-color: var(--color-primary); color: var(--color-primary); }
.badge-neu { border-color: var(--color-border); color: var(--color-muted); }

/* ── Math / ledger tables ───────────────────────────────────────────── */
.math-tbl {
    width: 100%;
    font-family: var(--font-body);
    font-size: 14px;
    color: var(--color-text);
    border-collapse: collapse;
    margin-top: 8px;
}
.math-tbl td { padding: 6px 0; border-bottom: 1px solid #2A2A2D; }
.math-tbl .mlbl { color: var(--color-muted); }
.math-tbl .mval { text-align: right; font-variant-numeric: tabular-nums; }
.math-tbl .sep { border-top: 1px solid var(--color-border); }
.math-tbl .sep td { padding-top: 10px; border-bottom: 1px solid #2A2A2D; }
.math-tbl .total td { font-weight: 600; }

/* Ledger header row */
.ledger-head {
    font-family: var(--font-body);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-muted);
    border-bottom: 1px solid var(--color-primary);
    padding-bottom: 8px;
    margin-bottom: 4px;
}

/* ── Progress bar — gold fill ───────────────────────────────────────── */
.prog-track {
    width: 100%;
    height: 4px;
    background: var(--color-border);
    border-radius: var(--radius);
    margin: 12px 0;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    border-radius: var(--radius);
    background: var(--color-primary);
}

/* ── Signal / status colours ────────────────────────────────────────── */
.sig-pos { color: var(--color-accent); }
.sig-neg { color: var(--color-neg); }
.sig-cau { color: var(--color-primary); }
.sig-neu { color: var(--color-muted); }

/* ── Gold hairline divider ──────────────────────────────────────────── */
.gold-line {
    width: 60%;
    height: 1px;
    background: var(--color-primary);
    margin: 12px auto;
}

/* ── Disclaimer ─────────────────────────────────────────────────────── */
.disclaimer {
    font-family: var(--font-body);
    font-size: 11px;
    color: var(--color-muted);
    font-style: italic;
    margin-top: 8px;
}

/* ── Sidebar branding ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
.sidebar-brand {
    padding: 18px 16px 14px 16px;
    border-bottom: 1px solid var(--color-border);
    margin-bottom: 12px;
}
.sidebar-brand-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 15px;
    font-weight: 600;
    color: var(--color-text);
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
        '<div class="sidebar-brand-title">Property Decision Engine</div>'
        '<div class="sidebar-brand-sub">Institutional Brief</div>'
        '</div>'
    )


def score_card_html(score, label: str = "", size: str = "large",
                    prefix: str = "", suffix: str = "/100") -> str:
    """
    Editorial score card — replaces the old SVG gauge.
    size: "large" (72px, hero), "medium" (48px), "small" (28px)
    prefix: e.g. "$" for dollar amounts
    suffix: e.g. "/100" or "%"
    """
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
    """Tiny SVG sparkline — gold by default."""
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
        return "#C5A880"   # gold
    if score >= 40:
        return "#8A8A93"   # muted
    return "#C45C5C"       # muted red


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


# Keep gauge_svg as a thin wrapper around score_card_html for backward compat
def gauge_svg(score: int, color: str = "#C5A880", size: int = 280,
              label: str = "", show_micro: bool = False) -> str:
    """Backward-compatible wrapper — returns score card HTML, not SVG."""
    sz = "large" if size >= 200 else "medium" if size >= 120 else "small"
    return score_card_html(score, label=label, size=sz)
