import unittest
from typing import Any, Dict

import pandas as pd
from censusdata import censusgeo

from censusdis.censusdata import (
    _augment_geography,
    _normalize_geography,
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


class NormalizeGeographyTestCase(unittest.TestCase):
    def test_normalize_block(self):

        expected_geo = censusgeo([("state", "34"), ("county", "*"), ("block", "*")])

        for block_in in [None, "*"]:
            geo, county, cousub, tract, block_group, block = _normalize_geography(
                resolution="block",
                state="34",
                county="*",
                cousub=None,
                tract=None,
                block_group=None,
                block=block_in,
            )

            self.assertEqual(expected_geo, geo)

    def test_normalize_block_group(self):
        expected_geo = censusgeo(
            [("state", "34"), ("county", "013"), ("block group", "*")]
        )

        for block_group_in in [None, "*"]:
            geo, county, cousub, tract, block_group, block = _normalize_geography(
                resolution="block group",
                state="34",
                county="013",
                cousub=None,
                tract=None,
                block_group=block_group_in,
                block=None,
            )

            self.assertEqual(expected_geo, geo)

    def test_normalize_tract(self):
        expected_geo = censusgeo([("state", "34"), ("county", "013"), ("tract", "*")])

        for tract_in in [None, "*"]:
            geo, county, cousub, tract, block_group, block = _normalize_geography(
                resolution="tract",
                state="34",
                county="013",
                cousub=None,
                tract=tract_in,
                block_group=None,
                block=None,
            )

            self.assertEqual(expected_geo, geo)

    def test_normalize_cousub(self):
        expected_geo = censusgeo(
            [("state", "34"), ("county", "013"), ("county subdivision", "*")]
        )

        for cousub_in in [None, "*"]:
            geo, county, cousub, tract, block_group, block = _normalize_geography(
                resolution="county subdivision",
                state="34",
                county="013",
                cousub=cousub_in,
                tract=None,
                block_group=None,
                block=None,
            )

            self.assertEqual(expected_geo, geo)


class AugmentGeographyTestCase(unittest.TestCase):
    def test_augment_block(self):
        df = pd.DataFrame(
            [
                [
                    censusgeo(
                        [
                            ("state", "34"),
                            ("county", "013"),
                            ("tract", "001900"),
                            ("block", "1001"),
                        ]
                    ),
                    100,
                    50,
                    200,
                ],
                [
                    censusgeo(
                        [
                            ("state", "34"),
                            ("county", "013"),
                            ("tract", "001900"),
                            ("block", "2002"),
                        ]
                    ),
                    220,
                    55,
                    110,
                ],
            ],
            columns=["index", "PX001", "PX002", "Px003"],
        )
        df = df.set_index("index")

        df = _augment_geography(
            df,
            ["PX001", "PX002", "Px003"],
            county="013",
            cousub=None,
            tract=None,
            block_group=None,
            block="*",
        )

        df_expected = pd.DataFrame(
            [
                ["34", "013", "001900", "1", "1001", 100, 50, 200],
                ["34", "013", "001900", "2", "2002", 220, 55, 110],
            ],
            columns=[
                "STATE",
                "COUNTY",
                "TRACT",
                "BLOCK_GROUP",
                "BLOCK",
                "PX001",
                "PX002",
                "Px003",
            ],
        )

        self.assertTrue((df_expected == df).all().all())

    def test_augment_block_broup(self):
        df = pd.DataFrame(
            [
                [
                    censusgeo(
                        [
                            ("state", "34"),
                            ("county", "013"),
                            ("tract", "001900"),
                            ("block group", "1"),
                        ]
                    ),
                    100,
                    50,
                    200,
                ],
                [
                    censusgeo(
                        [
                            ("state", "34"),
                            ("county", "013"),
                            ("tract", "001900"),
                            ("block group", "2"),
                        ]
                    ),
                    220,
                    55,
                    110,
                ],
            ],
            columns=["index", "PX001", "PX002", "Px003"],
        )
        df = df.set_index("index")

        df = _augment_geography(
            df,
            ["PX001", "PX002", "Px003"],
            county="013",
            cousub=None,
            tract=None,
            block_group="*",
            block=None,
        )

        df_expected = pd.DataFrame(
            [
                ["34", "013", "001900", "1", 100, 50, 200],
                ["34", "013", "001900", "2", 220, 55, 110],
            ],
            columns=[
                "STATE",
                "COUNTY",
                "TRACT",
                "BLOCK_GROUP",
                "PX001",
                "PX002",
                "Px003",
            ],
        )

        self.assertTrue((df_expected == df).all().all())

    def test_augment_tract(self):
        df = pd.DataFrame(
            [
                [
                    censusgeo(
                        [("state", "34"), ("county", "013"), ("tract", "001900")]
                    ),
                    100,
                    50,
                    200,
                ],
                [
                    censusgeo(
                        [("state", "34"), ("county", "013"), ("tract", "001800")]
                    ),
                    220,
                    55,
                    110,
                ],
            ],
            columns=["index", "PX001", "PX002", "Px003"],
        )
        df = df.set_index("index")

        df = _augment_geography(
            df,
            ["PX001", "PX002", "Px003"],
            county="013",
            cousub=None,
            tract="*",
            block_group=None,
            block=None,
        )

        df_expected = pd.DataFrame(
            [
                ["34", "013", "001900", 100, 50, 200],
                ["34", "013", "001800", 220, 55, 110],
            ],
            columns=["STATE", "COUNTY", "TRACT", "PX001", "PX002", "Px003"],
        )

        self.assertTrue((df_expected == df).all().all())

    def test_augment_cousub(self):
        df = pd.DataFrame(
            [
                [
                    censusgeo(
                        [
                            ("state", "34"),
                            ("county", "013"),
                            ("county subdivision", "06260"),
                        ]
                    ),
                    100,
                    50,
                    200,
                ],
                [
                    censusgeo(
                        [
                            ("state", "34"),
                            ("county", "013"),
                            ("county subdivision", "13045"),
                        ]
                    ),
                    220,
                    55,
                    110,
                ],
            ],
            columns=["index", "PX001", "PX002", "Px003"],
        )
        df = df.set_index("index")

        df = _augment_geography(
            df,
            ["PX001", "PX002", "Px003"],
            county="013",
            cousub="*",
            tract=None,
            block_group=None,
            block=None,
        )

        df_expected = pd.DataFrame(
            [
                ["34", "013", "06260", 100, 50, 200],
                ["34", "013", "13045", 220, 55, 110],
            ],
            columns=["STATE", "COUNTY", "COUSUB", "PX001", "PX002", "Px003"],
        )

        self.assertTrue((df_expected == df).all().all())

    def test_augment_county(self):
        df = pd.DataFrame(
            [
                [censusgeo([("state", "34"), ("county", "013")]), 100, 50, 200],
                [censusgeo([("state", "34"), ("county", "014")]), 220, 55, 110],
            ],
            columns=["index", "PX001", "PX002", "Px003"],
        )
        df = df.set_index("index")

        df = _augment_geography(
            df,
            ["PX001", "PX002", "Px003"],
            county="*",
            cousub=None,
            tract=None,
            block_group=None,
            block=None,
        )

        df_expected = pd.DataFrame(
            [
                ["34", "013", 100, 50, 200],
                ["34", "014", 220, 55, 110],
            ],
            columns=["STATE", "COUNTY", "PX001", "PX002", "Px003"],
        )

        self.assertTrue((df_expected == df).all().all())


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
