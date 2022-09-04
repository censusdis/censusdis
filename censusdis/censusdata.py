import censusdata
import pandas as pd
from typing import Iterable, List, Optional, Tuple
import requests


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
    return _VALID_RESOLUTIONS


def census_data(
    source: str,
    state: str,
    year: int,
    resolution: str,
    census_fields: Iterable[str],
    *,
    county: Optional[str] = None,
    tract: Optional[str] = None,
    cousub: Optional[str] = None,
    block_group: Optional[str] = None,
    block: Optional[str] = None,
) -> pd.DataFrame:

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
    state: str,
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

    geo = [
        ("state", state),
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


def census_voting_field_metadata(census_field: str, year: int):
    baseurl = "https://api.census.gov/data"

    url = f"{baseurl}/{year}/cps/voting/nov/variables/{census_field}.json"

    r = requests.get(url)

    if r.status_code != 200:
        raise ValueError(
            f"{r.url} returned status code {r.status_code} and body:\n{r.text}"
        )

    metadata = r.json()

    return metadata


def census_voting_data(
    states: str, year: int, census_fields: List[str], weight_field: str = "PWSSWGT"
):
    baseurl = "https://api.census.gov/data"

    url = (
        f"{baseurl}/{year}/cps/voting/nov?tabulate=weight({weight_field})&row+for&row+"
        f"{'&row+'.join(census_fields)}&for=state:{states}"
    )

    r = requests.get(url)

    if r.status_code != 200:
        raise ValueError(
            f"{r.url} returned status code {r.status_code} and body:\n{r.text}"
        )

    data = r.json()

    field_values = {}

    for field in census_fields:
        metadata = census_voting_field_metadata(field, year)
        field_values[field] = metadata["values"]["item"]

    columns = data[0]
    values = [
        [
            field_values.get(column, {}).get(val, val)
            for column, val in zip(columns, row)
        ]
        for row in data[1:]
    ]

    df = pd.DataFrame(values, columns=columns)

    return df
