import unittest

from censusdis.geography import PathSpec, CensusGeographyQuerySpec


class CanonicalGeometryTestCase(unittest.TestCase):
    def test_init_raises(self):
        with self.assertRaises(ValueError):
            PathSpec(["state"])

    def test_partial_match_self(self):
        # 150 is state:county:tract:block group,
        # which is not a prefix of anything else.
        path_spec = PathSpec.by_number("150")
        kwargs = {k: "*" for k in path_spec.keys()}

        self.assertTrue(path_spec._partial_match(**kwargs))

        partial_matches = PathSpec.partial_matches(**kwargs)

        self.assertEqual(1, len(partial_matches))
        self.assertEqual(path_spec, partial_matches[0].path_spec)

    def test_partial_match_no_match(self):
        path_spec = PathSpec.by_number("101")

        self.assertFalse(path_spec._partial_match(unknown="*"))
        self.assertFalse(path_spec._partial_match(state="034", unknown="*"))
        self.assertFalse(path_spec._partial_match(is_prefix=False, unknown="*"))
        self.assertFalse(
            path_spec._partial_match(is_prefix=False, state="034", unknown="*")
        )

    def test_partial_match_underscore(self):
        # 150 is state:county:tract:block group,
        # which is not a prefix of anything else.
        path_spec = PathSpec.by_number("150")

        self.assertTrue(path_spec._partial_match(state="34", block_group="12345"))
        self.assertTrue(path_spec._partial_match(is_prefix=False, block_group="12345"))

    def test_partial_matches(self):
        partial_matches = PathSpec.partial_matches(state="034", county="*")
        for bound_path in partial_matches:
            self.assertIn("state", bound_path.path_spec.path)
            self.assertIn("county", bound_path.path_spec.path)

    def test_partial_prefix_match(self):
        bound_path = PathSpec.partial_prefix_match(state="034", county="*")

        self.assertEqual("050", bound_path.num)
        self.assertIs(PathSpec.by_number("050"), bound_path.path_spec)

    def test_partial_prefix_match_101(self):
        bound_path = PathSpec.partial_prefix_match(state="034", block="*")

        self.assertEqual("101", bound_path.num)
        self.assertIs(PathSpec.by_number("101"), bound_path.path_spec)

    def test_partial_prefix_match_140(self):
        bound_path = PathSpec.partial_prefix_match(state="034", tract="*")

        self.assertEqual("140", bound_path.num)
        self.assertIs(PathSpec.by_number("140"), bound_path.path_spec)

    def test_partial_prefix_match_150(self):
        bound_path = PathSpec.partial_prefix_match(state="034", block_group="*")

        self.assertEqual("150", bound_path.num)
        self.assertIs(PathSpec.by_number("150"), bound_path.path_spec)

    def test_full_match(self):
        num, path_spec = PathSpec.full_match(state="*")
        self.assertEqual("040", num)
        self.assertIs(PathSpec.by_number("040"), path_spec)

        num, path_spec = PathSpec.full_match(state="34", county="013", tract="019013")
        self.assertEqual("140", num)
        self.assertIs(PathSpec.by_number("140"), path_spec)

    def test_full_match_none(self):
        num, path_spec = PathSpec.full_match(unknown="*", other="foo")
        self.assertIsNone(num)
        self.assertIsNone(path_spec)

    def test_by_number_none(self):
        self.assertIsNone(PathSpec.by_number("999"))

    def test_full_match_all(self):
        for num, path_spec in PathSpec.ALL.items():
            num_match, path_spec_match = PathSpec.full_match(
                **{k: "*" for k in path_spec.keys()}
            )
            self.assertEqual(num, num_match)
            self.assertIs(path_spec, path_spec_match)

    def test_fill_in(self):
        # 150 is state:county:tract:block group.
        path_spec = PathSpec.by_number("150")

        with self.assertRaises(ValueError):
            path_spec.fill_in()

        with self.assertRaises(ValueError):
            path_spec.fill_in(state="34", county="013", county_subdivision="132")

        filled_in = path_spec.fill_in(state="34", county="013", block_group="*")

        self.assertEqual(
            {"state": "34", "county": "013", "tract": "*", "block group": "*"},
            filled_in,
        )

        filled_in = path_spec.fill_in(**filled_in)

        self.assertEqual(
            {"state": "34", "county": "013", "tract": "*", "block group": "*"},
            filled_in,
        )

        filled_in = path_spec.fill_in(
            state="34", county="013", tract="012345", block_group="3"
        )

        self.assertEqual(
            {"state": "34", "county": "013", "tract": "012345", "block group": "3"},
            filled_in,
        )

    def test_fill_partial_prefix_match(self):
        bound_path = PathSpec.partial_prefix_match(state="34", block_group="*")

        self.assertEqual("150", bound_path.num)

        filled_in = bound_path.path_spec.fill_in(state="34", block_group="*")

        self.assertEqual(
            {"state": "34", "county": "*", "tract": "*", "block group": "*"}, filled_in
        )


