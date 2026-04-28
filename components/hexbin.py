import numpy as np
import plotly.graph_objects as go

from utils.constants import X_MIN_LOG, X_MAX_LOG, Y_MIN_LOG, Y_MAX_LOG
from utils.helpers import base_layout, add_radius_reflines


def _fmt_log(log_v):
    v = 10 ** log_v
    if v >= 1:
        return str(int(v))
    return f"{v:.4g}".rstrip("0").rstrip(".")


def build_hexbin(filtered_df):
    sub = filtered_df.dropna(subset=["pl_orbsmax", "pl_rade"]).copy()
    sub = sub[(sub["pl_orbsmax"] > 0) & (sub["pl_rade"] > 0)]
    sub = sub[
        (np.log10(sub["pl_orbsmax"]) >= X_MIN_LOG) &
        (np.log10(sub["pl_orbsmax"]) <= X_MAX_LOG) &
        (np.log10(sub["pl_rade"])    >= Y_MIN_LOG) &
        (np.log10(sub["pl_rade"])    <= Y_MAX_LOG)
    ]

    fig = go.Figure()
    if sub.empty:
        fig.update_layout(**base_layout(title="Density View"))
        return fig

    fig.add_trace(go.Histogram2dContour(
        x=np.log10(sub["pl_orbsmax"]),
        y=np.log10(sub["pl_rade"]),
        colorscale="Viridis",
        reversescale=False,
        contours=dict(showlines=False),
        showscale=True,
        colorbar=dict(
            title=dict(text="Planet count", side="right",
                       font=dict(size=10, family="'IBM Plex Mono', monospace")),
            x=1.02, xanchor="left",
            thickness=14, len=0.75, tickfont=dict(size=9), outlinewidth=0,
        ),
        ncontours=25,
        hovertemplate="log\u2081\u2080 dist: %{x:.2f}<br>log\u2081\u2080 radius: %{y:.2f}<extra></extra>",
    ))

    add_radius_reflines(fig, xref_mode="paper")

    x_tvals = list(range(X_MIN_LOG, X_MAX_LOG + 1))
    y_tvals = list(range(int(np.floor(Y_MIN_LOG)), int(np.ceil(Y_MAX_LOG)) + 1))

    fig.update_layout(
        **base_layout(
            title="Density View \u2014 Where Do Planets Cluster?",
            margin=dict(l=60, r=80, t=45, b=55),
        ),
        xaxis=dict(
            title="Orbital Distance (AU, log scale)",
            showgrid=True, gridcolor="#3a4d6b", gridwidth=1,
            range=[X_MIN_LOG, X_MAX_LOG], dtick=1,
            tickmode="array", tickvals=x_tvals,
            ticktext=[_fmt_log(v) for v in x_tvals],
            zeroline=False,
        ),
        yaxis=dict(
            title="Planet Radius (R\u2295, log scale)",
            showgrid=True, gridcolor="#3a4d6b", gridwidth=1,
            range=[Y_MIN_LOG, Y_MAX_LOG], dtick=1,
            tickmode="array", tickvals=y_tvals,
            ticktext=[_fmt_log(v) for v in y_tvals],
            zeroline=False,
        ),
    )
    return fig
