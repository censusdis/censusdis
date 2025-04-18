# censusdis

[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)
![PyPI](https://img.shields.io/pypi/v/censusdis)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/censusdis)

![PyPI - Status](https://img.shields.io/pypi/status/censusdis?label=PyPI%20Status)
![PyPI - Format](https://img.shields.io/pypi/format/censusdis?label=PyPI%20Format)
![PyPI - Downloads](https://img.shields.io/pypi/dm/censusdis?label=PyPI%20Downloads)

![GitHub last commit](https://img.shields.io/github/last-commit/censusdis/censusdis)
[![Tests Badge](../reports/junit/tests-badge.svg)](https://censusdis.github.io/censusdis/)
[![Coverage Badge](../reports/coverage/coverage-badge.svg)](https://censusdis.github.io/censusdis/)
[![Documentation Status](https://readthedocs.org/projects/censusdis/badge/?version=latest)](https://censusdis.readthedocs.io/en/latest/?badge=latest)

`censusdis` is a package for discovering, loading, analyzing, and computing diversity, integration, and segregation metrics to U.S. Census demographic data. 
It is designed

- to support **every dataset**, **every geography, and every year**. It's not just about ACS data through the last time the software
was updated and released;
- to support **all geographies, on and off-spine**, not just states, counties, and census tracts;
- to have **integrated mapping capabilities** that save you time and extra coding;
- to be intuitive, Pythonic, and fast.

Click any of the thumbnails below to see the notebook that generated it.

[<img src="../docs/_static/images/sample01.png" alt="Diversity in New Jersey" height=160>](../notebooks/ACS%20Demo.ipynb)
[<img src="../docs/_static/images/sample02.png" alt="2020 Median Income by County in Georgia" height=160>](../notebooks/Data%20With%20Geometry.ipynb)
[<img src="../docs/_static/images/sample05.png" alt="Nationwide Integration at the Census Tract over Block Group Level" height=160>](../notebooks/Nationwide%20Diversity%20and%20Integration.ipynb)
[<img src="../docs/_static/images/sample03.png" alt="White Alone Population as a Percent of County Population" height=160>](../notebooks/Seeing%20White.ipynb)
[<img src="../docs/_static/images/sample06.png" alt="Urban Census Tracts in Illinois" height=160>](../notebooks/Geographies%20Contained%20within%20Geographies.ipynb)
[<img src="../docs/_static/images/sample07.png" alt="NYC Area with Water Overlap Removed" height=160>](../notebooks/Remove%20Water.ipynb)
[<img src="../docs/_static/images/sample00.png" alt="Integration in SoMa Tracts" height=160>](../notebooks/SoMa%20DIS%20Demo.ipynb)
[<img src="../docs/_static/images/sample04.png" alt="Average Age by Public Use Microdata Area in Massachusetts" height=160>](../notebooks/PUMS%20Demo.ipynb)

## Installation and First Example

censusdis can be installed with `pip`:

```shell
pip install censusdis
```

Every censusdis query needs four things:

1. What data set we want to query.
2. What vintage, or year.
3. What variables.
4. What geographies.

Here is an example of how we can use censusdis to download data once we know
those four things.

```python
import censusdis.data as ced
from censusdis.datasets import ACS5
from censusdis import states

df_median_income = ced.download(
    # Data set: American Community Survey 5-Year
    dataset=ACS5,
    
    # Vintage: 2022
    vintage=2022, 
    
    # Variable: median household income
    download_variables=['NAME', 'B19013_001E'], 
    
    # Geography: All counties in New Jersey.
    state=states.NJ,
    county='*'
)
```

There are many more examples in the tuturial and in the sample notebooks.

## Tutorial (A Great Place to Start!)

We presented a [half-day tutorial](https://cfp.scipy.org/2024/talk/BTG9U3/) 
on `censusdis` at [SciPy '24](https://www.scipy2024.scipy.org/). All the 
material covered in the tutorial is available as in a github repo at
https://github.com/censusdis/censusdis-tutorial-2024.
The tutorial consists of a series of five lessons, 
each with worked exercises, and two choices for a final project. If you 
really want to learn the ins and outs of what `censusdis` can do, from the
most basic queries all the way through some relatively advanced topics, this
is the tutorial for you.


### An Older Tutorial

For an older tutorial that is shorter but does not include some of the newest features, 
please see the [censusdis-tutorial](https://github.com/vengroff/censusdis-tutorial) repository.
This tutorial was presented at [PyData Seattle 2023](https://pydata.org/seattle2023/). If you want to try it out for yourself, the README.md
contains links that let you run the tutorial notebooks live on [mybinder.org](https://mybinder.org/) in your browser without needing to set up a
local development environment or download or install any code.

### Tutorial Video

We expect a vireo of the [SciPy '24 tutorial](https://github.com/censusdis/censusdis-tutorial-2024) to be available soon, 
hopefully by some time in August '24.

A 86 minute 
[video](https://www.youtube.com/watch?v=3vyC7ON0Tvg) 
of the older tutorial as presented at 
[PyData Seattle 2023](https://pydata.org/seattle2023/)
is also available.

[![PyData Seattle Tutorial Video](https://img.youtube.com/vi/3vyC7ON0Tvg/0.jpg)](https://www.youtube.com/watch?v=3vyC7ON0Tvg)

## Overview 

`censusdis` is a package for discovering, loading, analyzing, and computing
diversity, integration, and segregation metrics
to U.S. Census demographic data. It is designed to be intuitive and Pythonic,
but give users access to the full collection of data and maps the US Census
publishes via their APIs. It also avoids hard-coding metadata
about U.S. Census variables, such as their names, types, and
hierarchies in groups. Instead, it queries this from the 
U.S. Census API. This allows it to operate over a large set
of datasets and years, likely including many that don't
exist as of time of this writing. It also integrates
downloading and merging the geometry of geographic 
geometries to make plotting data and derived metrics simple
and easy. Finally, it interacts with the `divintseg`
package to compute diversity and integration metrics.

The design goal of `censusdis` are discussed in more
detail in [design-goals.md](../design-goals.md).

> ### I'm not sure I get it. Show me what it can do.
> 
> The [Nationwide Diversity and Integration](../notebooks/Nationwide%20Diversity%20and%20Integration.ipynb)
> notebook demonstrates how we can download, process, and 
> plot a large amount of US Census demographic data quickly
> and easily to produce compelling results with just a few
> lines of code.

> ### I'm sold! I want to dive right in!
> 
> To get straight to installing and trying out
> code hop over to our 
> [Getting Started](https://censusdis.readthedocs.io/en/latest/intro.html)
> guide.

`censusdis` lets you quickly and easily load US Census data and make plots like 
this one:

![Median income by block group in GA](../docs/_static/images/sample02.png)

We downloaded the data behind this plot, including
the geometry of all the block groups, with a
single call:

```python
import censusdis.data as ced
from censusdis.states import STATE_GA

# This is a census variable for median household income.
# See https://api.census.gov/data/2020/acs/acs5/variables/B19013_001E.html
MEDIAN_HOUSEHOLD_INCOME_VARIABLE = "B19013_001E"

gdf_bg = ced.download(
    "acs/acs5",  # The American Community Survey 5-Year Data
    2020,
    ["NAME", MEDIAN_HOUSEHOLD_INCOME_VARIABLE],
    state=STATE_GA,
    block_group="*",
    with_geometry=True
)
```

Similarly, we can download data and geographies, do a little
analysis on our own using familiar [Pandas](https://pandas.pydata.org/)
data frame operations, and plot graphs like these

![Percent of population identifying as white by county](../docs/_static/images/sample03.png)
![Integration is SoMa](../docs/_static/images/sample00.png)

## Modules

The public modules that make up the `censusdis` package are

| Module                | Description                                                                                                   |
|-----------------------|:--------------------------------------------------------------------------------------------------------------|
| `censusdis.geography` | Code for managing geography hierarchies in which census data is organized.                                    | 
| `censusdis.data`      | Code for fetching data from the US Census API, including managing datasets, groups, and variable hierarchies. |
| `censusdis.maps`      | Code for downloading map data from the US, caching it locally, and using it to render maps.                   |
| `censusdis.states`    | Constants defining the US States. Used by the other modules.                                                  |
| `censusdis.counties`  | Constants defining counties in all of the US States.                                                          |

## Demonstration Notebooks

There are several demonstration notebooks available to illustrate how `censusdis` can
be used. They are found in the 
[notebook](https://github.com/vengroff/censusdis/tree/main/notebooks) 
directory of the source code.

The demo notebooks include

| Notebook Name                                                                                                       | Description                                                                                                                                                                          |
|---------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [ACS Comparison Profile.ipynb](../notebooks/ACS%20Comparison%20Profile.ipynb)                                       | Load and plot American Community Survey (ACS) Comparison Profile data at the state level.                                                                                            |
| [ACS Data Profile.ipynb](../notebooks/ACS%20Data%20Profile.ipynb)                                                   | Load and plot American Community Survey (ACS) Data Profile data at the state level.                                                                                                  |
| [ACS Demo.ipynb](../notebooks/ACS%20Demo.ipynb)                                                                     | Load American Community Survey (ACS) Detail Table data for New Jersey and plot diversity statewide at the census block group level.                                                  |
| [ACS Subject Table.ipynb](../notebooks/ACS%20Subject%20Table.ipynb)                                                 | Load and plot American Community Survey (ACS) Subject Table data at the state level.                                                                                                 |
| [Block Groups in CBSAs.ipynb](../notebooks/Block%20Groups%20in%20CBSAs.ipynb)                                       | Load and spatially join on-spine and off-spine geographies and plot the results on a map.                                                                                            |
| [Congressional Districts.ipynb](../notebooks/Congressional%20Districts.ipynb)                                       | Load congressional districts and tract-level data within them.                                                                                                                       |
| [Data With Geometry.ipynb](../notebooks/Data%20With%20Geometry.ipynb)                                               | Load American Community Survey (ACS) data for New Jersey and plot diversity statewide at the census block group level.                                                               |
| [Exploring Variables.ipynb](../notebooks/Exploring%20Variables.ipynb)                                               | Load metatdata on a group of variables, visualize the tree hierarchy of variables in the group, and load data from the leaves of the tree.                                           |
| [Geographies Contained within Geographies.ipynb](../notebooks/Geographies%20Contained%20within%20Geographies.ipynb) | Demonstrate working with geograhies from different hierarchies.                                                                                                                      |
| [Getting Started Examples.ipynb](../notebooks/Getting%20Started%20Examples.ipynb)                                   | Sample code from the [Getting Started](https://censusdis.readthedocs.io/en/latest/intro.html) guide.                                                                                 |                                                         |
| [Nationwide Diversity and Integration.ipynb](../notebooks/Nationwide%20Diversity%20and%20Integration.ipynb)         | Load nationwide demographic data, compute diversity and integration, and plot.                                                                                                       |
| [Map Demo.ipynb](../notebooks/Map%20Demo.ipynb)                                                                     | Demonstrate loading at plotting maps of New Jersey at different geographic granularity.                                                                                              |
| [Map Geographies.ipynb](../notebooks/Map%20Geographies.ipynb)                                                       | Illustrates a large number of different map geogpraphies and how to load them.                                                                                                       |
| [Population Change 2020-2021.ipynb](../notebooks/Population%20Change%202020-2021.ipynb)                             | Track the change in state population from 2020 to 2021 using ACS5 data.                                                                                                              |
| [PUMS Demo.ipynb](../notebooks/PUMS%20Demo.ipynb)                                                                   | Load Public-Use Microdata Samples (PUMS) data for Massachusetts and plot it.                                                                                                         |
| [Querying Available Data Sets.ipynb](../notebooks/Querying%20Available%20Data%20Sets.ipynb)                         | Query all available data sets. A starting point for moving beyond ACS.                                                                                                               |
| [Seeing White.ipynb](../notebooks/Seeing%20White.ipynb)                                                             | Load nationwide demographic data at the county level and plot of map of the US showing the percent of the population who identify as white only (no other race) at the county level. | 
| [SoMa DIS Demo.ipynb](../notebooks/SoMa%20DIS%20Demo.ipynb)                                                         | Load race and ethnicity data for two towns in Essex County, NJ and compute diversity and integration metrics.                                                                        |
| [Time Series School District Poverty.ipynb](../notebooks/Time%20Series%20School%20District%20Poverty.ipynb)         | Demonstrates how to work with time series datasets, which are a little different than vintaged data sets.                                                                            |



## Diversity and Integration Metrics

Diversity and integration metrics from the `divintseg` package are 
demonstrated in some notebooks.

For more information on these metrics
see the [divintseg](https://github.com/vengroff/divintseg/) 
project.