class CensusGeographyQuerySpecTestCase(unittest.TestCase):
    def test_for(self):
        bound_path = PathSpec.partial_prefix_match(state="*")

        self.assertEqual("040", bound_path.num)
        self.assertEqual(dict(state="*"), bound_path.bindings)

        query_spec = CensusGeographyQuerySpec("acs/acs5", 2020, ["NAME"], bound_path)

        self.assertEqual("state", query_spec.for_component)
        self.assertFalse(query_spec.in_components)

        self.assertEqual(
            (
                "https://api.census.gov/data/2020/acs/acs5",
                {"for": "state", "get": "NAME"},
            ),
            query_spec.detail_table_url(),
        )

    def test_for_bound(self):
        bound_path = PathSpec.partial_prefix_match(state="36")

        self.assertEqual("040", bound_path.num)
        self.assertEqual(dict(state="36"), bound_path.bindings)

        query_spec = CensusGeographyQuerySpec("acs/acs5", 2020, ["NAME"], bound_path)

        self.assertEqual("state:36", query_spec.for_component)
        self.assertFalse(query_spec.in_components)

        self.assertEqual(
            (
                "https://api.census.gov/data/2020/acs/acs5",
                {"for": "state:36", "get": "NAME"},
            ),
            query_spec.detail_table_url(),
        )

    def test_for_in(self):
        bound_path = PathSpec.partial_prefix_match(state="36", county="001", tract="*")

        self.assertEqual("140", bound_path.num)
        self.assertEqual(dict(state="36", county="001", tract="*"), bound_path.bindings)

        query_spec = CensusGeographyQuerySpec("acs/acs5", 2020, ["NAME"], bound_path)

        self.assertEqual("tract", query_spec.for_component)
        self.assertEqual("state:36 county:001", query_spec.in_components)

        self.assertEqual(
            (
                "https://api.census.gov/data/2020/acs/acs5",
                {"for": "tract", "get": "NAME", "in": "state:36 county:001"},
            ),
            query_spec.detail_table_url(),
        )

    def test_for_in_skip_components(self):
        bound_path = PathSpec.partial_prefix_match(state="36", block_group="*")

        self.assertEqual("150", bound_path.num)
        self.assertEqual(
            {"state": "36", "county": "*", "tract": "*", "block group": "*"},
            bound_path.bindings,
        )

        query_spec = CensusGeographyQuerySpec("acs/acs5", 2020, ["NAME"], bound_path)

        self.assertEqual("block group", query_spec.for_component)
        self.assertEqual("state:36 county:* tract:*", query_spec.in_components)

        self.assertEqual(
            (
                "https://api.census.gov/data/2020/acs/acs5",
                {
                    "for": "block group",
                    "get": "NAME",
                    "in": "state:36 county:* tract:*",
                },
            ),
            query_spec.detail_table_url(),
        )

    def test_for_in_bound(self):
        bound_path = PathSpec.partial_prefix_match(
            state="36", county="001", tract="001802"
        )

        self.assertEqual("140", bound_path.num)
        self.assertEqual(
            dict(state="36", county="001", tract="001802"), bound_path.bindings
        )

        query_spec = CensusGeographyQuerySpec("acs/acs5", 2020, ["NAME"], bound_path)

        self.assertEqual("tract:001802", query_spec.for_component)
        self.assertEqual("state:36 county:001", query_spec.in_components)

        self.assertEqual(
            (
                "https://api.census.gov/data/2020/acs/acs5",
                {"for": "tract:001802", "get": "NAME", "in": "state:36 county:001"},
            ),
            query_spec.detail_table_url(),
        )


if __name__ == "__main__":
    unittest.main()
