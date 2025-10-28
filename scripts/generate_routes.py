#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script that downloads routes using openrouteservice API."""

import argparse
import json
import logging
import shutil

import openrouteservice as ors

from advanced_geoscripting.scripts.utils import load_config
from advanced_geoscripting.scripts.filepaths import FilePaths

config_path = "advanced_geoscripting/config.yml"

def download_routes(config, filepaths):
    """Download routes from openrouteservice API and save them to a file."""

    # This code snippet shows how to request a route from the OpenRouteService API
    headers = {
        "headers": {
            "Accept": "application/json, application/geo+json, "
            "application/gpx+xml, img/png; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8",
        }
    }

    client = ors.Client(base_url=config["ors_url"])

    start_coordinate = [8.687119006209203, 49.418902395440135]
    destination_coordinate = [8.683683615325759, 49.38768076265261]

    profile = "foot-walking"
    parameters = {
        "coordinates": [start_coordinate, destination_coordinate],
        "instructions": "false",
        "preference": "recommended",
        "extra_info": ["csv"],
        "elevation": "true",
        "continue_straight": "true",
        "options": {
            "avoid_features": ["ferries"],
            "profile_params": {"weightings": {"csv_factor": 1, "csv_column": "noon"}},
        },
    }

    ors_response = client.request(
        url=f"v2/directions/{profile}/geojson",
        post_json=parameters,
        requests_kwargs=headers,
    )
    print(ors_response)
    with open(filepaths.ROUTES_DIR / "route_1.geojson", "w") as f:
        json.dump(ors_response, f)


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
    filepaths = FilePaths(config["output_dir"], config["run_name"])
    filepaths.create_dirs()
    logging.info(f"Successfully created output directories in {filepaths.OUTPUT_DIR}")

    # Copy config file to output directory
    shutil.copy(args.config, filepaths.OUTPUT_DIR)

    download_routes(config, filepaths)

