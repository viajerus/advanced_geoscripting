#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate metrics of routes"""
import argparse
import logging
import shutil

from advanced_geoscripting.scripts.utils import load_config
from advanced_geoscripting.scripts.filepaths import FilePaths
from pathlib import Path
from advanced_geoscripting.scripts.route import Route




def calculate_route_metrics(config: dict, filepaths: FilePaths):
    """
    Calculate metrics of routes
    :param config: Dictionary containing configuration parameters
    :param filepaths: File paths for input and output files and directories
    :return: None
    """
    f = Path(__file__).parent / Path("../data/run_v1/01_raw/01_routes/route_0_noon.geojson")

    route = Route(f)

    #df = route.as_dataframe()

    #route.plot()

    #route.explore()

    df = route.summary_criterion('csv')

    print(df)







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
    filepaths = FilePaths(config["output_dir_metrics"], config["run_name"])
    filepaths.create_dirs()
    print(filepaths.OUTPUT_DIR)
    logging.info(f"Successfully created output directories in {filepaths.OUTPUT_DIR}")


    calculate_route_metrics(config, filepaths)
