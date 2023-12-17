"""Details of how U.S. Census shapefiles and their contents are named."""
from typing import Dict, Callable, Tuple, Optional, List, Generator

import pandas as pd

from censusdis import CensusApiException


_GEO_QUERY_FROM_DATA_QUERY_INNER_GEO: Dict[
    str,
    Callable[[int], Tuple[Optional[str], str, List[str], List[str]]],
] = {
    # innermost geo: ( shapefile_scope, shapefile_geo_name, df_on, gdf_on )
    "region": lambda year: ("us", "region", ["REGION"], ["REGIONCE"]),
    "division": lambda year: ("us", "division", ["DIVISION"], ["DIVISIONCE"]),
    "combined statistical area": lambda year: (
        "us",
        "csa",
        ["COMBINED_STATISTICAL_AREA"],
        ["CSAFP"],
    ),
    "metropolitan statistical area/micropolitan statistical area": lambda year: (
        "us",
        "cbsa",
        ["METROPOLITAN_STATISTICAL_AREA_MICROPOLITAN_STATISTICAL_AREA"],
        ["CBSAFP"],
    ),
    "state": lambda year: ("us", "state", ["STATE"], ["STATEFP"]),
    "consolidated city": lambda year: (
        "us",
        "concity",
        ["STATE", "CONSOLIDATED_CITY"],
        ["STATEFP", "CONCTYFP"],
    ),
    "county": lambda year: (
        "us",
        "county",
        ["STATE", "COUNTY"],
        ["STATEFP", "COUNTYFP"],
    ),
    "public use microdata area": lambda year: (
        "us",
        "puma10" if year < 2020 else "puma20",
        ["STATE", "PUBLIC_USE_MICRODATA_AREA"],
        ["STATEFP", "PUMACE"] if year < 2020 else ["STATEFP20", "PUMACE20"],
    ),
    "congressional district": lambda year: (
        "us",
        _congressional_district_from_year(year),
        ["STATE", "CONGRESSIONAL_DISTRICT"],
        ["STATEFP", f"{_congressional_district_from_year(year).upper()}FP"],
    ),
    "zip code tabulation area": lambda year: (
        "us",
        "zcta520" if year >= 2020 else "zcta510",
        ["ZIP_CODE_TABULATION_AREA"],
        ["ZCTA5CE10" if year < 2020 else "ZCTA5CE20" if year == 2020 else "ZCTA5CE"],
    ),
    # For these, the shapefiles are at the state level, so `None`
    # indicates that we have to fill it in based on the geometry
    # being queried.
    "county subdivision": lambda year: (
        None,
        "cousub",
        ["STATE", "COUNTY_SUBDIVISION"],
        ["STATEFP", "COUSUBFP"],
    ),
    "place": lambda year: (None, "place", ["STATE", "PLACE"], ["STATEFP", "PLACEFP"]),
    "tract": lambda year: (
        None,
        "tract",
        ["STATE", "COUNTY", "TRACT"],
        ["STATEFP", "COUNTYFP", "TRACTCE"],
    ),
    "block group": lambda year: (
        None,
        "bg",
        ["STATE", "COUNTY", "TRACT", "BLOCK_GROUP"],
        ["STATEFP", "COUNTYFP", "TRACTCE", "BLKGRPCE"],
    ),
    "block": lambda year: (
        None,
        "tabblock",
        ["STATE", "COUNTY", "TRACT", "BLOCK"],
        ["STATEFP", "COUNTYFP", "TRACTCE", "BLOCKCE"],
    ),
    "school district (unified)": lambda year: (
        None,
        "unsd",
        ["STATE", "SCHOOL_DISTRICT_UNIFIED"],
        ["STATEFP", "UNSDLEA"],
    ),
    "school district (elementary)": lambda year: (
        None,
        "sde",
        ["STATE", "SCHOOL_DISTRICT_ELEMENTARY"],
        ["STATEFP", "ESDLEA"],
    ),
    "school district (secondary)": lambda year: (
        None,
        "sde",
        ["STATE", "SCHOOL_DISTRICT_SECONDARY"],
        ["STATEFP", "SSDLEA"],
    ),
    "state legislative district (upper chamber)": lambda year: (
        None,
        "sldu",
        ["STATE", "STATE_LEGISLATIVE_DISTRICT_UPPER_CHAMBER"],
        ["STATEFP", "SLDUST"],
    ),
    "state legislative district (lower chamber)": lambda year: (
        None,
        "sldl",
        ["STATE", "STATE_LEGISLATIVE_DISTRICT_LOWER_CHAMBER"],
        ["STATEFP", "SLDLST"],
    ),
    "voting district": lambda year: (
        None,
        "vtd",
        ["STATE", "COUNTY", "VOTING_DISTRICT"],
        ["STATEFP20", "COUNTYFP20", "VTDST20"]
        if year >= 2020
        else ["STATEFP10", "COUNTYFP10", "VTDST10"],
    ),
}
"""
Helper map for the _with_geometry case.

A map from the innermost level of a geometry specification
to the arguments we need to pass to `get_cb_shapefile`
to get the right shapefile for the geography and the columns
we need to join the data and shapefile on.

Most values are tuples, but a few are functions of the year.
If a value is callable, then we call it with the year as an
argument to get the final value. This is necessary for e.g.
congressional districts, which have names that change every
two years.

We should add everything in
https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
to this map.
"""


