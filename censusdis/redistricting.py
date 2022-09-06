from typing import Dict, Iterable, List, Optional, Tuple, Union

import pandas as pd
import requests

from .censusdata import census_data, GeoFilterType


# Different group names were used in 2000.
_2000_GROUP_NAMES = {
    "P1": "PL001",
    "P2": "PL002",
}


def metadata(
    year: int, group: str = "P2"
) -> Tuple[Dict[str, str], str, Dict[str, List[str]]]:
    """
    Get metadata about the fields available in a given
    redistricting data group in a given year.

    Parameters
    ----------
    year
        Must be 2000, 2010, or 2020.
    group
        The group, e.g. 'P1', 'P2', .... See
        https://www.census.gov/programs-surveys/decennial-census/about/rdo/summary-files.html
        for more details.
    Returns
    -------
        field_names
            A dictionary of field names and their descriptions. This does not include
            the total population field. So when data is queried the sum of all these fields
            should be the same as the totla field.
         total_field
            The name of the field containing total population.
         fields_by_race
            Fields grouped by the race that members are, or are in combination
            with other races.
    """
    # Unfortunately 'dec/pl' is not accepted by
    # censusdata.censustable, so we have to do things
    # a little more manually.
    #
    # metadata = censusdata.censustable('dec/pl', year, 'P1')

    if year == 2000:
        group = _2000_GROUP_NAMES[group]

    request = requests.get(
        "https://api.census.gov/data/{:04d}/dec/pl/groups/{:}/".format(year, group)
    )
    metadata = request.json()

    field_names = {}

    black_fields = []
    white_fields = []
    asian_fields = []
    native_american_fields = []
    hawaiian_fields = []

    hispanic_latino_fields = []

    black_alone_fields = []
    white_alone_fields = []
    asian_alone_fields = []
    native_american_alone_fields = []
    hawaiian_alone_fields = []

    two_or_more_races = []

    total_field = ""

    # The rules here embed knowledge of the naming
    # schemes used in 2010 and 2020, which differ.
    for k, v in metadata["variables"].items():
        if not k.endswith("ERR"):
            if (k.endswith("001") or k.endswith("001N")) and ("Total" in v["label"]):
                total_field = k
            if v["label"] != "Total":
                if not v["label"].startswith("Annotation"):
                    components = v["label"].split("!!")

                    if not components[-1].endswith("race"):
                        if components[-1] != "Not Hispanic or Latino":
                            if "two or more races" in components[-1].lower():
                                field_names[k] = components[-1]
                                two_or_more_races.append(k)
                            elif not components[-1].endswith("races"):
                                if not components[-1].endswith(":"):
                                    field_names[k] = components[-1]
                                    if (
                                        "Black" in components[-1]
                                        or "black" in components[-1]
                                    ):
                                        black_fields.append(k)
                                        if "alone" in components[-1]:
                                            black_alone_fields.append(k)

                                    if (
                                        "White" in components[-1]
                                        or "white" in components[-1]
                                    ):
                                        white_fields.append(k)
                                        if "alone" in components[-1]:
                                            white_alone_fields.append(k)

                                    if (
                                        "Asian" in components[-1]
                                        or "asian" in components[-1]
                                    ):
                                        asian_fields.append(k)
                                        if "alone" in components[-1]:
                                            asian_alone_fields.append(k)

                                    if (
                                        "Native" in components[-1]
                                        or "native" in components[-1]
                                    ):
                                        if (
                                            "Alaska" in components[-1]
                                            or "alaska" in components[-1]
                                        ):
                                            native_american_fields.append(k)
                                            if "alone" in components[-1]:
                                                native_american_alone_fields.append(k)
                                        elif (
                                            "Hawaiian" in components[-1]
                                            or "hawaiian" in components[-1]
                                        ):
                                            hawaiian_fields.append(k)
                                            if "alone" in components[-1]:
                                                hawaiian_alone_fields.append(k)

                                    if "Hispanic or Latino" in components[-1]:
                                        hispanic_latino_fields.append(k)

    fields_by_race = {
        "black": black_fields,
        "white": white_fields,
        "asian": asian_fields,
        "american_indian_and_alaska_native": native_american_fields,
        "native_hawaiian_and_other_pacific_islander": hawaiian_fields,
        "hispanic_or_latino": hispanic_latino_fields,
        "black_alone": black_alone_fields,
        "white_alone": white_alone_fields,
        "asian_alone": asian_alone_fields,
        "american_indian_and_alaska_native_alone": native_american_alone_fields,
        "native_hawaiian_and_other_pacific_islander_alone": hawaiian_alone_fields,
        "two_or_more_races": two_or_more_races,
    }

    return field_names, total_field, fields_by_race


def data(
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
    Get redistricting data.

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
    source = "dec/pl"

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
