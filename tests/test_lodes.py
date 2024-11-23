# Copyright (c) 2023 Darren Erik Vengroff
"""Test LODES data."""
import unittest

import censusdis.data as ced
from censusdis.datasets import LODES_OD_MAIN_JT00
from censusdis.states import NJ


class LodesTestCase(unittest.TestCase):
    """Test downloading LODES data."""

    def test_download_lodes(self):
        """Test download_lodes()."""
        df_lodes = ced.download(LODES_OD_MAIN_JT00, 2020, state=NJ)

        self.assertEqual((3_081_578, 13), df_lodes.shape)


if __name__ == "__main__":
    unittest.main()
