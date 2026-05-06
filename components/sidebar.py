from dash import html, dcc
from utils.constants import (
    CAT_ORDER, PTYPE_COLORS, DMETHOD_COLORS, EARTH_COLOR,
    PANEL_BG, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT, DARK_BG,
    PTYPE_EXPLANATIONS, METHOD_EXPLANATIONS,
)


def _sidebar_label(text):
    return html.Div(text, style={
        "fontSize": "0.65rem", "letterSpacing": "0.2em",
        "color": TEXT_SECONDARY, "marginBottom": "8px",
        "textTransform": "uppercase",
    })


def _field_label(text):
    return html.Label(text, style={
        "fontSize": "0.72rem", "color": TEXT_SECONDARY,
        "letterSpacing": "0.08em", "textTransform": "uppercase",
        "marginBottom": "6px", "display": "block",
    })


def _hr():
    return html.Hr(style={"border": f"1px solid {BORDER_COLOR}", "margin": "0 0 16px 0"})


_SIZE_ROWS = [
    ("#C44E52", "< 1.5 R\u2295: Terrestrial"),
    ("#DD8452", "1.5 \u2013 2.5 R\u2295: Super-Earth"),
    ("#55A868", "2.5 \u2013 6.0 R\u2295: Neptunian"),
    ("#4C72B0", "> 6.0 R\u2295: Gas Giant"),
]


def _tooltip_panel_entries(explanations):
    """Build entry divs for the tooltip panel from (name, color, desc) tuples."""
    entries = []
    for i, (name, color, desc) in enumerate(explanations):
        is_last = i == len(explanations) - 1
        entries.append(
            html.Div([
                html.Div(style={
                    "width": "8px", "height": "8px", "borderRadius": "50%",
                    "background": color, "flexShrink": "0", "marginTop": "4px",
                }),
                html.Div([
                    html.Div(name, style={
                        "fontFamily": "'IBM Plex Mono', monospace",
                        "fontSize": "0.78rem", "fontWeight": "700",
                        "color": color, "marginBottom": "2px",
                    }),
                    html.P(desc, style={
                        "fontFamily": "'IBM Plex Mono', monospace",
                        "fontSize": "0.74rem", "color": TEXT_SECONDARY,
                        "lineHeight": "1.5", "margin": "0",
                    }),
                ], style={"flex": "1"}),
            ], style={
                "display": "flex", "gap": "10px", "alignItems": "flex-start",
                "padding": "8px 0",
                "borderBottom": "none" if is_last else f"1px solid {BORDER_COLOR}",
            })
        )
    return entries


def _info_icon_with_tooltip(explanations):
    """
    Renders the i icon alongside a hidden .info-tooltip-panel sibling.

    The panel is kept display:none in the DOM. tooltip_portal.js reads its
    contents on mouseenter, clones it into <body> as position:fixed (escaping
    all overflow ancestors), positions it via getBoundingClientRect(), and
    removes the clone on mouseleave.
    """
    panel = html.Div(
        _tooltip_panel_entries(explanations),
        className="info-tooltip-panel",
        style={"display": "none"},
    )

    icon = html.Span("i", className="info-tooltip-icon")

    return html.Span(
        [icon, panel],
        className="info-tooltip-wrap",
        style={
            "display": "inline-flex", "alignItems": "center",
            "marginLeft": "6px", "verticalAlign": "middle",
            "position": "relative",
        },
    )


def _field_label_with_tooltip(text, explanations):
    """A filter section label with an inline i info icon."""
    return html.Div([
        html.Label(text, style={
            "fontSize": "0.72rem", "color": TEXT_SECONDARY,
            "letterSpacing": "0.08em", "textTransform": "uppercase",
            "marginBottom": "0", "display": "inline",
        }),
        _info_icon_with_tooltip(explanations),
    ], style={"display": "flex", "alignItems": "center", "marginBottom": "6px"})


