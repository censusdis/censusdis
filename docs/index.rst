.. censusdis documentation master file, created by
   sphinx-quickstart on Mon Sep  5 15:32:12 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``censusdis``
=============

`censusdis` is a package for loading demographic data
from the
`US Census API <https://www.census.gov/data/developers/guidance/api-user-guide.html>`_
and maps from the
`US Census TIGER/Line Geodatabases <https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-geodatabase-file.2020.html>`_
and
`US Census Cartographic Boundary Files <https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html>`_.
It attempts to provide access to these resources in a
simple and easy to use Pythonic manner.

The related
`divintseg <https://github.com/vengroff/divintseg>`__
project provides utilities for computing diversity,
integration, and segregation metrics from US Census and
other data.

.. _installation:

Installation
------------

Installation follows the typical model for Python::

    pip install censusdis

will install the package in your python environment.

If you are using a tool like `conda <https://docs.conda.io/en/latest/>`_
or `poetry <https://python-poetry.org/>`_ to manage
your dependencies, then you can add ``censusdis`` the
same way you would add any other dependency.

Sample Notebooks
----------------

If you would like to see some examples
of what this package can do, there are a number of `demo
notebooks <./notebooks.html>`_.

.. toctree::
   :maxdepth: 2
   :hidden:

   intro.rst
   notebooks.rst
   api.rst

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
