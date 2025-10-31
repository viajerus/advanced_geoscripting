#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script that downloads routes using openrouteservice API."""

import argparse
import json
import logging
import shutil
from tqdm import tqdm
import time
import json

import openrouteservice as ors

import os

print(os.getcwd())

from scripts.utils import load_config
from scripts.filepaths import FilePaths
from scripts.spatial import RandomPoints
from itertools import product
import geopandas as gpd



def download_routes(df, config, filepaths, list_times, max_routes_per_i, max_total_requests=500):
    """Download routes from OpenRouteService API and save them to a file."""

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }

    parameters = {
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

    err_iso = []

    client = ors.Client(base_url=config["ors_url"])

    total_requests = 0

    list_modes = ["shortest", "recommended"]

    from tqdm import tqdm
    import time, json

    if max_routes_per_i <= 100:
        # Take the first n rows once
        selected_df = df.head(max_routes_per_i)

        for i in tqdm(list_times, desc="Times loop", leave=False):
            for row in selected_df.itertuples(index=False):
                for j in list_modes:
                    if total_requests >= max_total_requests:
                        print(f"Reached maximum total requests: {max_total_requests}")
                        break

                    try:
                        parameters['coordinates'] = [[row.lon, row.lat], [row.lon2, row.lat2]]
                        parameters['preference'] = j
                        parameters["options"]["profile_params"]["weightings"]["csv_column"] = i

                        ors_response = client.request(
                            url="v2/directions/foot-walking/geojson",
                            post_json=parameters,
                            requests_kwargs={"headers": headers},
                        )

                        out_path = filepaths.ROUTES_DIR / f"route_{row.id}_{i}_{j}.geojson"
                        with open(out_path, "w") as f:
                            json.dump(ors_response, f)

                    except Exception as e:
                        print(f"Error for row {row.id} at time {i}: {e}")
                        err_iso.append(row)

                    finally:
                        total_requests += 1
                        time.sleep(0.1)

                if total_requests >= max_total_requests:
                    print(f"Reached maximum total requests: {max_total_requests}")
                    break
    else:
        print("error")


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


    # Extract list times from config file
    list_times = config['times_of_day']

    #Extract max of routes per times of day
    max_routes_per_i = config['number_of_routes_per_time_of_day']

    #Extract input Geodataframe (boundaries of HD)
    gdf = gpd.read_file(config["input_gdf"])

    #Calculates the amount of random points for the AOI.
    rp = RandomPoints(gdf)
    rp.random_points(config["random_points"])
    rp.sample_df()
    #Returns a Geodatframe with max. 100 routes
    out_df = rp.compute_distance()
    #Creates and stores the routes.
    download_routes(out_df, config, filepaths, list_times, max_routes_per_i)

    logging.info(f"Successfully calculated and stores the routes")

