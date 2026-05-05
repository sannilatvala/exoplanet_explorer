import pandas as pd
import plotly.graph_objects as go

from utils.constants import CAT_ORDER, PTYPE_COLORS, DMETHOD_COLORS
from utils.helpers import base_layout

_LEGEND = dict(x=1.01, y=1, bgcolor="rgba(0,0,0,0)", font=dict(size=10))

def _year_label(y):
    if pd.notna(y) and y < 2000:
        return "<2000"
    return str(int(y)) if pd.notna(y) else "Unknown"


def _year_order(df):
    return ["<2000"] + sorted(
        [y for y in df["yr_lbl"].unique() if y != "<2000"],
        key=lambda x: int(x),
    )


def build_discovery_charts(filtered_df):
    if "discoverymethod_mapped" not in filtered_df.columns or filtered_df.empty:
        empty = go.Figure(layout=base_layout())
        return empty, empty, empty, empty

    myd = filtered_df.copy()
    myd["yr_lbl"] = myd["disc_year"].apply(_year_label)
    myd = myd[myd["yr_lbl"] != "Unknown"]
    all_years = _year_order(myd)
    method_year = myd.groupby(["yr_lbl", "discoverymethod_mapped"]).size().reset_index(name="count")

    fig_stack = go.Figure()
    for method in method_year["discoverymethod_mapped"].unique():
        s = method_year[method_year["discoverymethod_mapped"] == method]
        full = pd.DataFrame({"yr_lbl": all_years}).merge(s[["yr_lbl", "count"]], how="left").fillna(0)
        fig_stack.add_trace(go.Bar(
            x=full["yr_lbl"], y=full["count"],
            name=method, marker_color=DMETHOD_COLORS.get(method, "#888"),
            hovertemplate=f"{method}: %{{y}}<extra></extra>",
        ))
    fig_stack.update_layout(
        **base_layout(title="Discoveries by Method per Year", barmode="stack",
                      legend=dict(title="Method", x=1.01, y=1, bgcolor="rgba(0,0,0,0)")),
        xaxis=dict(title="Year", tickangle=-45,
                   categoryorder="array", categoryarray=all_years, gridcolor="#2a3a55"),
        yaxis=dict(title="Count", gridcolor="#2a3a55"),
    )

    pie_data = (filtered_df.groupby("discoverymethod_mapped", observed=True)
                .size().reset_index(name="count"))
    fig_pie = go.Figure(go.Pie(
        labels=pie_data["discoverymethod_mapped"],
        values=pie_data["count"],
        marker_colors=[DMETHOD_COLORS.get(m, "#888") for m in pie_data["discoverymethod_mapped"]],
        textinfo="percent+label", textposition="inside",
        pull=[0.04] * len(pie_data),
        showlegend=True,
        insidetextfont=dict(size=10),
    ))
    fig_pie.update_layout(
    **base_layout(title="Share by Discovery Method",
                  legend=dict(title="Method", **_LEGEND))
)

    tyd = filtered_df.copy()
    tyd["yr_lbl"] = tyd["disc_year"].apply(_year_label)
    tyd = tyd[tyd["yr_lbl"] != "Unknown"]
    type_year = tyd.groupby(["yr_lbl", "pl_type"], observed=False).size().reset_index(name="count")
    yr_order = ["<2000"] + sorted(
        [y for y in type_year["yr_lbl"].unique() if y != "<2000"], key=lambda x: int(x)
    )

    fig_type_yr = go.Figure()
    for ptype in CAT_ORDER:
        s = type_year[type_year["pl_type"] == ptype]
        full = pd.DataFrame({"yr_lbl": yr_order}).merge(s[["yr_lbl", "count"]], how="left").fillna(0)
        fig_type_yr.add_trace(go.Bar(
            x=full["yr_lbl"], y=full["count"],
            name=ptype, marker_color=PTYPE_COLORS.get(ptype, "#888"),
            offsetgroup=ptype,
        ))
    fig_type_yr.update_layout(
        **base_layout(title="Discoveries per Year by Planet Type", barmode="group",
                      legend=dict(title="Planet Type", x=1.01, y=1, bgcolor="rgba(0,0,0,0)")),
        xaxis=dict(title="Year", tickangle=-45,
                   categoryorder="array", categoryarray=yr_order, gridcolor="#2a3a55"),
        yaxis=dict(title="Count", gridcolor="#2a3a55"),
    )

    tm = (filtered_df
          .groupby(["pl_type", "discoverymethod_mapped"], observed=False)
          .size().reset_index(name="count"))
    fig_type_method = go.Figure()
    for method in tm["discoverymethod_mapped"].unique():
        s = tm[tm["discoverymethod_mapped"] == method]
        fig_type_method.add_trace(go.Bar(
            x=s["pl_type"], y=s["count"],
            name=method, marker_color=DMETHOD_COLORS.get(method, "#888"),
            hovertemplate=f"{method}: %{{y}}<extra></extra>",
        ))
    fig_type_method.update_layout(
    **base_layout(title="Planet Types vs Discovery Methods",
                  barmode="stack",
                  legend=dict(title="Method", **_LEGEND)),
        xaxis=dict(title="Planet Type", categoryorder="array", categoryarray=CAT_ORDER),
        yaxis=dict(title="Count", gridcolor="#2a3a55"),
    )

    return fig_stack, fig_pie, fig_type_yr, fig_type_method
