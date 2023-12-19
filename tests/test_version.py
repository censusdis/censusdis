# Copyright (c) 2022-2023 Darren Erik Vengroff
"""Test censusdis.version."""
import unittest
import re

import censusdis


class VersionTestCase(unittest.TestCase):
    """Test censusdis.version."""

    def test_version(self):
        """Test censusdis.version."""
        version = censusdis.version

        # Version should be X.Y.Z with an optional + to indicate
        # an unreleased development version.
        pattern = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(\+?)$")

        self.assertTrue(pattern.match(version))


if __name__ == "__main__":
    unittest.main()
