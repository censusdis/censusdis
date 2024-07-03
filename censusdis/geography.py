# Copyright (c) 2022 Darren Erik Vengroff
"""Utilities for managing hierarchies of geographies."""

import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    DefaultDict,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import requests

from .impl.exceptions import CensusApiException
from .impl.fetch import certificates


InSpecType = Union[str, Iterable[str]]


class GeoException(CensusApiException):
    """An exception raised by the `censusdis.geography` module."""


class PathSpec:
    """
    A path specification.

    This class is used to represent a path of allowable geographies,
    such as state, county, census tract.
    """

    # We hide this object inside the class to make __init__
    # effectively private. If you don't have access to this
    # key you can't successfully call __init___.
    __init_key = object()

    def __init__(self, path: Iterable[str], init_key: Optional[Any] = None):
        if init_key is not PathSpec.__init_key:
            raise ValueError(
                "CanonicalGeographies cannot be created directly. "
                "Try `PathSpec.partial_matches(**kwargs)` or "
                "`PathSpec.full_match(**kwargs) instead."
            )

        self._path = list(path)

    def __str__(self):
        """Convert to a string."""
        return ":".join(self._path)

    def __repr__(self):
        """Generate a representation."""
        quoted_path = (f'"{c}"' for c in self._path)
        return f"PathSpec([{', '.join(quoted_path)}])"

    def __len__(self):
        """How many components are in the path."""
        return len(self._path)

    @property
    def path(self):
        """The path."""
        return self._path

    @staticmethod
    def _u2s(**kwargs):
        return {k.replace("_", " "): v for k, v in kwargs.items()}

    def _partial_match(
        self,
        is_prefix: bool = True,
        **kwargs: InSpecType,
    ) -> bool:
        kwargs = self._u2s(**kwargs)
        path_elements_in_kwargs = [key for key in self._path if key in kwargs]
        keys_from_kwargs = list(kwargs)

        match = (len(path_elements_in_kwargs) > 0) and (
            path_elements_in_kwargs == keys_from_kwargs
        )

        if is_prefix:
            return match and path_elements_in_kwargs[0] == self._path[0]

        return match

    def _full_match(self, **kwargs):
        return self._partial_match(**kwargs) and len(kwargs) == len(self._path)

    def fill_in(self, **kwargs: InSpecType) -> InSpecType:
        """
        Fill in missing levels in a parial specification.

        This can only be done if a unique partial match can be found
        amony the set of all valid paths.
        """
        if not self._partial_match(is_prefix=False, **kwargs):
            raise ValueError("Must be at least a partial match to fill in.")
        reversed_result = {}
        matching = False
        kwargs = self._u2s(**kwargs)

        for element in reversed(self._path):
            matching = matching or element in kwargs.keys()
            if matching:
                reversed_result[element] = kwargs.get(element, "*")

        result = {k: reversed_result[k] for k in reversed(reversed_result.keys())}

        return result

    def keys(self) -> List[str]:
        """Get the keys identifying the path components."""
        return list(self._path)

    @classmethod
    def partial_matches(
        cls, dataset: str, year: int, is_prefix=True, **kwargs: InSpecType
    ) -> List["BoundGeographyPath"]:
        """Find all partial matches for the path."""
        kwargs = PathSpec._u2s(**kwargs)

        return [
            BoundGeographyPath(num, path_spec, **kwargs)
            for num, path_spec in PathSpec.get_path_specs(dataset, year).items()
            if path_spec._partial_match(is_prefix, **kwargs)
        ]

    @classmethod
    def partial_prefix_match(
        cls, dataset: str, year: int, **kwargs: InSpecType
    ) -> Optional["BoundGeographyPath"]:
        """Find the minimal partial prefix match."""
        matches = cls.partial_matches(dataset, year, is_prefix=True, **kwargs)

        min_bgp = None

        for bgp in matches:
            if min_bgp is None or len(bgp.path_spec) < len(min_bgp.path_spec):
                min_bgp = bgp

        return min_bgp

    @classmethod
    def full_match(cls, dataset: str, year: int, **kwargs: InSpecType):
        """Find a full match."""
        full_matches = [
            (num, path_spec)
            for num, path_spec in cls.get_path_specs(dataset, year).items()
            if path_spec._full_match(**kwargs)
        ]
        if not full_matches:
            return None, None
        if len(full_matches) > 1:
            raise ValueError(
                f"Internal Error, multiple matches for {dataset} in {year} for {kwargs}."
            )
        return full_matches[0]

    @classmethod
    def by_number(cls, dataset: str, year: int, num: str):
        """
        Get the path spec for a given U.S. Census numerical geography code.

        For example, the code '050' represents a state and county specification.
        """
        return cls.get_path_specs(dataset, year).get(num, None)

    @staticmethod
    def _geo_url(dataset: str, year: int) -> str:
        if isinstance(year, int):
            return f"https://api.census.gov/data/{year}/{dataset}/geography.json"
        else:
            return f"https://api.census.gov/data/{dataset}/geography.json"

    @staticmethod
    def _fetch_path_specs(dataset: str, year: int) -> Dict[str, "PathSpec"]:
        url = PathSpec._geo_url(dataset, year)

        request = requests.get(
            url, cert=certificates.data_cert, verify=certificates.data_verify
        )

        if request.status_code == 200:
            parsed_json = request.json()

            path_specs = {}

            for row in parsed_json["fips"]:
                level = row.get("geoLevelId", None)
                if level is None:
                    level = row.get("geoLevelDisplay", None)

                if level is not None:
                    path = row.get("requires", [])
                    path.append(row["name"])

                    path_specs[level] = PathSpec(path, PathSpec.__init_key)

            return path_specs

        # Do our best to tell the user something informative.
        raise GeoException(
            f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
        )

    _PATH_SPECS_BY_DATASET_YEAR: DefaultDict[str, Dict[int, Dict[str, "PathSpec"]]] = (
        defaultdict(dict)
    )

    _PATH_SPEC_SNAKE_MAP: DefaultDict[str, Dict[int, Dict[str, str]]] = defaultdict(
        dict
    )
    _PATH_SPEC_SNAKE_INV_MAP: DefaultDict[str, Dict[int, Dict[str, str]]] = defaultdict(
        dict
    )

    @staticmethod
    def get_path_specs(dataset: str, vintage: int) -> Dict[str, "PathSpec"]:
        """Fet all the path specifications for the given dataset and vintage."""
        if vintage not in PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset]:
            PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset][vintage] = (
                PathSpec._fetch_path_specs(dataset, vintage)
            )
            PathSpec._PATH_SPEC_SNAKE_MAP[dataset][vintage] = {
                component.replace(" ", "_")
                .replace("/", "_")
                .replace("-", "_")
                .replace("(", "")
                .replace(")", "")
                .lower(): component
                for path_spec in PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset][
                    vintage
                ].values()
                for component in path_spec.path
            }
            PathSpec._PATH_SPEC_SNAKE_INV_MAP[dataset][vintage] = {
                name: py_name
                for py_name, name in PathSpec._PATH_SPEC_SNAKE_MAP[dataset][
                    vintage
                ].items()
            }

        return PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset][vintage]


