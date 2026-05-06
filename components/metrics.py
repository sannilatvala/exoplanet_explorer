from dash import html
from utils.constants import CARD_BG, BORDER_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT


def stat_card(label, value, subtitle, icon="●"):
    return html.Div([
        html.Div(icon, style={"fontSize": "1.3rem", "color": ACCENT, "marginBottom": "3px"}),
        html.Div(value, style={
            "fontSize": "1.45rem", "fontWeight": "700",
            "color": TEXT_PRIMARY, "fontFamily": "'IBM Plex Mono', monospace",
        }),
        html.Div(label, style={
            "fontSize": "0.68rem", "color": TEXT_SECONDARY,
            "textTransform": "uppercase", "letterSpacing": "0.1em", "marginTop": "2px",
        }),
        html.Div(subtitle, style={
            "fontSize": "0.64rem", "color": "rgba(139,157,195,0.65)",
            "marginTop": "3px", "lineHeight": "1.3",
        }),
    ], style={
        "background": CARD_BG, "border": f"1px solid {BORDER_COLOR}",
        "borderRadius": "10px", "padding": "14px 16px",
        "flex": "1", "minWidth": "120px", "textAlign": "center",
    })


def build_stats_strip(fdf):
    n_planets = len(fdf)
    n_stars   = fdf["hostname"].nunique() if "hostname" in fdf.columns else None
    med_rad   = (fdf["pl_rade"].median()
                 if "pl_rade" in fdf.columns and fdf["pl_rade"].notna().any() else None)
    med_dist  = (fdf["pl_orbsmax"].median()
                 if "pl_orbsmax" in fdf.columns and fdf["pl_orbsmax"].notna().any() else None)
    med_temp  = (fdf["pl_eqt"].dropna().median()
                 if "pl_eqt" in fdf.columns and fdf["pl_eqt"].notna().any() else None)

    return [
        stat_card("Planets",      f"{n_planets:,}",
                  "confirmed exoplanets", "\U0001fa90"),
        stat_card("Host Stars",
                  f"{n_stars:,}" if n_stars is not None else "\u2014",
                  "stars hosting planets", "\u2b50"),
        stat_card("Median Radius",
                  f"{med_rad:.1f} R\u2295" if med_rad else "\u2014",
                  "in Earth radii (R\u2295 = 6,371 km)", "\U0001f4cf"),
        stat_card("Median Dist",
                  f"{med_dist:.3g} AU" if med_dist else "\u2014",
                  "in AU (1 AU = Earth\u2013Sun distance)", "\U0001f4e1"),
        stat_card(
            "Median Temp",
            (f"{med_temp:.0f} K"
            if med_temp else "\u2014"),
            "average planet temperature",
            "\U0001f321\ufe0f"
        ),
    ]
