import censusdata
import pandas as pd
from typing import Iterable, List, Optional, Tuple, Union


def geo_state(geo):
    d = dict(geo.params())
    return d["state"]


def geo_county(geo):
    d = dict(geo.params())
    return d["county"]


def geo_cousub(geo):
    d = dict(geo.params())
    return d["county subdivision"]


def geo_tract(geo):
    d = dict(geo.params())
    return d["tract"]


def geo_block_group(geo):
    d = dict(geo.params())
    return d["block group"]


def geo_block(geo):
    d = dict(geo.params())
    return d["block"]


_VALID_RESOLUTIONS = ("block", "block group", "tract", "county subdivision", "county")


def resolutions() -> Iterable[str]:
    """
    Return a list of valid resolutions for the `resolution`
    argument of :py:func:`~censusdis.redistricting.data`
    and similar.

    Returns
    -------
        The valid resolulions.
    """
    return _VALID_RESOLUTIONS


# This is the type we can accept for geographic
# filters. When provided, these filters are either
# single values as a string, or, if multivalued,
# then an iterable containing all the values allowed
# by the filter.
GeoFilterType = Optional[Union[str, Iterable[str]]]


def _gf2s(filter: GeoFilterType) -> Optional[str]:
    """
    Utility to convert a filter to a string.

    For the Census API, multiple values are encoded
    in a single comma separated string.
    """
    if filter is None or isinstance(filter, str):
        return filter
    return ",".join(filter)


def census_data(
    source: str,
    state: Union[str, Iterable[str]],
    year: int,
    resolution: str,
    census_fields: Iterable[str],
    *,
    county: GeoFilterType = None,
    tract: GeoFilterType = None,
    cousub: GeoFilterType = None,
    block_group: GeoFilterType = None,
    block: GeoFilterType = None,
    key: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch census data from the remote API. Normally this is not
    called directly, but rather via higher-level APIs like
    :py:func:`~censusdis.redistricting.data`.

    Parameters
    ----------
    state
        The state to get data for.
    source
        The census data source to use, for example, `"dec/pl"` for
        redistricting date.
    year
        What year? 2000, 2010, or 2020
    resolution
        The lowest resolution data we want. The return value
        will have a row for each unique value of this, and
        the outer geographies that contain it. Accepted values
        are `"block"`, `"block group"`, `"tract"`, `"county subdivision"`,
        and `"county"`.
    census_fields
        What fields do we want. Typically these are fields returned by
        :py:func:`~metadata`.
    county
        A county filter.
    tract
        A census tract filter.
    cousub
        A county subdivision filter.
    block_group
        A block group filter.
    block
        A block filter.
    key
        A Census API key to be used when calling the US Census API. See
        https://api.census.gov/data/key_signup.html to request one if you
        don't have one.

    Returns
    -------
        Counts of the membership of each field filtered as specified by
        the various parameters.
    """
    if resolution not in _VALID_RESOLUTIONS:
        raise ValueError(
            "resolution {resolution} is not valid. "
            f"Please use one of {_VALID_RESOLUTIONS}. "
        )

    if not isinstance(census_fields, list):
        census_fields = list(census_fields)

    geo, county, cousub, tract, block_group, block = _normalize_geography(
        resolution,
        state=state,
        county=county,
        cousub=cousub,
        tract=tract,
        block_group=block_group,
        block=block,
    )

    df = censusdata.download(
        source,
        year,
        geo,
        census_fields,
        key=key,
    )

    df = _augment_geography(
        df,
        census_fields=census_fields,
        county=county,
        cousub=cousub,
        tract=tract,
        block_group=block_group,
        block=block,
    )

    return df


def _normalize_geography(
    resolution: str,
    state: Union[str, Iterable[str]],
    county: str,
    cousub: Optional[str],
    tract: Optional[str],
    block_group: Optional[str],
    block: Optional[str],
) -> Tuple[
    censusdata.censusgeo,
    str,
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
]:
    """
    A helper function for normalizing geography.

    Broken out mainly so it can be tested without making
    any brittle remote calls to the US Census API.
    """
    county = _gf2s(county)
    cousub = _gf2s(cousub)
    tract = _gf2s(tract)
    block_group = _gf2s(block_group)
    block = _gf2s(block)

    geo = [
        ("state", _gf2s(state)),
    ]
    # If we don't have a filter at the resolution level,
    # make it a wildcard.
    if resolution == "county" and county is None:
        county = "*"
    if resolution == "county subdivision" and cousub is None:
        cousub = "*"
    if resolution == "tract" and tract is None:
        tract = "*"
    if resolution == "block group" and block_group is None:
        block_group = "*"
    if resolution == "block" and block is None:
        block = "*"
    # Below county resolution we always need a "*" for county.
    if county is None:
        county = "*"
    # Put all of our filters into the geo.
    if county is not None:
        geo.append(("county", county))
    if cousub is not None:
        geo.append(("county subdivision", cousub))
    if tract is not None:
        geo.append(("tract", tract))
    if block_group is not None:
        geo.append(("block group", block_group))
    if block is not None:
        geo.append(("block", block))

    geo = censusdata.censusgeo(geo)

    return geo, county, cousub, tract, block_group, block


def _augment_geography(
    df: pd.DataFrame,
    census_fields: List[str],
    county: str,
    cousub: Optional[str],
    tract: Optional[str],
    block_group: Optional[str],
    block: Optional[str],
) -> pd.DataFrame:
    """
    A helper function for augmenting geography.

    Broken out mainly so it can be tested without making
    any brittle remote calls to the US Census API.
    """

    # There is a little magic here as far as rules go
    # for what geographic hierarchies nest. The two
    # options are:
    #
    # STATE : COUNTY : COUSUB
    # STATE : COUNTY : TRACT : BLOCK_GROUP : BLOCK
    #
    # For either case we want to pull the all
    # the fields from the narrowest one that was specified
    # all the way out to state so that we can
    # properly identify every row of data returned.
    #
    # To further complicate things, block group is
    # encoded in block and sometimes has to be pulled
    # out to make it more convenient for later analysis.

    add_cousub = cousub is not None
    add_county = county is not None or add_cousub

    add_block = block is not None
    add_block_group = block_group is not None
    add_tract = tract is not None or add_block_group or add_block

    # A list of the columns in the order we want them.
    cols = ["STATE"]

    df["STATE"] = df.index.map(geo_state)

    if add_county:
        cols.append("COUNTY")
        df["COUNTY"] = df.index.map(geo_county)
    if add_cousub:
        cols.append("COUSUB")
        df["COUSUB"] = df.index.map(geo_cousub)
    if add_tract:
        cols.append("TRACT")
        df["TRACT"] = df.index.map(geo_tract)
    if add_block_group or add_block:
        cols.append("BLOCK_GROUP")
        if add_block_group:
            df["BLOCK_GROUP"] = df.index.map(geo_block_group)
    if add_block:
        cols.append("BLOCK")
        df["BLOCK"] = df.index.map(geo_block)

    if add_block and not add_block_group:
        # The block group is the first digit of the block.
        df["BLOCK_GROUP"] = df["BLOCK"].apply(lambda b: b[0])

    df.reset_index(inplace=True, drop=True)

    # Put the columns in a nice order.

    df = df[cols + census_fields]

    return df
