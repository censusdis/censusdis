# Copyright (c) 2022 Darren Erik Vengroff
"""
Utilities for loading census data.
"""

from logging import getLogger
from typing import Any, Mapping, Optional

import pandas as pd
import requests

from censusdis.impl.exceptions import CensusApiException

logger = getLogger(__name__)


def json_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> Any:
    request = requests.get(url, params=params)

    if request.status_code == 200:
        parsed_json = request.json()
        return parsed_json

    # Do our best to tell the user something informative.
    raise CensusApiException(
        f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
    )


def data_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> pd.DataFrame:
    logger.info(f"Downloading data from {url} with {params}.")

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
            columns=[
                c.upper()
                .replace(" ", "_")
                .replace("-", "_")
                .replace("/", "_")
                .replace("(", "")
                .replace(")", "")
                for c in parsed_json[0]
            ],
        )

    raise CensusApiException(
        f"Expected json data to be a list of lists, not a {type(parsed_json)}"
    )
