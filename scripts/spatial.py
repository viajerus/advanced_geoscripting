#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script that creates random points within a given polygon"""

import numpy as np
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from numpy import cos, sin, arcsin, sqrt
from math import radians


class RandomPoints:
    """Class that creates random points within a given polygon"""
    def __init__(self, polygon):
        self.polygon = polygon

    def random_points(self, number:int):
        minx, miny, maxx, maxy = self.polygon.total_bounds
        x = np.random.uniform(minx, maxx, number)
        y = np.random.uniform(miny, maxy, number)

        self.polygon = self.polygon.set_crs("EPSG:4326")
        self.polygon['poly'] = 'poly'
        self.polygon.set_index('poly', inplace=True)

        df = pd.DataFrame()

        df['points'] = list(zip(x, y))
        df['points'] = df['points'].apply(Point)
        gdf_points = gpd.GeoDataFrame(df, geometry='points')

        gdf_points = gdf_points.set_crs("EPSG:4326")

        Sjoin = gpd.tools.sjoin(gdf_points, self.polygon, predicate="within", how='left')

        self.pnts_in_poly = gdf_points[Sjoin.poly == 'poly']



    def sample_df(self):
        self.pnts_in_poly.loc[:, 'lon'] = self.pnts_in_poly.geometry.x
        self.pnts_in_poly.loc[:, 'lat'] = self.pnts_in_poly.geometry.y
        del self.pnts_in_poly['points']
        df1 = self.pnts_in_poly.iloc[:200].copy()

        df2 = self.pnts_in_poly.iloc[-100:].reset_index(drop=True)

        df1_tail = df1.iloc[-100:].reset_index(drop=True)

        # now attach lon2 and lat2
        df1_tail['lon2'] = df2['lon']
        df1_tail['lat2'] = df2['lat']

        self.df1_tail = df1_tail

    def compute_distance(self):
        """Computes haversine distance between (lon, lat) and (lon2, lat2)"""

        def haversine(row):
            lon1, lat1, lon2, lat2 = map(radians, [row['lon'], row['lat'], row['lon2'], row['lat2']])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * arcsin(sqrt(a))
            km = 6367 * c
            return km

        self.df1_tail['distance_km'] = self.df1_tail.apply(haversine, axis=1)
        return self.df1_tail























