# censusdis

[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)
![Tests Badge](reports/junit/tests-badge.svg)
![Coverage Badge](reports/coverage/coverage-badge.svg)

## Introduction 

`censusdis` is a package for discovering, loading, analyzing, and computing
diversity, integration, and segregation metrics
to U.S. Census demographic data. It is designed to be intuitive and Pythonic,
but give users access to the full collection of data and maps the US Census
publishes via their APIs. Data and maps are returned in familiar
[Pandas](https://pandas.pydata.org/)
and 
[GeoPandas](https://geopandas.org/en/stable/)
formats for easy integration with a wide variety of other Python data 
analysis, machine learning, and plotting tools.

### Data Loading

The `censusdis` data loading capabilities have been tested extensively with data from the 
[American Community Survey (ACS) 5-year data set](https://www.census.gov/data/developers/data-sets/acs-5year.html).
They also work well with other data sets available via the US Census API. 

### Maps

'censusdis' can also be used to load geographic data from the US Census
for geospatial calculations. Maps for a variety of geographic features 
as described [here](https://www.census.gov/cgi-bin/geo/shapefiles/index.php)
can be downloaded and cached locally via Python APIs instead of by manual
download from the US Census website.

Additionally, for plotting high quality maps, `censusdis` can download
cartographic boundary file data. These are available at various resolutions
and sometimes change from year to year. For example, here is what is
available from the US Census for 
[2020](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html).

### Installation and Getting Started

`censusdis` can be installed in any python 3.9+ virtual environment using

```shell
pip install censusdis
```

From there, you can download your first data with something as simple as

```python
import censusdis.data as ced

df_county_names = ced.download_detail(
    'acs/acs5',
    2020,
    ['NAME'],
    state="*",
    county="*"
)
```

This will return a dataframe of containing the names of all 3,221 counties
in the United States as of 2020.

Of course, there is far more you can do with `censusdis` than this. We encourage
you to check out the [sample notebooks](https://github.com/vengroff/censusdis/tree/main/notebooks)
provided with the project for more complete examples.

## Modules

The modules that make up the `censusdis` package are

| Module                | Description                                                                                                   |
|-----------------------|:--------------------------------------------------------------------------------------------------------------|
| `censusdis.geography` | Code for managing geography hierarchies in which census data is organized.                                    | 
| `censusdis.data`      | Code for fetching data from the US Census API, including managing datasets, groups, and variable hierarchies. |
| `censusdis.maps`      | Code for downloading map data from the US, caching it locally, and using it to render maps.                   |
| `censusdis.states`    | Constants defining the US States. Used by the three other modules.                                            |

## Demonstration Notebooks

There are several demonstration notebooks available to illustrate how `censusdis` can
be used. They are found in the 
[notebook](https://github.com/vengroff/censusdis/tree/main/notebooks) 
directory of the source code.

The notebooks include

| Notebook Name                                                                                                      | Description                                                                                                                                                                          |
|--------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [SoMa DIS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/SoMa%20DIS%20Demo.ipynb)           | Load race and ethnicity data for two towns in Essex County, NJ and compute diversity and integration metrics.                                                                        |
| [ACS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/ACS%20Demo.ipynb)                       | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level.                                                               |
| [PUMS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/PUMS%20Demo.ipynb)                     | Load Public-Use Microdata Samples (PUMS) data for Massachusetts and plot it.                                                                                                         |
| [Seeing White.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Seeing%20White.ipynb)               | Load nationwide demographic data at the county level and plot of map of the US showing the percent of the population who identify as white only (no other race) at the county level. | 
| [Map Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Map%20Demo.ipynb)                       | Demonstrate loading at plotting maps of New Jersey at different geographic granularity.                                                                                              |
| [Exploring Variables.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/Exploring%20Variables.ipynb) | Load metatdata on a group of variables, visualize the tree hierarchy of variables in the group, and load data from the leaves of the tree.                                           |


## Diversity and Integration Metrics

Diversity and integration metrics from the `divintseg` package are 
demonstrated in some notebooks.

For more information on these metrics
see the [divintseg](https://github.com/vengroff/divintseg/) 
project.

