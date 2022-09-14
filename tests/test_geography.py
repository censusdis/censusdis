import unittest

from censusdis.geography import CanonicalGeography


class CanonicalGeometryTestCase(unittest.TestCase):
    def test_init_raises(self):
        with self.assertRaises(ValueError):
            CanonicalGeography(["state"])

    def test_partial_match_self(self):
        # 150 is state:county:tract:block group,
        # which is not a prefix of anything else.
        cg = CanonicalGeography.by_number("150")
        kwargs = {k: "*" for k in cg.keys()}

        self.assertTrue(cg._partial_match(**kwargs))

        partial_matches = CanonicalGeography.partial_matches(**kwargs)

        self.assertEqual(1, len(partial_matches))
        self.assertEqual(cg, partial_matches["150"])

    def test_partial_match_no_match(self):
        cg = CanonicalGeography.by_number("101")

        self.assertFalse(cg._partial_match(unknown="*"))
        self.assertFalse(cg._partial_match(state="034", unknown="*"))
        self.assertFalse(cg._partial_match(is_prefix=False, unknown="*"))
        self.assertFalse(cg._partial_match(is_prefix=False, state="034", unknown="*"))

    def test_partial_match_underscore(self):
        # 150 is state:county:tract:block group,
        # which is not a prefix of anything else.
        cg = CanonicalGeography.by_number("150")

        self.assertTrue(cg._partial_match(state="34", block_group="12345"))
        self.assertTrue(cg._partial_match(is_prefix=False, block_group="12345"))

    def test_partial_matches(self):
        partial_matches = CanonicalGeography.partial_matches(state="034", county="*")
        for cg in partial_matches.values():
            self.assertIn("state", cg.path)
            self.assertIn("county", cg.path)

    def test_partial_prefix_match(self):
        num, cg = CanonicalGeography.partial_prefix_match(state="034", county="*")

        self.assertEqual("050", num)
        self.assertIs(CanonicalGeography.by_number("050"), cg)

    def test_partial_prefix_match_101(self):
        num, cg = CanonicalGeography.partial_prefix_match(state="034", block="*")

        self.assertEqual("101", num)
        self.assertIs(CanonicalGeography.by_number("101"), cg)

    def test_partial_prefix_match_140(self):
        num, cg = CanonicalGeography.partial_prefix_match(state="034", tract="*")

        self.assertEqual("140", num)
        self.assertIs(CanonicalGeography.by_number("140"), cg)

    def test_partial_prefix_match_150(self):
        num, cg = CanonicalGeography.partial_prefix_match(state="034", block_group="*")

        self.assertEqual("150", num)
        self.assertIs(CanonicalGeography.by_number("150"), cg)

    def test_full_match(self):
        num, cg = CanonicalGeography.full_match(state="*")
        self.assertEqual("040", num)
        self.assertIs(CanonicalGeography.by_number("040"), cg)

        num, cg = CanonicalGeography.full_match(
            state="34", county="013", tract="019013"
        )
        self.assertEqual("140", num)
        self.assertIs(CanonicalGeography.by_number("140"), cg)

    def test_full_match_none(self):
        num, cg = CanonicalGeography.full_match(unknown="*", other="foo")
        self.assertIsNone(num)
        self.assertIsNone(cg)

    def test_by_number_none(self):
        self.assertIsNone(CanonicalGeography.by_number("999"))

    def test_full_match_all(self):
        for num, cg in CanonicalGeography.ALL.items():
            num_match, cg_match = CanonicalGeography.full_match(
                **{k: "*" for k in cg.keys()}
            )
            self.assertEqual(num, num_match)
            self.assertIs(cg, cg_match)

    def test_fill_in(self):
        # 150 is state:county:tract:block group.
        cg = CanonicalGeography.by_number("150")

        with self.assertRaises(ValueError):
            cg.fill_in()

        with self.assertRaises(ValueError):
            cg.fill_in(state="34", county="013", county_subdivision="132")

        filled_in = cg.fill_in(state="34", county="013", block_group="*")

        self.assertEqual(
            {"state": "34", "county": "013", "tract": "*", "block group": "*"}, filled_in
        )

        filled_in = cg.fill_in(**filled_in)

        self.assertEqual(
            {"state": "34", "county": "013", "tract": "*", "block group": "*"}, filled_in
        )

        filled_in = cg.fill_in(
            state="34", county="013", tract="012345", block_group="3"
        )

        self.assertEqual(
            {"state": "34", "county": "013", "tract": "012345", "block group": "3"}, filled_in
        )

    def test_fill_partial_prefix_match(self):
        num, cg = CanonicalGeography.partial_prefix_match(state="34", block_group="*")

        self.assertEqual("150", num)

        filled_in = cg.fill_in(state="34", block_group="*")

        self.assertEqual(
            {"state": "34", "county": "*", "tract": "*", "block group": "*"}, filled_in
        )


if __name__ == "__main__":
    unittest.main()
