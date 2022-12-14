# Copyright (c) 2022 Darren Erik Vengroff
"""
Utilities for loading census dats.

This module relies on the US Census API, which
it wraps in a pythonic manner.
"""

import tempfile
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import (
    Any,
    DefaultDict,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import geopandas as gpd
import pandas as pd
import requests

import censusdis.geography as cgeo
import censusdis.maps as cmap

# This is the type we can accept for geographic
# filters. When provided, these filters are either
# single values as a string, or, if multivalued,
# then an iterable containing all the values allowed
# by the filter.
GeoFilterType = Optional[Union[str, Iterable[str]]]


def _gf2s(geo_filter: GeoFilterType) -> Optional[str]:
    """
    Utility to convert a filter to a string.

    For the Census API, multiple values are encoded
    in a single comma separated string.
    """
    if geo_filter is None or isinstance(geo_filter, str):
        return geo_filter
    return ",".join(geo_filter)


class CensusApiException(Exception):
    pass


def data_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> pd.DataFrame:
    parsed_json = json_from_url(url, params)

    return _df_from_census_json(parsed_json)


def _df_from_census_json(parsed_json):

    if (
        isinstance(parsed_json, list)
        and len(parsed_json) >= 1
        and isinstance(parsed_json[0], list)
    ):
        return pd.DataFrame(
            parsed_json[1:],
            columns=(
                c.upper()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
                .replace("(", "")
                .replace(")", "")
                for c in parsed_json[0]
            ),
        )

    raise CensusApiException(
        f"Expected json data to be a list of lists, not a {type(parsed_json)}"
    )


def json_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> Any:
    request = requests.get(url, params=params)

    if request.status_code == 200:
        parsed_json = request.json()
        return parsed_json

    # Do our best to tell the user something informative.
    raise CensusApiException(
        f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
    )


_MAX_FIELDS_PER_DOWNLOAD = 50


def _download_concat_detail(
    dataset: str,
    year: int,
    fields: List[str],
    *,
    key: Optional[str],
    census_variables: "VariableCache",
    with_geometry: bool = False,
    **kwargs: cgeo.InSpecType,
) -> pd.DataFrame:

    # Divide the fields into groups.
    field_groups = [
        # black and flake8 disagree about the whitespace before ':' here...
        fields[start : start + _MAX_FIELDS_PER_DOWNLOAD]  # noqa: 203
        for start in range(0, len(fields), _MAX_FIELDS_PER_DOWNLOAD)
    ]

    # Get the data for each chunk.
    dfs = [
        download_detail(
            dataset,
            year,
            field_group,
            api_key=key,
            variable_cache=census_variables,
            with_geometry=with_geometry and (ii == 0),
            **kwargs,
        )
        for ii, field_group in enumerate(field_groups)
    ]

    # What fields came back in the first df but were not
    # requested? These are the ones that will be duplicated
    # in the later dfs.
    extra_fields = [f for f in dfs[0].columns if f not in set(field_groups[0])]

    # If we put in the geometry column, it's not part of the merge
    # key.
    if with_geometry:
        extra_fields = [f for f in extra_fields if f != "geometry"]

    df_data = dfs[0]

    for df_right in dfs[1:]:
        df_data = df_data.merge(df_right, on=extra_fields)

    return df_data


__shapefile_root: str = tempfile.mkdtemp(prefix="data_shapefiles_")
__shapefile_readers: Dict[int, cmap.ShapeReader] = {}


def set_shapefile_path(shapefile_path: str) -> None:
    """
    Set the path to the directory to cache shapefiles.

    This is where we will cache shapefiles downloaded when
    `with_geometry=True` is passed to :py:func:`~download_detail`.

    Parameters
    ----------
    shapefile_path
        The path to use for caching shapefiles.
    """
    global __shapefile_root

    __shapefile_root = shapefile_path


def get_shapefile_path() -> str:
    """
    Get the path to the directory to cache shapefiles.

    This is where we will cache shapefiles downloaded when
    `with_geometry=True` is passed to :py:func:`~download_detail`.

    Returns
    -------
        The path to use for caching shapefiles.
    """
    global __shapefile_root

    return __shapefile_root


def __shapefile_reader(year: int):
    reader = __shapefile_readers.get(year, None)

    if reader is None:
        reader = cmap.ShapeReader(
            __shapefile_root,
            year,
        )

        __shapefile_readers[year] = reader

    return reader


_GEO_QUERY_FROM_DATA_QUERY_INNER_GEO: Dict[
    str, Tuple[Optional[str], str, List[str], List[str]]
] = {
    # innermost geo: ( shapefile_scope, shapefile_geo_name, df_on, gdf_on )
    "region": ("us", "region", ["REGION"], ["REGIONCE"]),
    "division": ("us", "division", ["DIVISION"], ["DIVISIONCE"]),
    "combined statistical area": (
        "us",
        "csa",
        ["COMBINED_STATISTICAL_AREA"],
        ["CSAFP"],
    ),
    "metropolitan statistical area/micropolitan statistical area": (
        "us",
        "cbsa",
        ["METROPOLITAN_STATISTICAL_AREA_MICROPOLITAN_STATISTICAL_AREA"],
        ["CBSAFP"],
    ),
    "state": ("us", "state", ["STATE"], ["STATEFP"]),
    "county": ("us", "county", ["STATE", "COUNTY"], ["STATEFP", "COUNTYFP"]),
    # For these, the shapefiles are at the state level, so `None`
    # indicates that we have to fill it in based on the geometry
    # being queried.
    "tract": (
        None,
        "tract",
        ["STATE", "COUNTY", "TRACT"],
        ["STATEFP", "COUNTYFP", "TRACTCE"],
    ),
    "block group": (
        None,
        "bg",
        ["STATE", "COUNTY", "TRACT", "BLOCK_GROUP"],
        ["STATEFP", "COUNTYFP", "TRACTCE", "BLKGRPCE"],
    ),
}
"""
Helper map for the _with_geometry case.

A map from the innermost level of a geometry specification
to the arguments we need to pass to `get_cb_shapefile`
to get the right shapefile for the geography and the columns
we need to join the data and shapefile on.
"""


def _add_geography(
    df_data: pd.DataFrame, year: int, shapefile_scope: str, geo_level: str
) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
    """
    Add geography to data.

    Parameters
    ----------
    df_data
        The data we downloaded from the census API
    year
        The year for which to fetch geometries. We need this
        because they change over time.
    shapefile_scope
        The scope of the shapefile. This is typically either a state
        such as `STATE_NJ` or the string `"us"`.
    geo_level
        The geography level we want to add.

    Returns
    -------
        A GeoDataFrame with the original data and an
        added geometry column for each row.
    """

    if geo_level not in _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO:
        raise CensusApiException(
            "The with_geometry=True flag is only allowed if the "
            f"geometry for the data to be loaded ('{geo_level}') is one of "
            f"{[geo for geo in _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO.keys()]}."
        )

    (
        query_shapefile_scope,
        shapefile_geo_level,
        df_on,
        gdf_on,
    ) = _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO[geo_level]

    # If the query spec has a hard-coded value then we use it.
    if query_shapefile_scope is not None:
        shapefile_scope = query_shapefile_scope

    gdf_shapefile = __shapefile_reader(year).read_cb_shapefile(
        shapefile_scope,
        shapefile_geo_level,
    )

    gdf_data = (
        gdf_shapefile[gdf_on + ["geometry"]]
        .merge(df_data, how="right", left_on=gdf_on, right_on=df_on)
        .drop(gdf_on, axis="columns")
    )

    # Rearrange columns so geometry is at the end.
    gdf_data = gdf_data[
        [col for col in gdf_data.columns if col != "geometry"] + ["geometry"]
    ]

    return gdf_data


def infer_geo_level(df: pd.DataFrame) -> str:
    """
    Infer the geography level based on columns names.

    Parameters
    ----------
    df
        A dataframe of variables with one or more columns that
        can be used to infer what geometry level the rows represent.

        For example, if the column `"STATE"` exists, we could infer that
        the data in on a state by state basis. But if there are
        columns for both `"STATE"` and `"COUNTY"`, the data is probably
        at the county level.

        If, on the other hand, there is a `"COUNTY" column but not a
        `"STATE"` column, then there is some ambiguity. The data
        probably corresponds to counties, but the same county ID can
        exist in multiple states, so we will raise a
        :py:class:`~CensusApiException` with an error message expalining
        the situation.

        If there is no match, we will also raise an exception. Again we
        do this, rather than for example, returning `None`, so that we
        can provide an informative error message about the likely cause
        and what to do about it.

        This function is not often called directly, but rather from
        :py:func:`~add_inferred_geography`, which infers the geography
        level and then adds a `geometry` column containing the appropriate
        geography for each row.

    Returns
    -------
        The name of the geography level.
    """
    match_key = None
    match_on_len = 0
    partial_match_keys = []

    for k, (_, _, df_on, _) in _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO.items():
        if all(col in df.columns for col in df_on):
            # Full match. We want the longest full match
            # we find.
            if match_key is None or len(df_on) > match_on_len:
                match_key = k
        elif df_on[-1] in df.columns:
            # Partial match. This could result in us
            # not getting what we expect. Like if we
            # have STATE and TRACT, but not COUNTY, we will
            # get a partial match on [STATE, COUNTY. TRACT]
            # and a full match on [STATE]. We probably did
            # not mean to match [STATE], we just lost the
            # COUNTY column somewhere along the way.
            partial_match_keys.append(k)

    if match_key is None:
        raise CensusApiException(
            f"Unable to infer geometry. Was not able to locate any of the "
            "known sets of columns "
            f"{tuple(df_on for _, _, df_on, _ in _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO.values())} "
            f"in the columns {list(df.columns)}."
        )

    if partial_match_keys:
        raise CensusApiException(
            f"Unable to infer geometry. Geometry matched {match_key} on columns "
            f"{_GEO_QUERY_FROM_DATA_QUERY_INNER_GEO[match_key][2]} "
            "but also partially matched one or more candidates "
            f"{tuple(_GEO_QUERY_FROM_DATA_QUERY_INNER_GEO[k][2] for k in partial_match_keys)}. "
            "Partial matches are usually unintended. Either add columns to allow a "
            "full match or rename some columns to prevent the undesired partial match."
        )

    return match_key


def add_inferred_geography(df: pd.DataFrame, year: int) -> gpd.GeoDataFrame:
    """
    Infer the geography level of the given dataframe and
    add geometry to each row for that level.

    See Also
    --------
        :py:ref:`~infer_geo_level` for more on how inference is done.

    Parameters
    ----------
    df
        A dataframe of variables with one or more columns that
        can be used to infer what geometry level the rows represent.
    year
        The year for which to fetch geometries. We need this
        because they change over time.

    Returns
    -------
        A geo data frame containing the original data augmented with
        the appropriate geometry for each row.
    """

    geo_level = infer_geo_level(df)

    shapefile_scope = _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO[geo_level][0]

    if shapefile_scope is not None:
        # The scope is the same across the board.
        gdf = _add_geography(df, year, shapefile_scope, geo_level)
        return gdf

    # We have to group by different values of the shapefile
    # scope from the appropriate column and add the right
    # geography to each group.
    shapefile_scope_column = _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO[geo_level][2][0]

    df_with_geo = (
        df.groupby(shapefile_scope_column, group_keys=False)
        .apply(lambda g: _add_geography(g, year, g.name, geo_level))
        .reset_index(drop=True)
    )

    gdf = gpd.GeoDataFrame(df_with_geo)

    return gdf


def download_detail(
    dataset: str,
    year: int,
    download_variables: Iterable[str],
    *,
    with_geometry: bool = False,
    api_key: Optional[str] = None,
    variable_cache: Optional["VariableCache"] = None,
    **kwargs: cgeo.InSpecType,
) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
    """
    Download data from the US Census API.

    This is the main API for downloading US Census data with the
    `censusdis` package. There are many examples of how to use
    this in the demo notebooks provided with the package at
    https://github.com/vengroff/censusdis/tree/main/notebooks.

    Parameters
    ----------
    dataset
        The dataset to download from. For example `acs/acs5` or
        `dec/pl`.
    year
        The year to download data for.
    download_variables
        The census variables to download, for example `["NAME", "B01001_001E"]`.
    with_geometry
        If `True` a :py:class:`gpd.GeoDataFrame` will be returned and each row
        will have a geometry that is a cartographic boundary suitable for platting
        a map. See https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
        for details of the shapefiles that will be downloaded on your behalf to
        generate these boundaries.
    api_key
        An optional API key. If you don't have or don't use a key, the number
        of calls you can make will be limited.
    variable_cache
        A cache of metadata about variables.
    kwargs
        A specification of the geometry that we want data for.

    Returns
    -------
        A :py:class:`~pd.DataFrame` containing the requested US Census data.
    """
    if variable_cache is None:
        variable_cache = variables

    # The side effect here is to prime the cache.
    cgeo.geo_path_snake_specs(dataset, year)

    # In case they came to us in py format, as kwargs often do.
    kwargs = {
        cgeo.path_component_from_snake(dataset, year, k): v for k, v in kwargs.items()
    }

    if not isinstance(download_variables, list):
        download_variables = list(download_variables)

    # Special case if we are trying to get too many fields.
    if len(download_variables) > _MAX_FIELDS_PER_DOWNLOAD:
        return _download_concat_detail(
            dataset,
            year,
            download_variables,
            key=api_key,
            census_variables=variable_cache,
            with_geometry=with_geometry,
            **kwargs,
        )

    # Prefetch all the types before we load the data.
    # That way we fail fast if a field is not known.
    for variable in download_variables:
        try:
            variable_cache.get(dataset, year, variable)
        except Exception:
            census_url = CensusApiVariableSource.url(
                dataset, year, variable, response_format="html"
            )
            census_variables_url = CensusApiVariableSource.variables_url(
                dataset, year, response_format="html"
            )

            raise CensusApiException(
                f"Unable to get metadata on the variable {variable} from the "
                f"dataset {dataset} for year {year} from the census API. "
                f"Check the census URL for the variable ({census_url}) to ensure it exists. "
                f"If not found, check {census_variables_url} for all variables in the dataset."
            )

    # If we were given a list, join it together into
    # a comma-separated string.
    string_kwargs = {k: _gf2s(v) for k, v in kwargs.items()}

    url, params, bound_path = census_detail_table_url(
        dataset, year, download_variables, api_key=api_key, **string_kwargs
    )
    df_data = data_from_url(url, params)

    for field in download_variables:
        field_type = variable_cache.get(dataset, year, field)["predicateType"]

        if field_type == "int":
            df_data[field] = df_data[field].astype(int)
        elif field_type == "float":
            df_data[field] = df_data[field].astype(float)
        elif field_type == "string":
            pass
        else:
            # Leave it as an object?
            pass

    # Put the geo fields that came back up front.
    df_data = df_data[
        [col for col in df_data.columns if col not in download_variables]
        + download_variables
    ]

    if with_geometry:
        # We need to get the geometry and merge it in.
        geo_level = bound_path.path_spec.path[-1]
        shapefile_scope = bound_path.bindings[bound_path.path_spec.path[0]]

        gdf_data = _add_geography(df_data, year, shapefile_scope, geo_level)
        return gdf_data

    return df_data


def census_detail_table_url(
    dataset: str,
    year: int,
    fields: Iterable[str],
    *,
    api_key: Optional[str] = None,
    **kwargs: cgeo.InSpecType,
) -> Tuple[str, Mapping[str, str], cgeo.BoundGeographyPath]:
    bound_path = cgeo.PathSpec.partial_prefix_match(dataset, year, **kwargs)

    if bound_path is None:
        raise CensusApiException(
            f"Unable to match the geography specification {kwargs}.\n"
            f"Supported geographies for dataset='{dataset}' in year={year} are:\n"
            + "\n".join(
                f"{path_spec}"
                for path_spec in cgeo.geo_path_snake_specs(dataset, year).values()
            )
        )

    query_spec = cgeo.CensusGeographyQuerySpec(
        dataset, year, list(fields), bound_path, api_key=api_key
    )

    url, params = query_spec.detail_table_url()

    return url, params, bound_path


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


class CensusApiVariableSource(VariableSource):
    """
    A :py:class:`~VariableSource` that gets data from the US Census remote API.

    Users will rarely if ever need to explicitly construct objects
    of this class. There is one behind the singleton cache
    `censusdis.censusdata.variables`.
    """

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
            f"https://api.census.gov/data/{year}/{dataset}/variables.{response_format}"
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
        return f"https://api.census.gov/data/{year}/{dataset}/variables/{name}.{response_format}"

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
            return f"https://api.census.gov/data/{year}/{dataset}/variables.json"

        return f"https://api.census.gov/data/{year}/{dataset}/groups/{group_name}.json"

    def get(self, dataset: str, year: int, name: str) -> Dict[str, Any]:
        url = self.url(dataset, year, name)
        value = json_from_url(url)

        return value

    def get_group(
        self, dataset: str, year: int, name: Optional[str]
    ) -> Dict[str, Dict]:
        url = self.group_url(dataset, year, name)
        value = json_from_url(url)

        # Put the name into the nested dictionaries, so it looks the same is if
        # we had gotten it via the variable API even though that API leaves it out.
        for k, v in value["variables"].items():
            v["name"] = k

        return value


class VariableCache:
    """
    A cache of vatiables and groups.

    This looks a lot like a :py:class:`~VariableSource` but it
    implements a cache in front of a :py:class:`~VariableSource`.

    Users will rarely if ever need to construct one of these
    themselves. In almost all cases they will use the singleton
    `censusdis.censusdata.variables`.
    """

    def __init__(self, *, variable_source: Optional[VariableSource] = None):
        if variable_source is None:
            variable_source = CensusApiVariableSource()

        self._variable_source = variable_source
        self._variable_cache: DefaultDict[
            str, DefaultDict[int, Dict[str, Any]]
        ] = defaultdict(lambda: defaultdict(dict))
        self._group_cache: DefaultDict[
            str, DefaultDict[int, Dict[str, Any]]
        ] = defaultdict(lambda: defaultdict(dict))

    def get(
        self,
        dataset: str,
        year: int,
        name: str,
    ) -> Dict[str, Dict]:
        """
        Get the description of a given variable.

        See :py:meth:`VariableSource.get`
        for details on the data format. We first look in the cache and then if
        we don't find what we are looking for, we call the source behind us and
        cache the results before returning them.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the variable.

        Returns
        -------
            The details of the variable.
        """
        cached_value = self._variable_cache[dataset][year].get(name, None)

        if cached_value is not None:
            return cached_value

        value = self._variable_source.get(dataset, year, name)

        self._variable_cache[dataset][year][name] = value

        return value

    def get_group(
        self,
        dataset: str,
        year: int,
        name: Optional[str],
    ) -> Dict[str, Dict]:
        """
        Get information on the variables in a group.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the group. Or None if this data set does not have
            groups.

        Returns
        -------
            A dictionary that maps from the names of each variable in the group
            to a dictionary containing a description of the variable. The
            format of the description is a dictionary as described in
            the documentation for
            :py:meth:`VariableSource.get`.
        """
        group_variable_names = self._group_cache[dataset][year].get(name, None)

        if group_variable_names is None:
            # Missed in the cache, so go fetch it.
            value = self._variable_source.get_group(dataset, year, name)

            # Cache all the variables in the group.
            group_variables = value["variables"]

            for variable_name, variable_details in group_variables.items():
                self._variable_cache[dataset][year][variable_name] = variable_details

            # Cache the names of the variables in the group.
            group_variable_names = list(
                variable_name for variable_name in group_variables
            )
            self._group_cache[dataset][year][name] = group_variable_names

        # Reformat what we return so it includes the full
        # details on each variable.
        return {
            group_variable_name: self.get(dataset, year, group_variable_name)
            for group_variable_name in group_variable_names
        }

    class GroupTreeNode:
        def __init__(self, name: Optional[str] = None):
            self._name = name

            self._children: Dict[str, "VariableCache.GroupTreeNode"] = {}

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name: Optional[str]):
            self._name = name

        def add_child(self, path_component: str, child: "VariableCache.GroupTreeNode"):
            self._children[path_component] = child

        def is_leaf(self) -> bool:
            return len(self._children) == 0

        def __len__(self):
            return len(self._children)

        def __contains__(self, component: str):
            return component in self._children

        def __getitem__(self, component: str):
            return self._children[component]

        def keys(self) -> Iterable[str]:
            for key, _ in self.items():
                yield key

        def values(self) -> Iterable["VariableCache.GroupTreeNode"]:
            for _, value in self.items():
                yield value

        def items(self) -> Iterable[Tuple[str, "VariableCache.GroupTreeNode"]]:
            return self._children.items()

        def get(
            self, component, default: Optional["VariableCache.GroupTreeNode"] = None
        ):
            return self._children.get(component, default)

        def leaves(self) -> Generator["VariableCache.GroupTreeNode", None, None]:
            if self.is_leaf():
                yield self
            for child in self._children.values():
                yield from child.leaves()

        def leaf_variables(self) -> Generator[str, None, None]:
            yield from (leaf.name for leaf in self.leaves())

        def _min_leaf_name(self) -> str:
            return min(self.leaf_variables())

        def _node_str(self, level: int, component: str, indent_prefix: str) -> str:
            line = indent_prefix * level
            if len(self._children) > 0 or self._name is not None:
                line = f"{line}+ {component}"
            if self.name is not None:
                line = f"{line} ({self.name})"

            return line

        def _subtree_str(self, level: int, component: str, indent_prefix: str) -> str:
            rep = self._node_str(level, component, indent_prefix)
            for path_component, child in sorted(
                self._children.items(), key=lambda t: t[1]._min_leaf_name()
            ):
                rep = (
                    rep
                    + "\n"
                    + child._subtree_str(level + 1, path_component, indent_prefix)
                )
            return rep

        def __str__(self) -> str:
            return "\n".join(
                child._subtree_str(0, path_component, indent_prefix="    ")
                for path_component, child in sorted(
                    self._children.items(), key=lambda t: t[1]._min_leaf_name()
                )
            )

        def __repr__(self) -> str:
            return str(self)

    def group_tree(
        self,
        dataset: str,
        year: int,
        group_name: Optional[str],
        *,
        skip_annotations: bool = True,
    ) -> "VariableCache.GroupTreeNode":
        group = self.get_group(dataset, year, group_name)

        root = VariableCache.GroupTreeNode()

        for variable_name, details in group.items():
            path = details["label"].split("!!")

            node = root

            # Construct a nested path of nodes down to the
            # leaf.
            for component in path:
                child = node.get(component, None)
                if child is None:
                    child = VariableCache.GroupTreeNode()
                    node.add_child(component, child)
                node = child

            # Put the variable name at the lead.
            node.name = variable_name

        return root

    def group_leaves(
        self, dataset: str, year: int, name: str, *, skip_annotations: bool = True
    ) -> List[str]:
        """
        Find the leaves of a given group.

        Parameters
        ----------
        dataset
            The census dataset.
        year
            The year
        name
            The name of the group.
        skip_annotations
            If `True` try to filter out variables that are
            annotations rather than actual values, by skipping
            those with labels that begin with "Annotation" or
            "Margin of Error".

        Returns
        -------
            A list of the variables in the group that are leaves,
            i.e. they are not aggregates of other variables. For example,
            in the group `B03002` in the `acs/acs5` dataset in the
            year `2020`, the variable `B03002_003E` is a leaf, because
            it represents
            "Estimate!!Total:!!Not Hispanic or Latino:!!White alone",
            whereas B03002_002E is not a leaf because it represents
            "Estimate!!Total:!!Not Hispanic or Latino:", which is a total
            that includes B03002_003E as well as others like "B03002_004E",
            "B03002_005E" and more.

            The typical reason we want leaves is because that gives us a set
            of variables representing counts that do not overlap and add up
            to the total. We can use these directly in diversity and integration
            calculations using the `divintseg` package.
        """
        tree = self.group_tree(dataset, year, name)
        leaves = tree.leaf_variables()

        if skip_annotations:
            group = self.get_group(dataset, year, name)
            leaves = (
                leaf
                for leaf in leaves
                if (not group[leaf]["label"].startswith("Annotation"))
                and (not group[leaf]["label"].startswith("Margin of Error"))
            )

        return sorted(leaves)

    def __contains__(self, item: Tuple[str, int, str]) -> bool:
        """Magic method behind the `in` operator."""
        source, year, name = item

        return name in self._variable_cache[source][year]

    def __getitem__(self, item: Tuple[str, int, str]):
        """Magic method behind the `[]` operator."""
        return self.get(*item)

    def __len__(self):
        """The number of elements in the cache."""
        return sum(
            len(names)
            for years in self._variable_cache.values()
            for names in years.values()
        )

    def keys(self) -> Iterable[Tuple[str, int, str]]:
        """Keys, i.e. the names of variables, in the cache."""
        for key, _ in self.items():
            yield key

    def __iter__(self) -> Iterable[Tuple[str, int, str]]:
        return self.keys()

    def values(self) -> Iterable[dict]:
        """Values, i.e. the descriptions of variables, in the cache."""
        for _, value in self.items():
            yield value

    def items(self) -> Iterable[Tuple[Tuple[str, int, str], dict]]:
        """Items in the mapping from variable name to descpription."""
        for source, values_for_source in self._variable_cache.items():
            for year, values_for_year in values_for_source.items():
                for name, value in values_for_year.items():
                    yield (source, year, name), value

    def invalidate(self, dataset: str, year: int, name: str):
        """Remove an item from the cache."""
        if self._variable_cache[dataset][year].pop(name, None):
            if len(self._variable_cache[dataset][year]) == 0:
                self._variable_cache[dataset].pop(year)
                if len(self._variable_cache[dataset]) == 0:
                    self._variable_cache.pop(dataset)

    def clear(self):
        """
        Clear the entire cache.

        This just means that further calls to :py:meth:`~get` will
        have to make a call to the source behind the cache.
        """
        self._variable_cache = defaultdict(lambda: defaultdict(dict))


variables = VariableCache()
