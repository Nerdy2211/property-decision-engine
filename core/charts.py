"""
Plotly chart builders for the Market Climate Dashboard.
"""

import plotly.graph_objects as go
import pandas as pd
from core.config import FACTOR_LABELS, WEIGHTS


def _score_color(score: float) -> str:
    if score >= 65:
        return "#00BFA5"   # teal / green
    elif score >= 40:
        return "#FFC107"   # amber
    else:
        return "#EF5350"   # red


def factor_bar_chart(sub_scores: dict) -> go.Figure:
    """
    Horizontal bar chart of factor sub-scores, grouped by category.
    """
    # Sort by weight descending so the chart reflects model priority
    sorted_keys = sorted(
        [k for k in WEIGHTS if k in sub_scores],
        key=lambda k: WEIGHTS[k],
        reverse=True,
    )

    labels = []
    scores = []
    colors = []

    for key in sorted_keys:
        score      = sub_scores[key]
        weight_pct = int(WEIGHTS[key] * 100)
        labels.append(f"{FACTOR_LABELS[key]}  ({weight_pct}% wt)")
        scores.append(round(score))
        colors.append(_score_color(score))

    fig = go.Figure(go.Bar(
        x=scores,
        y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"{s}/100" for s in scores],
        textposition="outside",
        textfont=dict(size=12),
        hovertemplate="%{y}: %{x}/100<extra></extra>",
    ))

    fig.update_layout(
        title=dict(text="Factor Scores", font=dict(size=15, color="#FAFAFA")),
        xaxis=dict(range=[0, 115], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=12)),
        plot_bgcolor="#1A1D23",
        paper_bgcolor="#1A1D23",
        font=dict(color="#FAFAFA"),
        margin=dict(l=10, r=60, t=40, b=10),
        height=360,
        bargap=0.35,
    )
    return fig


def historical_line_chart(
    df: pd.DataFrame,
    title: str,
    yaxis_label: str,
    line_color: str,
    current_value: float = None,
    reference_label: str = None,
    invert_signal: bool = False,
) -> go.Figure:
    """
    Clean line chart for a single historical time series.

    df must have columns: 'date' (datetime) and 'value' (float).
    current_value, if provided, adds a horizontal reference line.
    invert_signal: True if lower value = better (used to colour the reference label).
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines",
        line=dict(color=line_color, width=2.5),
        hovertemplate="%{x|%b %Y}: %{y:.2f}<extra></extra>",
    ))

    if current_value is not None:
        fig.add_hline(
            y=current_value,
            line_dash="dot",
            line_color="rgba(255,255,255,0.25)",
            annotation_text=reference_label or f"Current: {current_value}",
            annotation_position="top right",
            annotation_font=dict(size=11, color="rgba(255,255,255,0.45)"),
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#FAFAFA"), x=0),
        xaxis=dict(
            title="",
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=11, color="#999"),
            tickformat="%Y",
        ),
        yaxis=dict(
            title=dict(text=yaxis_label, font=dict(size=11, color="#888")),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            tickfont=dict(size=11, color="#999"),
        ),
        plot_bgcolor="#1A1D23",
        paper_bgcolor="#1A1D23",
        font=dict(color="#FAFAFA"),
        margin=dict(l=10, r=20, t=40, b=10),
        height=240,
        showlegend=False,
    )
    return fig


def city_bar_chart(city_scores: dict) -> go.Figure:
    """
    Horizontal bar chart of city adjusted investment scores, sorted descending.
    """
    sorted_cities = sorted(city_scores.items(), key=lambda x: x[1]["score"], reverse=True)

    cities = [c for c, _ in sorted_cities]
    scores = [d["score"] for _, d in sorted_cities]
    colors = [_score_color(d["score"]) for _, d in sorted_cities]
    labels = [f"{d['offset_direction']} {d['state']}" for _, d in sorted_cities]

    fig = go.Figure(go.Bar(
        x=scores,
        y=cities,
        orientation="h",
        marker_color=colors,
        text=[f"{s}/100" for s in scores],
        textposition="outside",
        textfont=dict(size=12),
        hovertemplate="%{y}: %{x}/100<extra></extra>",
        customdata=labels,
    ))

    fig.update_layout(
        title=dict(text="Adjusted Investment Score by City", font=dict(size=15, color="#FAFAFA")),
        xaxis=dict(range=[0, 115], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=13)),
        plot_bgcolor="#1A1D23",
        paper_bgcolor="#1A1D23",
        font=dict(color="#FAFAFA"),
        margin=dict(l=10, r=60, t=40, b=10),
        height=320,
        bargap=0.35,
    )
    return fig
