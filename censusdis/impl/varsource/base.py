# Copyright (c) 2022 Darren Erik Vengroff
"""
Abstract base class for variable sources.

The two concrete implementations are a mock
version for testing and a version that loads
from the U.S. Census API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional, Union

VintageType = Union[int, Literal["timeseries"]]
"""
The type we use to specify the vintage of a dataset.

Most datasets are organized by year, so we pass an integer
year like 2020. But some datasets are timeseries that cover
multiple years, so we specify the literal value "timeseries".
"""


class VariableSource(ABC):
    """
    A source of variables, typically used behind a :py:class:`~VariableCache`.

    The purpose of this class is to get variable and group information
    from a source, typically a remote API call to the US Census API.
    Another use case is to enable mocking for testing the rest of the
    :py:class:`~VariableCache` functionality, which is a superset of
    what this class does.
    """

    @abstractmethod
    def get(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Any]:
        """
        Get information on a variable for a given dataset in a given year.

        The return value is a dictionary with the following fields:

        .. list-table:: Title
            :widths: 25 75
            :header-rows: 0

            * - `"name"`
              - The name of the variable.
            * - '"label"`
              - A description of the variable. Within groups, hierarchies of
                variables are represented by seperating levels with `"!!"`.
            * - `"concept"`
              - The concept this variable and others in the group represent.
            * - `"group"`
              - The group the variable belongs to. To query an entire group,
                use the :py:meth:`~get_group` method.
            * - `"limit"`
              -
            * - `"attributes"`
              - A comma-separated list of variables that are attributes of this
                one.

        This dictionary is very much like the JSON returned from US Census
        API URLs like
        https://api.census.gov/data/2020/acs/acs5/variables/B03001_001E.json

        Parameters
        ----------
        dataset
            The census dataset, for example `dec/acs5` for ACS5 data
            (https://www.census.gov/data/developers/data-sets/acs-5year.html and
            https://api.census.gov/data/2020/acs/acs5.html)
            or `dec/pl` for redistricting data
            (https://www.census.gov/programs-surveys/decennial-census/about/rdo.html and
            https://api.census.gov/data/2020/dec/pl.html)
        year
            The year
        name
            The name of the variable to get information about. For example,
            `B03002_001E` is a variable from the ACS5 data set that represents
            total population in a geographic area.
        Returns
        -------
            A dictionary of information about the variable.
        """
        raise NotImplementedError("Abstract method.")

    @abstractmethod
    def get_group(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Dict]:
        """
        Get information on a group of variables for a given dataset in a given year.

        The return value is a dictionary that is very much like the JSON returned
        from US Census API URLs like
        https://api.census.gov/data/2020/acs/acs5/groups/B03002.json

        See :py:meth:`~VariableSource.get` for more details.

        Parameters
        ----------
        dataset
            The census dataset, for example `dec/acs5` for ACS5 data
            (https://www.census.gov/data/developers/data-sets/acs-5year.html and
            https://api.census.gov/data/2020/acs/acs5.html)
            or `dec/pl` for redistricting data
            (https://www.census.gov/programs-surveys/decennial-census/about/rdo.html and
            https://api.census.gov/data/2020/dec/pl.html)
        year
            The year
        name
            The name of the group to get information about. For example,
            `B03002` is a group from the ACS5 data set that contains
            variables that represent the population of various racial and
            ethnic groups in a geographic area.

        Returns
        -------
            A dictionary with a single key `"variables"`. The value
            associated with that key is a dictionary that maps from the
            names of variables in the group to dictionaries of attributes
            of the variable, in the same form as that returned for individual
            variables by the method :py:meth:`~VariableSource.get`.
        """
        raise NotImplementedError("Abstract method.")

    @abstractmethod
    def get_all_groups(self, dataset: str, year: int) -> Dict[str, List]:
        """
        Get information on a group of variables for a given dataset in a given year.

        The return value is a dictionary that is very much like the JSON returned
        from US Census API URLs like
        https://api.census.gov/data/2020/acs/acs5/groups.json

        See :py:meth:`~VariableSource.get_all_groups` for more details.

        dataset
            The census dataset, for example `dec/acs5` for ACS5 data
            (https://www.census.gov/data/developers/data-sets/acs-5year.html and
            https://api.census.gov/data/2020/acs/acs5.html)
            or `dec/pl` for redistricting data
            (https://www.census.gov/programs-surveys/decennial-census/about/rdo.html and
            https://api.census.gov/data/2020/dec/pl.html)
        year
            The year

        Returns
        -------
            A dictionary with a single key `"groups"`. The value
            associated with that key is a dictionary that maps from the
            names of groups to dictionaries of attributes
            of each group.
        """
        raise NotImplementedError("Abstract method.")

    @abstractmethod
    def get_datasets(self, year: Optional[int]) -> Dict[str, Any]:
        """
        Get descriptions of all the datasets available for a given year.

        Parameters
        ----------
        year
            The year. If `None`, get all datasets for all years.

        Returns
        -------
            A dictionary with a key "datasets". The value associated
            with that key is a dictionary that maps from the names
            of data sets to dictionaries of attributes of each data
            set.
        """
        raise NotImplementedError("Abstract method.")
