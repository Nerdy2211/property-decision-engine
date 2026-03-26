"""
Plotly chart builders — editorial/luxury palette.
Gold (#C5A880) primary, charcoal backgrounds, muted axis text.
"""

import plotly.graph_objects as go
import pandas as pd
from core.config import FACTOR_LABELS, WEIGHTS


def _score_color(score: float) -> str:
    if score >= 65:
        return "#C5A880"
    elif score >= 40:
        return "#8A8A93"
    else:
        return "#C45C5C"


def factor_bar_chart(sub_scores: dict) -> go.Figure:
    sorted_keys = sorted(
        [k for k in WEIGHTS if k in sub_scores],
        key=lambda k: WEIGHTS[k],
        reverse=True,
    )

    labels = []
    scores = []
    colors = []

    for key in sorted_keys:
        score = sub_scores[key]
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
        textfont=dict(size=12, color="#8A8A93"),
        hovertemplate="%{y}: %{x}/100<extra></extra>",
    ))

    fig.update_layout(
        title=dict(text="Factor Scores", font=dict(size=15, color="#F4F4F5",
                   family="Playfair Display, Georgia, serif")),
        xaxis=dict(range=[0, 115], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=12, color="#8A8A93", family="DM Sans, sans-serif"),
            gridcolor="rgba(255,255,255,0.03)",
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8A8A93", family="DM Sans, sans-serif"),
        margin=dict(l=10, r=60, t=40, b=10),
        height=280,
        bargap=0.35,
    )
    return fig


def historical_line_chart(
    df: pd.DataFrame,
    title: str,
    yaxis_label: str,
    line_color: str = "#C5A880",
    current_value: float = None,
    reference_label: str = None,
    invert_signal: bool = False,
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines",
        line=dict(color=line_color, width=2),
        hovertemplate="%{x|%b %Y}: %{y:.2f}<extra></extra>",
    ))

    if current_value is not None:
        fig.add_hline(
            y=current_value,
            line_dash="dot",
            line_color="rgba(255,255,255,0.15)",
            annotation_text=reference_label or f"Current: {current_value}",
            annotation_position="top right",
            annotation_font=dict(size=11, color="#8A8A93",
                                 family="DM Sans, sans-serif"),
        )

    fig.update_layout(
        title=dict(text=title,
                   font=dict(size=14, color="#F4F4F5",
                             family="Playfair Display, Georgia, serif"),
                   x=0),
        xaxis=dict(
            title="", showgrid=False, zeroline=False,
            tickfont=dict(size=11, color="#8A8A93", family="DM Sans"),
            tickformat="%Y",
        ),
        yaxis=dict(
            title=dict(text=yaxis_label,
                       font=dict(size=11, color="#8A8A93", family="DM Sans")),
            showgrid=True, gridcolor="rgba(255,255,255,0.04)",
            zeroline=False,
            tickfont=dict(size=11, color="#8A8A93", family="DM Sans"),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F4F4F5", family="DM Sans, sans-serif"),
        margin=dict(l=10, r=20, t=40, b=10),
        height=240,
        showlegend=False,
    )
    return fig


def city_bar_chart(city_scores: dict) -> go.Figure:
    sorted_cities = sorted(city_scores.items(), key=lambda x: x[1]["score"], reverse=True)

    cities = [c for c, _ in sorted_cities]
    scores = [d["score"] for _, d in sorted_cities]
    colors = [_score_color(d["score"]) for _, d in sorted_cities]

    fig = go.Figure(go.Bar(
        x=scores,
        y=cities,
        orientation="h",
        marker_color=colors,
        text=[f"{s}/100" for s in scores],
        textposition="outside",
        textfont=dict(size=12, color="#8A8A93"),
        hovertemplate="%{y}: %{x}/100<extra></extra>",
    ))

    fig.update_layout(
        title=dict(text="Adjusted Investment Score by City",
                   font=dict(size=15, color="#F4F4F5",
                             family="Playfair Display, Georgia, serif")),
        xaxis=dict(range=[0, 115], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(autorange="reversed",
                   tickfont=dict(size=13, color="#8A8A93", family="DM Sans")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F4F4F5", family="DM Sans, sans-serif"),
        margin=dict(l=10, r=60, t=40, b=10),
        height=320,
        bargap=0.35,
    )
    return fig
