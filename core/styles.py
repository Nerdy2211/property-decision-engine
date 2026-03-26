"""
Shared CSS design system for the Property Decision Engine.

All pages import get_common_css() and inject it once.
Page-specific CSS stays in the page file.
"""


def get_common_css() -> str:
    """Return the full shared CSS block wrapped in <style> tags."""
    return """<style>
/* ── Design tokens ──────────────────────────────────────────────────── */
:root {
    --bg-card: #111827;
    --border-card: 1px solid rgba(0,191,165,0.06);
    --radius-card: 12px;
    --accent: #00BFA5;
    --cyan: #06B6D4;
    --pos: #00BFA5;
    --neg: #EF4444;
    --caution: #F59E0B;
    --text-1: #F1F5F9;
    --text-2: rgba(255,255,255,0.45);
    --text-3: rgba(255,255,255,0.25);
}

/* ── Base card ──────────────────────────────────────────────────────── */
.card {
    background: var(--bg-card);
    border: var(--border-card);
    border-radius: var(--radius-card);
    padding: 20px;
}
.card-row {
    display: flex;
    gap: 12px;
    align-items: stretch;
}
.card-row > .card { flex: 1; box-sizing: border-box; }

/* ── Typography ─────────────────────────────────────────────────────── */
.lbl {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-3);
    margin-bottom: 6px;
}
.val {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-1);
    line-height: 1.15;
    margin-bottom: 4px;
}
.val-sm {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-1);
    line-height: 1.15;
    margin-bottom: 4px;
}
.sub {
    font-size: 12px;
    color: var(--text-2);
}
.micro {
    font-size: 10px;
    color: var(--text-3);
    letter-spacing: 0.04em;
}

/* ── Delta badge pills ──────────────────────────────────────────────── */
.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    line-height: 1.4;
}
.badge-pos {
    background: rgba(0,191,165,0.15);
    color: #00BFA5;
}
.badge-neg {
    background: rgba(239,68,68,0.15);
    color: #EF4444;
}
.badge-cau {
    background: rgba(245,158,11,0.15);
    color: #F59E0B;
}
.badge-neu {
    background: rgba(255,255,255,0.06);
    color: rgba(255,255,255,0.45);
}

/* ── Math / breakdown tables ────────────────────────────────────────── */
.math-tbl {
    width: 100%;
    font-size: 13px;
    color: var(--text-1);
    border-collapse: collapse;
    margin-top: 8px;
}
.math-tbl td { padding: 4px 0; }
.math-tbl .mlbl { color: var(--text-2); }
.math-tbl .mval { text-align: right; }
.math-tbl .sep { border-top: 1px solid rgba(255,255,255,0.06); }
.math-tbl .sep td { padding-top: 8px; }
.math-tbl .total td { font-weight: 700; }

/* ── Progress bar ───────────────────────────────────────────────────── */
.prog-track {
    width: 100%;
    height: 3px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    margin: 6px 0 4px 0;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s;
}

/* ── Signal colours (utility) ───────────────────────────────────────── */
.sig-pos { color: #00BFA5; }
.sig-neg { color: #EF4444; }
.sig-cau { color: #F59E0B; }
.sig-neu { color: var(--text-2); }

/* ── Disclaimer / footnote ──────────────────────────────────────────── */
.disclaimer {
    font-size: 11px;
    color: var(--text-3);
    font-style: italic;
    margin-top: 8px;
}

/* ── Sidebar branding ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0;
}
.sidebar-brand {
    padding: 16px 16px 12px 16px;
    border-bottom: 1px solid rgba(0,191,165,0.15);
    margin-bottom: 12px;
}
.sidebar-brand-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-1);
    margin-bottom: 2px;
}
.sidebar-brand-sub {
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #00BFA5;
}
</style>"""


def sidebar_branding() -> str:
    """Return the sidebar brand HTML."""
    return (
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-title">Property Decision Engine</div>'
        '<div class="sidebar-brand-sub">Decision Terminal</div>'
        '</div>'
    )


def gauge_svg(score: int, color: str = "#00BFA5", size: int = 200,
              label: str = "", show_micro: bool = True) -> str:
    """
    Circular gauge SVG. Teal ring partially filled by score (0-100).
    Large score number centred, band label below.
    """
    r = 80
    cx = cy = size // 2
    circumference = 2 * 3.14159 * r
    filled = circumference * score / 100
    gap = circumference - filled
    glow_id = f"glow_{score}"

    micro_line = ""
    if show_micro:
        micro_line = (
            f'<text x="{cx}" y="{cy + 56}" text-anchor="middle" '
            f'font-size="9" fill="rgba(255,255,255,0.25)" letter-spacing="0.04em">'
            f'9-factor weighted \u00b7 0\u2013100 \u00b7 March 2026</text>'
        )

    label_line = ""
    if label:
        label_line = (
            f'<text x="{cx}" y="{cy + 36}" text-anchor="middle" '
            f'font-size="13" fill="rgba(255,255,255,0.45)" font-weight="500">'
            f'{label}</text>'
        )

    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<defs><filter id="{glow_id}" x="-30%" y="-30%" width="160%" height="160%">'
        f'<feGaussianBlur stdDeviation="4" result="blur"/>'
        f'<feComposite in="SourceGraphic" in2="blur" operator="over"/>'
        f'</filter></defs>'
        # Track
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="rgba(255,255,255,0.04)" stroke-width="8"/>'
        # Filled arc
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
        f'stroke="{color}" stroke-width="8" '
        f'stroke-dasharray="{filled:.1f} {gap:.1f}" '
        f'stroke-linecap="round" '
        f'transform="rotate(-90 {cx} {cy})" '
        f'filter="url(#{glow_id})"/>'
        # Score number
        f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" '
        f'font-size="48" font-weight="700" fill="#F1F5F9">{score}</text>'
        # Label
        + label_line +
        # Micro
        micro_line +
        f'</svg>'
    )


def sparkline_svg(values: list, width: int = 80, height: int = 24,
                  color: str = "#00BFA5") -> str:
    """Tiny SVG sparkline polyline from a list of numbers."""
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
    pts_str = " ".join(points)
    return (
        f'<svg width="{width}" height="{height}" style="display:block;margin-top:8px">'
        f'<polyline points="{pts_str}" fill="none" stroke="{color}" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg>'
    )


def score_color(score: int) -> str:
    """Return accent colour for a 0-100 score."""
    if score >= 65:
        return "#00BFA5"
    if score >= 40:
        return "#F59E0B"
    return "#EF4444"


def badge_class(score_or_value, thresholds=(65, 40), invert=False):
    """Return badge CSS class based on value vs thresholds."""
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
