import unittest
from typing import Any, Dict

from censusdis.data import (
    _gf2s,
    VariableSource,
    VariableCache,
)


class TestFilters(unittest.TestCase):
    """Test that we can properly convert geo filters to strings."""

    def test_filter_none(self):
        self.assertIsNone(_gf2s(None))

    def test_filter_str(self):
        self.assertEqual("013", _gf2s("013"))

    def test_filter_list(self):
        self.assertEqual("013", _gf2s(["013"]))
        self.assertEqual("013,014", _gf2s(["013", "014"]))
        self.assertEqual("013,014,015", _gf2s(["013", "014", "015"]))


class VariableCacheTestCase(unittest.TestCase):
    class MockVariableSource(VariableSource):
        """A mock variable source."""

        def __init__(self):
            self._gets = 0
            self._group_gets = 0

        @property
        def gets(self):
            return self._gets

        @property
        def group_gets(self):
            return self._group_gets

        def reset_counts(self):
            self._gets = 0
            self._group_gets = 0

        def get(self, source: str, year: int, name: str) -> Dict[str, Any]:
            """
            Construct a mock variable.

            This looks a bit like a variable we get get from
            https://api.census.gov/data/2020/acs/acs5/variables/B03002_001E.json
            """
            self._gets = self.gets + 1

            return {
                "name": f"{name}",
                "label": "Estimate!!Total:",
                "concept": "HISPANIC OR LATINO ORIGIN BY RACE",
                "predicateType": "int",
                "group": name.split("_")[0],
                "limit": 0,
                "attributes": f"{name}A,{name}M,{name}MA",
            }

        def get_group(self, source: str, year: int, name: str) -> Dict[str, Dict]:
            """
            Construct a mock group.

            This looks a bit like a subset of what we might get from
            https://api.census.gov/data/2020/acs/acs5/groups/B03002.json
            """
            self._group_gets = self.group_gets + 1

            return {
                "variables": {
                    f"{name}_002E": {
                        "name": f"{name}_002E",
                        "label": "Estimate!!Total:!!Not Hispanic or Latino:",
                        "concept": "HISPANIC OR LATINO ORIGIN BY RACE",
                        "predicateType": "int",
                        "group": f"{name}",
                        "limit": 0,
                        "predicateOnly": True,
                        "universe": "TOTAL_POP",
                    },
                    f"{name}_003E": {
                        "name": f"{name}_003E",
                        "label": "Estimate!!Total:!!Not Hispanic or Latino:!!White alone",
                        "concept": "HISPANIC OR LATINO ORIGIN BY RACE",
                        "predicateType": "int",
                        "group": f"{name}",
                        "limit": 0,
                        "predicateOnly": True,
                        "universe": "TOTAL_POP",
                    },
                    f"{name}_004E": {
                        "name": f"{name}_004E",
                        "label": "Estimate!!Total:!!Not Hispanic or Latino:!!Black or African American alone",
                        "concept": "HISPANIC OR LATINO ORIGIN BY RACE",
                        "predicateType": "int",
                        "group": f"{name}",
                        "limit": 0,
                        "predicateOnly": True,
                        "universe": "TOTAL_POP",
                    },
                }
            }

    def setUp(self) -> None:
        """Set up before each test."""
        self.source = "acs/acs5"
        self.year = 2020
        self.mock_source = self.MockVariableSource()
        self.variables = VariableCache(variable_source=self.mock_source)

    def test_operators(self):
        """Test basic operators."""
        self.assertEqual(0, len(self.variables))
        self.assertNotIn((self.source, self.year, "X02002_002E"), self.variables)

        self.assertEqual(0, self.mock_source.gets)
        self.assertEqual(0, self.mock_source.group_gets)

        _ = self.variables[self.source, self.year, "X02002_002E"]
        self.assertEqual(1, len(self.variables))
        self.assertIn((self.source, self.year, "X02002_002E"), self.variables)

        self.assertEqual(1, self.mock_source.gets)
        self.assertEqual(0, self.mock_source.group_gets)

        # No second call to the source if we hit in the cache.
        _ = self.variables[self.source, self.year, "X02002_002E"]

        self.assertEqual(1, self.mock_source.gets)
        self.assertEqual(0, self.mock_source.group_gets)

    def test_get(self):
        self.assertEqual(0, len(self.variables))
        variable = self.variables.get(self.source, self.year, "X01001_001E")

        # One in the cache now.
        self.assertEqual(1, len(self.variables))
        self.assertIn((self.source, self.year, "X01001_001E"), self.variables)

        self.assertEqual("X01001_001E", variable["name"])
        self.assertEqual("X01001", variable["group"])
        self.assertEqual("Estimate!!Total:", variable["label"])

        self.variables.invalidate(self.source, self.year, "X01001_001E")

        # No longer in the cache.
        self.assertEqual(0, len(self.variables))
        self.assertNotIn((self.source, self.year, "X01001_001E"), self.variables)

    def test_many_vars(self):
        for n, source in enumerate(["foo/abc", "bar/xyz"]):
            for ii in range(20):
                name = f"X01001_0{ii:02}E"

                source_variable = self.mock_source.get(source, self.year, name)
                cached_variable = self.variables.get(source, self.year, name)

                self.assertEqual(40 * n + 2 * ii + 2, self.mock_source.gets)
                self.assertEqual(0, self.mock_source.group_gets)

                self.assertEqual(20 * n + ii + 1, len(self.variables))
                self.assertIn((source, self.year, name), self.variables)
                self.assertEqual(source_variable, cached_variable)

                # These all hit in the cache, so the get count does not go up.
                self.variables.get(source, self.year, name)
                _ = self.variables[source, self.year, name]
                self.variables.get(source, self.year, name)
                _ = self.variables[source, self.year, name]

                self.assertEqual(40 * n + 2 * ii + 2, self.mock_source.gets)
                self.assertEqual(0, self.mock_source.group_gets)

        # Now drop half of them, nust from one source.
        for ii in range(20):
            name = f"X01001_0{ii:02}E"
            self.variables.invalidate(source, self.year, name)
            self.assertEqual(20 * (n + 1) - (ii + 1), len(self.variables))

        # Bulk drop the rest
        self.variables.clear()
        self.assertEqual(0, len(self.variables))

    def test_group(self):
        self.assertEqual(0, self.mock_source.gets)
        self.assertEqual(0, self.mock_source.group_gets)

        group = self.variables.get_group(self.source, self.year, "X02002")
        self.assertEqual(3, len(group))

        # We only make the one group call to the source, not
        # calls for all the individual variables.
        self.assertEqual(0, self.mock_source.gets)
        self.assertEqual(1, self.mock_source.group_gets)

        # All the variables in the group should now be in the cache.
        self.assertEqual(3, len(self.variables))

        for name in group.keys():
            self.assertIn((self.source, self.year, name), self.variables)
            self.assertEqual(
                "X02002", self.variables[self.source, self.year, name]["group"]
            )
            self.assertEqual(name, self.variables[self.source, self.year, name]["name"])

        # We had all the variables in the cache.
        self.assertEqual(0, self.mock_source.gets)


if __name__ == "__main__":
    unittest.main()
