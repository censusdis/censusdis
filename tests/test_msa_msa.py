# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for Metropolitan Statistical Area Micropolitan Statistical Area symbols."""

import unittest

import censusdis.msa_msa


class Msa_MsaTestCase(unittest.TestCase):
    """Tests for Metropolitan Statistical Area Micropolitan Statistical Area symbols."""

    def test_metropolitan_statistical_area_micropolitan_statistical_areas(self):
        """Test metropolitan_statistical_area_micropolitan_statistical_area."""

        symbols = [
            symbol
            for symbol, val in censusdis.msa_msa.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(939, sym_count)
