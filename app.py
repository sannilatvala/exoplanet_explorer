import dash
import dash_bootstrap_components as dbc

from data.loader import load_data, derive_filter_options
from components.sidebar import build_sidebar
from layout import build_layout
from callbacks import register_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:"
         "wght@300;400;600;700&family=Space+Grotesk:wght@400;600&display=swap"),
    ],
    suppress_callback_exceptions=True,
    title="Exoplanet Explorer",
)

df = load_data()
all_ptypes, all_methods, year_min, year_max = derive_filter_options(df)

sidebar = build_sidebar(all_methods, year_min, year_max)
app.layout = build_layout(sidebar)

register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
