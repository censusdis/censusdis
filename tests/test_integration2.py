# Copyright (c) 2023-2024 Darren Erik Vengroff
"""
These are integration tests because they require access to the remote census API.

Most of the functionality can be unit tested elsewhere or with mocks, but
these tests actually call the census API itself to cover the bits of code
immediately around those calls.

This file is split off from test_integration.py so that we can do more testing
in parallel.
"""
import unittest
from pandas.testing import assert_frame_equal

import censusdis.data as ced
from censusdis.datasets import CBP, EWKS, ACS1
from censusdis.states import NJ, ALL_STATES_AND_DC

from censusdis.impl.exceptions import CensusApiException


class QueryFilterTestCase(unittest.TestCase):
    """Test queru filters."""

    def setUp(self):
        """Set up before each test."""
        self.dataset = CBP
        self.vintage = 2022

    def test_cbp_filter(self):
        """Test using a query filter."""
        df_filtered_cbp = ced.download(
            self.dataset,
            self.vintage,
            ["NAME", "ESTAB", "EMP", "PAYANN"],
            query_filter={"NAICS2017": "72251"},
            state=NJ,
            county="*",
        )

        # One row per county.
        self.assertEqual((21, 7), df_filtered_cbp.shape)

        self.assertSetEqual(
            {"STATE", "COUNTY", "NAME", "ESTAB", "EMP", "PAYANN", "NAICS2017"},
            set(df_filtered_cbp.columns),
        )

        self.assertTrue((df_filtered_cbp["NAICS2017"] == "72251").all())

        # Everything in the filtered should be in the unfiltered.
        df_unfiltered_cbp = ced.download(
            self.dataset,
            self.vintage,
            ["NAME", "ESTAB", "EMP", "PAYANN", "NAICS2017"],
            state=NJ,
            county="*",
        )

        self.assertSetEqual(
            set(df_unfiltered_cbp.columns), set(df_filtered_cbp.columns)
        )

        self.assertGreater(len(df_unfiltered_cbp.index), len(df_filtered_cbp.index))

        df_both = df_filtered_cbp.merge(
            df_unfiltered_cbp, on=list(df_filtered_cbp.columns)
        )

        assert_frame_equal(df_filtered_cbp, df_both)


class EwksTestCase(unittest.TestCase):
    """Test geographies of EWKS data set."""

    def test_ewks_geography(self):
        """Test geographies of EWKS data set."""
        year_to_geograpy_count = {
            1997: 6,
            2002: 10,
            2007: 10,
            2012: 11,
        }

        for year, count in year_to_geograpy_count.items():
            geographies = ced.geographies(EWKS, year)
            self.assertEqual(count, len(geographies))


class NoGeographyTestCase(unittest.TestCase):
    """Test a timeseries data set with no geography."""

    def test_exports_hs(self):
        """Test a timeseries data set with no geography."""
        dataset = "timeseries/intltrade/exports/hs"
        vintage = "timeseries"
        variables = ["YEAR", "MONTH", "ALL_VAL_MO", "VES_WGT_MO", "AIR_WGT_MO"]

        df_ts = ced.download(
            dataset,
            vintage,
            variables,
        )

        self.assertEqual(len(variables), df_ts.shape[1])


class BadApiKeyTestCase(unittest.TestCase):
    """Test with an invalid API key that still gets a 200."""

    def test_no_api_key(self):
        """
        Test with no API key.

        This version should work fine assuming we don't hit 500 calls a day.
        """
        df = ced.download(
            dataset=ACS1,
            vintage=2023,
            download_variables=["NAME"],
            state=NJ,
            api_key=None,
        )

        self.assertEqual((1, 2), df.shape)

    def test_bad_api_key(self):
        """Test with a bad API key."""
        with self.assertRaises(CensusApiException) as context:
            ced.download(
                dataset=ACS1,
                vintage=2023,
                download_variables=["NAME"],
                state=NJ,
                api_key="BOGUS API KEY",
            )

        self.assertIn("failed because your key is invalid.", str(context.exception))


class MispelledKeywordTestCase(unittest.TestCase):
    """
    Test that we get a good exception when we test a misspelled keyword.

    We don't want it to get confused for being a geo keyword.
    """

    def test_variable(self):
        """Test with variable= instead of download_variable=."""
        with self.assertRaises(CensusApiException) as ctx:
            ced.download(
                dataset=ACS1,
                vintage=2023,
                variables=["B25003_001E", "B25003_002E", "B25003_003E"],
                state=ALL_STATES_AND_DC,
            )
        self.assertTrue(
            str(ctx.exception).startswith(
                "\nThe following arguments are not recognized as non-geographic arguments "
                "or goegraphic arguments"
            )
        )
        self.assertIn("Supported geographies for dataset", str(ctx.exception))

    def test_bad_geo(self):
        """Test with variable= instead of download_variable=."""
        with self.assertRaises(CensusApiException) as ctx:
            ced.download(
                dataset=ACS1,
                vintage=2023,
                download_variables=["B25003_001E", "B25003_002E", "B25003_003E"],
                state=NJ,
                place="*",
                county="*",
            )
        self.assertTrue(
            str(ctx.exception).startswith(
                "\nUnable to match the geography specification {'state': '34', 'place': '*', 'county': '*'}."
            )
        )
        self.assertIn("Supported geographies for dataset", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
