# Copyright (c) 2022 Darren Erik Vengroff
"""
A variable source that loads metadata about variables from the U.S. Census API.
"""

from typing import Any, Dict, List, Optional

from censusdis.impl.fetch import json_from_url
from censusdis.impl.varsource.base import VariableSource


class CensusApiVariableSource(VariableSource):
    """
    A :py:class:`~VariableSource` that gets data from the US Census remote API.

    Users will rarely if ever need to explicitly construct objects
    of this class. There is one behind the singleton cache
    `censusdis.censusdata.variables`.
    """

    @staticmethod
    def _url_part(dataset: str, year: int):
        if not isinstance(year, int):
            return f"{dataset}"

        return f"{year}/{dataset}"

    @staticmethod
    def variables_url(dataset: str, year: int, response_format: str = "json") -> str:
        """
        Construct the URL to fetch metadata about all variables.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        response_format
            The desired format of the response. Either `json` (the default)
            or `html`.

        Returns
        -------
            The URL to fetch the metadata from.

        """
        return (
            f"https://api.census.gov/data/{CensusApiVariableSource._url_part(dataset, year)}/"
            f"variables.{response_format}"
        )

    @staticmethod
    def url(dataset: str, year: int, name: str, response_format: str = "json") -> str:
        """
        Construct the URL to fetch metadata about a variable.

        This is where we fetch metadata that is then put into the
        local cache.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the variable.
        response_format
            The desired format of the response. Either `json` (the default)
            or `html`.

        Returns
        -------
            The URL to fetch the metadata from.
        """
        return (
            f"https://api.census.gov/data/{CensusApiVariableSource._url_part(dataset, year)}/"
            f"variables/{name}.{response_format}"
        )

    @staticmethod
    def group_url(
        dataset: str,
        year: int,
        group_name: Optional[str] = None,
    ) -> str:
        """
        Get the URL to fetch metadata about a group of variables.

        This can either be all the variables in a dataset, if a group
        name is not specified, or just the variables in a particular
        group if the data set has groups.

        Some datasets, `dec/pl` dataset for example, do not have
        groups, so a group name need not be passed. Others, like
        `acs/acs5` have groups, so a group name such as `B01001`
        will normally be passed in.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        group_name
            The name of the group, or `None` if the dataset has no
            groups.

        Returns
        -------
            The URL to fetch the metadata from.
        """

        if group_name is None:
            return f"https://api.census.gov/data/{CensusApiVariableSource._url_part(dataset, year)}/variables.json"

        return (
            f"https://api.census.gov/data/{CensusApiVariableSource._url_part(dataset, year)}/"
            f"groups/{group_name}.json"
        )

    @staticmethod
    def all_groups_url(dataset: str, year: int) -> str:
        """
        Get the URL to fetch the names of all groups.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year

        Returns
        -------
            The URL to fetch the metadata from.
        """
        return f"https://api.census.gov/data/{CensusApiVariableSource._url_part(dataset, year)}/groups.json"

    def get(self, dataset: str, year: int, name: str) -> Dict[str, Any]:
        url = self.url(dataset, year, name)
        value = json_from_url(url)

        return value

    def get_group(
        self, dataset: str, year: int, name: Optional[str]
    ) -> Dict[str, Dict]:
        url = self.group_url(dataset, year, name)
        value = json_from_url(url)

        # Filter out psuedo-variables like 'for' and 'in'.
        value["variables"] = {
            k: v
            for k, v in value["variables"].items()
            if k not in ["in", "for", "ucgid"]
        }

        # Put the name into the nested dictionaries, so it looks the same is if
        # we had gotten it via the variable API even though that API leaves it out.
        for k, val in value["variables"].items():
            val["name"] = k

        return value

    def get_all_groups(self, dataset: str, year: int) -> Dict[str, List]:
        url = self.all_groups_url(dataset, year)
        value = json_from_url(url)

        return value

    def get_datasets(self, year: Optional[int]) -> Dict[str, Any]:
        if year is not None:
            url = f"https://api.census.gov/data/{year}.json"
        else:
            url = "https://api.census.gov/data.json"

        json = json_from_url(url)

        return json
