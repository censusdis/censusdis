"""Tests for the state lists in censusdis.states."""

import unittest

from censusdis import states


class StatesTestCase(unittest.TestCase):
    """Tests for the state lists."""

    def test_all_states(self):
        """ALL_STATES has the 50 states and neither DC nor PR."""
        self.assertEqual(50, len(states.ALL_STATES))
        self.assertNotIn(states.DC, states.ALL_STATES)
        self.assertNotIn(states.PR, states.ALL_STATES)

    def test_all_states_and_dc(self):
        """ALL_STATES_AND_DC adds DC but not PR."""
        self.assertEqual(51, len(states.ALL_STATES_AND_DC))
        self.assertIn(states.DC, states.ALL_STATES_AND_DC)
        self.assertNotIn(states.PR, states.ALL_STATES_AND_DC)

    def test_all_states_dc_and_pr(self):
        """ALL_STATES_DC_AND_PR adds DC and PR."""
        self.assertEqual(52, len(states.ALL_STATES_DC_AND_PR))
        self.assertIn(states.DC, states.ALL_STATES_DC_AND_PR)
        self.assertIn(states.PR, states.ALL_STATES_DC_AND_PR)


if __name__ == "__main__":
    unittest.main()
