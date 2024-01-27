# `censusdis`

![U.S. Map of Integration](https://github.com/vengroff/censusdis/raw/main/docs/_static/images/sample05.png)

[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)
![PyPI](https://img.shields.io/pypi/v/censusdis)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/censusdis)

![PyPI - Status](https://img.shields.io/pypi/status/censusdis?label=PyPI%20Status)
![PyPI - Format](https://img.shields.io/pypi/format/censusdis?label=PyPI%20Format)
![PyPI - Downloads](https://img.shields.io/pypi/dm/censusdis?label=PyPI%20Downloads)

![GitHub last commit](https://img.shields.io/github/last-commit/vengroff/censusdis)
![Tests Badge](https://github.com/vengroff/censusdis/raw/main/reports/junit/tests-badge.svg)
![Coverage Badge](https://github.com/vengroff/censusdis/raw/main/reports/coverage/coverage-badge.svg)
[![Documentation Status](https://readthedocs.org/projects/censusdis/badge/?version=latest)](https://censusdis.readthedocs.io/en/latest/?badge=latest)

censusdis is a package for discovering, loading, analyzing, and computing diversity, integration, and segregation metrics to U.S. Census demographic data. 
It is designed

- to support **every dataset**, **every geography, and every year**. It's not just about ACS data through the last time the software
was updated and released;
- to support **all geographies, on and off-spine**, not just states, counties, and census tracts;
- to have **integrated mapping capabilities** that save you time and extra coding;
- to be intuitive, Pythonic, and fast.
  
## Note:

For the full README, please visit the 
[censusdis source repository](https://github.com/vengroff/censusdis).

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

For a tutorial, please see the [censusdis-tutorial](https://github.com/vengroff/censusdis-tutorial) repository.
This tutorial was presented at [PyData Seattle 2023](https://pydata.org/seattle2023/). If you want to try it out for yourself, the README.md
contains links that let you run the tutorial notebooks live on [mybinder.org](https://mybinder.org/) in your browser without needing to set up a
local development environment or download or install any code.

### Tutorial Video

A 86 minute 
[video](https://www.youtube.com/watch?v=3vyC7ON0Tvg) 
of the tutorial as presented at 
[PyData Seattle 2023](https://pydata.org/seattle2023/)
is also available.

[![PyData Seattle Tutorial Video](https://img.youtube.com/vi/3vyC7ON0Tvg/0.jpg)](https://www.youtube.com/watch?v=3vyC7ON0Tvg)

## More Details

For the full README, lots of maps, demo notebooks, and more, please visit the 
[censusdis source repository](https://github.com/vengroff/censusdis).

