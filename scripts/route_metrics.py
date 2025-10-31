#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate metrics of routes"""

from scripts.utils import load_config
from scripts.filepaths import FilePaths, ResultPaths
import argparse
import logging
from pathlib import Path
from scripts.route import Route
import pandas as pd


def calculate_route_metrics(filepaths: FilePaths, filepaths_res: ResultPaths) -> None:
    """
    Calculate metrics of routes
    :param filepaths: File paths for input and output files and directories
    :return: None
    """

    directory = filepaths.ROUTES_DIR

    desktop = Path(directory)

    dataframes = []

    for i in desktop.glob("*.geojson"):
        route = Route(i)
        r = route.file_name()
        df = route.summary_criterion("csv")
        s_exp = route.solar_exposure()
        df["s_exp"] = s_exp
        df["source"] = r
        dataframes.append(df)

    df_all = pd.concat(dataframes)

    df_all.to_parquet(filepaths_res.CSV_RESULTS_DIR / "all.parquet")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Starting route metrics calculation...")

    # Get command line arguments
    parser = argparse.ArgumentParser(description="Calculate metrics of routes.")
    parser.add_argument("--config", type=str, required=True, help="Config file as YAML")
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    logging.info(f"Successfully read config file: {args.config}")

    # Create output directories
    filepaths_res = ResultPaths(config["output_dir_metrics"], config["run_name"])
    filepaths_res.create_dirs()
    logging.info(
        f"Successfully created output directories in {filepaths_res.OUTPUT_DIR}"
    )

    filepaths = FilePaths(config["output_dir"], config["run_name"])

    # Calculates the metrics for the routes. Output file is one parquet file.

    calculate_route_metrics(filepaths, filepaths_res)

    logging.info("Successfully calculated parquet file with metrics")
