from dash import html
from utils.constants import (
    DARK_BG, CARD_BG, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT,
    PTYPE_EXPLANATIONS, METHOD_EXPLANATIONS,
)


def info_banner(toggle_id, chevron_id, body_id, header_icon, header_text,
                body_content, initially_open=False):
    chevron   = " \u25b2" if initially_open else " \u25bc"
    body_disp = "block"   if initially_open else "none"
    return html.Div([
        html.Div(
            id=toggle_id, n_clicks=0,
            children=[
                html.Span(header_icon, style={"marginRight": "8px"}),
                html.Span(header_text,
                          style={"letterSpacing": "0.1em", "fontSize": "0.72rem"}),
                html.Span(chevron, id=chevron_id,
                          style={"marginLeft": "8px", "fontSize": "0.7rem",
                                 "color": TEXT_SECONDARY}),
            ],
            style={
                "display": "flex", "alignItems": "center",
                "color": ACCENT, "cursor": "pointer",
                "fontFamily": "'IBM Plex Mono', monospace",
                "fontWeight": "600", "padding": "11px 16px",
                "borderBottom": f"1px solid {BORDER_COLOR}",
            },
        ),
        html.Div(id=body_id, style={"display": body_disp}, children=[body_content]),
    ], style={
        "background": CARD_BG, "border": f"1px solid {BORDER_COLOR}",
        "borderRadius": "12px", "marginBottom": "16px", "overflow": "hidden",
    })


def _explanation_grid(items, min_width="200px"):
    return html.Div([
        html.Div([
            html.Div([
                html.Span("\u25cf", style={"color": color, "marginRight": "8px",
                                           "fontSize": "1rem"}),
                html.Span(name, style={"color": color, "fontWeight": "600",
                                       "fontSize": "0.82rem"}),
            ], style={"marginBottom": "4px", "display": "flex", "alignItems": "center"}),
            html.P(desc, style={
                "color": TEXT_SECONDARY, "fontSize": "0.77rem",
                "margin": "0", "lineHeight": "1.5",
            }),
        ], style={
            "background": DARK_BG, "border": f"1px solid {BORDER_COLOR}",
            "borderRadius": "8px", "padding": "12px 14px",
            "flex": "1", "minWidth": min_width,
        })
        for name, color, desc in items
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "10px", "padding": "16px"})


def _tool_intro_content(scatter_mode=True):
    hover_tip = (
        "Hover over any point for details. Scroll to zoom; click and drag to pan."
        if scatter_mode
        else "Hover over any point for details. Click legend items to toggle series."
    )
    return html.Div([
        html.P(
            "Welcome to the Exoplanet Explorer \u2014 an interactive tool for exploring "
            "thousands of confirmed planets discovered beyond our solar system.",
            style={"color": TEXT_PRIMARY, "fontSize": "0.85rem",
                   "marginBottom": "10px", "lineHeight": "1.6"},
        ),
        html.Div([
            html.Div([
                html.Span("\U0001f50e  ", style={"color": ACCENT}),
                html.Span("Use the sidebar filters to narrow down planets by type, "
                          "discovery method, or year of discovery.",
                          style={"color": TEXT_SECONDARY, "fontSize": "0.8rem"}),
            ], style={"marginBottom": "6px"}),
            html.Div([
                html.Span("\U0001f5b1\ufe0f  ", style={"color": ACCENT}),
                html.Span(hover_tip,
                          style={"color": TEXT_SECONDARY, "fontSize": "0.8rem"}),
            ], style={"marginBottom": "6px"}),
            html.Div([
                html.Span("\U0001f4ca  ", style={"color": ACCENT}),
                html.Span("Switch between tabs to explore different views of the data.",
                          style={"color": TEXT_SECONDARY, "fontSize": "0.8rem"}),
            ]),
        ], style={"paddingLeft": "4px"}),
    ], style={"padding": "14px 16px"})


