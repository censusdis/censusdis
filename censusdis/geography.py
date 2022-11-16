# Copyright (c) 2022 Darren Erik Vengroff
"""
Utilities for managing hierarchies of geographies.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Iterable, List, Mapping, Optional, Tuple, Union

import requests

InSpecType = Union[str, Iterable[str]]


class GeoException(Exception):
    pass


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
        return ":".join(self._path)

    def __repr__(self):
        quoted_path = (f'"{c}"' for c in self._path)
        return f"PathSpec([{', '.join(quoted_path)}])"

    def __len__(self):
        return len(self._path)

    @property
    def path(self):
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

    def keys(self):
        return list(self._path)

    @classmethod
    def partial_matches(
        cls, dataset: str, year: int, is_prefix=True, **kwargs: InSpecType
    ) -> List["BoundGeographyPath"]:
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
        matches = cls.partial_matches(dataset, year, is_prefix=True, **kwargs)

        min_bgp = None

        for bgp in matches:
            if min_bgp is None or len(bgp.path_spec) < len(min_bgp.path_spec):
                min_bgp = bgp

        return min_bgp

    @classmethod
    def full_match(cls, dataset: str, year: int, **kwargs: InSpecType):
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
        return cls.get_path_specs(dataset, year).get(num, None)

    @staticmethod
    def _geo_url(dataset: str, year: int) -> str:
        return f"https://api.census.gov/data/{year}/{dataset}/geography.json"

    @staticmethod
    def _fetch_path_specs(dataset: str, year: int) -> Dict[str, "PathSpec"]:
        url = PathSpec._geo_url(dataset, year)

        request = requests.get(url)

        if request.status_code == 200:
            parsed_json = request.json()

            path_specs = {}

            for row in parsed_json["fips"]:
                level = row["geoLevelDisplay"]
                path = row.get("requires", [])
                path.append(row["name"])

                path_specs[level] = PathSpec(path, PathSpec.__init_key)

            return path_specs

        # Do our best to tell the user something informative.
        raise GeoException(
            f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
        )

    _PATH_SPECS_BY_DATASET_YEAR = defaultdict(dict)

    _PATH_SPEC_SNAKE_MAP = defaultdict(dict)
    _PATH_SPEC_SNAKE_INV_MAP = defaultdict(dict)

    @staticmethod
    def get_path_specs(dataset: str, year: int) -> Dict[str, "PathSpec"]:
        if year not in PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset]:
            PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset][
                year
            ] = PathSpec._fetch_path_specs(dataset, year)
            PathSpec._PATH_SPEC_SNAKE_MAP[dataset][year] = {
                component.replace(" ", "_")
                .replace("/", "_")
                .replace("-", "_")
                .replace("(", "")
                .replace(")", "")
                .lower(): component
                for path_spec in PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset][
                    year
                ].values()
                for component in path_spec.path
            }
            PathSpec._PATH_SPEC_SNAKE_INV_MAP[dataset][year] = {
                name: py_name
                for py_name, name in PathSpec._PATH_SPEC_SNAKE_MAP[dataset][
                    year
                ].items()
            }

        return PathSpec._PATH_SPECS_BY_DATASET_YEAR[dataset][year]


class BoundGeographyPath:
    def __init__(self, num: str, path_spec: PathSpec, **kwargs: InSpecType):
        self._num = num
        self._path_spec = path_spec
        self._bindings = path_spec.fill_in(**kwargs)

    @property
    def num(self) -> str:
        return self._num

    @property
    def path_spec(self) -> PathSpec:
        return self._path_spec

    @property
    def bindings(self) -> Mapping[str, InSpecType]:
        return self._bindings


@dataclass(frozen=True)
class CensusGeographyQuerySpec:

    dataset: str
    year: int
    variables: List[str]
    bound_path: BoundGeographyPath
    api_key: Optional[str] = None

    _BASE_URL: ClassVar[str] = "https://api.census.gov/data"

    @property
    def for_component(self) -> str:
        *_, (key, value) = self.bound_path.bindings.items()
        if value == "*":
            return f"{key}"
        return f"{key}:{value}"

    @property
    def in_components(self) -> Optional[str]:
        *components, _ = self.bound_path.bindings.items()

        if components:
            return " ".join(f"{k}:{v}" for (k, v) in components)

        return None

    def detail_table_url(self) -> Tuple[str, Mapping[str, str]]:
        url = "/".join([self._BASE_URL, f"{self.year:04}", self.dataset])

        params = {
            "get": ",".join(self.variables),
            "for": self.for_component,
        }

        in_components = self.in_components
        if in_components is not None:
            params["in"] = in_components

        if self.api_key is not None:
            params["key"] = self.api_key

        return url, params


def geo_path_specs(dataset: str, year: int) -> Dict[str, List[str]]:
    return {
        name: [c for c in path_spec.path]
        for name, path_spec in PathSpec.get_path_specs(dataset, year).items()
    }


def path_component_to_snake(dataset: str, year: int, component: str) -> str:
    return PathSpec._PATH_SPEC_SNAKE_INV_MAP[dataset][year].get(component, component)


def path_component_from_snake(dataset: str, year: int, component: str) -> str:
    return PathSpec._PATH_SPEC_SNAKE_MAP[dataset][year].get(component, component)


def geo_path_snake_specs(dataset: str, year: int) -> Dict[str, List[str]]:
    return {
        name: [path_component_to_snake(dataset, year, c) for c in path_spec.path]
        for name, path_spec in PathSpec.get_path_specs(dataset, year).items()
    }
