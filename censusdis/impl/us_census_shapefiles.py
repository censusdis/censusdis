# Copyright (c) 2023 Darren Erik Vengroff
"""
Details of how U.S. Census shapefiles and their contents are named.

Also includes utilities for managing downloaded shapefiles and
for water clipping.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Callable, Tuple, Optional, List, Generator, Union
from logging import getLogger

import geopandas as gpd
import pandas as pd

from censusdis import CensusApiException, maps as cmap
from censusdis.impl.geometry import drop_slivers_from_gdf
from censusdis.impl.varsource.base import VintageType


logger = getLogger(__name__)


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
    "american indian area/alaska native area/hawaiian home land": lambda year: (
        "us",
        "aiannh",
        ["AMERICAN_INDIAN_AREA_ALASKA_NATIVE_AREA_HAWAIIAN_HOME_LAND"],
        ["AIANNHCE"],
    ),
    "new england city and town area": lambda year: (
        "us",
        "necta",
        ["NEW_ENGLAND_CITY_AND_TOWN_AREA"],
        ["NECTAFP"],
    ),
    # For these, the shapefiles are at the state level, so `None`
    # indicates that we have to fill it in based on the geometry
    # being queried.
    "county subdivision": lambda year: (
        None,
        "cousub",
        ["STATE", "COUNTY_SUBDIVISION"],
        ["STATEFP", "COUSUB" if year == 2010 else "COUSUBFP"],
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
        # CB files from 2016 on exist with the "elsd" name and "ELSDLEA" column.
        # Earlier tiger files use the name "sda" and "ESDLEA" column.
        None,
        "elsd" if year >= 2016 else "sde",
        ["STATE", "SCHOOL_DISTRICT_ELEMENTARY"],
        ["STATEFP", "ELSDLEA" if year >= 2016 else "ESDLEA"],
    ),
    "school district (secondary)": lambda year: (
        # Similar scenario to school district (secondary).
        None,
        "scsd" if year >= 2016 else "sde",
        ["STATE", "SCHOOL_DISTRICT_SECONDARY"],
        ["STATEFP", "SCSDLEA" if year >= 2016 else "SSDLEA"],
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
        (
            ["STATEFP20", "COUNTYFP20", "VTDST20"]
            if year >= 2020
            else ["STATEFP10", "COUNTYFP10", "VTDST10"]
        ),
    ),
    # This one could be a little dangerous if subminor civil
    # divisions exist in states and are not mapped as subbarios.
    # It appears the only example of this is the ESTATE in the
    # USVI. So we are going to punt for the moment and deal with
    # it at some future time, probably by adding an arg to the
    # lambdas to take in the bound params so we can look at them.
    #
    # Noted in https://github.com/vengroff/censusdis/issues/223.
    "subminor civil division": lambda year: (
        None,
        "subbarrio",
        ["STATE", "COUNTY", "COUNTY_SUBDIVISION", "SUBMINOR_CIVIL_DIVISION"],
        ["STATEFP", "COUNTYFP", "COUSUBFP", "SUBMCDFP"],
    ),
    "alaska native regional corporation": lambda year: (
        None,
        "anrc",
        ["ALASKA_NATIVE_REGIONAL_CORPORATION"],
        ["ANRCFP"],
    ),
}
"""
Helper map for the _with_geometry case.

A map from the innermost level of a geometry specification
to the arguments we need to pass to `get_cb_shapefile`
to get the right shapefile for the geography and the columns
we need to join the data and shapefile on.

The values are functions of the year. Once we locate one, we
call it with the year as an argument to get the final value.
This is necessary for e.g. congressional districts, which have
names that change every two years. It also turns out to be very
helpful in dealing with little quirks in the data like changing
the name of the COUSUB/COSUBFP column in just one year.

We should add everything in
https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
to this map.
"""


def geo_query_from_data_query_inner_geo(
    year: int, geo_level: str
) -> Tuple[Optional[str], str, List[str], List[str]]:
    """
    Map lookup and call the for the give year to produce the result.

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


