# Copyright (c) 2026 Mobility Solutions, Inc.
"""Test that censusdis advertises its inline type annotations."""

import unittest
from importlib.resources import files


class TypingTestCase(unittest.TestCase):
    """Test the PEP 561 package marker."""

    def test_py_typed_marker(self) -> None:
        """The installed package should expose its py.typed marker."""
        self.assertTrue((files("censusdis") / "py.typed").is_file())


if __name__ == "__main__":
    unittest.main()
