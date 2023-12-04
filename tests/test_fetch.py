"""Tests for the fetch implementation."""
import unittest

import pandas as pd

import censusdis.impl.fetch
from censusdis import CensusApiException


class ParseCensusJsonTestCase(unittest.TestCase):
    """Tests of parsing census JSON."""

    def test_parse_json(self):
        """Test parsing JSON."""
        # This is an example of what comes back in JSON
        # form from the census API.
        parsed_json = [
            ["B01001_001E", "state", "county", "tract"],
            ["1959", "01", "001", "020200"],
            ["2527", "01", "001", "021000"],
        ]

        # This is what we should turn that into. Note the
        # use of the header row for column names and that we
        # capitalize them.
        expected_df = pd.DataFrame(
            [
                ["1959", "01", "001", "020200"],
                ["2527", "01", "001", "021000"],
            ],
            columns=["B01001_001E", "STATE", "COUNTY", "TRACT"],
        )

        df = censusdis.impl.fetch._df_from_census_json(parsed_json)

        self.assertTrue((df == expected_df).all().all())

    def test_parse_bad_json(self):
        """Test with malformed JSON."""
        with self.assertRaises(CensusApiException):
            censusdis.impl.fetch._df_from_census_json([])


if __name__ == "__main__":
    unittest.main()
