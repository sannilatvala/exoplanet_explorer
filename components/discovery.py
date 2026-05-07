import pandas as pd
import plotly.graph_objects as go

from utils.constants import CAT_ORDER, PTYPE_COLORS, DMETHOD_COLORS
from utils.helpers import base_layout

_LEGEND = dict(x=1.01, y=1, bgcolor="rgba(0,0,0,0)", font=dict(size=10))
_DISCOVERY_UIREVISION = "discovery-chart-axes-v3"

ALLOWED_METHODS = [
    "Transit",
    "Radial Velocity",
    "Microlensing",
    "Imaging",
    "Other",
]


def _year_label(y):
    if pd.notna(y) and y < 2000:
        return "<2000"
    return str(int(y)) if pd.notna(y) else "Unknown"


def _canonical_year_order(df):
    """
    Build the full year/category domain from a canonical dataframe.

    This is intentionally independent from the sidebar-filtered dataframe so
    that empty sidebar states do not collapse the axes.
    """
    if df is None or df.empty or "disc_year" not in df.columns:
        return []

    years = pd.to_numeric(df["disc_year"], errors="coerce").dropna()
    if years.empty:
        return []

    years = years.astype(int)
    order = []

    if (years < 2000).any():
        order.append("<2000")

    order.extend(str(y) for y in sorted(years[years >= 2000].unique()))
    return order


def _normalize_method(m):
    if pd.isna(m):
        return "Other"
    return m if m in ALLOWED_METHODS and m != "Other" else (
        m if m in ["Transit", "Radial Velocity", "Microlensing", "Imaging"] else "Other"
    )


def _trace_visibility(category, active_set):
    """
    True         → sidebar ON  → trace data shown,   legend entry shown
    "legendonly" → sidebar OFF → trace data hidden,  legend entry STILL shown

    Used for Bar traces (fig_stack, fig_type_yr, fig_type_method).
    """
    return True if category in active_set else "legendonly"


def _year_axis_layout(years):
    return dict(
        title="Year",
        type="category",
        tickangle=-45,
        categoryorder="array",
        categoryarray=years,
        tickmode="array",
        tickvals=years,
        ticktext=years,
        gridcolor="#2a3a55",
    )