def build_sidebar(all_methods, year_min, year_max):
    method_options = [
        {
            "label": html.Span(m, style={
                "color": DMETHOD_COLORS.get(m, TEXT_SECONDARY),
                "marginLeft": "6px", "fontSize": "0.82rem",
            }),
            "value": m,
        }
        for m in all_methods
    ]

    return html.Div([
        _sidebar_label("FILTERS"),

        _field_label_with_tooltip("Planet Type", PTYPE_EXPLANATIONS),
        dcc.Checklist(
            id="filter-ptype",
            options=[{
                "label": html.Span(t, style={
                    "color": PTYPE_COLORS.get(t, "#fff"),
                    "marginLeft": "6px", "fontSize": "0.85rem",
                }),
                "value": t,
            } for t in CAT_ORDER],
            value=CAT_ORDER,
            style={"marginBottom": "18px"},
            inputStyle={"marginRight": "6px"},
        ),

        _hr(),

        _field_label_with_tooltip("Discovery Method", METHOD_EXPLANATIONS),
        dcc.Checklist(
            id="filter-method",
            options=method_options,
            value=all_methods,
            style={"marginBottom": "18px"},
            inputStyle={"marginRight": "6px"},
        ),

        _hr(),

        _field_label("Discovery Year Range"),
        dcc.RangeSlider(
            id="filter-year",
            min=year_min, max=year_max, step=1,
            value=[year_min, year_max],
            marks=None,
            tooltip={
                "placement": "bottom",
                "always_visible": False,
                "style": {
                    "color": DARK_BG,
                    "backgroundColor": TEXT_PRIMARY,
                    "fontSize": "12px",
                    "fontFamily": "'IBM Plex Mono', monospace",
                    "fontWeight": "600",
                },
            },
        ),
        html.Div(id="year-display", style={
            "color": ACCENT, "fontSize": "0.82rem",
            "marginTop": "10px", "textAlign": "center",
            "letterSpacing": "0.06em",
        }),

        html.Hr(style={"border": f"1px solid {BORDER_COLOR}", "margin": "18px 0"}),

        _sidebar_label("SCATTER OPTIONS"),

        dcc.Checklist(
            id="filter-show-nan-temp",
            options=[{
                "label": html.Span(
                    "Show planets with unknown temperature",
                    style={"color": TEXT_SECONDARY, "fontSize": "0.8rem", "marginLeft": "6px"},
                ),
                "value": "show",
            }],
            value=["show"],
            style={"marginBottom": "6px"},
            inputStyle={"marginRight": "6px"},
        ),
        html.Div([
            html.Span("\u25cf  ", style={"color": "rgba(160,170,190,0.7)", "fontSize": "0.9rem"}),
            html.Span("Grey points = unknown temperature",
                      style={"color": "rgba(160,170,190,0.65)", "fontSize": "0.72rem"}),
        ], style={"marginBottom": "12px", "paddingLeft": "2px"}),

        dcc.Checklist(
            id="filter-show-earth",
            options=[{
                "label": html.Span(
                    "Show Earth reference",
                    style={"color": EARTH_COLOR, "fontSize": "0.8rem", "marginLeft": "6px"},
                ),
                "value": "show",
            }],
            value=["show"],
            style={"marginBottom": "6px"},
            inputStyle={"marginRight": "6px"},
        ),
        html.Div([
            html.Span("\u25cf  ", style={"color": EARTH_COLOR, "fontSize": "0.85rem"}),
            html.Span("Green circle = Earth at 1 AU, 1 R\u2295",
                      style={"color": "rgba(57,255,20,0.6)", "fontSize": "0.72rem"}),
        ], style={"marginBottom": "18px", "paddingLeft": "2px"}),

        _hr(),

        _sidebar_label("PLANET SIZE GUIDE"),
        html.Div([
            html.Div(
                html.Span(text, style={"color": color, "fontSize": "0.79rem"}),
                style={"marginBottom": "6px"},
            )
            for color, text in _SIZE_ROWS
        ], style={"paddingLeft": "2px"}),

    ], style={
        "position": "sticky", "top": "0",
        "background": PANEL_BG, "border": f"1px solid {BORDER_COLOR}",
        "borderRadius": "12px", "padding": "22px 16px",
        "overflowY": "auto", "maxHeight": "98vh",
    })