from dash import dcc, html, Input, Output

from utils.constants import CARD_BG, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT
from utils.helpers import filter_dataframe
from components.scatter import build_scatter
from components.hexbin import build_hexbin
from components.discovery import build_discovery_charts
from components.metrics import build_stats_strip


def _section_header(title, subtitle=""):
    return html.Div([
        html.H3(title, style={
            "color": TEXT_PRIMARY, "fontFamily": "'IBM Plex Mono', monospace",
            "fontWeight": "700", "marginBottom": "4px",
            "fontSize": "1rem", "letterSpacing": "0.05em",
        }),
        html.P(subtitle, style={
            "color": TEXT_SECONDARY, "fontSize": "0.8rem",
            "margin": "0", "lineHeight": "1.55",
        }),
    ], style={"marginBottom": "14px"})


def _chart_card(children, height="420px"):
    return html.Div(children, style={
        "background": CARD_BG, "border": f"1px solid {BORDER_COLOR}",
        "borderRadius": "12px", "padding": "20px",
        "minHeight": height, "marginBottom": "20px",
    })


def _view_label(text):
    return html.Div(text, style={
        "fontSize": "0.62rem", "letterSpacing": "0.18em",
        "color": ACCENT, "textTransform": "uppercase",
        "marginBottom": "6px", "fontWeight": "600",
    })


def register_callbacks(app, df):

    @app.callback(
        Output("year-display", "children"),
        Input("filter-year", "value"),
    )
    def update_year_label(yr):
        return f"{yr[0]} \u2014 {yr[1]}" if yr else ""

    @app.callback(
        Output("stat-strip",  "children"),
        Output("tab-content", "children"),
        Input("filter-ptype",         "value"),
        Input("filter-method",        "value"),
        Input("filter-year",          "value"),
        Input("filter-show-nan-temp", "value"),
        Input("filter-show-earth",    "value"),
        Input("tabs",                 "value"),
    )
    def update_all(ptypes, methods, year_range, show_nan_temp_val, show_earth_val, tab):
        fdf = filter_dataframe(df, ptypes, methods, year_range)
        show_nan_temp = "show" in (show_nan_temp_val or [])
        show_earth    = "show" in (show_earth_val    or [])

        stats_strip = build_stats_strip(fdf)

        if tab == "tab-scatter":
            content = _build_scatter_tab(fdf, show_nan_temp, show_earth)
        elif tab == "tab-discovery":
            content = _build_discovery_tab(fdf, ptypes, methods)
        else:
            content = html.Div("Select a tab above.", style={"color": TEXT_SECONDARY})

        return stats_strip, content


def _build_scatter_tab(fdf, show_nan_temp, show_earth):
    nan_count = int(fdf["pl_eqt"].isna().sum()) if "pl_eqt" in fdf.columns else 0
    nan_note = html.Div(
        [
            html.Span("\u2139\ufe0f  ", style={"marginRight": "4px"}),
            html.Span(
                f"{nan_count:,} planet{'s' if nan_count != 1 else ''} "
                f"{'are' if nan_count != 1 else 'is'} missing temperature data. "
                + ("Shown as grey points." if show_nan_temp
                   else "Enable \u201cShow planets with unknown temperature\u201d "
                        "in the sidebar to display them."),
            ),
        ],
        style={
            "fontSize": "0.76rem", "color": TEXT_SECONDARY,
            "background": CARD_BG, "border": f"1px solid {BORDER_COLOR}",
            "borderRadius": "8px", "padding": "10px 14px",
            "marginBottom": "14px", "lineHeight": "1.5",
        },
    ) if nan_count > 0 else html.Div()

    return html.Div([
        html.Div([
            _view_label("Scatter View"),
            _section_header(
                "Orbital Distance vs Planet Radius",
                "Each dot = one planet. X-axis = distance from star (AU). "
                "Y-axis = planet size (Earth = 1). "
                "Colour = temperature (purple = cold, yellow = hot).",
            ),
            nan_note,
            _chart_card(
                dcc.Graph(
                    figure=build_scatter(fdf, show_nan_temp=show_nan_temp, show_earth=show_earth),
                    config={"displayModeBar": False},
                    style={"height": "430px"},
                ),
                height="470px",
            ),
        ]),
        html.Div([
            _view_label("Density View"),
            _section_header(
                "Where Do Planets Cluster?",
                "Same axes as the scatter plot. Brighter cells = more planets in that region. "
                "Useful for spotting where planets concentrate in distance and size.",
            ),
            _chart_card(
                dcc.Graph(
                    figure=build_hexbin(fdf),
                    config={"displayModeBar": False},
                    style={"height": "430px"},
                ),
                height="470px",
            ),
        ]),
    ])


def _build_discovery_tab(fdf, active_ptypes=None, active_methods=None):
    fig_stack, fig_pie, fig_type_yr, fig_type_method = build_discovery_charts(
        fdf,
        active_ptypes=active_ptypes,
        active_methods=active_methods,
    )
    return html.Div([
        html.Div([
            html.Div([
                _section_header(
                    "Discoveries Over Time",
                    "Confirmed planets per year by detection method, showing Kepler mission's spike around 2014\u201316.",
                ),
                _chart_card(dcc.Graph(figure=fig_stack, config={"displayModeBar": False},
                                      style={"height": "320px"}), height="360px"),
            ], style={"flex": "6", "minWidth": "0"}),
            html.Div([
                _section_header(
                    "Method Share",
                    "Fraction of confirmed planets found by each detection method",
                ),
                _chart_card(dcc.Graph(figure=fig_pie, config={"displayModeBar": False},
                                      style={"height": "320px"}), height="360px"),
            ], style={"flex": "4", "minWidth": "0"}),
        ], style={"display": "flex", "gap": "20px"}),
        html.Div([
            html.Div([
                _section_header(
                    "Planet Types per Year",
                    "Confirmed planets per year by size, showing how discovery methods shaped findings.",
                ),
                _chart_card(dcc.Graph(figure=fig_type_yr, config={"displayModeBar": False},
                                      style={"height": "320px"}), height="360px"),
            ], style={"flex": "6", "minWidth": "0"}),
            html.Div([
                _section_header(
                    "Planet Types vs Discovery Methods",
                    "Which detection methods tend to find which planet sizes. ",
                ),
                _chart_card(dcc.Graph(figure=fig_type_method, config={"displayModeBar": False},
                                      style={"height": "320px"}), height="360px"),
            ], style={"flex": "4", "minWidth": "0"}),
        ], style={"display": "flex", "gap": "20px"}),
    ])