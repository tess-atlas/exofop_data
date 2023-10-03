import os

import numpy as np

from typing import Dict
from tess_atlas.logger import all_logging_disabled
from tess_atlas.data.lightcurve_data.lightcurve_search import LightcurveSearch
from tess_atlas.data.exofop.constants import (
    TIC_DATASOURCE,
    TOI,
    TIC_ID,
    PLANET_COUNT,
    MULTIPLANET,
    PERIOD,
    SINGLE_TRANSIT
)
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

from tess_atlas.data.exofop.constants import LK_AVAIL, TOI_INT


def load_exofop_data() -> pd.DataFrame:
    """Load the exofop data from the online CSV file"""
    db = pd.read_csv(TIC_DATASOURCE)
    db[TOI_INT], db[PLANET_COUNT] = zip(*db[TOI].astype(str).str.split(".").map(lambda x: (int(x[0]), int(x[1]))))
    db = db.astype({TOI_INT: "int", PLANET_COUNT: "int"})
    db[MULTIPLANET] = db[TOI_INT].duplicated(keep=False)
    db[SINGLE_TRANSIT] = db[PERIOD] <= 0
    db[LK_AVAIL] = np.nan
    print(f"ExoFOP TIC database has {len(db)} entries")
    return db


def check_if_tic_has_2min_lightcurve_data(tic_id: int) -> bool:
    """Check if a TIC has lightcurve data available"""
    with all_logging_disabled():
        try:
            return LightcurveSearch(tic_id).lk_data_available
        except Exception:
            return np.nan


def get_tic_to_lk_dict(table: pd.DataFrame):
    return dict(zip(table[TIC_ID], table[LK_AVAIL]))


def update_lk_status_in_table(table: pd.DataFrame, lk_dict: Dict[int, bool], save_fname: str):
    """Update lightcurve status in the table using the provided dictionary"""
    table_lk_dict = get_tic_to_lk_dict(table)
    table_lk_dict.update(lk_dict)
    table[LK_AVAIL] = table[TIC_ID].map(table_lk_dict)
    table.to_csv(save_fname, index=False)


def update_cached_exofop_data(cached_fn: str) -> None:
    """Update the TIC cache from the exofop database"""
    new_table = load_exofop_data()

    if os.path.exists(cached_fn):
        cached_db = pd.read_csv(cached_fn)
        init_n = len(cached_db)
        print(f"Loaded cached TIC database with {init_n} entries")
    else:
        cached_db = new_table.copy()
        init_n = 0

    cached_lk_dict = get_tic_to_lk_dict(cached_db)
    new_lk_dict = get_tic_to_lk_dict(new_table)

    new_lk_dict.update(cached_lk_dict)
    update_lk_status_in_table(new_table, new_lk_dict, cached_fn)

    nan_lk_dict = {tic_id: lk for tic_id, lk in new_lk_dict.items() if np.isnan(lk)}
    num_nan = len(nan_lk_dict)

    print(f"Checking {num_nan}/{len(new_table)} TICs for lightcurve availability")
    for i, (tic_id, lk_status) in tqdm(enumerate(nan_lk_dict.items()), total=num_nan,
                                       desc="Checking TIC lightcurve availability"):
        if np.isnan(lk_status):
            nan_lk_dict[tic_id] = check_if_tic_has_2min_lightcurve_data(tic_id)
        if i % 100 == 0:  # save every 100 iterations
            update_lk_status_in_table(new_table, nan_lk_dict, cached_fn)

    update_lk_status_in_table(new_table, nan_lk_dict, cached_fn)
    print(f"Updated from {init_n} --> {len(new_table)} TICs")
    plot_lk_status(cached_fn)


def plot_lk_status(fname: str):
    """Plot if the TOI has lightcurve data using the old and new TIC caches"""
    data = pd.read_csv(fname)

    valid = data[data[LK_AVAIL] == True][TOI_INT]
    invalid = data[data[LK_AVAIL] == False][TOI_INT]
    nans = data[data[LK_AVAIL].isna()][TOI_INT]
    total = len(data)

    fig, ax = plt.subplots(figsize=(10, 2.5))

    settings = [
        ("Valid", valid, "tab:green"),
        ("Invalid", invalid, "tab:orange"),
        ("Nans", nans, "tab:red"),
    ]

    for (label, toi_set, color) in settings:
        ax.vlines(toi_set, ymin=0, ymax=2, lw=0.1, alpha=0.5, color=color,
                  label=f"{label} ({len(toi_set)}/{total} TOIs)")

    # Make legend with larger markers visible in the plot
    handles = [Line2D([0], [0], color=s[2], lw=2) for s in settings]
    labels = [f"{s[0]} ({len(s[1])})" for s in settings]

    ax.legend(handles, labels, loc="upper left", fontsize=8)
    ax.set_ylim(0.99, 1.01)
    ax.set_xlim(left=100, right=max(data[TOI_INT]))
    ax.set_yticks([])
    ax.set_xlabel("TOI Number")
    ax.set_ylabel("Cache")
    fig.suptitle("TOIs with 2-min Lightcurve data", fontsize="xx-large")
    fig.tight_layout()
    fig.savefig(fname.replace(".csv", ".png"), dpi=300)


if __name__ == "__main__":
    update_cached_exofop_data("data/exofop_data.csv")
