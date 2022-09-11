#

import censusdata
from typing import Iterable, Optional, Union

import pandas as pd

from .censusdata import census_data, GeoFilterType


def metadata(
    year: int,
    survey_years: int,
    group: str,
):
    fields = censusdata.censustable(f"acs{survey_years}", year, group)

    total_field = [f for f, v in fields.items() if v["label"].endswith("!!Total:")][0]
    leaf_fields = [f for f, v in fields.items() if not v["label"].endswith(":")]
    subtotal_fields = [
        f
        for f, v in fields.items()
        if v["label"].endswith(":") and not v["label"].endswith("!!Total:")
    ]

    return (
        {f: v["label"] for f, v in fields.items()},
        total_field,
        subtotal_fields,
        leaf_fields,
    )


def data(
    state: Union[str, Iterable[str]],
    year: int,
    survey_years: int,
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
    Get acs data.

    The filter parameter allow the caller to specify that they want to filter
    the geographic regions for which data is returned down to one or more
    specific values. For example, using the county and tract filters with::

        import censusdis.redistricting as crd
        from censusdis.states import STATE_NJ

        df_soma = crd.data(
            STATE_NJ,
            2020,
            "block",
            field_names,
            county='013',
            tract=['0019000', '0019100'],
            key=CENSUS_API_KEY,
        )

    would load data for every block in two particular census tracts in Essex
    County, NJ (whose id is `"013"`).

    Parameters
    ----------
    state
        What state do we want data for?
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
    # See https://api.census.gov/data/2020/dec/pl.html
    # Examples at https://api.census.gov/data/2020/dec/pl/examples.html
    source = f"acs/acs{survey_years}"

    return census_data(
        source,
        state,
        year,
        resolution,
        census_fields,
        county=county,
        tract=tract,
        cousub=cousub,
        block_group=block_group,
        block=block,
        key=key,
    )
