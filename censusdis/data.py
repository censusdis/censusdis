# Copyright (c) 2022 Darren Erik Vengroff
"""
Utilities for loading census data.

This module relies on the US Census API, which
it wraps in a pythonic manner.
"""

import warnings
from logging import getLogger
from typing import Dict, Iterable, List, Mapping, Optional, Tuple, Union

import geopandas as gpd
import pandas as pd

import censusdis.geography as cgeo
import censusdis.maps as cmap
from censusdis.impl.exceptions import CensusApiException
from censusdis.impl.fetch import data_from_url
from censusdis.impl.varcache import VariableCache
from censusdis.impl.varsource.censusapi import CensusApiVariableSource


logger = getLogger(__name__)


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


_MAX_VARIABLES_PER_DOWNLOAD = 50
"""
The maximum number of variables we can ask for in one census API query.

The U.S. Census sets this limit, not us. In order to not expose our
users to the limit, :py:func:`~download` mostly obscures the fact that
requests to download more than this many variables are broken into
multiple calls to the census API and then the results are stitched back
together be either merging or concatenation. This is all handled in
:py:func:`~_download_multiple`.
"""


__dw_strategy_metrics = {"merge": 0, "concat": 0}
"""
Counters for how often we use each strategy for wide tables.
"""


def _download_wide_strategy_metrics() -> Dict[str, int]:
    """
    Metrics on which strategies have been used for wide tables.

    Returns
    -------
        A dictionary of metrics on how often each strategy has
        been used.
    """
    return dict(**__dw_strategy_metrics)