def build_discovery_charts(filtered_df, active_ptypes=None, active_methods=None, full_df=None):
    """
    Build all four discovery charts.

    Parameters
    ----------
    filtered_df : pd.DataFrame
        Already sidebar-filtered dataframe (year + active selections applied).
        Used for counts.
    active_ptypes : list[str] | None
        Planet types currently enabled in the sidebar.
        Defaults to all CAT_ORDER entries when not supplied.
    active_methods : list[str] | None
        Discovery methods currently enabled in the sidebar.
        Defaults to all ALLOWED_METHODS entries when not supplied.
    full_df : pd.DataFrame | None
        Canonical unfiltered dataframe used to preserve axis/category domains.
        This prevents axes from collapsing when the sidebar filters remove all
        visible rows.
    """
    if active_ptypes is None:
        active_ptypes = list(CAT_ORDER)
    if active_methods is None:
        active_methods = list(ALLOWED_METHODS)

    active_ptype_set = set(active_ptypes)
    active_method_set = set(active_methods)

    if "discoverymethod_mapped" not in filtered_df.columns:
        empty = go.Figure(layout=base_layout())
        return empty, empty, empty, empty

    myd = filtered_df.copy()
    myd["discoverymethod_ui"] = myd["discoverymethod_mapped"].apply(_normalize_method)
    myd["yr_lbl"] = myd["disc_year"].apply(_year_label)
    myd = myd[myd["yr_lbl"] != "Unknown"]

    axis_source = full_df if full_df is not None else filtered_df
    all_years = _canonical_year_order(axis_source)
    if not all_years:
        all_years = _canonical_year_order(myd)

    method_year = (
        myd.groupby(["yr_lbl", "discoverymethod_ui"])
        .size()
        .reset_index(name="count")
    )
    method_year["discoverymethod_ui"] = pd.Categorical(
        method_year["discoverymethod_ui"],
        categories=ALLOWED_METHODS,
        ordered=True,
    )

    fig_stack = go.Figure()
    for method in ALLOWED_METHODS:
        s = method_year[method_year["discoverymethod_ui"] == method][["yr_lbl", "count"]]
        full = (
            pd.DataFrame({"yr_lbl": all_years})
            .merge(s, how="left", on="yr_lbl")
            .fillna(0)
        ) if all_years else pd.DataFrame({"yr_lbl": [], "count": []})

        fig_stack.add_trace(go.Bar(
            x=full["yr_lbl"],
            y=full["count"],
            name=method,
            marker_color=DMETHOD_COLORS.get(method, "#888"),
            hovertemplate=f"{method}: %{{y}}<extra></extra>",
            visible=_trace_visibility(method, active_method_set),
        ))

    fig_stack.update_layout(
        **base_layout(
            title="Discoveries by Method per Year",
            barmode="stack",
            legend=dict(title="Method", x=1.01, y=1, bgcolor="rgba(0,0,0,0)"),
        ),
        uirevision=_DISCOVERY_UIREVISION,
        xaxis=_year_axis_layout(all_years),
        yaxis=dict(title="Count", gridcolor="#2a3a55"),
    )

    pie_counts = (
        myd.groupby("discoverymethod_ui")
        .size()
        .reindex(ALLOWED_METHODS, fill_value=0)
    )
    inactive_methods = [m for m in ALLOWED_METHODS if m not in active_method_set]

    fig_pie = go.Figure(go.Pie(
        labels=ALLOWED_METHODS,
        values=pie_counts.tolist(),
        marker_colors=[DMETHOD_COLORS.get(m, "#888") for m in ALLOWED_METHODS],
        textinfo="percent+label",
        textposition="inside",
        pull=[0.04] * len(ALLOWED_METHODS),
        showlegend=True,
        sort=False,
        insidetextfont=dict(size=10),
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))

    fig_pie.update_layout(
        **base_layout(
            title="Share by Discovery Method",
            legend=dict(title="Method", **_LEGEND),
            hiddenlabels=inactive_methods,
        ),
        uirevision=_DISCOVERY_UIREVISION,
    )

    type_year = (
        myd.groupby(["yr_lbl", "pl_type"], observed=False)
        .size()
        .reset_index(name="count")
    )

    yr_order = all_years
    full_grid = pd.MultiIndex.from_product(
        [yr_order, CAT_ORDER],
        names=["yr_lbl", "pl_type"]
    ).to_frame(index=False)
    type_year_full = (
        full_grid.merge(type_year, on=["yr_lbl", "pl_type"], how="left")
        .fillna({"count": 0})
    )

    fig_type_yr = go.Figure()
    for ptype in CAT_ORDER:
        s = type_year_full[type_year_full["pl_type"] == ptype]
        fig_type_yr.add_trace(go.Bar(
            x=s["yr_lbl"],
            y=s["count"],
            name=ptype,
            marker_color=PTYPE_COLORS.get(ptype, "#888"),
            offsetgroup=ptype,
            visible=_trace_visibility(ptype, active_ptype_set),
        ))

    fig_type_yr.update_layout(
        **base_layout(
            title="Discoveries per Year by Planet Type",
            barmode="group",
            legend=dict(title="Planet Type", x=1.01, y=1, bgcolor="rgba(0,0,0,0)"),
        ),
        uirevision=_DISCOVERY_UIREVISION,
        xaxis=_year_axis_layout(yr_order),
        yaxis=dict(title="Count", gridcolor="#2a3a55"),
    )

    tm = (
        myd.groupby(["pl_type", "discoverymethod_ui"], observed=False)
        .size()
        .reset_index(name="count")
    )
    full_grid = pd.MultiIndex.from_product(
        [CAT_ORDER, ALLOWED_METHODS],
        names=["pl_type", "discoverymethod_ui"],
    ).to_frame(index=False)
    tm_full = (
        full_grid.merge(tm, on=["pl_type", "discoverymethod_ui"], how="left")
        .fillna({"count": 0})
    )

    fig_type_method = go.Figure()
    for method in ALLOWED_METHODS:
        s = tm_full[tm_full["discoverymethod_ui"] == method]
        fig_type_method.add_trace(go.Bar(
            x=s["pl_type"],
            y=s["count"],
            name=method,
            marker_color=DMETHOD_COLORS.get(method, "#888"),
            hovertemplate=f"{method}: %{{y}}<extra></extra>",
            showlegend=True,
            visible=_trace_visibility(method, active_method_set),
        ))

    fig_type_method.update_layout(
        **base_layout(
            title="Planet Types vs Discovery Methods",
            barmode="stack",
            legend=dict(title="Method", **_LEGEND),
        ),
        uirevision=_DISCOVERY_UIREVISION,
        xaxis=dict(
            title="Planet Type",
            type="category",
            categoryorder="array",
            categoryarray=list(CAT_ORDER),
            tickmode="array",
            tickvals=list(CAT_ORDER),
            ticktext=list(CAT_ORDER),
        ),
        yaxis=dict(title="Count", gridcolor="#2a3a55"),
    )

    return fig_stack, fig_pie, fig_type_yr, fig_type_method