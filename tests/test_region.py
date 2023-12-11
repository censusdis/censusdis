# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for Region symbols."""

import unittest

import censusdis.region


class RegionTestCase(unittest.TestCase):
    """Tests for Region symbols."""

    def test_regions(self):
        """Test region."""
        symbols = [
            symbol
            for symbol, val in censusdis.region.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(4, sym_count)
