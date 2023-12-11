# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for Combined Statistical Area symbols."""

import unittest

import censusdis.csa


class CsaTestCase(unittest.TestCase):
    """Tests for Combined Statistical Area symbols."""
    
    def test_combined_statistical_areas(self):
        """Test combined_statistical_area."""
        symbols = [
            symbol
            for symbol, val in censusdis.csa.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(175, sym_count)
