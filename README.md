[![Hippocratic License HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-CL-ECO-EXTR-FFD-LAW-MIL-SV&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/cl-eco-extr-ffd-law-mil-sv.html)
![PyPI](https://img.shields.io/pypi/v/censusdis)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/censusdis)

![PyPI - Status](https://img.shields.io/pypi/status/censusdis?label=PyPI%20Status)
![PyPI - Format](https://img.shields.io/pypi/format/censusdis?label=PyPI%20Format)
![PyPI - Downloads](https://img.shields.io/pypi/dw/censusdis?label=PyPI%20Downloads)

![GitHub last commit](https://img.shields.io/github/last-commit/vengroff/censusdis)
![Tests Badge](https://github.com/vengroff/censusdis/raw/main/reports/junit/tests-badge.svg)
![Coverage Badge](https://github.com/vengroff/censusdis/raw/main/reports/coverage/coverage-badge.svg)
[![Documentation Status](https://readthedocs.org/projects/censusdis/badge/?version=latest)](https://censusdis.readthedocs.io/en/latest/?badge=latest)

![U.S. Map in Black and White](https://github.com/vengroff/censusdis/raw/main/docs/_static/images/sample05.png)

## Note:

For the full README, please visit the 
[censusdis source repository](https://github.com/vengroff/censusdis).

## Introduction 

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

## Tutorial

If you are interested in a tutorial, please see the [censusdis-tutorial](https://github.com/vengroff/censusdis-tutorial) repository.
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

