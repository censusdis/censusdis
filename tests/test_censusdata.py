import unittest

import pandas as pd
from censusdata import censusgeo

from censusdis.censusdata import _augment_geography, _normalize_geography


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


if __name__ == "__main__":
    unittest.main()
