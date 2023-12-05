# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for `censusdis.data`."""
import unittest

import pandas as pd

import censusdis.data as ced
from censusdis import CensusApiException


class TestFilters(unittest.TestCase):
    """Test that we can properly convert geo filters to strings."""

    def test_filter_none(self):
        """Test the None arg."""
        self.assertIsNone(ced._gf2s(None))

    def test_filter_str(self):
        """Test with a string."""
        self.assertEqual("013", ced._gf2s("013"))

    def test_filter_list(self):
        """Test with a list."""
        self.assertEqual("013", ced._gf2s(["013"]))
        self.assertEqual("013,014", ced._gf2s(["013", "014"]))
        self.assertEqual("013,014,015", ced._gf2s(["013", "014", "015"]))


class InferGeoTestCase(unittest.TestCase):
    """Test our ability to infer geometry from column names."""

    def test_infer_geo_state(self):
        """Match in a df with state only."""
        df = pd.DataFrame([["34"]], columns=["STATE"])

        geo = ced.infer_geo_level(df)

        self.assertEqual("state", geo)

    def test_infer_geo_county(self):
        """Match in a df with state and county."""
        df = pd.DataFrame([["34", "013"]], columns=["STATE", "COUNTY"])

        geo = ced.infer_geo_level(df)

        self.assertEqual("county", geo)

    def test_infer_geo_bg(self):
        """Match in a df with state, county, tract and block group."""
        df = pd.DataFrame(
            [["34", "013", "019400", "1"]],
            columns=["STATE", "COUNTY", "TRACT", "BLOCK_GROUP"],
        )

        geo = ced.infer_geo_level(df)

        self.assertEqual("block group", geo)

    def test_infer_geo_no_match_county(self):
        """County without state is ambiguous and does not match."""
        df = pd.DataFrame([["013"]], columns=["COUNTY"])

        with self.assertRaises(CensusApiException):
            _ = ced.infer_geo_level(df)

    def test_infer_geo_no_match_block_group(self):
        """Missing state and county is ambiguous and does not match."""
        df = pd.DataFrame([["019400", "1"]], columns=["TRACT", "BLOCK_GROUP"])

        with self.assertRaises(CensusApiException) as cm:
            _ = ced.infer_geo_level(df)

        # Make sure the text is informative.
        self.assertIn(
            "Was not able to locate any of the known sets of columns", str(cm.exception)
        )
        self.assertIn("in the columns ['TRACT', 'BLOCK_GROUP']", str(cm.exception))

    def test_infer_geo_no_match_block_group_partial(self):
        """Missing state and county is ambiguous and does not match."""
        df = pd.DataFrame(
            [["34", "019400", "1"]], columns=["STATE", "TRACT", "BLOCK_GROUP"]
        )

        with self.assertRaises(CensusApiException) as cm:
            _ = ced.infer_geo_level(df)

        # Make sure the text is informative.
        self.assertIn("matched state on columns ['STATE']", str(cm.exception))
        self.assertIn("partially matched", str(cm.exception))
        self.assertIn("['STATE', 'COUNTY', 'TRACT']", str(cm.exception))
        self.assertIn("['STATE', 'COUNTY', 'TRACT', 'BLOCK_GROUP']", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
