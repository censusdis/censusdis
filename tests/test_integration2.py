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
from censusdis.datasets import CBP, EWKS
from censusdis.states import NJ


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


if __name__ == "__main__":
    unittest.main()
