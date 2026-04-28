import numpy as np
import pandas as pd
import plotly.graph_objects as go

from utils.constants import (
    X_MIN_LOG, X_MAX_LOG, Y_MIN_LOG, Y_MAX_LOG,
    EARTH_DIST, EARTH_RADIUS, EARTH_EQT, EARTH_COLOR,
)
from utils.helpers import base_layout, scatter_xaxis, scatter_yaxis, add_radius_reflines


def _hover_text(s):
    name_col = s.get("pl_name", pd.Series([""] * len(s))).fillna("").astype(str)
    temp_str = (
        s["pl_eqt"].map(lambda v: f"{v:.0f} K" if pd.notna(v) else "N/A")
        if "pl_eqt" in s.columns
        else pd.Series(["N/A"] * len(s))
    )
    return (
        name_col
        + "<br>Orbital dist: " + s["pl_orbsmax"].map("{:.3g} AU".format)
        + "<br>Radius: "       + s["pl_rade"].map("{:.2f} R\u2295".format)
        + "<br>Eq. Temp: "     + temp_str
        + "<br>Type: "         + s["pl_type"].astype(str)
    )


def build_scatter(filtered_df, show_nan_temp=True, show_earth=True):
    sub = filtered_df.dropna(subset=["pl_orbsmax", "pl_rade"]).copy()
    sub = sub[(sub["pl_orbsmax"] > 0) & (sub["pl_rade"] > 0)]
    sub = sub[
        (np.log10(sub["pl_orbsmax"]) >= X_MIN_LOG) &
        (np.log10(sub["pl_orbsmax"]) <= X_MAX_LOG) &
        (np.log10(sub["pl_rade"])    >= Y_MIN_LOG) &
        (np.log10(sub["pl_rade"])    <= Y_MAX_LOG)
    ]

    fig = go.Figure()
    has_temp = "pl_eqt" in sub.columns

    if has_temp:
        sub_nan   = sub[sub["pl_eqt"].isna()].copy()
        sub_known = sub[sub["pl_eqt"].notna()].copy()
    else:
        sub_nan   = sub.copy()
        sub_known = pd.DataFrame()

    if show_nan_temp and not sub_nan.empty:
        fig.add_trace(go.Scatter(
            x=sub_nan["pl_orbsmax"], y=sub_nan["pl_rade"],
            mode="markers",
            name="Unknown temp.",
            marker=dict(color="rgba(160,170,190,0.28)", size=5, line=dict(width=0)),
            hovertemplate="%{customdata}<extra></extra>",
            customdata=_hover_text(sub_nan),
            showlegend=False,
        ))

    if not sub_known.empty and has_temp:
        t_min = float(sub_known["pl_eqt"].min())
        t_max = float(sub_known["pl_eqt"].max())
        fig.add_trace(go.Scatter(
            x=sub_known["pl_orbsmax"], y=sub_known["pl_rade"],
            mode="markers",
            name="Planets (temp. known)",
            marker=dict(
                color=sub_known["pl_eqt"],
                colorscale="Plasma",
                reversescale=False,
                cmin=t_min, cmax=t_max,
                size=5, opacity=0.72,
                line=dict(width=0),
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Eq. Temp (K)",
                        side="right",
                        font=dict(size=9, family="'IBM Plex Mono', monospace"),
                    ),
                    x=1.02, xanchor="left",
                    thickness=12, len=0.70,
                    tickfont=dict(size=8), outlinewidth=0,
                ),
            ),
            hovertemplate="%{customdata}<extra></extra>",
            customdata=_hover_text(sub_known),
            showlegend=False,
        ))

    if show_earth:
        fig.add_trace(go.Scatter(
            x=[EARTH_DIST],
            y=[EARTH_RADIUS],
            mode="markers",
            name="Earth",
            marker=dict(
                color=EARTH_COLOR,
                size=9,
                symbol="circle",
                line=dict(color="white", width=1.5),
            ),
            showlegend=False,
            hovertemplate=(
                "<b>Earth (reference)</b><br>"
                "Orbital dist: 1.00 AU<br>"
                "Radius: 1.00 R\u2295<br>"
                f"Eq. Temp: {EARTH_EQT:.0f} K<br>"
                "Type: Terrestrial<extra></extra>"
            ),
        ))

    add_radius_reflines(fig, xref_mode="data")

    fig.update_layout(
        **base_layout(
            title="Scatter View \u2014 Orbital Distance vs Planet Radius",
            margin=dict(l=60, r=80, t=45, b=55),
        ),
        xaxis=scatter_xaxis("Orbital Distance (AU, log scale)"),
        yaxis=scatter_yaxis("Planet Radius (R\u2295, log scale)"),
        showlegend=False,
    )
    return fig
