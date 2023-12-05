# Copyright (c) 2023 Darren Erik Vengroff
"""Test for geography functionality."""
import unittest
from typing import Mapping, Optional, Tuple

from censusdis.geography import CensusGeographyQuerySpec, PathSpec


class CanonicalGeometryTestCase(unittest.TestCase):
    """Test canonical geometry matching."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.dataset = "acs/acs5"
        self.year = 2019

    def test_init_raises(self):
        """Test that the constructor raises an exception when it should."""
        with self.assertRaises(ValueError):
            PathSpec(["state"])

    def test_partial_match_self(self):
        """Test the partial match case."""
        # 150 is state:county:tract:block group,
        # which is not a prefix of anything else.
        path_spec = PathSpec.by_number(self.dataset, self.year, "150")
        kwargs = {k: "*" for k in path_spec.keys()}

        self.assertTrue(path_spec._partial_match(**kwargs))

        partial_matches = PathSpec.partial_matches(self.dataset, self.year, **kwargs)

        self.assertEqual(1, len(partial_matches))
        self.assertEqual(path_spec, partial_matches[0].path_spec)

    def test_partial_match_no_match(self):
        """Test when there is no match."""
        path_spec = PathSpec.by_number(self.dataset, self.year, "150")

        self.assertFalse(path_spec._partial_match(unknown="*"))
        self.assertFalse(path_spec._partial_match(state="034", unknown="*"))

    def test_partial_match_underscore(self):
        """Test the private match method."""
        # 150 is state:county:tract:block group,
        # which is not a prefix of anything else.
        path_spec = PathSpec.by_number(self.dataset, self.year, "150")

        self.assertTrue(path_spec._partial_match(state="34", block_group="12345"))
        self.assertTrue(path_spec._partial_match(is_prefix=False, block_group="12345"))

    def test_partial_matches(self):
        """Test partial matches."""
        partial_matches = PathSpec.partial_matches(
            self.dataset, self.year, state="034", county="*"
        )
        for bound_path in partial_matches:
            self.assertIn("state", bound_path.path_spec.path)
            self.assertIn("county", bound_path.path_spec.path)

    def test_partial_prefix_match(self):
        """Test a partial prefix match."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="034", county="*"
        )

        self.assertEqual("050", bound_path.num)
        self.assertIs(
            PathSpec.by_number(self.dataset, self.year, "050"), bound_path.path_spec
        )

    def test_partial_prefix_match_140(self):
        """Test a partial prefix match of 140."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="034", tract="*"
        )

        self.assertEqual("140", bound_path.num)
        self.assertIs(
            PathSpec.by_number(self.dataset, self.year, "140"), bound_path.path_spec
        )

    def test_partial_prefix_match_150(self):
        """Test a partial prefix match of 150."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="034", block_group="*"
        )

        self.assertEqual("150", bound_path.num)
        self.assertIs(
            PathSpec.by_number(self.dataset, self.year, "150"), bound_path.path_spec
        )

    def test_full_match(self):
        """Test full matches."""
        num, path_spec = PathSpec.full_match(self.dataset, self.year, state="*")
        self.assertEqual("040", num)
        self.assertIs(PathSpec.by_number(self.dataset, self.year, "040"), path_spec)

        num, path_spec = PathSpec.full_match(
            self.dataset, self.year, state="34", county="013", tract="019013"
        )
        self.assertEqual("140", num)
        self.assertIs(PathSpec.by_number(self.dataset, self.year, "140"), path_spec)

    def test_full_match_none(self):
        """Test gull match returns None, None when expected."""
        num, path_spec = PathSpec.full_match(
            self.dataset, self.year, unknown="*", other="foo"
        )
        self.assertIsNone(num)
        self.assertIsNone(path_spec)

    def test_by_number_none(self):
        """Test with a bad number."""
        self.assertIsNone(PathSpec.by_number(self.dataset, self.year, "999"))

    def test_full_match_all(self):
        """Test a full match on all components."""
        for num, path_spec in PathSpec.get_path_specs(self.dataset, self.year).items():
            num_match, path_spec_match = PathSpec.full_match(
                self.dataset, self.year, **{k: "*" for k in path_spec.keys()}
            )
            self.assertEqual(num, num_match)
            self.assertIs(path_spec, path_spec_match)

    def test_fill_in(self):
        """Test filling in missing components."""
        # 150 is state:county:tract:block group.
        path_spec = PathSpec.by_number(self.dataset, self.year, "150")

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
        """Test filling in a partial prefix match."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="34", block_group="*"
        )

        self.assertEqual("150", bound_path.num)

        filled_in = bound_path.path_spec.fill_in(state="34", block_group="*")

        self.assertEqual(
            {"state": "34", "county": "*", "tract": "*", "block group": "*"}, filled_in
        )


class CensusGeographyQuerySpecTestCase(unittest.TestCase):
    """Test geographic queries."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.dataset = "acs/acs5"
        self.year = 2013

    def assertEqualExceptKey(
        self,
        t0: Tuple[str, Mapping[str, str]],
        t1: Tuple[str, Mapping[str, str]],
        message: Optional[str] = None,
    ) -> None:
        """
        Assert the url and params are equal except for an API key.

        We might have gotten the key from the environment, and it
        could be different in different environments.
        """
        url0, url1 = t0[0], t1[0]
        params0 = {k: v for k, v in t0[1].items() if k != "key"}
        params1 = {k: v for k, v in t1[1].items() if k != "key"}

        self.assertEqual(url0, url1, message)
        self.assertEqual(params0, params1, message)

    def test_for(self):
        """Test the for clause in the get params."""
        bound_path = PathSpec.partial_prefix_match(self.dataset, self.year, state="*")

        self.assertEqual("040", bound_path.num)
        self.assertEqual(dict(state="*"), bound_path.bindings)

        query_spec = CensusGeographyQuerySpec(
            self.dataset, self.year, ["NAME"], bound_path
        )

        self.assertEqual("state", query_spec.for_component)
        self.assertFalse(query_spec.in_components)

        self.assertEqualExceptKey(
            (
                f"https://api.census.gov/data/{self.year}/{self.dataset}",
                {"for": "state", "get": "NAME"},
            ),
            query_spec.table_url(),
        )

    def test_for_bound(self):
        """Test the for clause with bound params."""
        bound_path = PathSpec.partial_prefix_match(self.dataset, self.year, state="36")

        self.assertEqual("040", bound_path.num)
        self.assertEqual(dict(state="36"), bound_path.bindings)

        query_spec = CensusGeographyQuerySpec(
            self.dataset, self.year, ["NAME"], bound_path
        )

        self.assertEqual("state:36", query_spec.for_component)
        self.assertFalse(query_spec.in_components)

        self.assertEqualExceptKey(
            (
                f"https://api.census.gov/data/{self.year}/{self.dataset}",
                {"for": "state:36", "get": "NAME"},
            ),
            query_spec.table_url(),
        )

    def test_for_in(self):
        """Test the for and in clauses in the same query."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="36", county="001", tract="*"
        )

        self.assertEqual("140", bound_path.num)
        self.assertEqual(dict(state="36", county="001", tract="*"), bound_path.bindings)

        query_spec = CensusGeographyQuerySpec(
            self.dataset, self.year, ["NAME"], bound_path
        )

        self.assertEqual("tract", query_spec.for_component)
        self.assertEqual("state:36 county:001", query_spec.in_components)

        self.assertEqualExceptKey(
            (
                f"https://api.census.gov/data/{self.year}/{self.dataset}",
                {"for": "tract", "get": "NAME", "in": "state:36 county:001"},
            ),
            query_spec.table_url(),
        )

    def test_for_in_skip_components(self):
        """Test the for and in clause on a partial prefix match."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="36", block_group="*"
        )

        self.assertEqual("150", bound_path.num)
        self.assertEqual(
            {"state": "36", "county": "*", "tract": "*", "block group": "*"},
            # Strip out the environment dependent API key that might be there.
            {k: v for k, v in bound_path.bindings.items() if k != "key"},
        )

        query_spec = CensusGeographyQuerySpec(
            self.dataset, self.year, ["NAME"], bound_path
        )

        self.assertEqual("block group", query_spec.for_component)
        self.assertEqual("state:36 county:* tract:*", query_spec.in_components)

        self.assertEqualExceptKey(
            (
                f"https://api.census.gov/data/{self.year}/{self.dataset}",
                {
                    "for": "block group",
                    "get": "NAME",
                    "in": "state:36 county:* tract:*",
                },
            ),
            query_spec.table_url(),
        )

    def test_for_in_bound(self):
        """Tets the for and in clauses with bound values."""
        bound_path = PathSpec.partial_prefix_match(
            self.dataset, self.year, state="36", county="001", tract="001802"
        )

        self.assertEqual("140", bound_path.num)
        self.assertEqual(
            dict(state="36", county="001", tract="001802"), bound_path.bindings
        )

        query_spec = CensusGeographyQuerySpec(
            self.dataset, self.year, ["NAME"], bound_path
        )

        self.assertEqual("tract:001802", query_spec.for_component)
        self.assertEqual("state:36 county:001", query_spec.in_components)

        self.assertEqualExceptKey(
            (
                f"https://api.census.gov/data/{self.year}/{self.dataset}",
                {"for": "tract:001802", "get": "NAME", "in": "state:36 county:001"},
            ),
            query_spec.table_url(),
        )


if __name__ == "__main__":
    unittest.main()
