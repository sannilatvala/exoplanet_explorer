from dash import html, dcc
from utils.constants import (
    DARK_BG, PANEL_BG, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT,
)


def _tab_style(selected=False):
    return {
        "background": "transparent",
        "color": TEXT_SECONDARY if not selected else ACCENT,
        "border": "none",
        "borderBottom": f"2px solid {ACCENT}" if selected else "2px solid transparent",
        "fontFamily": "'IBM Plex Mono', monospace",
        "fontSize": "0.72rem",
        "letterSpacing": "0.12em",
        "padding": "10px 18px",
    }


def build_layout(sidebar):
    return html.Div(
        style={
            "background": DARK_BG, "minHeight": "100vh",
            "color": TEXT_PRIMARY, "fontFamily": "'IBM Plex Mono', monospace",
        },
        children=[
            html.Div([
                html.Div([
                    html.Div("\u2736", style={
                        "color": ACCENT, "fontSize": "2rem",
                        "lineHeight": "1", "marginRight": "14px", "marginTop": "2px",
                    }),
                    html.Div([
                        html.H1("EXOPLANET EXPLORER", style={
                            "fontSize": "1.5rem", "fontWeight": "700", "margin": "0",
                            "letterSpacing": "0.15em", "color": TEXT_PRIMARY,
                            "fontFamily": "'IBM Plex Mono', monospace",
                        }),
                        html.P("Mapping worlds beyond our solar system", style={
                            "color": TEXT_SECONDARY, "fontSize": "0.78rem",
                            "margin": "0", "letterSpacing": "0.08em",
                        }),
                    ]),
                ], style={"display": "flex", "alignItems": "flex-start"}),
                html.Div(id="stat-strip",
                         style={"display": "flex", "gap": "10px", "flexWrap": "wrap"}),
            ], style={
                "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                "padding": "20px 32px", "borderBottom": f"1px solid {BORDER_COLOR}",
                "background": PANEL_BG,
            }),

            html.Div([
                html.Div(sidebar, style={"width": "255px", "flexShrink": "0", "padding": "24px 0"}),
                html.Div([
                    dcc.Tabs(
                        id="tabs", value="tab-scatter",
                        style={"marginBottom": "20px"},
                        children=[
                            dcc.Tab(label="SCATTER & DENSITY", value="tab-scatter",
                                    style=_tab_style(), selected_style=_tab_style(selected=True)),
                            dcc.Tab(label="DISCOVERY CHARTS",  value="tab-discovery",
                                    style=_tab_style(), selected_style=_tab_style(selected=True)),
                        ],
                    ),
                    html.Div(id="tab-content"),
                ], style={"flex": "1", "padding": "24px 24px 24px 20px", "minWidth": "0"}),
            ], style={
                "display": "flex", "gap": "0",
                "maxWidth": "1600px", "margin": "0 auto", "padding": "0 32px",
            }),

            dcc.Store(id="filtered-data"),
        ],
    )
