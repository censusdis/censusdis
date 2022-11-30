"""
These are integration tests because they require access to the remote census API.

Most of the functionality can be unit tested elsewhere or with mocks, but
these tests actually call the census API itself to cover the bits of code
immediately around those calls.
"""
import os.path
import tempfile
import unittest

import geopandas
import geopandas as gpd
import pandas as pd

from censusdis import data as ced
from censusdis import maps as cmp
from censusdis.states import STATE_NJ

if __name__ == "__main__":
    unittest.main()


class DownloadDetailTestCase(unittest.TestCase):
    """
    Test the full download capability.

    This is more an integration test than a unit test, which
    calls the census api and downloads real data. We are mainly
    just testing that we can do this without error. We're not that
    concerned with the data that comes back.
    """

    PATH_PREFIX = "test_data_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        ced.set_shapefile_path(tempfile.mkdtemp(prefix=cls.PATH_PREFIX))

    def setUp(self) -> None:
        """Set up before each test."""
        self._variable_source = ced.CensusApiVariableSource()
        self._dataset = "acs/acs5"
        self._year = 2020
        self._group_name = "B19001"
        self._name = f"{self._group_name}_001E"

    def test_path(self):
        """Are we using the right cache path for shapefiles?"""
        path = ced.get_shapefile_path()
        filename = os.path.basename(path)
        self.assertTrue(filename.startswith(self.PATH_PREFIX))

    def test_download(self):
        """Download just a couple of variables."""

        df = ced.download_detail(
            self._dataset, self._year, ["NAME", self._name], state=STATE_NJ, county="*"
        )

        self.assertEqual((21, 4), df.shape)

        self.assertEqual(["STATE", "COUNTY", "NAME", "B19001_001E"], list(df.columns))

    def test_wide(self):
        """
        Download a really wide set of variables.

        The goal is to trigger a call to
        `_download_concat_detail`.
        """

        # A bunch of sex by age variables.
        variables = (
            [f"B01001_{ii:03d}E" for ii in range(1, 50)]
            + [f"B01001A_{ii:03d}E" for ii in range(1, 32)]
            + [f"B01001B_{ii:03d}E" for ii in range(1, 32)]
            + [f"B01001I_{ii:03d}E" for ii in range(1, 32)]
        )

        self.assertGreater(len(variables), ced._MAX_FIELDS_PER_DOWNLOAD)

        df = ced.download_detail(
            self._dataset, self._year, ["NAME"] + variables, state=STATE_NJ, county="*"
        )

        # One column per variable plus state, county, and name.
        self.assertEqual((21, 3 + len(variables)), df.shape)

        columns = set(df.columns)
        for variable in ["STATE", "COUNTY", "NAME"] + variables:
            self.assertIn(variable, columns)

    def test_download_with_geometry_county(self):
        """Download at the county level with geometry."""

        gdf = ced.download_detail(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=STATE_NJ,
            county="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((21, 5), gdf.shape)

        self.assertEqual(
            ["STATE", "COUNTY", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
        )

    def test_download_with_geometry_state(self):
        """Download at the county level with geometry."""

        gdf = ced.download_detail(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((52, 4), gdf.shape)

        self.assertEqual(
            ["STATE", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
        )

    def test_download_with_geometry_tract(self):
        """Download at the county level with geometry."""

        gdf = ced.download_detail(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=STATE_NJ,
            county="001",
            tract="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((74, 6), gdf.shape)

        self.assertEqual(
            ["STATE", "COUNTY", "TRACT", "NAME", "B19001_001E", "geometry"],
            list(gdf.columns),
        )

    def test_download_with_geometry_block_group(self):
        """Download at the county level with geometry."""

        gdf = ced.download_detail(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=STATE_NJ,
            county="001",
            block_group="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((194, 7), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "COUNTY",
                "TRACT",
                "BLOCK_GROUP",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_cousub(self):
        """Download at the county level with geometry."""

        with self.assertRaises(ced.CensusApiException) as assertion:
            ced.download_detail(
                self._dataset,
                self._year,
                ["NAME", self._name],
                with_geometry=True,
                state=STATE_NJ,
                county_subdivision="*",
            )

        self.assertTrue(
            str(assertion.exception).startswith(
                "The with_geometry=True flag is only allowed if"
            )
        )

        # But it is OK without geometry.

        df = ced.download_detail(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=False,
            state=STATE_NJ,
            county_subdivision="*",
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertNotIsInstance(df, gpd.GeoDataFrame)

        self.assertEqual((570, 5), df.shape)


class ShapefileTestCase(unittest.TestCase):

    PATH_PREFIX = "test_data_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        cls.shapefile_path = tempfile.mkdtemp(prefix=cls.PATH_PREFIX)

    def setUp(self) -> None:
        """Set up before each test."""
        self._year = 2019
        self.reader = cmp.ShapeReader(self.shapefile_path, self._year)

    def test_county_shapefile(self):
        gdf_counties = self.reader.read_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3233, 18), gdf_counties.shape)

    def test_puma_shapefile(self):
        gdf_puma = self.reader.read_cb_shapefile("us", "puma")

        self.assertIsInstance(gdf_puma, gpd.GeoDataFrame)

        self.assertEqual((2380, 9), gdf_puma.shape)
