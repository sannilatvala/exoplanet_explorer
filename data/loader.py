import os
import warnings
import pandas as pd

from utils.constants import CAT_ORDER, THRESHOLD

warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data", "planets_clean.csv")

_EMPTY_COLUMNS = [
    "pl_rade", "pl_orbsmax", "pl_eqt", "pl_type",
    "discoverymethod", "discoverymethod_mapped", "disc_year",
    "st_mass", "st_rad", "sy_dist", "pl_name", "hostname",
]


def load_data(path=DATA_PATH):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"Data file not found at {path}. Using empty DataFrame.")
        return pd.DataFrame(columns=_EMPTY_COLUMNS)

    if "pl_type" in df.columns:
        df["pl_type"] = pd.Categorical(df["pl_type"], categories=CAT_ORDER)
    else:
        df["pl_type"] = "Unknown"

    if "discoverymethod" in df.columns:
        totals = df.groupby("discoverymethod", observed=True).size()
        fracs = totals / totals.sum()
        df["discoverymethod_mapped"] = df["discoverymethod"].apply(
            lambda m: m if fracs.get(m, 0) >= THRESHOLD else "Other"
        )
    else:
        df["discoverymethod_mapped"] = "Unknown"

    if "disc_year" in df.columns:
        df["disc_year"] = pd.to_numeric(df["disc_year"], errors="coerce")

    print(f"Loaded {len(df):,} planets from {path}")
    return df


def derive_filter_options(df):
    ps = df.get("pl_type", pd.Series(dtype="object"))
    all_ptypes = (
        [t for t in CAT_ORDER if t in ps.cat.categories]
        if hasattr(ps, "cat") else CAT_ORDER
    )
    all_methods = (
        sorted(df["discoverymethod_mapped"].dropna().unique().tolist())
        if "discoverymethod_mapped" in df.columns else []
    )
    year_min = (
        int(df["disc_year"].min())
        if "disc_year" in df.columns and df["disc_year"].notna().any() else 1990
    )
    year_max = (
        int(df["disc_year"].max())
        if "disc_year" in df.columns and df["disc_year"].notna().any() else 2024
    )
    return all_ptypes, all_methods, year_min, year_max
