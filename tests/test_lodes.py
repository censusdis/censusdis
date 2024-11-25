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
from censusdis.states import NJ, NY
from censusdis.counties.new_jersey import ESSEX


class LodesTestCase(unittest.TestCase):
    """Test downloading LODES data."""

    def test_download_lodes_state(self):
        """Test download_lodes() for a single state."""
        df_lodes = ced.download(LODES_WAC_S000_JT05, 2020, state=NJ)

        self.assertEqual((1, 52), df_lodes.shape)

    def test_download_lodes_state_with_geometry(self):
        """Test download_lodes() for a single state."""
        df_lodes = ced.download(LODES_WAC_S000_JT05, 2020, state=NJ, with_geometry=True)

        self.assertEqual((1, 53), df_lodes.shape)

    def test_download_lodes_county(self):
        """Test download_lodes() for a single county."""
        df_lodes = ced.download(LODES_RAC_SI03_JT03, 2020, state=NJ, county=ESSEX)

        self.assertEqual((1, 43), df_lodes.shape)

    def test_download_lodes_counties(self):
        """Test download_lodes() for all counties in a state."""
        df_lodes = ced.download(LODES_RAC_SI03_JT03, 2020, state=NJ, county="*")

        self.assertEqual((21, 43), df_lodes.shape)

    def test_download_lodes_tracts_in_state(self):
        """Test download_lodes() for all tracts in a state."""
        df_lodes = ced.download(LODES_WAC_S000_JT05, 2020, state=NJ, tract="*")

        self.assertEqual((537, 54), df_lodes.shape)

    def test_download_lodes_state_to_state_main(self):
        """Test from state to itself."""
        df_lodes = ced.download(LODES_OD_MAIN_JT00, 2020, state=NJ, home_geography=True)

        # All workplaces are in NJ.
        self.assertTrue((df_lodes["STATE"] == NJ).all())

        # Only one row. NJ to NJ
        self.assertEqual((1, 12), df_lodes.shape)

        # All within the state.
        self.assertTrue((df_lodes["STATE"] == NJ).all())
        self.assertTrue((df_lodes["STATE_H"] == NJ).all())

    def test_download_lodes_anywhere_to_state_aux(self):
        """Test work in state from home in all states."""
        df_lodes = ced.download(
            LODES_OD_AUX_JT00,
            2020,
            state=NJ,
        )

        self.assertEqual((143878, 15), df_lodes.shape)

        # All workplaces in NJ
        self.assertTrue((df_lodes["STATE"] == NJ).all())

        # Residences in all states.
        self.assertEqual(50, len(df_lodes["STATE_H"].unique()))

    def test_download_lodes_state_to_state_aux_one_pair(self):
        """Test from state to another."""
        df_lodes = ced.download(
            LODES_OD_AUX_JT00, 2020, state=NJ, home_geography=dict(state=NY)
        )

        # NY to NJ
        self.assertEqual((1, 12), df_lodes.shape)

        # All workplaces in NJ; all homes in NY
        self.assertTrue((df_lodes["STATE"] == NJ).all())
        self.assertTrue((df_lodes["STATE_H"] == NY).all())

    def test_download_lodes_county_to_county(self):
        """Test download_lodes()."""
        df_lodes = ced.download(
            LODES_OD_MAIN_JT00, 2020, state=NJ, county="*", home_geography=True
        )

        # All within the state.
        self.assertTrue((df_lodes["STATE"] == NJ).all())
        self.assertTrue((df_lodes["STATE_H"] == NJ).all())

        # We see all 21 counties on both sides.
        self.assertEqual(21, len(df_lodes["COUNTY"].unique()))
        self.assertEqual(21, len(df_lodes["COUNTY_H"].unique()))

        # All pairs of 21 counties occur.
        self.assertEqual((21 * 21, 14), df_lodes.shape)

    def test_download_lodes_one_county_from_all_counties_in_state(self):
        """Test people commuting from all counties to one."""
        df_lodes = ced.download(
            LODES_OD_MAIN_JT00,
            2020,
            state=NJ,
            county=ESSEX,
            home_geography=dict(state=NJ, county="*"),
        )

        # All within the state.
        self.assertTrue((df_lodes["STATE"] == NJ).all())
        self.assertTrue((df_lodes["STATE_H"] == NJ).all())

        # We see one work county and all 21 home counties.
        self.assertEqual({ESSEX}, set(df_lodes["COUNTY"].unique()))
        self.assertEqual(21, len(df_lodes["COUNTY_H"].unique()))

        # To one county from 21 counties.
        self.assertEqual((21, 14), df_lodes.shape)

    def test_download_lodes_tracts_in_county(self):
        """Test download_lodes() for all tracts in a county to the same."""
        df_lodes = ced.download(
            LODES_OD_AUX_JT00, 2020, state=NJ, county=ESSEX, tract="*"
        )

        self.assertEqual((28465, 17), df_lodes.shape)

    def test_download_lodes_blocks_in_county(self):
        """Test download_lodes() for all blocks in a county to the same."""
        df_lodes = ced.download(
            LODES_OD_AUX_JT00, 2020, state=NJ, county=ESSEX, block="*"
        )

        self.assertEqual((28887, 18), df_lodes.shape)


if __name__ == "__main__":
    unittest.main()
