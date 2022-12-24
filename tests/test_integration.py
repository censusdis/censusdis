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
import numpy as np
import pandas as pd

from censusdis import data as ced
from censusdis import maps as cmp
from censusdis.states import (
    STATE_NJ,
    STATE_NY,
    STATE_CA,
    ALL_STATES_AND_DC,
    TERRITORY_PR,
)

if __name__ == "__main__":
    unittest.main()


class DownloadTestCase(unittest.TestCase):
    """
    Test the full download capability.

    This is more an integration test than a unit test, which
    calls the census api and downloads real data. We are mainly
    just testing that we can do this without error. We're not that
    concerned with the data that comes back.
    """

    PATH_PREFIX = "test_integration_shapefiles_"

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

        df = ced.download(
            self._dataset, self._year, ["NAME", self._name], state=STATE_NJ, county="*"
        )

        self.assertEqual((21, 4), df.shape)

        self.assertEqual(["STATE", "COUNTY", "NAME", "B19001_001E"], list(df.columns))

    def test_download_detail(self):
        """Use the deprecated API and assert it warns."""

        with self.assertWarns(DeprecationWarning):
            df = ced.download_detail(
                self._dataset,
                self._year,
                ["NAME", self._name],
                state=STATE_NJ,
                county="*",
            )

        self.assertEqual((21, 4), df.shape)

        self.assertEqual(["STATE", "COUNTY", "NAME", "B19001_001E"], list(df.columns))

    def test_bad_variable(self):
        """Try to download a variable that does not exist."""

        with self.assertRaises(ced.CensusApiException) as cm:
            ced.download(
                self._dataset,
                self._year,
                ["NAME", "I_DONT_EXIST"],
                state=STATE_NJ,
                county="*",
            )

        self.assertIn(
            "https://api.census.gov/data/2020/acs/acs5/variables/I_DONT_EXIST.html",
            str(cm.exception),
        )
        self.assertIn(
            "https://api.census.gov/data/2020/acs/acs5/variables.html",
            str(cm.exception),
        )

    def test_wide(self):
        """
        Download a really wide set of variables.

        The goal is to trigger a call to
        `_download_concat`.
        """

        # A bunch of sex by age variables.
        variables = (
            [f"B01001_{ii:03d}E" for ii in range(1, 50)]
            + [f"B01001A_{ii:03d}E" for ii in range(1, 32)]
            + [f"B01001B_{ii:03d}E" for ii in range(1, 32)]
            + [f"B01001I_{ii:03d}E" for ii in range(1, 32)]
        )

        self.assertGreater(len(variables), ced._MAX_FIELDS_PER_DOWNLOAD)

        df = ced.download(
            self._dataset, self._year, ["NAME"] + variables, state=STATE_NJ, county="*"
        )

        # One column per variable plus state, county, and name.
        self.assertEqual((21, 3 + len(variables)), df.shape)

        columns = set(df.columns)
        for variable in ["STATE", "COUNTY", "NAME"] + variables:
            self.assertIn(variable, columns)

    def test_download_with_geometry_county(self):
        """Download at the county level with geometry."""

        gdf = ced.download(
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

        gdf = ced.download(
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

        gdf = ced.download(
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

        gdf = ced.download(
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
            ced.download(
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

        df = ced.download(
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

    def test_multi_state(self):
        """
        Test the case where the only geo argument has multiple values.

        As in `state=[STATE_NJ, STATE_NY]`, vs. the more general
        `state="*"`.
        """

        df = ced.download(
            self._dataset, self._year, ["NAME", self._name], state=[STATE_NJ, STATE_NY]
        )

        self.assertEqual((2, 3), df.shape)

        self.assertIn(STATE_NJ, list(df["STATE"]))
        self.assertIn(STATE_NY, list(df["STATE"]))

    def test_multi_state_county(self):
        """
        Test the case where the first geo argument has multiple values.

        As in `state=[STATE_NJ, STATE_NY]`, vs. the more general
        `state="*"` and `county="*"`.
        """

        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[STATE_NJ, STATE_NY],
            county="*",
        )

        self.assertEqual((83, 4), df.shape)

        df_51 = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=ALL_STATES_AND_DC,
            county="*",
        )

        df_star = ced.download(
            self._dataset, self._year, ["NAME", self._name], state="*", county="*"
        )

        # This will get us some outside the 51.
        self.assertLess(len(df_51.index), len(df_star.index))

        df_star = df_star[df_star.STATE.isin(ALL_STATES_AND_DC)]

        self.assertEqual(len(df_51.index), len(df_star.index))

    def test_multi_state_tract(self):
        """
        Test the case where the first geo argument has multiple values.

        As in `state=[STATE_NJ, STATE_NY]`, vs. the more general
        `state="*"` and `tract="*"`.

        In this test we also skip a level.
        """

        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[STATE_NJ, STATE_NY],
            tract="*",
        )

        self.assertEqual((7592, 5), df.shape)

        self.assertIn("STATE", df.columns)
        self.assertIn("COUNTY", df.columns)
        self.assertIn("TRACT", df.columns)
        self.assertIn("NAME", df.columns)
        self.assertIn(self._name, df.columns)

    def test_multi_state_bg(self):
        """
        Test the case where the first geo argument has multiple values.

        As in `state=[STATE_NJ, STATE_NY]`, vs. the more general
        `state="*"` and `tract="*"`.

        In this test we also skip two levels.
        """

        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[STATE_NJ, STATE_NY],
            block_group="*",
        )

        self.assertEqual((22669, 6), df.shape)

        self.assertIn("STATE", df.columns)
        self.assertIn("COUNTY", df.columns)
        self.assertIn("TRACT", df.columns)
        self.assertIn("BLOCK_GROUP", df.columns)
        self.assertIn("NAME", df.columns)
        self.assertIn(self._name, df.columns)


class AcsSubjectTestCase(unittest.TestCase):
    """
    Test on ACS Subject Data that includes null in an int field.
    """

    def setUp(self) -> None:
        """Set up before each test."""
        self._dataset = "acs/acs5/profile"
        self._year = 2021
        self._variable_name = "DP02_0001E"

    def test_states_with_null_in_pr(self):
        df = ced.download(
            self._dataset, self._year, ["NAME", self._variable_name], state="*"
        )

        self.assertEqual((52, 3), df.shape)

        # The API returns a null for PR but numbers for all others.
        # We have to convert to a float to represent this even though
        # the census metadata says the variable is an int.
        self.assertEqual(np.float64, df[self._variable_name].dtype)

        self.assertFalse(
            df[df.STATE != TERRITORY_PR][self._variable_name].isnull().any()
        )
        self.assertTrue(
            df[df.STATE == TERRITORY_PR][self._variable_name].isnull().all()
        )


class ShapefileTestCase(unittest.TestCase):

    PATH_PREFIX = "test_integration_shapefiles_"

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

    def test_county_cb_shapefile(self):
        gdf_counties = self.reader.read_cb_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3233, 10), gdf_counties.shape)

    def test_puma_shapefile(self):
        gdf_puma = self.reader.read_cb_shapefile("us", "puma")

        self.assertIsInstance(gdf_puma, gpd.GeoDataFrame)

        self.assertEqual((2380, 9), gdf_puma.shape)

    def test_2010_shapefile(self):
        # Override the normal setup for 2010.
        self._year = 2010
        self.reader = cmp.ShapeReader(self.shapefile_path, self._year)

        gdf_counties = self.reader.read_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3221, 18), gdf_counties.shape)

    def test_2010_cb_shapefile(self):
        # Override the normal setup for 2010.
        self._year = 2010
        self.reader = cmp.ShapeReader(self.shapefile_path, self._year)

        gdf_counties = self.reader.read_cb_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3221, 7), gdf_counties.shape)


