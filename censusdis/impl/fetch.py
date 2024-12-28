# Copyright (c) 2022 Darren Erik Vengroff
"""Utilities for loading census data."""
from logging import getLogger
from typing import Any, Mapping, Optional, Union, Tuple

import pandas as pd
import requests

from censusdis.impl.exceptions import CensusApiException

logger = getLogger(__name__)


class _CertificateManager:
    """Manage the certificates and verification flags used when we make calls to the U.S. Census servers."""

    _have_a_singletop_certificate_manager = False

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
        if self._have_a_singletop_certificate_manager:
            raise ValueError(
                "Cannot create a CertificateManager. Please use `censusdis.data.certificates`."
            )

        self._data_verify = data_verify
        self._data_cert = data_cert
        self._map_verify = map_verify
        self._map_cert = map_cert

        self._have_a_singletop_certificate_manager = True

    @property
    def data_verify(self) -> Union[bool, str]:
        """Value to pass to `requests.get` in the `verify=` argument for data from `https://api.census.gov`."""
        return self._data_verify

    @property
    def data_cert(self) -> Union[str, Tuple[str, str], None]:
        """Value to pass to `requests.get` in the `cert=` argument for data from `https://api.census.gov`."""
        return self._data_cert

    @property
    def map_verify(self) -> Union[bool, str]:
        """Value to pass to `requests.get` in the `verify=` argument for maps from `https://www2.census.gov`."""
        return self._map_verify

    @property
    def map_cert(self) -> Union[str, Tuple[str, str], None]:
        """Value to pass to `requests.get` in the `cert=` argument for maps from `https://www2.census.gov`."""
        return self._map_cert

    def use(
        self,
        *,
        data_verify: Union[bool, str] = True,
        data_cert: Optional[Union[str, Tuple[str, str]]] = None,
        map_verify: Union[bool, str] = True,
        map_cert: Optional[Union[str, Tuple[str, str]]] = None,
    ) -> "_CertificateManagerContext":
        """
        Set certificates and verification flags globally or within a context.

        If you want to set up certificate handling globally, you can just call this
        method alone, for example:

            import censusdis.data as ced

            ced.certificates.use(data_verify=False, map_verify=False)

        will turn off certificate verification for all data and map calls. This can by useful
        in a notebook environment, where you want to set up how certificates are handled once
        at the top of the notebook.

        If you want the effects to only be temporary, you can use a context manager with a `with`
        statement as follows::

            import censusdis.data as ced

            with ced.certificates.use(data_verify=False, map_verify=False):
                # No verification will be performed here.
                df = ced.download(...)

            # Upon exiting the context, verification is back on.
            df = ced.download(...)

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
        context = _CertificateManagerContext(self)
        self._data_verify = data_verify
        self._data_cert = data_cert
        self._map_verify = map_verify
        self._map_cert = map_cert
        return context


class _CertificateManagerContext:
    def __init__(self, certificate_manager: _CertificateManager):
        self._certificate_manager = certificate_manager
        self._data_verify = certificate_manager.data_verify
        self._data_cert = certificate_manager.data_cert
        self._map_verify = certificate_manager.map_verify
        self._map_cert = certificate_manager.map_cert

    def __enter__(self):
        pass

    def __exit__(self, type_, value, traceback):
        self._certificate_manager._data_verify = self._data_verify
        self._certificate_manager._data_cert = self._data_cert
        self._certificate_manager._map_verify = self._map_verify
        self._certificate_manager._map_cert = self._map_cert


certificates = _CertificateManager()
"""
A container for the certificates and verification flags used when we make calls to the U.S. Census servers.

Unless you are working behind a security proxy or firewall that manipulates certificates in
some way, you will never have to use this.

If you would not normally use the `verify=` or `cert=` arguments when using `requests.get` then
you need not worry about this. If you would, then use the values you would pass for accessing
`https://api.census.gov` or `https://www2.census.gov`.
"""


def json_from_url(url: str, params: Optional[Mapping[str, str]] = None) -> Any:
    """Get json from a URL."""
    request = requests.get(
        url, params=params, cert=certificates.data_cert, verify=certificates.data_verify
    )

    if request.status_code == 200:
        try:
            parsed_json = request.json()
            return parsed_json
        except requests.exceptions.JSONDecodeError:
            logger.debug(f"API call got 200 with unparseable JSON:\n{request.text}")
            if (
                "You included a key with this request, however, it is not valid."
                in request.text
            ):
                message = f"Census API request to {request.url} failed because your key is invalid."
            else:
                message = f"Census API request to {request.url} failed. Unable to parse returned JSON:\n{request.text}"
            raise CensusApiException(message)

    # Do our best to tell the user something informative.
    message = f"Census API request to {request.url} failed with status {request.status_code}. {request.text}"
    logger.debug(message)
    raise CensusApiException(message)


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