class BoundGeographyPath:
    """A fully bound geography path."""

    def __init__(self, num: str, path_spec: PathSpec, **kwargs: InSpecType):
        """
        Initialize a bound geography path.

        This means it corresponds to a path spec with a numeric ID from
        the U.S. Census, like '050' for state and county.

        It also means that it has bound values for all components.

        Parameters
        ----------
        num
            A numeric code from the U.S. Census. E.g. '050' for state and county.
        path_spec
            The path specification.
        kwargs
            Keyword args specifying the bound values.
        """
        self._num = num
        self._path_spec = path_spec
        self._bindings = path_spec.fill_in(**kwargs)

    @property
    def num(self) -> str:
        """
        The U.S. Census numeric code for the geography.

        For example, '050' for state and county.
        """
        return self._num

    @property
    def path_spec(self) -> PathSpec:
        """The path specification."""
        return self._path_spec

    @property
    def bindings(self) -> Mapping[str, InSpecType]:
        """The values bound for each path element."""
        return self._bindings


class EnvironmentApiKey:
    """
    A small class that holds an API key loaded from the environment.

    There are two places it could come from, the environment variable
    US_CENSUS_API_KEY or a file ~/.censusdis/api_key.txt
    in the current users home directory. If it is in both, the environment
    variable value is used.
    """

    _env_var = "US_CENSUS_API_KEY"

    _api_key = None

    @classmethod
    def api_key(cls):
        """
        Determine the API key we should use.

        This could come from the environment variable US_CENSUS_API_KEY or,
        if that is not set, a value stored in a single line in the file
        `'~/.censusdis/api_key.txt'`.

        If neither of these is set, access to the U.S. Census API may be throttled
        or limited. See https://api.census.gov/data/key_signup.html to sign up for
        a key.
        """
        # Try the env var,
        if cls._api_key is None:
            cls._api_key = os.environ.get(cls._env_var, None)

        # Try the file.
        if cls._api_key is None:
            path = Path.home() / ".censusdis" / "api_key.txt"

            if path.is_file():
                with path.open("r") as file:
                    file_key = file.read().splitlines()[0]
                    cls._api_key = file_key

        return cls._api_key


