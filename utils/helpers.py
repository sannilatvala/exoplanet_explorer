import numpy as np
from utils.constants import (
    LAYOUT_BASE, X_MIN_LOG, X_MAX_LOG, Y_MIN_LOG, Y_MAX_LOG,
    CARD_BG, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT,
)


def base_layout(**overrides):
    layout = {**LAYOUT_BASE}
    layout.update(overrides)
    return layout


_SCATTER_AXIS_BASE = dict(
    type="log",
    showgrid=True,
    gridcolor="#3a4d6b",
    gridwidth=1,
    zeroline=False,
    showline=False,
    tickmode="array",
)


def scatter_xaxis(title):
    return {
        **_SCATTER_AXIS_BASE,
        "title": title,
        "range": [X_MIN_LOG, X_MAX_LOG],
        "tickvals": [0.01, 0.1, 1, 10, 100],
        "ticktext": ["0.01", "0.1", "1", "10", "100"],
    }


def scatter_yaxis(title):
    return {
        **_SCATTER_AXIS_BASE,
        "title": title,
        "range": [Y_MIN_LOG, Y_MAX_LOG],
        "tickvals": [1, 10, 100],
        "ticktext": ["1", "10", "100"],
    }


def add_radius_reflines(fig, xref_mode="data"):
    for y_val, lbl in [(1.5, "1.5 R\u2295"), (2.5, "2.5 R\u2295"), (6.0, "6.0 R\u2295")]:
        if xref_mode == "data":
            fig.add_shape(
                type="line",
                x0=10**X_MIN_LOG, x1=10**X_MAX_LOG, y0=y_val, y1=y_val,
                xref="x", yref="y",
                line=dict(color="rgba(255,255,255,0.25)", width=1, dash="dash"),
            )
            fig.add_annotation(
                x=X_MIN_LOG, xref="x",
                y=np.log10(y_val), yref="y",
                text=lbl, showarrow=False,
                xanchor="left", yanchor="bottom",
                font=dict(color="rgba(255,255,255,0.55)", size=9,
                          family="'IBM Plex Mono', monospace"),
            )
        else:
            fig.add_shape(
                type="line",
                x0=0, x1=1, xref="paper",
                y0=np.log10(y_val), y1=np.log10(y_val), yref="y",
                line=dict(color="rgba(255,255,255,0.25)", width=1, dash="dash"),
            )
            fig.add_annotation(
                x=X_MIN_LOG, xref="x",
                y=np.log10(y_val), yref="y",
                text=lbl, showarrow=False,
                xanchor="left", yanchor="bottom",
                font=dict(color="rgba(255,255,255,0.55)", size=9,
                          family="'IBM Plex Mono', monospace"),
            )
    return fig


def filter_dataframe(df, ptypes, methods, year_range):
    fdf = df.copy()
    if ptypes:
        fdf = fdf[fdf["pl_type"].isin(ptypes)]
    if methods:
        fdf = fdf[fdf["discoverymethod_mapped"].isin(methods)]
    if year_range and "disc_year" in fdf.columns:
        fdf = fdf[
            fdf["disc_year"].isna() |
            ((fdf["disc_year"] >= year_range[0]) & (fdf["disc_year"] <= year_range[1]))
        ]
    return fdf
