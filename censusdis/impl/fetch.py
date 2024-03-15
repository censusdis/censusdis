# Copyright (c) 2022 Darren Erik Vengroff
"""Utilities for loading census data."""
from contextlib import contextmanager
from logging import getLogger
from typing import Any, Mapping, Optional, Union, Tuple, Generator

import pandas as pd
import requests

from censusdis.impl.exceptions import CensusApiException

logger = getLogger(__name__)


class CertificateManager:
    """Manage the certificates and verification flags used when we make calls to the U.S. Census servers."""

    def __init__(
        self,
        *,
        data_verify: Union[bool, str] = True,
        data_cert: Optional[Union[str, Tuple[str, str]]] = None,
        map_verify: Union[bool, str] = True,
        map_cert: Optional[Union[str, Tuple[str, str]]] = None,
    ):
        """
        Manage the certificates and verification flags used when we make calls to the U.S. Census servers.

        Parameters
        ----------
        data_verify
            Value to pass to `requests.get` in the `verify=` argument for data API calls to `https://api.census.gov`.
        data_cert
            Value to pass to `requests.get` in the `cert=` argument for data API calls to `https://api.census.gov`.
        map_verify
            Value to pass to `requests.get` in the `verify=` argument for getting map data with calls to
            `https://www2.census.gov`.
        map_cert
            Value to pass to `requests.get` in the `cert=` argument for getting map data with calls to
            `https://www2.census.gov`.
        """
        self._data_verify = data_verify
        self._data_cert = data_cert
        self._map_verify = map_verify
        self._map_cert = map_cert

    @property
    def data_verify(self) -> Union[bool, str]:
        """Value to pass to `requests.get` in the `verify=` argument for data API calls to `https://api.census.gov`."""
        return self._data_verify

    @data_verify.setter
    def data_verify(self, value: Union[bool, str]):
        self._data_verify = value

    @property
    def data_cert(self) -> Union[str, Tuple[str, str], None]:
        """Value to pass to `requests.get` in the `cert=` argument for data API calls to `https://api.census.gov`."""
        return self._data_cert

    @data_cert.setter
    def data_cert(self, value: Union[str, Tuple[str, str], None]):
        self._data_cert = value

    @property
    def map_verify(self) -> Union[bool, str]:
        """Value to pass to `requests.get` in the `verify=` argument for getting map data with calls to `https://www2.census.gov`."""
        return self._map_verify

    @map_verify.setter
    def map_verify(self, value: Union[bool, str]):
        self._map_verify = value

    @property
    def map_cert(self) -> Union[str, Tuple[str, str], None]:
        """Value to pass to `requests.get` in the `cert=` argument for getting map data with calls to `https://www2.census.gov`."""
        return self._map_cert

    @map_cert.setter
    def map_cert(self, value: Union[str, Tuple[str, str], None]):
        self._map_cert = value

    @contextmanager
    def use(
        self,
        *,
        data_verify: Union[bool, str] = True,
        data_cert: Optional[Union[str, Tuple[str, str]]] = None,
        map_verify: Union[bool, str] = True,
        map_cert: Optional[Union[str, Tuple[str, str]]] = None,
    ):
        """Use certificates and verification flags within a context."""
        saved_data_verify = self.data_verify
        saved_data_cert = self.data_cert
        saved_map_verify = self.map_verify
        saved_map_cert = self.map_cert

        self.data_verify = data_verify
        self.data_cert = data_cert
        self.map_verify = map_verify
        self.map_cert = map_cert

        try:
            yield None
        finally:
            self.data_verify = saved_data_verify
            self.data_cert = saved_data_cert
            self.map_verify = saved_map_verify
            self.map_cert = saved_map_cert


certificates = CertificateManager()


def json_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> Any:
    """Get json from a URL."""
    request = requests.get(
        url, params=params, cert=certificates.data_cert, verify=certificates.data_verify
    )

    if request.status_code == 200:
        parsed_json = request.json()
        return parsed_json

    # Do our best to tell the user something informative.
    raise CensusApiException(
        f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
    )


def data_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> pd.DataFrame:
    """Get json from a URL and parse into a data frame."""
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
