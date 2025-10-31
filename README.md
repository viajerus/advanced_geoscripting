# Advanced Geoscripting 

## Final Project

## Description

This final project downloads, creates and analyzes routes created with the ORS-HEAL instance.

## Data

You will generate most of the data. The [geometry](geodata/hd.geojson) of Heidelberg is stored as a geojson and must be passed in the [config](config/config.yml) file. 

### Dependencies

I am working with the latest mamba version to manage the packages. 

[YAML File](config/adv_geo.yaml)

```
mamba create -f adv_geo.yaml
```

After creating the mamba environment, activate it and clone this repository. Access the repository once it has been cloned. 


### Executing the scripts

The first script is [generate_routes.py](scripts/generate_routes.py). The script will create n routes, depending on the variables you have set in the config file. We will begin with 500 random points and 40 routes per time of day. 

Execute the script with the following command: 

```
python3 -m scripts.route_metrics --config ./config/config.yml
```
We use the flag -m to avoid conflict with the import of the modules. 

This first step should not last more than one minute. 

The second script, [route_metrics.py](scripts/route_metrics.py), will create a parquet file, where the metrics for all the routes are stored. 

Finally, we will analyze the parquet file we have created before in [this](results/visualization.ipynb) notebook. No paths have to be changed during the execution of the code blocks. 


## Authors

Daniel Abanto // abanto@stud.uni-heidelberg.de



