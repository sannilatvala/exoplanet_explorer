# Exoplanet Explorer

An interactive dark-theme dashboard for exploring thousands of confirmed exoplanets. Built with Dash and Plotly.

🌐 **Live App:** https://exoplanet-explorer-uzh9.onrender.com

## Features

- **Scatter & Density tab**: Orbital distance vs planet radius, coloured by equilibrium temperature (Plasma scale), with a 2D density contour view
- **Discovery Charts tab**: Method timeline, share pie, types-per-year, and type-vs-method breakdowns
- **Sidebar filters**: Filter by planet type, discovery method, and year range; toggle Earth reference and unknown-temperature points
- **5 stat cards**: Confirmed planets, host stars, median radius, median distance, median temperature

## Local Setup

Follow these steps to run the dashboard locally on your machine.

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

Open your browser at: [http://127.0.0.1:8050](http://127.0.0.1:8050)

## Project Structure

```
exoplanet_explorer/
├── app.py                        # Entry point
├── layout.py                     # Top-level layout
├── callbacks.py                  # All Dash callbacks
├── data/
│   └── loader.py                 # Data loading and preprocessing
├── components/
│   ├── scatter.py                # Scatter plot figure
│   ├── hexbin.py                 # Density contour figure
│   ├── discovery.py              # Discovery chart figures
│   ├── sidebar.py                # Sidebar UI
│   ├── metrics.py                # Stat strip cards
│   └── info_sections.py          # Collapsible info panels
├── utils/
│   ├── constants.py              # Colors, mappings, axis bounds
│   └── helpers.py                # Shared layout/axis helpers, filtering
├── assets/
│   └── styles.css                # Global CSS overrides
│   └── tooltip_portal.js         # Custom tooltip
└── requirements.txt
```
