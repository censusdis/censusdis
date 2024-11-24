# Copyright (c) 2023 Darren Erik Vengroff
"""Test LODES data."""
import unittest

import censusdis.data as ced
from censusdis.datasets import (
    LODES_OD_MAIN_JT00,
    LODES_OD_AUX_JT00,
    LODES_WAC_S000_JT05,
    LODES_RAC_SI03_JT03,
)
from censusdis.states import NJ
from censusdis.counties.new_jersey import ESSEX


class LodesTestCase(unittest.TestCase):
    """Test downloading LODES data."""

    def test_download_lodes_state(self):
        """Test download_lodes()."""
        df_lodes = ced.download(LODES_OD_MAIN_JT00, 2020, state=NJ)

        self.assertEqual((1, 11), df_lodes.shape)

    def test_download_lodes_county(self):
        """Test download_lodes() for a single county."""
        df_lodes = ced.download(LODES_OD_AUX_JT00, 2020, state=NJ, county=ESSEX)

        self.assertEqual((1, 12), df_lodes.shape)

    def test_download_lodes_counties(self):
        """Test download_lodes() for all counties in a state."""
        df_lodes = ced.download(LODES_RAC_SI03_JT03, 2020, state=NJ, county="*")

        self.assertEqual((21, 43), df_lodes.shape)

    def test_download_lodes_tracts_in_state(self):
        """Test download_lodes() for all tracts in a state."""
        df_lodes = ced.download(LODES_WAC_S000_JT05, 2020, state=NJ, tract="*")

        self.assertEqual((537, 54), df_lodes.shape)

    def test_download_lodes_tracts_in_county(self):
        """Test download_lodes() for all tracts in a county."""
        df_lodes = ced.download(LODES_OD_AUX_JT00, 2020, state=NJ, county=ESSEX, tract="*")

        self.assertEqual((208, 13), df_lodes.shape)

    def test_download_lodes_blocks_in_county(self):
        """Test download_lodes() for all tracts in a county."""
        df_lodes = ced.download(LODES_OD_AUX_JT00, 2020, state=NJ, county=ESSEX, block="*")

        self.assertEqual((2225, 14), df_lodes.shape)


if __name__ == "__main__":
    unittest.main()
