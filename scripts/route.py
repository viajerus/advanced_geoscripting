import json
from pathlib import Path

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import pyproj
from shapely.geometry import LineString

from scripts.line import Line


class Route(Line):
    json_response = None
    crs = "epsg:4326"

    def __init__(self, file_path: str):
        """
        Initializes the Route object with a file path to a GeoJSON file.
        Loads the route data from the specified file.
        Extracts route id, destination, and time of day from the file name.

        :param file_path: Path to the GeoJSON file containing route data
        """
        self.file_path = Path(file_path)
        self.extract_coordinates()
        self.convert_coordinates()
        self.extract_metadata()

    def load_file(self):
        """
        Loads the GeoJSON file and returns the JSON response.
        """
        with open(self.file_path) as src:
            self.json_response = json.load(src)

    def extract_coordinates(self):
        """
        Loads route from file
        """
        if self.json_response is None:
            self.load_file()
        self.coordinates = self.json_response["features"][0]["geometry"]["coordinates"]

    def extract_metadata(self):
        """
        Extracts metadata from the file name.
        """
        self.filename = self.file_path.stem
        name_parts = self.filename.split("_")
        self.route_id = name_parts[1]
        self.time_of_day = name_parts[2]
        self.type_route = name_parts[3]

    def convert_coordinates(self):
        """Converts coordinates from WGS84 to UTM Zone 32N."""
        """
        Converts a list of coordinates from WGS84 to UTM Zone 32N.
        :param coordinates: list of tuples [(lon, lat), ...]
        :return: list of tuples [(x, y, z), ...] in UTM Zone 32N
        """
        if self.crs == "epsg:4326":
            transformer = pyproj.Transformer.from_crs(
                "epsg:4326", "epsg:32632", always_xy=False
            )
            self.coordinates = [
                transformer.transform(lat, lon, z) for lon, lat, z in self.coordinates
            ]
            self.crs = "epsg:32632"
        else:
            transformer = pyproj.Transformer.from_crs(
                "epsg:32632", "epsg:4326", always_xy=False
            )
            self.coordinates = [
                transformer.transform(lat, lon, z) for lon, lat, z in self.coordinates
            ]
            self.crs = "epsg:4326"

    def as_dataframe(self):
        return gpd.GeoDataFrame(
            geometry=[LineString(self.coordinates)], crs="EPSG:4326"
        )

    def plot(self):
        """
        Plots the route on a map using GeoPandas and adds a basemap with contextily.
        """
        gdf = self.as_dataframe()
        gdf_webmerc = gdf.to_crs(epsg=3857)
        ax = gdf_webmerc.plot(figsize=(10, 6), color="blue", linewidth=2)
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.PositronNoLabels)
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.PositronOnlyLabels)
        ax.set_title("Route Plot")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    def explore(self):
        """
        Plots the route on a map using GeoPandas and adds a basemap with contextily.
        """
        gdf = self.as_dataframe()
        gdf.explore()

    @property
    def extras(self):
        """
        Returns the extra information of the route
        :return:
        """
        try:
            return self.json_response["features"][0]["properties"]["extras"]
        except Exception:
            return None

    def file_name(self):
        if self.filename is not None:
            fn = f"route_{self.route_id}_{self.time_of_day}_{self.type_route}"
            return fn
        else:
            return None

    def summary_criterion(self, criterion):
        """
        Returns the summary for a certain criterion of the ORS response as
        a pandas dataframe
        :param criterion: Criterion from ORS, e.g. 'csv', 'green',
        'noise' or 'steepness'
        :return: Dataframe with summary
        """
        if criterion in self.extras.keys():
            return pd.DataFrame(self.extras[criterion]["summary"])
        else:
            raise ValueError("criterion '%s' does not exist.")

    def solar_exposure(self):
        """
        Returns the overall exposure to solar radiation of the route
        :return: solar exposure/shadow
        """
        summary = self.summary_criterion("csv")
        return sum(summary["value"] * summary["distance"]) / summary["distance"].sum()
