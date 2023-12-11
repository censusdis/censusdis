# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for Division symbols."""

import unittest

import censusdis.division


class DivisionTestCase(unittest.TestCase):
    """Tests for Division symbols."""

    def test_divisions(self):
        """Test division."""

        symbols = [
            symbol
            for symbol, val in censusdis.division.__dict__.items()
            if not symbol.startswith("__") and isinstance(val, str)
        ]
        sym_count = len(symbols)

        self.assertEqual(9, sym_count)