def _geo_query_from_data_query_inner_geo_items(
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

    for k, (_, _, df_on, _) in _geo_query_from_data_query_inner_geo_items(year):
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
            f"{tuple(df_on for _, (_, _, df_on, _) in _geo_query_from_data_query_inner_geo_items(year))} "
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


def add_geography(
    df_data: pd.DataFrame,
    year: Optional[VintageType],
    shapefile_scope: str,
    geo_level: str,
) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
    """
    Add geography to data.

    Parameters
    ----------
    df_data
        The data we downloaded from the census API
    year
        The year for which to fetch geometries. We need this
        because they change over time. If `None`, look for a
        `'YEAR'` column in `df_data` and possibly add different
        geometries for different years as needed.
    shapefile_scope
        The scope of the shapefile. This is typically either a state
        such as `NJ` or the string `"us"`.
    geo_level
        The geography level we want to add.

    Returns
    -------
        A GeoDataFrame with the original data and an
        added geometry column for each row.
    """
    (
        query_shapefile_scope,
        shapefile_geo_level,
        df_on,
        gdf_on,
    ) = geo_query_from_data_query_inner_geo(year, geo_level)

    # If the query spec has a hard-coded value then we use it.
    if query_shapefile_scope is not None:
        shapefile_scope = query_shapefile_scope

    def individual_shapefile(sub_scope: str, query_year: int) -> gpd.GeoDataFrame:
        """Read the relevant shapefile and add a YEAR column to it."""
        try:
            gdf = __shapefile_reader(query_year).try_cb_tiger_shapefile(
                sub_scope, shapefile_geo_level
            )
            gdf["YEAR"] = query_year
            return gdf
        except cmap.MapException as ex:
            # If there are some years where we can't find a shapefile,
            # skip over it and those rows will not have geometry in the
            # final result.
            logger.info(
                "Unable to load shapefile for scope %s for year %d",
                sub_scope,
                query_year,
                exc_info=ex,
            )
            return gpd.GeoDataFrame()

    # If there is a single defined year then we can load the single
    # shapefile. If not, then we have to load multiple shapefiles,
    # one per year, and concatenate them.
    #
    # Whether there is a single or multiple years, there could also
    # me mutliple scopes, e.g. states, for which we have to download
    # shapefiles. If so, by the time we get here, they are encoded in
    # one string with comma separators.
    if isinstance(year, int):
        gdf_shapefile = pd.concat(
            individual_shapefile(sub_scope, year)
            for sub_scope in shapefile_scope.split(",")
        )
        merge_gdf_on = gdf_on
    else:
        gdf_shapefile = pd.concat(
            individual_shapefile(sub_scope, unique_year)
            for unique_year in df_data["YEAR"].unique()
            for sub_scope in shapefile_scope.split(",")
        )

        merge_gdf_on = ["YEAR"] + gdf_on
        df_on = ["YEAR"] + df_on

    if len(gdf_shapefile.index) == 0:
        # None of the years matched, so we add None for geometry to all.
        gdf = gpd.GeoDataFrame(df_data, copy=True)
        gdf.set_geometry([None for _ in gdf.index], inplace=True)
        return gdf

    if "TRACT" in df_data.columns:
        df_data["TRACT"] = df_data["TRACT"].str.ljust(
            6, "0"
        )  # Pre 2010 data has inconsistencies in TRACT string length

    gdf_data = gdf_shapefile[merge_gdf_on + ["geometry"]].merge(
        df_data, how="right", left_on=merge_gdf_on, right_on=df_on
    )

    # Get the columns we want in a reasonable order matching
    # how they are in the data, with geometry at the end.
    gdf_data = gdf_data[list(df_data.columns) + ["geometry"]]

    # Rearrange columns so geometry is at the end.
    gdf_data = gdf_data[
        [col for col in gdf_data.columns if col != "geometry"] + ["geometry"]
    ]

    return gdf_data


@dataclass
class _ShapefileRoot:
    """A private class to stash the root we will use to cache shapefiles locally."""

    shapefile_root: Optional[Path] = None


__shapefile_root = _ShapefileRoot()
__shapefile_readers: Dict[int, cmap.ShapeReader] = {}


def set_shapefile_path(shapefile_path: Union[Path, None]) -> None:
    """
    Set the path to the directory to cache shapefiles.

    This is where we will cache shapefiles downloaded when
    `with_geometry=True` is passed to :py:func:`~download`.

    Parameters
    ----------
    shapefile_path
        The path to use for caching shapefiles.
    """
    __shapefile_root.shapefile_root = shapefile_path


def get_shapefile_path() -> Union[Path, None]:
    """
    Get the path to the directory to cache shapefiles.

    This is where we will cache shapefiles downloaded when
    `with_geometry=True` is passed to :py:func:`~download`.

    Returns
    -------
        The path to use for caching shapefiles.
    """
    return __shapefile_root.shapefile_root


def __shapefile_reader(year: int):
    reader = __shapefile_readers.get(year, None)

    if reader is None:
        reader = cmap.ShapeReader(
            __shapefile_root.shapefile_root,
            year,
        )

        __shapefile_readers[year] = reader

    return reader


def _identify_counties(gdf_geo: gpd.GeoDataFrame, year: int):
    """
    Take a geodataframe and identify which US counties the supplied geography overlaps.

    Parameters
    ----------
    gdf_geo
        A GeoDataFrame containing polygons within the United States
    year
        The year for which to fetch geometries. We need this
        because they change over time.

    Returns
    -------
        A list of five digit county FIPS codes.
    """
    # Some dataframes will contain the county column already
    if "STATE" in gdf_geo and "COUNTY" in gdf_geo:
        fips_codes = gdf_geo["STATE"] + gdf_geo["COUNTY"]

        return fips_codes.unique().tolist()
    # Otherwise, we load all the US counties and perform an overlap operation
    else:
        reader = __shapefile_readers.get(year)
        us_counties = reader.read_cb_shapefile("us", "county")
        us_counties["FIPS"] = us_counties["STATEFP"] + us_counties["COUNTYFP"]

        county_overlap = us_counties.overlay(gdf_geo, keep_geom_type=False)
        fips_codes = county_overlap["STATEFP"] + county_overlap["COUNTYFP"]

        return fips_codes.unique().tolist()


def clip_water(
    gdf_geo: gpd.GeoDataFrame,
    year: int,
    minimum_area_sq_meters: int = 10000,
    sliver_threshold=0.01,
):
    """
    Remove water from input `GeoDataFrame`.

    Parameters
    ----------
    gdf_geo
        The GeoDataFrame from which we want to remove water
    year
        The year for which to fetch geometries. We need this
        because they change over time.
    minimum_area_sq_meters
        The minimimum size of a water area to be removed

    Returns
    -------
        A GeoDataFrame with the water areas larger than
        the specified threshold removed.
    """
    counties = _identify_counties(gdf_geo, year)
    gdf_water = _retrieve_water(counties, year)

    gdf_without_water = _water_difference(gdf_geo, gdf_water, minimum_area_sq_meters)

    original_crs = gdf_without_water.crs
    gdf_without_water = drop_slivers_from_gdf(
        gdf_without_water.to_crs(epsg=3857), threshold=sliver_threshold
    ).to_crs(original_crs)

    return gdf_without_water


def _retrieve_water(county_fips_codes: list[str], year: int):
    """
    Load `AREAWATER` files from tiger for specified counties.

    Parameters
    ----------
    county_FIPS_codes
        A list of five digit county FIPS codes

    Returns
    -------
        A GeoDataFrame containing the census defined water in the supplied counties
    """
    reader = __shapefile_readers.get(year)

    gdf_water = pd.concat(
        reader.read_shapefile(shapefile_scope=county, geography="areawater")
        for county in county_fips_codes
    )
    # Geo pandas has no concat method, so we convert from a pandas df
    gdf_water = gpd.GeoDataFrame(gdf_water)
    return gdf_water


def _water_difference(
    gdf_geo: gpd.GeoDataFrame, gdf_water: gpd.GeoDataFrame, minimum_area_sq_meters: int
):
    """
    Remove water polygons exceeding minimum size from supplied `GeoDataFrame`.

    Parameters
    ----------
    gdf_geo
        A GeoDataFrame containing polygons within the United States
    gdf_water
        A GeoDataFrame containing census AREAWATER polygons
    minimum_area_sq_meters
        The smallest water polygon to be removed, specified in square meters

    Returns
    -------
        A version of gdf_geo with the water areas removed
    """
    # Combining polygons speeds up the overlay operation
    geo_combined_water = gdf_water[
        gdf_water["AWATER"] >= minimum_area_sq_meters
    ].unary_union
    gdf_combined_water = gpd.GeoDataFrame(geometry=[geo_combined_water])
    gdf_combined_water = gdf_combined_water.set_crs(gdf_water.crs)

    return gdf_geo.overlay(
        gdf_combined_water,
        "difference",
        keep_geom_type=False,
    )
