from advanced_geoscripting.scripts.spatial import RandomPoints

import geopandas as gpd

gdf = gpd.read_file("../geodata/hd.geojson")

rp = RandomPoints(gdf)
rp.random_points(400)
rp.sample_df()

out_df = rp.compute_distance()

print(out_df)


