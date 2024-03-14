"""Test that we can pass verify and cert through our API to requests.get."""

import unittest
from typing import Callable, Union, Optional, Tuple
from unittest import mock

from requests import get as requests_get
from requests import Response

import geopandas as gpd

import censusdis.data as ced
from censusdis.datasets import ACS5


def verified_requests_get_side_effect(
    test_case,
    expected_verify: Union[bool, str],
    expected_cert: Optional[Union[str, Tuple[str, str]]],
) -> Callable:
    """
    Create a function to verify that a call to requests.get has the `verify` and `cert` args we expect.

    The function verifies that the args are as we expect, then it strips them off, calls
    `requests.get` normally with the other args, and returns the result.

    This is intended to be used with `unittest.mock.patch`.
    Note that although we are using `unittest.mock` tooling around this function, it is not
    a classic mock. It ends up calling the function it is mocking, but it verifies that the
    args are as expected before it does so.
    """

    def verified_requests_get(
        url: str,
        *args,
        verify: Union[bool, str] = True,
        cert: Optional[Union[str, Tuple[str, str]]] = None,
        **kwargs
    ) -> Response:
        """Verify that we got the verify and cert we expected, then return actual `requests.get` results."""

        # These should have been passed all the way down the stack.
        test_case.assertEqual(expected_verify, verify)
        test_case.assertEqual(expected_cert, cert)

        # Note we drop `verify` and `cert` here. Hopefully we are
        # running tests in an environment where they are not
        # needed.
        return requests_get(url, *args, **kwargs)

    return verified_requests_get


class VerifyCertTestCase(unittest.TestCase):
    """Test that we pass `verify` and `cert` from `ced.download` through to `requests.get`."""

    def test_download_with_defaults(self) -> None:
        with mock.patch(
            "requests.get",
            side_effect=verified_requests_get_side_effect(self, True, None),
        ):
            gdf_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
                with_geometry=True,
            )

            self.assertIsInstance(gdf_states, gpd.GeoDataFrame)
            self.assertEqual((52, 3), gdf_states.shape)

    def test_download_with_verify_false(self) -> None:
        with mock.patch(
            "requests.get",
            side_effect=verified_requests_get_side_effect(self, False, None),
        ):
            gdf_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
                with_geometry=True,
                verify=False,
            )

            self.assertIsInstance(gdf_states, gpd.GeoDataFrame)
            self.assertEqual((52, 3), gdf_states.shape)

    def test_download_with_cert(self) -> None:
        cert = "my_certificate_file.pem"

        with mock.patch(
            "requests.get",
            side_effect=verified_requests_get_side_effect(self, True, cert),
        ):
            gdf_states = ced.download(
                dataset=ACS5,
                vintage=2020,
                download_variables="NAME",
                state="*",
                with_geometry=True,
                cert=cert,
            )

            self.assertIsInstance(gdf_states, gpd.GeoDataFrame)
            self.assertEqual((52, 3), gdf_states.shape)

    def test_wide_download_with_cert(self) -> None:
        """Make sure the cert gets through multiples downloads."""
        dataset = "acs/acs1/spp"
        year = 2019
        group = "S0201"

        cert = "my_certificate_file.pem"

        with mock.patch(
            "requests.get",
            side_effect=verified_requests_get_side_effect(self, True, cert),
        ):
            variables = ced.variables.group_variables(
                dataset, year, group, skip_annotations=False, cert=cert
            )

            self.assertGreater(len(variables), ced._MAX_VARIABLES_PER_DOWNLOAD)

            metrics_0 = ced._download_wide_strategy_metrics()

            df = ced.download(dataset, year, variables, state="*", cert=cert)

            self.assertEqual((51, 1 + len(variables)), df.shape)

            metrics_1 = ced._download_wide_strategy_metrics()

            metrics_diff = {k: v - metrics_0[k] for k, v in metrics_1.items()}

            self.assertEqual(1, metrics_diff["merge"])
            self.assertEqual(0, metrics_diff["concat"])

    def test_metadata(self):
        """Test that the metadata APIs pass cert correctly down the stack."""

        cert = "my_certificate_file.pem"

        with mock.patch(
            "requests.get",
            side_effect=verified_requests_get_side_effect(self, True, cert),
        ):
            df_all_datasets = ced.variables.all_data_sets(cert=cert)

            self.assertEqual(5, len(df_all_datasets.columns))

            df_groups = ced.variables.all_groups(ACS5, 2020, cert=cert)

            self.assertEqual(4, len(df_groups.columns))

            df_variables = ced.variables.all_variables(ACS5, 2020, "B03001", cert=cert)

            self.assertEqual(7, len(df_variables.columns))


class UnMockedTestCase(unittest.TestCase):
    """
    This repeats the tests above but passes `verify=False` through to `requests.get`.

    This should work even in environments where there are not firewalls or proxies
    mucking around with certs.
    """

    def test_download_with_verify_false(self) -> None:
        gdf_states = ced.download(
            dataset=ACS5,
            vintage=2020,
            download_variables="NAME",
            state="*",
            with_geometry=True,
            verify=False,
        )

        self.assertIsInstance(gdf_states, gpd.GeoDataFrame)
        self.assertEqual((52, 3), gdf_states.shape)


if __name__ == "__main__":
    unittest.main()
