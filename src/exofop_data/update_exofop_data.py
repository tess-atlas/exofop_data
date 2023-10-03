import argparse

from tess_atlas.data.exofop.exofop_database import ExofopDatabase
from tess_atlas.logger import setup_logger

logger = setup_logger()

PROG = "update_tic_cache"
FNAME = "docs/exofop_data.csv"



def get_cli_args():
    parser = argparse.ArgumentParser(
        prog=PROG,
        description=(
            "Update TIC cache from ExoFOP database. "
            "NOTE: Lightkurve is queried for each TIC ID to "
            "verify that the correct data is available."
        ),
        usage=f"{PROG} [--clean]",
    )
    parser.add_argument(
        "--clean",
        action="store_true",  # False by default
        help="Update cache from scratch",
    )
    args = parser.parse_args()
    return args


def main():
    args = get_cli_args()
    logger.info(f"Updating ExoFOP data table... clean={args.clean}")
    db = ExofopDatabase(update=True, clean=args.clean, fname=FNAME)
    db.plot()
    logger.info("Update complete!")