def build_scatter_info_panels():
    tool_intro = info_banner(
        "tool-intro-toggle", "tool-intro-chevron", "tool-intro-body",
        "\u2139\ufe0f", "ABOUT THIS TOOL \u2014 HOW TO USE",
        _tool_intro_content(scatter_mode=True),
        initially_open=True,
    )

    scatter_help_content = html.Div([
        html.P([
            html.B("Scatter View: "),
            "Each dot is one exoplanet. Its position shows how far from its star it orbits "
            "(x-axis, in AU) and how large it is (y-axis, in Earth radii). "
            "Colour shows the planet\u2019s equilibrium temperature \u2014 "
            "dark purple = cold, bright yellow = very hot. "
            "Grey dots have no temperature data. "
            "The green dot marks Earth as a familiar reference point.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem",
                  "lineHeight": "1.6", "marginBottom": "8px"}),
        html.P([
            html.B("Density View: "),
            "The same data shown as a heatmap \u2014 brighter regions contain more planets. "
            "Useful for spotting where planets cluster in the distance\u2013size space.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem",
                  "lineHeight": "1.6", "marginBottom": "8px"}),
        html.P([
            html.B("Interaction tips: "),
            "Hover over any point for details. Scroll to zoom, drag to pan. "
            "Use the sidebar to filter by planet type, discovery method, or year. "
            "Dashed horizontal lines mark the boundaries between planet size categories.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem", "lineHeight": "1.6",
                  "margin": "0"}),
    ], style={"padding": "14px 16px"})

    scatter_help = info_banner(
        "scatter-help-toggle", "scatter-help-chevron", "scatter-help-body",
        "\U0001f4c8", "HOW TO READ THIS PAGE", scatter_help_content,
        initially_open=False,
    )

    ptype_panel = info_banner(
        "ptype-explainer-toggle", "ptype-explainer-chevron", "ptype-explainer-body",
        "\U0001fa90", "WHAT ARE THESE PLANET TYPES?",
        _explanation_grid(PTYPE_EXPLANATIONS, min_width="200px"),
        initially_open=False,
    )

    return tool_intro, scatter_help, ptype_panel


def build_discovery_info_panels():
    tool_intro = info_banner(
        "tool-intro-d-toggle", "tool-intro-d-chevron", "tool-intro-d-body",
        "\u2139\ufe0f", "ABOUT THIS TOOL \u2014 HOW TO USE",
        _tool_intro_content(scatter_mode=False),
        initially_open=True,
    )

    discovery_help_content = html.Div([
        html.P([
            html.B("Discoveries Over Time: "),
            "Each coloured segment shows how many planets were found per year using a given "
            "method. The huge spike around 2014\u201316 is when the Kepler mission released "
            "thousands of transit discoveries.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem",
                  "lineHeight": "1.6", "marginBottom": "8px"}),
        html.P([
            html.B("Method Share: "),
            "The pie shows what fraction of all known exoplanets were found by each method. "
            "Transit dominates because space telescopes can screen thousands of stars at once.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem",
                  "lineHeight": "1.6", "marginBottom": "8px"}),
        html.P([
            html.B("Types per Year / Type vs Method: "),
            "These panels show how different planet types were discovered over time and which "
            "detection methods favour which planet sizes.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem",
                  "lineHeight": "1.6", "marginBottom": "8px"}),
        html.P([
            html.B("Interaction: "),
            "Use sidebar filters (planet type, method, year range) to focus on subsets. "
            "Click legend items in the charts to toggle individual series. "
            "Hover for exact counts.",
        ], style={"color": TEXT_SECONDARY, "fontSize": "0.8rem",
                  "lineHeight": "1.6", "margin": "0"}),
    ], style={"padding": "14px 16px"})

    discovery_help = info_banner(
        "discovery-help-toggle", "discovery-help-chevron", "discovery-help-body",
        "\U0001f4c8", "HOW TO READ THIS PAGE", discovery_help_content,
        initially_open=False,
    )

    method_panel = info_banner(
        "method-explainer-toggle", "method-explainer-chevron", "method-explainer-body",
        "\U0001f4e1", "HOW ARE EXOPLANETS DISCOVERED?",
        _explanation_grid(METHOD_EXPLANATIONS, min_width="220px"),
        initially_open=False,
    )

    return tool_intro, discovery_help, method_panel
