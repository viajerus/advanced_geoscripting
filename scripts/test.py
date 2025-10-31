import geopandas as gpd
from shapely.geometry import box
from spatial import RandomPoints

#test if the polygon crs is set to 4326

def test_polygon_crs_is_4326():
    heidelberg_bbox = (8.598690, 49.339503, 8.755589, 49.456632)
    polygon = box(*heidelberg_bbox)
    heidelberg_polygon_gs = gpd.GeoSeries(polygon, crs="EPSG:3857")
    rp = RandomPoints(heidelberg_polygon_gs)

    assert rp.polygon.crs.to_string() == "EPSG:4326"

#test if the desired amount of random points is created

def test_random_points_count():
    heidelberg_bbox = (8.598690, 49.339503, 8.755589, 49.456632)
    polygon = box(*heidelberg_bbox)
    heidelberg_polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    rp = RandomPoints(heidelberg_polygon_gdf)
    rp.random_points(50)

    assert len(rp.pnts_in_poly) == 50

#test if the random points are within the geometry

def test_random_points_within_polygon():
    heidelberg_bbox = (8.598690, 49.339503, 8.755589, 49.456632)
    polygon = box(*heidelberg_bbox)
    heidelberg_polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    rp = RandomPoints(heidelberg_polygon_gdf)
    rp.random_points(50)

    for point in rp.pnts_in_poly.geometry:
        assert heidelberg_polygon_gdf.contains(point).any()

#test if the required columns are there
def test_sample_df_columns():
    heidelberg_bbox = (8.598690, 49.339503, 8.755589, 49.456632)
    polygon = box(*heidelberg_bbox)
    heidelberg_polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    rp = RandomPoints(heidelberg_polygon_gdf)
    rp.random_points(300)
    rp.sample_df()
    expected_columns = {"lon", "lat", "lon2", "lat2", "id"}

    assert set(rp.df1_tail.columns) == expected_columns

#test if the function does not return negative values
def test_compute_distance_non_negative():
    heidelberg_bbox = (8.598690, 49.339503, 8.755589, 49.456632)
    polygon = box(*heidelberg_bbox)
    heidelberg_polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    rp = RandomPoints(heidelberg_polygon_gdf)
    rp.random_points(300)
    rp.sample_df()
    df_distances = rp.compute_distance()

    assert (df_distances["distance_km"] >= 0).all()
