PTYPE_COLORS = {
    "Gas Giant":   "#4C72B0",
    "Neptunian":   "#55A868",
    "Super-Earth": "#DD8452",
    "Terrestrial": "#C44E52",
}

DMETHOD_COLORS = {
    "Transit":                       "#17BECF",
    "Radial Velocity":               "#E377C2",
    "Microlensing":                  "#BCBD22",
    "Imaging":                       "#9467BD",
    "Other":                         "#7F7F7F",
    "Pulsar Timing":                 "#9467bd",
    "Pulsation Timing Variations":   "#8c564b",
    "Eclipse Timing Variations":     "#e377c2",
    "Orbital Brightness Modulation": "#7f7f7f",
    "Transit Timing Variations":     "#bcbd22",
    "Astrometry":                    "#17becf",
    "Disk Kinematics":               "#aec7e8",
}

CAT_ORDER = ["Terrestrial", "Super-Earth", "Neptunian", "Gas Giant"]
THRESHOLD = 0.01

X_MIN_LOG = -3
X_MAX_LOG =  2
Y_MIN_LOG = -0.5
Y_MAX_LOG =  2.3

EARTH_DIST   = 1.0
EARTH_RADIUS = 1.0
EARTH_EQT    = 255.0
EARTH_COLOR  = "#39ff14"

DARK_BG        = "#0b0e1a"
PANEL_BG       = "#111827"
CARD_BG        = "#161d2e"
BORDER_COLOR   = "#1f2d45"
TEXT_PRIMARY   = "#e8eaf6"
TEXT_SECONDARY = "#8b9dc3"
ACCENT         = "#4fd1c5"
PLOT_TEMPLATE  = "plotly_dark"

LAYOUT_BASE = dict(
    template=PLOT_TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'IBM Plex Mono', monospace", color=TEXT_PRIMARY, size=11),
    margin=dict(l=60, r=20, t=45, b=55),
)

PTYPE_EXPLANATIONS = [
    ("Terrestrial", "#C44E52",
     "Small rocky worlds like Earth or Mars. Less than 1.5\u00d7 Earth\u2019s "
     "radius. Could potentially host liquid water and life."),
    ("Super-Earth", "#DD8452",
     "Larger rocky planets with no equivalent in our solar system. Between 1.5 "
     "and 2.5\u00d7 Earth\u2019s radius. May have thick atmospheres or deep oceans."),
    ("Neptunian",   "#55A868",
     "Ice-giant class planets similar to Uranus or Neptune. Between 2.5 and 6\u00d7 "
     "Earth\u2019s radius. Likely rich in water, methane, and ammonia ice."),
    ("Gas Giant",   "#4C72B0",
     "Massive gas-dominated planets like Jupiter and Saturn. Larger than 6\u00d7 "
     "Earth\u2019s radius. Mostly hydrogen and helium; many orbit very close to their star."),
]

METHOD_EXPLANATIONS = [
    ("Transit", "#17BECF",
     "A planet passes in front of its star, dimming it slightly. "
     "Kepler & TESS use this — it’s why most known exoplanets were found this way."),
    ("Radial Velocity", "#E377C2",
     "A planet’s gravity makes its star wobble toward and away from us. "
     "Detected as a Doppler shift — like a passing siren."),
    ("Microlensing", "#BCBD22",
     "A planet bends and briefly amplifies background starlight via gravity. "
     "Great for finding distant planets invisible by other means."),
    ("Imaging", "#9467BD",
     "The planet is photographed directly — very rare, since planets are "
     "billions of times fainter than their host stars."),
    ("Other", "#7F7F7F",
     "Rarer techniques: Pulsar Timing, Transit Timing Variations, "
     "Astrometry, Eclipse Timing Variations, and Orbital Brightness Modulation."),
]