def _download_multiple(
    dataset: str,
    year: int,
    fields: List[str],
    *,
    key: Optional[str],
    census_variables: "VariableCache",
    with_geometry: bool = False,
    **kwargs: cgeo.InSpecType,
) -> pd.DataFrame:
    """
    Download data in groups of columns and concatenate the results together.

    The reason for this function is that the API will only return a maximum
    of 50 columns per query. This function downloads wider data 50 columns
    at a time and concatenates them.

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
        The full results of the query with all columns.

    """
    # Divide the fields into groups.
    field_groups = [
        # black and flake8 disagree about the whitespace before ':' here...
        fields[start : start + _MAX_VARIABLES_PER_DOWNLOAD]  # noqa: 203
        for start in range(0, len(fields), _MAX_VARIABLES_PER_DOWNLOAD)
    ]

    if len(field_groups) < 2:
        raise ValueError(
            "_download_multiple expects to be called with at least "
            f"{_MAX_VARIABLES_PER_DOWNLOAD + 1} variables. With fewer,"
            "use download instead."
        )

    # Get the data for each chunk.
    dfs = [
        download(
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
    # requested? These are a key to the geography the row
    # represents. For example, 'STATE' amd 'COUNTY' might
    # be these variables if we did a county-level query to
    # the census API.
    geo_key_variables = [f for f in dfs[0].columns if f not in set(field_groups[0])]

    # If we put in the geometry column, it's not part of the
    # key.
    if with_geometry:
        geo_key_variables = [f for f in geo_key_variables if f != "geometry"]

    # Now we have to decide if we are going to use the merge
    # strategy or the concat strategy to combine the data frames
    # we downloaded. Why do we have two strategies? Because we are
    # dealing with two kinds of data. One kind, from data sets like
    # ACS (https://www.census.gov/programs-surveys/acs.html),
    # has a unique key of columns that specify geography. The other
    # kind, from data sets like CPS
    # (https://www.census.gov/programs-surveys/cps.html) doesn't.
    #
    # In the unique key case, we can join the data frames that come
    # back on those key columns and get the final wide data frame
    # we want for the user.
    #
    # In the non-unique key case, we can't do this. There data sets
    # may have multiple rows for a value of the key columns. We can't
    # join here. Instead, we can only concatenate the tables
    # horizontally and hope that the rows came back in the same order
    # for each of them.

    # We hope to be able to merge. It is safer.
    merge_strategy = True

    # But if there are any non-unique keys in any df, we can't
    # merge.
    for df in dfs:
        if len(df.value_counts(geo_key_variables, sort=False)) != len(df.index):
            merge_strategy = False
            break

    if merge_strategy:
        # We can do the merge strategy.

        __dw_strategy_metrics["merge"] = __dw_strategy_metrics["merge"] + 1

        df_data = dfs[0]

        for df_right in dfs[1:]:
            df_data = df_data.merge(df_right, on=geo_key_variables)
    else:
        # We are going to have to fall back on the concat
        # strategy. Before we do the concat, however, let's
        # double-check that the key columns are the same in
        # at the corresponding row in every df. Otherwise, something
        # is fishy, and it is not safe to concat without mixing
        # data that should be in different rows.

        rows0 = len(dfs[0].index)

        for df in dfs[1:]:
            if not (
                rows0 == len(df.index)
                and (dfs[0][geo_key_variables] == df[geo_key_variables]).all().all()
            ):
                # At least one difference. So we cannot use the
                # concat strategy either.
                raise CensusApiException(
                    "Neither the merge nor the concat strategy is viable. "
                    "We made multiple queries to the census API because more than "
                    f"{_MAX_VARIABLES_PER_DOWNLOAD} variables were requested. "
                    "If you don't need all the variables, it is always safer to "
                    f"download less than {_MAX_VARIABLES_PER_DOWNLOAD} variables. "
                )

        # Concat strategy is as safe as it will ever be. We hope the server
        # side did not reorder the results across queries.
        logger.info(
            "Using the concat strategy, which is not guaranteed reliable if "
            "the census API returned data for multiple sub-queries of less than "
            f"or equal to {_MAX_VARIABLES_PER_DOWNLOAD} in different row orders. "
            f"It is always safest to query no more than {_MAX_VARIABLES_PER_DOWNLOAD} "
            "variables at a time. Please do so unless you really need them all."
        )

        __dw_strategy_metrics["concat"] = __dw_strategy_metrics["concat"] + 1

        df_data = pd.concat(
            [dfs[0]] + [df.drop(geo_key_variables, axis="columns") for df in dfs[1:]],
            axis="columns",
        )

    return df_data


__shapefile_root: Union[str, None] = None
__shapefile_readers: Dict[int, cmap.ShapeReader] = {}


def set_shapefile_path(shapefile_path: Union[str, None]) -> None:
    """
    Set the path to the directory to cache shapefiles.

    This is where we will cache shapefiles downloaded when
    `with_geometry=True` is passed to :py:func:`~download`.

    Parameters
    ----------
    shapefile_path
        The path to use for caching shapefiles.
    """
    global __shapefile_root

    __shapefile_root = shapefile_path


def get_shapefile_path() -> Union[str, None]:
    """
    Get the path to the directory to cache shapefiles.

    This is where we will cache shapefiles downloaded when
    `with_geometry=True` is passed to :py:func:`~download`.

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
    Deprecated version of :py:ref:`~download`; use `download` instead.

    Same functionality but under the old name. Back in the pre-history
    of `censusdis`, this function started life as a way to download
    ACS detail tables. It evolved significantly since then and does much
    more now. Hence the name change.

    This function will disappear completely in a future version.
    """
    warnings.warn(
        "censusdis.data.download_detail is deprecated. "
        "Please use censusdis.data.download instead.",
        DeprecationWarning,
        2,
    )
    return download(
        dataset,
        year,
        download_variables,
        with_geometry=with_geometry,
        api_key=api_key,
        variable_cache=variable_cache,
        **kwargs,
    )


def download(
    dataset: str,
    year: int,
    download_variables: Optional[Union[str, Iterable[str]]] = None,
    *,
    group: Optional[Union[str, Iterable[str]]] = None,
    leaves_of_group: Optional[Union[str, Iterable[str]]] = None,
    skip_annotations: bool = True,
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

    *A note on variables and groups*: there are multiple ways to specify the
    variables you want to download, either individually in `download_variables`,
    by one or more groups in `group`, and by the leaves of one or more groups
    in `leaves_of_group`. Note that these three sources af variables are
    deduplicated, so you will only get one column for a variable no matter
    how many times it is specified.

    Parameters
    ----------
    dataset
        The dataset to download from. For example `acs/acs5` or
        `dec/pl`.
    year
        The year to download data for.
    download_variables
        The census variables to download, for example `["NAME", "B01001_001E"]`.
    group
        One or more groups (as defined by the U.S. Census for the data set)
        whose variable values should be downloaded. These are in addition to
        any specified in `download_variables`.
    leaves_of_group
        One or more groups (as defined by the U.S. Census for the data set)
        whose leaf variable values should be downloaded.These are in addition to
        any specified in `download_variables` or `group`. See
        :py:meth:`VariableCache.group_leaves` for more details on the semantics of
        leaves vs. non-leaf group variables.
    skip_annotations
        If `True` try to filter out `group` or `leaves_of_group` variables that are
        annotations rather than actual values. See :py:meth:`VariableCache.group_variables`
        for more details. Variable names passed in `download_variables` are not
        affected by this flag.
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

    # Turn the variables we were given into a list if they are not already.
    if download_variables is None:
        download_variables = []
    elif isinstance(download_variables, str):
        download_variables = [download_variables]
    elif not isinstance(download_variables, list):
        download_variables = list(download_variables)

    if group is None:
        group = []
    elif isinstance(group, str):
        group = [group]

    if leaves_of_group is None:
        leaves_of_group = []
    elif isinstance(leaves_of_group, str):
        leaves_of_group = [leaves_of_group]

    # Add group variables and leaves as appropriate.
    group_variables: List[str] = []
    for group_name in group:
        group_variables = group_variables + variable_cache.group_variables(
            dataset, year, group_name, skip_annotations=skip_annotations
        )

    group_leaf_variables: List[str] = []
    for group_name in leaves_of_group:
        group_leaf_variables = group_leaf_variables + variable_cache.group_leaves(
            dataset, year, group_name, skip_annotations=skip_annotations
        )

    # Concatenate them all.
    download_variables = download_variables + group_variables + group_leaf_variables

    # Dedup and maintain order.
    download_variables = list(dict.fromkeys(download_variables))

    # Special case if we are trying to get too many fields.
    if len(download_variables) > _MAX_VARIABLES_PER_DOWNLOAD:
        return _download_multiple(
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

    url, params, bound_path = census_table_url(
        dataset, year, download_variables, api_key=api_key, **string_kwargs
    )
    df_data = data_from_url(url, params)

    for field in download_variables:
        # predicateType does not exist in some older data sets like acs/acs3
        # So in that case we just go with what we got in the JSON. But if we
        # have it try to set the type.
        if "predicateType" in variable_cache.get(dataset, year, field):
            field_type = variable_cache.get(dataset, year, field)["predicateType"]

            if field_type == "int":
                if df_data[field].isnull().any():
                    # Some Census data sets put in null in int fields.
                    # We have to go with a float to make this a NaN.
                    # Int has no representation for NaN or None.
                    df_data[field] = df_data[field].astype(float, errors="ignore")
                else:
                    try:
                        df_data[field] = df_data[field].astype(int)
                    except ValueError:
                        # Sometimes census metadata says int, but they
                        # put in float values anyway, so fall back on
                        # trying to get them as floats.
                        df_data[field] = df_data[field].astype(float, errors="ignore")
            elif field_type == "float":
                df_data[field] = df_data[field].astype(float)
            elif field_type == "string":
                pass
            else:
                # Leave it as an object?
                pass

    download_variables_upper = [dv.upper() for dv in download_variables]

    # Put the geo fields (STATE, COUNTY, etc...) that came back up front.
    df_data = df_data[
        [col for col in df_data.columns if col not in download_variables_upper]
        + download_variables_upper
    ]

    if with_geometry:
        # We need to get the geometry and merge it in.
        geo_level = bound_path.path_spec.path[-1]
        shapefile_scope = bound_path.bindings[bound_path.path_spec.path[0]]

        gdf_data = _add_geography(df_data, year, shapefile_scope, geo_level)
        return gdf_data

    return df_data


def census_table_url(
    dataset: str,
    year: int,
    download_variables: Iterable[str],
    *,
    api_key: Optional[str] = None,
    **kwargs: cgeo.InSpecType,
) -> Tuple[str, Mapping[str, str], cgeo.BoundGeographyPath]:
    """
    Construct the URL to download data from the U.S. Census API.

    Parameters
    ----------
    dataset
        The dataset to download from. For example `acs/acs5` or
        `dec/pl`.
    year
        The year to download data for.
    download_variables
        The census variables to download, for example `["NAME", "B01001_001E"]`.
    api_key
        An optional API key. If you don't have or don't use a key, the number
        of calls you can make will be limited.
    kwargs
        A specification of the geometry that we want data for.

    Returns
    -------
        The URL, parameters and bound path.

    """
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
        dataset, year, list(download_variables), bound_path, api_key=api_key
    )

    url, params = query_spec.table_url()

    return url, params, bound_path


variables = VariableCache()