@dataclass(init=False)
class CensusGeographyQuerySpec:
    """A specification for a geography query."""

    dataset: str
    year: int
    variables: List[str]
    bound_path: BoundGeographyPath
    api_key: Optional[str] = None

    _BASE_URL: ClassVar[str] = "https://api.census.gov/data"

    def __init__(
        self,
        dataset: str,
        year: int,
        variables: List[str],
        bound_path: BoundGeographyPath,
        api_key: Optional[str] = None,
    ):
        """
        Construct a geographic query.

        Parameters
        ----------
        dataset
            The dataset to download from. For example `"acs/acs5"`,
            `"dec/pl"`, or `"timeseries/poverty/saipe/schdist"`. There are
            symbolic names for datasets, like `ACS5` for `"acs/acs5"
            in :py:module:`censusdis.datasets`.
        year
            The vintage to download data for. For most data sets this is
            an integer year, for example, `2020`.
        variables
            The variables to download.
        bound_path
            A bound geographic query.
        api_key
            An optional API key. You may be throttled or prevented from using
            the U.S. Census API if you don't provide one.
        """
        self.dataset = dataset
        self.year = year
        self.variables = variables
        self.bound_path = bound_path

        if api_key is None:
            api_key = EnvironmentApiKey.api_key()

        self.api_key = api_key

    @property
    def for_component(self) -> str:
        """The part of the query string that is the `for` clause."""
        *_, (key, value) = self.bound_path.bindings.items()
        if value == "*":
            return f"{key}"
        return f"{key}:{value}"

    @property
    def in_components(self) -> Optional[str]:
        """The part of the query string specifying the `in` components."""
        *components, _ = self.bound_path.bindings.items()

        if components:
            return " ".join(f"{k}:{v}" for (k, v) in components)

        return None

    def table_url(
        self, *, query_filter: Optional[Dict[str, str]] = None
    ) -> Tuple[str, Mapping[str, str]]:
        """
        Construct the URL to query census data.

        Parameters
        ----------
        query_filter
            A dictionary of values to filter on. For example, if
            `query_filter={'NAICS2017': '72251'}` then only rows
            where the variable `NAICS2017` has a value of `'72251'`
            will be returned.

            This filtering is done on the server side, not the client
            side, so it is far more efficient than querying without a
            query filter and then manually filtering the results.

        Returns
        -------
            The URL and the parameters to pass to it.
        """
        if isinstance(self.year, int):
            url = "/".join([self._BASE_URL, f"{self.year:04}", self.dataset])
        else:
            url = "/".join([self._BASE_URL, self.dataset])

        params = {
            "get": ",".join(self.variables),
            "for": self.for_component,
        }

        if query_filter is not None:
            params.update(query_filter)

        in_components = self.in_components
        if in_components is not None:
            params["in"] = in_components

        if self.api_key is not None:
            params["key"] = self.api_key

        return url, params


def geo_path_specs(dataset: str, year: int) -> Dict[str, List[str]]:
    """Construct a map of all known path specs for a given data set and year."""
    return {
        name: [c for c in path_spec.path]
        for name, path_spec in PathSpec.get_path_specs(dataset, year).items()
    }


def path_component_to_snake(dataset: str, year: int, component: str) -> str:
    """Convert path components to snake case."""
    return PathSpec._PATH_SPEC_SNAKE_INV_MAP[dataset][year].get(component, component)


def path_component_from_snake(dataset: str, year: int, component: str) -> str:
    """Convert path components out of snake case."""
    return PathSpec._PATH_SPEC_SNAKE_MAP[dataset][year].get(component, component)


def geo_path_snake_specs(dataset: str, year: int) -> Dict[str, List[str]]:
    """Construc a map to snake case for all know geo path specs."""
    return {
        name: [path_component_to_snake(dataset, year, c) for c in path_spec.path]
        for name, path_spec in PathSpec.get_path_specs(dataset, year).items()
    }
