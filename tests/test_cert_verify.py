"""
Test that we can pass verify and cert through our API to requests.get.

The overall strategy here is to use `unittest.mock` to intercept calls
to `requests.get` and make sure that the `cert` and `verify` arguments we
pass in through public `censusdis` APIs make it down to them. Since these
APIs typically end up making several calls to `requests.get`, we don't go
to the trouble of trying to completely mock out their return values. Instead,
we pass the arguments on to the real `requests.get` after filtering out
the `cert` and `verify` arguments we just verified.

These tests are designed to be run in an environment where `cert` and `verify`
are not actually needed. In an environment where they are needed, things will
probably fail as we filter them out before making the actual call.
"""

import unittest
from contextlib import contextmanager
from typing import Union, Optional, Tuple
from unittest import mock

import geopandas as gpd
import pandas as pd
from requests import Response
from requests import get as requests_get

import censusdis.data as ced
from censusdis.datasets import ACS5


@contextmanager
def verify_requests_gets(
    test_case,
    *,
    data_verify: Union[bool, str] = True,
    data_cert: Optional[Union[str, Tuple[str, str]]] = None,
    map_verify: Union[bool, str] = True,
    map_cert: Optional[Union[str, Tuple[str, str]]] = None,
):
    """Verify that `cert` and `verify` flags make it down to `request.get` call in a context."""

    def verified_requests_get(url: str, *args, **kwargs) -> Response:
        """Verify that we got the verify and cert we expected, then return actual `requests.get` results."""
        if url.startswith("https://api.census.gov"):
            # This is the data case.

            # Make sure it was set to what we set it to.
            test_case.assertEqual(data_verify, ced.certificates.data_verify)
            test_case.assertEqual(data_cert, ced.certificates.data_cert)
            # Make sure the args came through.
            test_case.assertEqual(data_verify, kwargs["verify"])
            test_case.assertEqual(data_cert, kwargs["cert"])
        elif url.startswith("https://www.census.gov") or url.startswith(
            "https://www2.census.gov"
        ):
            # This is the map case.

            # Make sure it was set to what we set it to.
            test_case.assertEqual(map_verify, ced.certificates.map_verify)
            test_case.assertEqual(map_cert, ced.certificates.map_cert)
            # Make sure the args came through.
            test_case.assertEqual(map_verify, kwargs["verify"])
            test_case.assertEqual(map_cert, kwargs["cert"])
        else:
            test_case.fail(f"Unexpected URL {url}")

        # Note we drop `verify` and `cert` here. Hopefully we are
        # running tests in an environment where they are not
        # needed.
        kwargs2 = {k: v for k, v in kwargs.items() if k not in ["verify", "cert"]}
        return requests_get(url, *args, **kwargs2)

    with ced.certificates.use(
        data_verify=data_verify,
        data_cert=data_cert,
        map_verify=map_verify,
        map_cert=map_cert,
    ):
        with mock.patch("requests.get", side_effect=verified_requests_get):
            yield


class VerifyCertTestCase(unittest.TestCase):
    """Test that we pass `verify` and `cert` from `ced.download` through to `requests.get`."""

    def test_download_with_defaults(self) -> None:
        """Make sure default cert and verify values are as expected in calls to `requests.get`."""
        with verify_requests_gets(self):
            df_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
            )

            self.assertIsInstance(df_states, pd.DataFrame)
            self.assertEqual((52, 2), df_states.shape)

    def test_download_with_verify_false(self) -> None:
        """Make sure a modified verify value is as expected in calls to `requests.get`."""
        with verify_requests_gets(self, data_verify=False):
            df_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
            )

            self.assertIsInstance(df_states, pd.DataFrame)
            self.assertEqual((52, 2), df_states.shape)

    def test_download_with_cert(self) -> None:
        """Make sure a modified cert value is as expected in calls to `requests.get`."""
        cert = "THE_CERTIFICATE"

        with verify_requests_gets(self, data_cert=cert):
            df_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
            )

            self.assertIsInstance(df_states, pd.DataFrame)
            self.assertEqual((52, 2), df_states.shape)

    def test_download_with_map_with_cert(self) -> None:
        """Make sure a modified cert value is as expected in calls to `requests.get`."""
        data_cert = "DATA_CERTIFICATE"
        map_cert = "MAP_CERTIFICATE"

        with verify_requests_gets(self, data_cert=data_cert, map_cert=map_cert):
            gdf_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
                with_geometry=True,
            )

            self.assertIsInstance(gdf_states, gpd.GeoDataFrame)
            self.assertEqual((52, 3), gdf_states.shape)

    # FIX #270
    # See similar test in test_integration.py. Working with census.data@census.gov
    # to resolve.
    @unittest.skip(
        reason='Since 4/24/2024. server producing "failed with status 500. '
        "There was an error while running your query. "
        "We've logged the error and we'll correct it ASAP.  Sorry for the inconvenience."
    )
    def test_wide_download_with_cert(self) -> None:
        """Make sure the cert gets through multiples downloads."""
        dataset = "acs/acs1/spp"
        year = 2019
        group = "S0201"

        cert = "THE_CERTIFICATE"

        with verify_requests_gets(self, data_cert=cert):
            variables = ced.variables.group_variables(
                dataset,
                year,
                group,
                skip_annotations=False,
            )

            self.assertGreater(len(variables), ced._MAX_VARIABLES_PER_DOWNLOAD)

            metrics_0 = ced._download_wide_strategy_metrics()

            df = ced.download(dataset, year, variables, state="*")

            self.assertEqual((51, 1 + len(variables)), df.shape)

            metrics_1 = ced._download_wide_strategy_metrics()

            metrics_diff = {k: v - metrics_0[k] for k, v in metrics_1.items()}

            self.assertEqual(1, metrics_diff["merge"])
            self.assertEqual(0, metrics_diff["concat"])

    def test_metadata(self):
        """Test that the metadata APIs pass cert correctly down the stack."""
        cert = "THE_CERTIFICATE"

        with verify_requests_gets(self, data_cert=cert):
            df_all_datasets = ced.variables.all_data_sets()

            self.assertEqual(6, len(df_all_datasets.columns))

            df_groups = ced.variables.all_groups(ACS5, 2020)

            self.assertEqual(4, len(df_groups.columns))

            df_variables = ced.variables.all_variables(ACS5, 2020, "B03001")

            self.assertEqual(7, len(df_variables.columns))


class CertificateTestCase(unittest.TestCase):
    """Test passing the correct certificates for the census servers."""

    def _download_and_assert(self):
        gdf_states = ced.download(
            dataset=ACS5,
            vintage=2020,
            download_variables="NAME",
            state="22",
            with_geometry=True,
        )

        self.assertIsInstance(gdf_states, gpd.GeoDataFrame)
        self.assertEqual((1, 3), gdf_states.shape)

    def test_default(self):
        """Test a normal download with no certificates."""
        self._download_and_assert()

    def test_no_verify(self):
        """Test without verification on either the data or the map."""
        with ced.certificates.use(data_verify=False, map_verify=False):
            self._download_and_assert()


if __name__ == "__main__":
    unittest.main()