def geo_query_from_data_query_inner_geo(
    year: int, geo_level: str
) -> Tuple[Optional[str], str, List[str], List[str]]:
    """
    Map lookup and call the value if it is callable to produce the result.

    Parameters
    ----------
    year
        The year to pass to callable values.
    geo_level
        The key to look up.

    Returns
    -------
        A tuple of results.
    """
    if geo_level not in _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO:
        raise CensusApiException(
            "The with_geometry=True flag is only allowed if the "
            f"geometry for the data to be loaded ('{geo_level}') is one of "
            f"{list(_GEO_QUERY_FROM_DATA_QUERY_INNER_GEO.keys())}."
        )

    return _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO[geo_level](year)


def geo_query_from_data_query_inner_geo_items(
    year: int,
) -> Generator[Tuple[Optional[str], str, List[str], List[str]], None, None]:
    """Generate the items in `GEO_QUERY_FROM_DATA_QUERY_INNER_GEO`."""
    for geo_level in _GEO_QUERY_FROM_DATA_QUERY_INNER_GEO:
        yield geo_level, geo_query_from_data_query_inner_geo(year, geo_level)


def _congressional_district_from_year(year: int) -> str:
    """Construct the short form of the congressional district used in a given year."""
    # See the files in https://www2.census.gov/geo/tiger/GENZ2020/shp/
    # and similar. The interesting ones are of the form
    #
    # cb_20YY_us_cdCCC_500k.zip
    #
    # where YY is the year and CCC is the congressional district
    # used.
    #
    # The mappings are not exactly at two year intervals as we would expect.
    if year == 2020 or year == 2021:
        # For some reason they did not update to cd117 for these years. Pandemic?
        return "cd116"

    # Regular year rule.
    congress = 104 + (year - 1994) // 2
    return f"cd{congress}"


def infer_geo_level(year: Optional[int], df_data: pd.DataFrame) -> str:
    """
    Infer the geography level based on columns names.

    Parameters
    ----------
    year
        The vintage of the data. `None` to infer from the data.
    df_data
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

    for k, (_, _, df_on, _) in geo_query_from_data_query_inner_geo_items(year):
        if all(col in df_data.columns for col in df_on):
            # Full match. We want the longest full match
            # we find.
            if match_key is None or len(df_on) > match_on_len:
                match_key = k
        elif df_on[-1] in df_data.columns:
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
            f"{tuple(df_on for _, (_, _, df_on, _) in geo_query_from_data_query_inner_geo_items(year))} "
            f"in the columns {list(df_data.columns)}."
        )

    if partial_match_keys:
        raise CensusApiException(
            f"Unable to infer geometry. Geometry matched {match_key} on columns "
            f"{geo_query_from_data_query_inner_geo(year, match_key)[2]} "
            "but also partially matched one or more candidates "
            f"{tuple(geo_query_from_data_query_inner_geo(year, k)[2] for k in partial_match_keys)}. "
            "Partial matches are usually unintended. Either add columns to allow a "
            "full match or rename some columns to prevent the undesired partial match."
        )

    return match_key