class AddInferredGeographyTestCase(unittest.TestCase):
    """Test our ability to add inferred geometry."""

    PATH_PREFIX = "test_integration_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        cls.shapefile_path = tempfile.mkdtemp(prefix=cls.PATH_PREFIX)

    def setUp(self) -> None:
        """Set up before each test."""
        self._year = 2020
        self.reader = cmp.ShapeReader(self.shapefile_path, self._year)

    def test_state(self):
        """Test that we can infer state geometries."""
        df_state = pd.DataFrame(
            [[STATE_NJ, 0.5, 0.6], [STATE_CA, 0.1, 0.2]],
            columns=["STATE", "metric1", "metric2"],
        )

        gdf_inferred = ced.add_inferred_geography(df_state, self._year)

        self._assert_data_unchanged_in_inference(df_state, gdf_inferred)

        # Now get the state shapefile directly and see if we
        # inferred the right geometries.

        gdf_state = self.reader.read_cb_shapefile("us", "state")

        for state in df_state["STATE"]:
            self.assertTrue(
                gdf_state[gdf_state.STATEFP == state].geometry.iloc[0],
                gdf_inferred[gdf_inferred.STATE == state].geometry.iloc[0],
            )

    def test_county(self):
        """Test that we can infer a county geometries."""
        df_county = pd.DataFrame(
            [[STATE_NJ, "011", 0.5, 0.6], [STATE_NJ, "013", 0.1, 0.2]],
            columns=["STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred = ced.add_inferred_geography(df_county, self._year)

        self._assert_data_unchanged_in_inference(df_county, gdf_inferred)

        # Now get the county shapefile directly and see if we
        # inferred the right geometries.

        gdf_county = self.reader.read_cb_shapefile("us", "county")

        for row in df_county[["STATE", "COUNTY"]].itertuples():
            state, county = row.STATE, row.COUNTY
            self.assertEqual(
                gdf_county[
                    (gdf_county.STATEFP == state) & (gdf_county.COUNTYFP == county)
                ].geometry.iloc[0],
                gdf_inferred[
                    (gdf_inferred.STATE == state) & (gdf_inferred.COUNTY == county)
                ].geometry.iloc[0],
            )

    def test_tract(self):
        """Test that we can infer census tract geometries."""
        df_tract = pd.DataFrame(
            [
                [STATE_NJ, "013", "019000", 0.1, 0.2],
                [STATE_NJ, "013", "019100", 0.3, 0.4],
                [STATE_NJ, "013", "019200", 0.5, 0.6],
                [STATE_NY, "061", "021600", 1.0, 1.1],
                [STATE_NY, "061", "021800", 1.2, 1.3],
            ],
            columns=["STATE", "COUNTY", "TRACT", "metric1", "metric2"],
        )

        gdf_inferred = ced.add_inferred_geography(df_tract, self._year)

        self._assert_data_unchanged_in_inference(df_tract, gdf_inferred)

        # Now get the county shapefiles directly and see if we
        # inferred the right geometries.

        gdf_tract_nj = self.reader.read_cb_shapefile(STATE_NJ, "tract")
        gdf_tract_ny = self.reader.read_cb_shapefile(STATE_NY, "tract")

        gdf_tract = gdf_tract_nj.append(gdf_tract_ny)

        for row in df_tract[["STATE", "COUNTY", "TRACT"]].itertuples():
            state, county, tract = row.STATE, row.COUNTY, row.TRACT
            self.assertEqual(
                gdf_tract[
                    (gdf_tract.STATEFP == state)
                    & (gdf_tract.COUNTYFP == county)
                    & (gdf_tract.TRACTCE == tract)
                ].geometry.iloc[0],
                gdf_inferred[
                    (gdf_inferred.STATE == state)
                    & (gdf_inferred.COUNTY == county)
                    & (gdf_inferred.TRACT == tract)
                ].geometry.iloc[0],
            )

    def _assert_data_unchanged_in_inference(self, df, gdf_inferred):
        """
        Assert that when we added a geometry column nothing else changed.

        Parameters
        ----------
        df
            The original df.
        gdf_inferred
            The gdf with inferred geometry.
        """
        # We should have the name number of rows and one new column
        # for geometry.
        old_shape = df.shape
        new_shape = gdf_inferred.shape

        self.assertEqual(old_shape[0], new_shape[0])
        self.assertEqual(old_shape[1] + 1, new_shape[1])

        self.assertTrue(all(col in gdf_inferred.columns for col in df.columns))
        self.assertIn("geometry", gdf_inferred.columns)

        # Make sure all the data we had stayed where it was.
        self.assertTrue((gdf_inferred[df.columns] == df).all().all())
