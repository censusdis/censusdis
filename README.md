# censusdis

[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)

## Introduction 

`censusdis` is a package for discovering, loading, analyzing, and computing
diversity, integration, and segregation metrics
to U.S. Census demographic data. 

It can be installed in any python 3.9+ virtual environment using

```shell
pip install censusdis
```

## Modules

The modules that make up the `censusdis` package are

| Module                | Description                                                                |
|-----------------------|:---------------------------------------------------------------------------|
| `censusdis.geography` | Code for managing geography hierarchies in which census data is organized. | 
| 'censusdis.data`      | Code for fetching data from the US Census API, including managing datasets, groups, and variable hierarchies. |
| `censusdis.maps`      | Code for downloading map data from the US, caching it locally, and using it to render maps. |
| `censusdis.states`    | Constants defining the US States. Used by the three other modules. |

## Demonstration Notebooks

There are several demonstration notebooks avaialable to illustrate how `censusdis` can
be used. They are found in the 
![notebook](https://github.com/vengroff/censusdis/tree/main/notebooks) 
directory of the source code.

The notebooks include

| Notebook Name | Description |
|---------------|:------------|
| ![SoMa DIS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/SoMa%20DIS%20Demo.ipynb) | Load race and ethhicity data for two twons in Essex County, NJ and compute diversity and integration metrics. |
| ![ACS Demo.ipynb](https://github.com/vengroff/censusdis/blob/main/notebooks/ACS%20Demo.ipynb) | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level. |


## Diversity and Integration Metrics

Diversity and integration metrics from the `divintseg` package are 
demonstrated in some of the notebooks.

For more information on these metrics
see the [divintseg](https://github.com/vengroff/divintseg/) 
project.

