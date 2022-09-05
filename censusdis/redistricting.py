from typing import Iterable, Optional

import pandas as pd
import requests

from .censusdata import census_data, GeoFilterType


# Different group names were used in 2000.
_2000_GROUP_NAMES = {
    "P1": "PL001",
    "P2": "PL002",
}


def metadata(year: int, group: str = "P2"):
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
    state: str,
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
