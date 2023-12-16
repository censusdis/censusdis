# Copyright (c) 2023 Darren Erik Vengroff
"""
These are integration tests because they require access to the remote census API.

Most of the functionality can be unit tested elsewhere or with mocks, but
these tests actually call the census API itself to cover the bits of code
immediately around those calls.
"""
import os
import tempfile
import unittest
from pathlib import Path

import geopandas
import geopandas as gpd
import numpy as np
import pandas as pd

import censusdis.data as ced
import censusdis.impl.exceptions
import censusdis.impl.varsource.censusapi
import censusdis.maps as cem
import utils.symbolic as sym
import censusdis.values as cev
from censusdis import states
import censusdis.counties.new_jersey
from censusdis.datasets import ACS3, ACS5, DECENNIAL_PUBLIC_LAW_94_171
from censusdis.states import WA, NY, NJ, CT, PA


class DownloadTestCase(unittest.TestCase):
    """
    Test the full download capability.

    This is more an integration test than a unit test, which
    calls the census api and downloads real data. We are mainly
    just testing that we can do this without error. We're not that
    concerned with the data that comes back.
    """

    def setUp(self) -> None:
        """Set up before each test."""
        self._dataset = "acs/acs5"
        self._year = 2020
        self._group_name = "B19001"
        self._name = f"{self._group_name}_001E"

    def test_download(self):
        """Download just a couple of variables."""
        df = ced.download(
            self._dataset, self._year, ["NAME", self._name], state=states.NJ, county="*"
        )

        self.assertEqual((21, 4), df.shape)

        self.assertEqual(["STATE", "COUNTY", "NAME", "B19001_001E"], list(df.columns))

    def test_bad_variable(self):
        """Try to download a variable that does not exist."""
        with self.assertRaises(censusdis.impl.exceptions.CensusApiException) as cm:
            ced.download(
                self._dataset,
                self._year,
                ["NAME", "I_DONT_EXIST"],
                state=states.NJ,
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

    def test_download_with_bad_values(self):
        """Test replacing bad values with NaN."""
        median_income_variable = "B19013_001E"

        df_raw = ced.download(
            self._dataset,
            self._year,
            ["NAME", median_income_variable],
            state=states.GA,
            tract="*",
            set_to_nan=False,
        )

        df_nan = ced.download(
            self._dataset,
            self._year,
            ["NAME", median_income_variable],
            state=states.GA,
            tract="*",
            set_to_nan=cev.ALL_SPECIAL_VALUES,
        )

        self.assertEqual(df_raw.shape, df_nan.shape)

        self.assertTrue(
            (
                df_raw[median_income_variable] == cev.INSUFFICIENT_SAMPLE_OBSERVATIONS
            ).any()
        )
        self.assertFalse(
            (
                df_nan[median_income_variable] == cev.INSUFFICIENT_SAMPLE_OBSERVATIONS
            ).any()
        )

        self.assertFalse(df_raw[median_income_variable].isna().any())
        self.assertTrue(df_nan[median_income_variable].isna().any())

        self.assertTrue(
            (
                (df_raw[median_income_variable] == cev.INSUFFICIENT_SAMPLE_OBSERVATIONS)
                == df_nan[median_income_variable].isna()
            ).all(),
            "All locations that were cev.INSUFFICIENT_SAMPLE_OBSERVATIONS should be NaN.",
        )

    def test_multi_state(self):
        """
        Test the case where the only geo argument has multiple values.

        As in `state=[states.NJ, states.NY]`, vs. the more general
        `state="*"`.
        """
        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[states.NJ, states.NY],
        )

        self.assertEqual((2, 3), df.shape)

        self.assertIn(states.NJ, list(df["STATE"]))
        self.assertIn(states.NY, list(df["STATE"]))

    def test_multi_county(self):
        """
        Test the case where the first geo argument has multiple values.

        As in `state=[states.NJ, states.NY]`, vs. the more general
        `state="*"` and `county="*"`.
        """
        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[states.NJ, states.NY],
            county="*",
        )

        self.assertEqual((83, 4), df.shape)

        df_51 = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=states.ALL_STATES_AND_DC,
            county="*",
        )

        df_star = ced.download(
            self._dataset, self._year, ["NAME", self._name], state="*", county="*"
        )

        # This will get us some outside the 51.
        self.assertLess(len(df_51.index), len(df_star.index))

        df_star = df_star[df_star.STATE.isin(states.ALL_STATES_AND_DC)]

        self.assertEqual(len(df_51.index), len(df_star.index))

    def test_multi_tract(self):
        """
        Test the case where the first geo argument has multiple values.

        As in `state=[states.NJ, states.NY]`, vs. the more general
        `state="*"` and `tract="*"`.

        In this test we also skip a level.
        """
        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[states.NJ, states.NY],
            tract="*",
        )

        self.assertEqual((7592, 5), df.shape)

        self.assertIn("STATE", df.columns)
        self.assertIn("COUNTY", df.columns)
        self.assertIn("TRACT", df.columns)
        self.assertIn("NAME", df.columns)
        self.assertIn(self._name, df.columns)

    def test_multi_bg(self):
        """
        Test the case where the first geo argument has multiple values.

        As in `state=[states.NJ, states.NY]`, vs. the more general
        `state="*"` and `tract="*"`.

        In this test we also skip two levels.
        """
        df = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            state=[states.NJ, states.NY],
            block_group="*",
        )

        self.assertEqual((22669, 6), df.shape)

        self.assertIn("STATE", df.columns)
        self.assertIn("COUNTY", df.columns)
        self.assertIn("TRACT", df.columns)
        self.assertIn("BLOCK_GROUP", df.columns)
        self.assertIn("NAME", df.columns)
        self.assertIn(self._name, df.columns)

    def test_get_all_groups(self):
        """Test get_all_groups and related functionality."""
        df_groups = ced.variables.all_groups(self._dataset, self._year)

        group = df_groups.iloc[0]["GROUP"]

        df_variables = ced.variables.all_variables(self._dataset, self._year, group)

        self.assertEqual((49, 7), df_variables.shape)

        self.assertEqual(
            [
                "YEAR",
                "DATASET",
                "GROUP",
                "VARIABLE",
                "LABEL",
                "SUGGESTED_WEIGHT",
                "VALUES",
            ],
            list(df_variables.columns),
        )

        self.assertTrue((df_variables["GROUP"] == group).all())

    def test_get_all_datasets(self):
        """Test getting all data sets."""
        df_datasets = ced.variables.all_data_sets()

        df_datasets_for_year = ced.variables.all_data_sets(year=self._year)

        self.assertEqual(list(df_datasets.columns), list(df_datasets_for_year.columns))

        # There are more total than in the one year.
        self.assertGreater(len(df_datasets.index), len(df_datasets_for_year.index))

        # Everything in the year is in the year.
        self.assertTrue((df_datasets_for_year["YEAR"] == self._year).all())

        # Everything in the year is in the df of all datasets.
        df_both = df_datasets_for_year.merge(
            df_datasets,
            on=list(df_datasets.columns),
        )

        self.assertEqual(df_both.shape, df_datasets_for_year.shape)

        self.assertTrue((df_both == df_datasets_for_year).all().all())


class DownloadWithGeometryTestCase(unittest.TestCase):
    """
    Test downloading with geometry at many different geo levels.

    This is similar to `DownloadTestCase` but adds geometry to
    make sure the mappings to shapefiles and merges happen correctly.
    """

    PATH_PREFIX = "test_integration_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        ced.set_shapefile_path(Path(tempfile.mkdtemp(prefix=cls.PATH_PREFIX)))

    def setUp(self) -> None:
        """Set up before each test."""
        self._dataset = "acs/acs5"
        self._year = 2020
        self._group_name = "B19001"
        self._name = f"{self._group_name}_001E"

    def test_path(self):
        """Are we using the right cache path for shapefiles."""
        path = ced.get_shapefile_path()

        filename = path.name
        self.assertTrue(filename.startswith(self.PATH_PREFIX))

    def test_download_with_geometry_region(self):
        """Download at the region level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            region="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((4, 4), gdf.shape)

        self.assertEqual(
            ["REGION", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
        )

    def test_download_with_geometry_division(self):
        """Download at the region level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            division="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((9, 4), gdf.shape)

        self.assertEqual(
            ["DIVISION", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
        )

    def test_download_with_geometry_zcta(self):
        """Download at the zip code tabulation area level with geometry."""
        for year, num_zcta in (2020, 33_120), (2022, 33_774):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                zip_code_tabulation_area="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_zcta, 4), gdf.shape)

            self.assertEqual(
                ["ZIP_CODE_TABULATION_AREA", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_state(self):
        """Download at the state level with geometry."""
        for year in range(2009, 2023):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((52, 4), gdf.shape)

            self.assertEqual(
                ["STATE", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
            )

    def test_download_with_geometry_state_zcta(self):
        """
        Download at the state and zip code tabulation area level with geometry.

        Before 2020, the data model nested zcta inside of state.
        """
        for year, num_zcta in (2011, 595), (2019, 595):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=NJ,
                zip_code_tabulation_area="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_zcta, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "ZIP_CODE_TABULATION_AREA",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_multi_state(self):
        """
        Download at the tract level for multiple states with geometry.

        The point of this test is that tract-level shapefiles exist
        only on a per-state basis, so inside the call we have to
        recognize this and download and concatenate several shapefiles
        before merging with our data.
        """
        for year, num_tracts in (2010, 1348), (2020, 1614):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=["01", "02"],  # Two specific states.
                tract="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_tracts, 6), gdf.shape)

            self.assertEqual(
                ["STATE", "COUNTY", "TRACT", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_county(self):
        """Download at the county level with geometry."""
        for year in range(2009, 2023):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((21, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "COUNTY", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_county_subdivision(self):
        """Download at the county subdivision level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=states.NJ,
            county=censusdis.counties.new_jersey.HUDSON,
            county_subdivision="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((12, 6), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "COUNTY",
                "COUNTY_SUBDIVISION",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_tract(self):
        """Download at the tract level with geometry."""
        for year, num_tracts in (
            (2009, 64),
            (2010, 70),
            (2015, 70),
            (2020, 74),
            (2022, 74),
        ):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county="001",
                tract="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_tracts, 6), gdf.shape)

            self.assertEqual(
                ["STATE", "COUNTY", "TRACT", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_block_group(self):
        """Download at the county level with geometry."""
        for year, num_bg in (2013, 184), (2020, 194), (2022, 194):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county="001",
                block_group="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_bg, 7), gdf.shape)

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

    def test_download_with_geometry_place(self):
        """Download at the PLACE level with geometry."""
        for year, num_place in (2010, 545), (2015, 545), (2020, 701), (2022, 700):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                place="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_place, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "PLACE", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_consolidated_city(self):
        """Download at the consolidated city level with geometry."""
        for year in range(2010, 2023, 2):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.IN,
                consolidated_city="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((1, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "CONSOLIDATED_CITY", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_congressional_district(self):
        """Download at the congressional district level with geometry."""
        for year, num_districts in (
            (2009, 13),
            (2010, 13),
            (2011, 13),
            (2012, 12),
            (2020, 12),
            (2022, 12),
        ):
            gdf = ced.download(
                self._dataset,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                congressional_district="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_districts, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "CONGRESSIONAL_DISTRICT", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_state_legislative_district_upper(self):
        """Download at the slate legislative district upper chamber level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=states.NY,
            state_legislative_district_upper_chamber="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((63, 5), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "STATE_LEGISLATIVE_DISTRICT_UPPER_CHAMBER",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_state_legislative_district_lower(self):
        """Download at the slate legislative district lower chamber level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=states.NY,
            state_legislative_district_lower_chamber="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((150, 5), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "STATE_LEGISLATIVE_DISTRICT_LOWER_CHAMBER",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_voting_district(self):
        """Download at the voting district level with geometry."""
        gdf = ced.download(
            DECENNIAL_PUBLIC_LAW_94_171,
            self._year,
            ["NAME", "P1_001N"],
            with_geometry=True,
            state=states.NJ,
            county=censusdis.counties.new_jersey.HUDSON,
            voting_district="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((452, 6), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "COUNTY",
                "VOTING_DISTRICT",
                "NAME",
                "P1_001N",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_school_district_unified(self):
        """Download at the school district unified level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=states.NJ,
            school_district_unified="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((343, 5), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "SCHOOL_DISTRICT_UNIFIED",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_school_district_elementary(self):
        """Download at the school district elementary level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=states.NJ,
            school_district_elementary="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((172, 5), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "SCHOOL_DISTRICT_ELEMENTARY",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_school_district_secondary(self):
        """Download at the school district secondary level with geometry."""
        gdf = ced.download(
            self._dataset,
            self._year,
            ["NAME", self._name],
            with_geometry=True,
            state=states.NJ,
            school_district_secondary="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((47, 5), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "SCHOOL_DISTRICT_SECONDARY",
                "NAME",
                "B19001_001E",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_not_available(self):
        """Download at a geography level that has no geometry available."""
        with self.assertRaises(
            censusdis.impl.exceptions.CensusApiException
        ) as assertion:
            ced.download(
                self._dataset,
                self._year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                combined_statistical_area_or_part="*",
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
            state=states.NJ,
            combined_statistical_area_or_part="*",
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertNotIsInstance(df, gpd.GeoDataFrame)

        self.assertEqual((2, 4), df.shape)


class DownloadWideTestCase(unittest.TestCase):
    """
    Test downloading wide tables.

    For these cases, we have to make multiple calls to the census
    API and then merge or concatenate the results that come back,
    depending on the details of the scenario.
    """

    def test_wide_merge(self):
        """
        Download a really wide set of variables.

        The goal is to trigger a call to
        `_download_multiple`. This version is for a scenario
        that will trigger the merge strategy because each
        sub-query will have rows with a unique geogrpahic key.
        """
        dataset = "acs/acs1/spp"
        year = 2019
        group = "S0201"

        variables = ced.variables.group_variables(
            dataset, year, group, skip_annotations=False
        )

        self.assertGreater(len(variables), ced._MAX_VARIABLES_PER_DOWNLOAD)

        metrics_0 = ced._download_wide_strategy_metrics()

        df = ced.download(dataset, year, variables, state="*")

        metrics_1 = ced._download_wide_strategy_metrics()

        metrics_diff = {k: v - metrics_0[k] for k, v in metrics_1.items()}

        self.assertEqual(1, metrics_diff["merge"])
        self.assertEqual(0, metrics_diff["concat"])

        self.assertEqual((51, 1 + len(variables)), df.shape)

        columns = set(df.columns)
        for variable in variables:
            self.assertIn(variable, columns)

    def test_wide_concat(self):
        """
        Download a really wide set of variables.

        The goal is to trigger a call to
        `_download_multiple`. This version is for a scenario
        that will trigger the concat strategy because the
        query column (state in this case) is not unique.
        """
        dataset = "cps/basic/nov"
        year = 2020

        variables = ced.variables.group_variables(dataset, year, None)

        self.assertEqual(389, len(variables))
        self.assertGreater(len(variables), ced._MAX_VARIABLES_PER_DOWNLOAD)

        metrics_0 = ced._download_wide_strategy_metrics()

        with self.assertLogs(ced.__name__, level="INFO") as cm:
            df = ced.download(dataset, year, variables, state=states.NJ)

        # Make sure we got the log message.

        self.assertTrue(
            any(
                message.startswith(
                    "INFO:censusdis.data:Using the concat strategy, which is not guaranteed reliable if "
                )
                for message in cm.output
            )
        )

        metrics_1 = ced._download_wide_strategy_metrics()

        metrics_diff = {k: v - metrics_0[k] for k, v in metrics_1.items()}

        self.assertEqual(1, metrics_diff["concat"])
        self.assertEqual(0, metrics_diff["merge"])

        # One column per variable, plus state. Lots of rows.
        self.assertEqual((2109, len(variables) + 1), df.shape)

        # All the same state.
        self.assertTrue((df["STATE"] == states.NJ).all())

        # One column per variable plus state.
        columns = set(df.columns)
        for variable in ["STATE"] + variables:
            self.assertIn(variable, columns)


class DownloadGroupTestCase(unittest.TestCase):
    """
    Test downloading by group.

    This is more an integration test than a unit test, which
    calls the census api and downloads real data. Similar to
    :py:class:`~DownloadTestCase` but with a focus on using
    the `group` and `leaves_of_group` args.
    """

    def setUp(self) -> None:
        """Set up before each test."""
        self._variable_source = (
            censusdis.impl.varsource.censusapi.CensusApiVariableSource()
        )
        self._dataset = "acs/acs5"
        self._year = 2019
        self._group_name_0 = "B19001"
        self._group_name_1 = "B03002"

    def test_group(self):
        """Download the whole group."""
        df_group = ced.download(
            self._dataset,
            self._year,
            group=self._group_name_0,
            state=states.NJ,
            county="*",
        )

        # Make sure we got the variables we expected.
        group_variables = ced.variables.group_variables(
            self._dataset, self._year, self._group_name_0
        )

        self.assertEqual(["STATE", "COUNTY"] + group_variables, list(df_group.columns))

    def test_leaves_of_group(self):
        """Download the leaves of the group."""
        df_leaves = ced.download(
            self._dataset,
            self._year,
            leaves_of_group=self._group_name_0,
            state=states.NJ,
            county="*",
        )

        # Make sure we got the variables we expected.
        leaf_variables = ced.variables.group_leaves(
            self._dataset, self._year, self._group_name_0
        )

        self.assertEqual(["STATE", "COUNTY"] + leaf_variables, list(df_leaves.columns))

    def test_group_plus(self):
        """Download the whole group plus another variable."""
        extra_variable = "NAME"

        df_group = ced.download(
            self._dataset,
            self._year,
            [extra_variable, extra_variable],  # should dedup here also
            group=self._group_name_0,
            state=states.NJ,
            county="*",
        )

        # Make sure we got the variables we expected.
        group_variables = ced.variables.group_variables(
            self._dataset, self._year, self._group_name_0
        )

        self.assertEqual(
            ["STATE", "COUNTY", extra_variable] + group_variables,
            list(df_group.columns),
        )

    def test_leaves_of_group_plus(self):
        """Download the leaves of the group plus another variable."""
        extra_variable = "NAME"

        df_leaves = ced.download(
            self._dataset,
            self._year,
            extra_variable,
            leaves_of_group=self._group_name_0,
            state=states.NJ,
            county="*",
        )

        # Make sure we got the variables we expected.
        leaf_variables = ced.variables.group_leaves(
            self._dataset, self._year, self._group_name_0
        )

        self.assertEqual(
            ["STATE", "COUNTY", extra_variable] + leaf_variables,
            list(df_leaves.columns),
        )

    def test_group_with_dups(self):
        """Test the case where some variables are double specified."""
        group_variables = ced.variables.group_variables(
            self._dataset, self._year, self._group_name_0
        )

        some_group_variables = [
            group_variables[ii] for ii in range(0, len(group_variables), 2)
        ]
        # Be sure we are requesting a few twice.
        self.assertGreater(len(some_group_variables), 2)

        df_leaves = ced.download(
            self._dataset,
            self._year,
            some_group_variables,
            group=self._group_name_0,
            state=states.NJ,
            county="*",
        )

        # Should be no dups. State and county are the two added.
        self.assertEqual(len(df_leaves.columns), 2 + len(group_variables))

        # Make sure we got the variables we expected.
        returned_variables = set(df_leaves.columns)

        self.assertEqual(len(returned_variables), len(df_leaves.columns))

        # State county and the extra are the two added.
        self.assertEqual(len(returned_variables), 2 + len(group_variables))

        for variable in group_variables:
            self.assertIn(variable, returned_variables)

        self.assertIn("STATE", returned_variables)
        self.assertIn("COUNTY", returned_variables)

    def test_leaves_of_group_with_dups(self):
        """Test the case where some variables are double specified."""
        extra_variable = "NAME"
        leaf_variables = ced.variables.group_leaves(
            self._dataset, self._year, self._group_name_0
        )

        some_leaf_variables = [
            leaf_variables[ii] for ii in range(0, len(leaf_variables), 2)
        ]
        # Be sure we are requesting a few twice.
        self.assertGreater(len(some_leaf_variables), 2)

        df_leaves = ced.download(
            self._dataset,
            self._year,
            [extra_variable] + some_leaf_variables,
            leaves_of_group=self._group_name_0,
            state=states.NJ,
            county="*",
        )

        # Should be no dups.
        # State, county, and the extra are the three added.
        self.assertEqual(len(df_leaves.columns), 3 + len(leaf_variables))

        # Make sure we got the variables we expected.
        returned_variables = set(df_leaves.columns)

        self.assertEqual(len(returned_variables), len(df_leaves.columns))

        # State county and the extra are the three added.
        self.assertEqual(len(returned_variables), 3 + len(leaf_variables))

        for variable in leaf_variables:
            self.assertIn(variable, returned_variables)

        self.assertIn("STATE", returned_variables)
        self.assertIn("COUNTY", returned_variables)
        self.assertIn(extra_variable, returned_variables)

    def test_multiple_groups(self):
        """Download from more than one group."""
        df_group = ced.download(
            self._dataset,
            self._year,
            group=[self._group_name_0, self._group_name_1],
            leaves_of_group=[self._group_name_0],
            state=states.NJ,
            county="*",
        )

        # Make sure we got the variables we expected.
        group_variables = ced.variables.group_variables(
            self._dataset, self._year, self._group_name_0
        ) + ced.variables.group_variables(self._dataset, self._year, self._group_name_1)

        self.assertEqual(["STATE", "COUNTY"] + group_variables, list(df_group.columns))

    def test_download_wide_survey(self):
        """Test case where row_keys are required to download more than 50 variables."""
        df_all_vars = ced.variables.all_variables("cps/internet/nov", 2021, None)
        all_vars = df_all_vars["VARIABLE"].to_list()

        df_wide = ced.download(
            "cps/internet/nov",
            2021,
            download_variables=all_vars,
            row_keys=["QSTNUM", "OCCURNUM"],
            state=WA,
        )

        self.assertIsInstance(df_wide, pd.DataFrame)

        self.assertEqual(df_wide.shape, (1836, 500))

        # Need to use sets because the row keys will have moved to the front of the dataframe
        self.assertEqual(set(["STATE"] + all_vars), set(df_wide.columns.to_list()))


class GeoNameTestCase(unittest.TestCase):
    """Test the ability to download geography names."""

    def test_county(self):
        """Test at the county level."""
        df_name = ced.geography_names(ACS5, 2020, state=states.NJ, county="017")

        self.assertEqual((1, 3), df_name.shape)

        self.assertEqual(["STATE", "COUNTY", "NAME"], list(df_name.columns))

        self.assertEqual("Hudson County, New Jersey", df_name["NAME"].iloc[0])


class AcsSubjectTestCase(unittest.TestCase):
    """Test on ACS Subject Data that includes null in an int field."""

    def setUp(self) -> None:
        """Set up before each test."""
        self._dataset = "acs/acs5/profile"
        self._year = 2021
        self._variable_name = "DP02_0001E"

    def test_states_with_null_in_pr(self):
        """Test a corner case where there is a null for PR."""
        df = ced.download(
            self._dataset, self._year, ["NAME", self._variable_name], state="*"
        )

        self.assertEqual((52, 3), df.shape)

        # The API returns a null for PR but numbers for all others.
        # We have to convert to a float to represent this even though
        # the census metadata says the variable is an int.
        self.assertEqual(np.float64, df[self._variable_name].dtype)

        self.assertFalse(df[df.STATE != states.PR][self._variable_name].isnull().any())
        self.assertTrue(df[df.STATE == states.PR][self._variable_name].isnull().all())


class ShapefileTestCase(unittest.TestCase):
    """Test shapefile functionality."""

    PATH_PREFIX = "test_integration_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        cls.shapefile_path = tempfile.mkdtemp(prefix=cls.PATH_PREFIX)

    def setUp(self) -> None:
        """Set up before each test."""
        self._year = 2019
        self.reader = cem.ShapeReader(self.shapefile_path, self._year)

    def test_county_shapefile(self):
        """Test reading a county level shapefile for the whole country."""
        gdf_counties = self.reader.read_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3233, 18), gdf_counties.shape)

    def test_county_cb_shapefile(self):
        """Test reading a county level cb shapefile for the whole country."""
        gdf_counties = self.reader.read_cb_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3233, 10), gdf_counties.shape)

    def test_puma_shapefile(self):
        """Test reading a puma level shapefile for the whole country."""
        gdf_puma = self.reader.read_cb_shapefile("us", "puma")

        self.assertIsInstance(gdf_puma, gpd.GeoDataFrame)

        self.assertEqual((2380, 9), gdf_puma.shape)

    def test_2010_shapefile(self):
        """Test special behavior in 2010."""
        # Override the normal setup for 2010.
        self._year = 2010
        self.reader = cem.ShapeReader(self.shapefile_path, self._year)

        gdf_counties = self.reader.read_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3221, 18), gdf_counties.shape)

    def test_2010_cb_shapefile(self):
        """Test special behavior in 2010."""
        # Override the normal setup for 2010.
        self._year = 2010
        self.reader = cem.ShapeReader(self.shapefile_path, self._year)

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
        self._year0 = 2020
        self.reader0 = cem.ShapeReader(self.shapefile_path, self._year0)

    def test_state(self):
        """Test that we can infer state geometries."""
        df_state = pd.DataFrame(
            [[states.NJ, 0.5, 0.6], [states.CA, 0.1, 0.2]],
            columns=["STATE", "metric1", "metric2"],
        )

        gdf_inferred = ced.add_inferred_geography(df_state, self._year0)

        self._assert_data_unchanged_in_inference(df_state, gdf_inferred)

        # Now get the state shapefile directly and see if we
        # inferred the right geometries.

        gdf_state = self.reader0.read_cb_shapefile("us", "state")

        for state in df_state["STATE"]:
            self.assertTrue(
                gdf_state[gdf_state.STATEFP == state].geometry.iloc[0],
                gdf_inferred[gdf_inferred.STATE == state].geometry.iloc[0],
            )

    def test_county(self):
        """Test that we can infer a county geometries."""
        df_county = pd.DataFrame(
            [[states.NJ, "011", 0.5, 0.6], [states.NJ, "013", 0.1, 0.2]],
            columns=["STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred = ced.add_inferred_geography(df_county, self._year0)

        self._assert_data_unchanged_in_inference(df_county, gdf_inferred)

        # Now get the county shapefile directly and see if we
        # inferred the right geometries.

        gdf_county = self.reader0.read_cb_shapefile("us", "county")

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
                [states.NJ, "013", "019000", 0.1, 0.2],
                [states.NJ, "013", "019100", 0.3, 0.4],
                [states.NJ, "013", "019200", 0.5, 0.6],
                [states.NY, "061", "021600", 1.0, 1.1],
                [states.NY, "061", "021800", 1.2, 1.3],
            ],
            columns=["STATE", "COUNTY", "TRACT", "metric1", "metric2"],
        )

        gdf_inferred = ced.add_inferred_geography(df_tract, self._year0)

        self._assert_data_unchanged_in_inference(df_tract, gdf_inferred)

        # Now get the county shapefiles directly and see if we
        # inferred the right geometries.

        gdf_tract_nj = self.reader0.read_cb_shapefile(states.NJ, "tract")
        gdf_tract_ny = self.reader0.read_cb_shapefile(states.NY, "tract")

        gdf_tract = gpd.GeoDataFrame(pd.concat([gdf_tract_nj, gdf_tract_ny]))

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

    def test_multi_year(self):
        """Test inferring geometry in a multi-year df."""
        df_county_multi_year = pd.DataFrame(
            [
                [2019, states.NJ, "011", 0.5, 0.6],
                [2019, states.NJ, "013", 0.1, 0.2],
                [2020, states.NJ, "011", 1.5, 1.6],
                [2020, states.NJ, "013", 1.1, 1.2],
                [2021, states.NJ, "011", 2.5, 2.6],
                [2021, states.NJ, "013", 2.5, 2.5],
            ],
            columns=["YEAR", "STATE", "COUNTY", "metric1", "metric2"],
        )

        df_county_by_year = {
            year: df_for_year
            for year, df_for_year in df_county_multi_year.groupby("YEAR")
        }

        gdf_inferred_geometry_multi_year = ced.add_inferred_geography(
            df_county_multi_year
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_multi_year
        )

        gdf_inferred_geometry_by_year = {
            year: ced.add_inferred_geography(df_for_year)
            for year, df_for_year in df_county_by_year.items()
        }

        gdf_inferred_geometry_by_year_all = gpd.GeoDataFrame(
            pd.concat(gdf_inferred_geometry_by_year.values()).reset_index(drop=True)
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_by_year_all
        )

        self.assertTrue(
            gdf_inferred_geometry_multi_year.equals(gdf_inferred_geometry_by_year_all)
        )

    def test_multi_year_missing_map_year(self):
        """Test inferring geometry when there are no maps for one year."""
        df_county_multi_year = pd.DataFrame(
            [
                # There are no maps for 1999.
                [1999, states.NJ, "011", 0.4, 0.5],
                [1999, states.NJ, "013", 0.0, 0.1],
                [2019, states.NJ, "011", 0.5, 0.6],
                [2019, states.NJ, "013", 0.1, 0.2],
                [2020, states.NJ, "011", 1.5, 1.6],
                [2020, states.NJ, "013", 1.1, 1.2],
                [2021, states.NJ, "011", 2.5, 2.6],
                [2021, states.NJ, "013", 2.5, 2.5],
            ],
            columns=["YEAR", "STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred_geometry_multi_year = ced.add_inferred_geography(
            df_county_multi_year
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_multi_year
        )

        # Make sure there is no geometry for 1999, but there is geometry
        # for other years.
        self.assertTrue(
            gdf_inferred_geometry_multi_year[
                gdf_inferred_geometry_multi_year["YEAR"] == 1999
            ]["geometry"]
            .isnull()
            .all()
        )

        self.assertFalse(
            gdf_inferred_geometry_multi_year[
                gdf_inferred_geometry_multi_year["YEAR"] != 1999
            ]["geometry"]
            .isnull()
            .any()
        )

    def test_multi_year_no_maps(self):
        """Test inferring geometry when there are no maps for any year."""
        df_county_multi_year = pd.DataFrame(
            [
                # There are no maps for these years.
                [1999, states.NJ, "011", 0.4, 0.5],
                [1999, states.NJ, "013", 0.0, 0.1],
                [1998, states.NJ, "011", 0.5, 0.6],
                [1998, states.NJ, "013", 0.1, 0.2],
            ],
            columns=["YEAR", "STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred_geometry_multi_year = ced.add_inferred_geography(
            df_county_multi_year
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_multi_year
        )

        # Make sure there is no geometry.
        self.assertTrue(gdf_inferred_geometry_multi_year["geometry"].isnull().all())


class LongIdTestCase(unittest.TestCase):
    """
    Test long IDs.

    Sometimes the metadata says a variable is an int, but it is
    too long to fit into one. So we fall back on treating it like
    a string.

    We used to fail to do this as described in issue #98.
    """

    def test_cps_asec_mar(self):
        """Test with the cps/asec/mar dataset."""
        df_cps_asec_mar = ced.download("cps/asec/mar", 2020, "H_IDNUM", state="*")

        self.assertEqual(2, len(df_cps_asec_mar.columns))
        self.assertIn("STATE", df_cps_asec_mar.columns)
        self.assertIn("H_IDNUM", df_cps_asec_mar.columns)


class RemoveWaterTestCase(unittest.TestCase):
    """Test removing water."""

    def test_remove_water_nyc(self):
        """Test census tracts in NYC."""
        nyc_counties = [
            "061",
            "081",
        ]  # "005", "047", "085"]

        # We use EPSG 3857 since we will be computing areas.

        gdf_tracts = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NY,
            county=nyc_counties,
            tract="*",
            with_geometry=True,
            remove_water=False,
        ).to_crs(epsg=3857)

        gdf_tracts_no_water = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NY,
            county=nyc_counties,
            tract="*",
            with_geometry=True,
            remove_water=True,
        ).to_crs(epsg=3857)

        # We should not lose any tracts.
        self.assertEqual(gdf_tracts.shape, gdf_tracts_no_water.shape)

        # The names should be the same.
        self.assertTrue(gdf_tracts.NAME.equals(gdf_tracts_no_water.NAME))

        # Some of the areas of the tracts without water should be smaller than or
        # equal to those of the original.
        self.assertTrue(
            (gdf_tracts_no_water.geometry.area < gdf_tracts.geometry.area).any()
        )

        # But there are some rare cases when they get distorted to be a little bigger.
        # Lat's make sure it's not a lot bigger.
        self.assertFalse(
            (gdf_tracts_no_water.geometry.area / gdf_tracts.geometry.area >= 1.01).any()
        )

    def test_remove_water_nj(self):
        """Test in which we don't have explicit counties to fetch water and join on."""
        df_nj = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NJ,
            with_geometry=True,
            remove_water=False,
        ).to_crs(epsg=3857)

        df_nj_remove_water = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NJ,
            with_geometry=True,
            remove_water=True,
        ).to_crs(epsg=3857)

        # All we have is the state boundary.
        self.assertEqual(1, len(df_nj.index))
        self.assertEqual(1, len(df_nj_remove_water.index))

        # Geometry should be a little different.
        self.assertNotEqual(
            df_nj["geometry"].iloc[0], df_nj_remove_water["geometry"].iloc[0]
        )


class SymbolicInsertTestCase(unittest.TestCase):
    """Test our ability to add symbolic names."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.df_datasets = ced.variables.all_data_sets()
        self.dataset_names = self.df_datasets["DATASET"].to_list()
        self.dataset_url = self.df_datasets["API BASE URL"].to_list()
        self.create_symbolic = sym.symbolic()
        self.symbolic_names = self.create_symbolic.store_dataset(
            self.dataset_names, self.dataset_url
        )
        self._variable_source = (
            censusdis.impl.varsource.censusapi.CensusApiVariableSource()
        )

    def test_insert_name_link(self):
        """Test that we can insert symbolic name and reference link of datasets to datasets.py."""
        file_path = os.path.realpath(__file__)
        file_directory = os.path.dirname(file_path)
        file_directory = file_directory.replace("tests", "censusdis")
        os.chdir(file_directory)

        with open("datasets.py", "r") as file:
            file_check = file.read()
            for key in self.symbolic_names.keys():
                value = self.symbolic_names[key]
                if not key.startswith("DEC") and not key.startswith("PUBS"):
                    self.assertTrue(key in file_check)
                    self.assertTrue(value[0] in file_check)
                    self.assertTrue(value[1] in file_check)
                elif key.startswith("DEC") or key.startswith("PUBS"):
                    self.assertTrue(value[0] in file_check)
                    self.assertTrue(value[1] in file_check)
                else:
                    self.assertTrue(value[0] in file_check)
                    self.assertTrue(value[1] in file_check)

    def test_use_symbolic_name(self):
        """Test that we can use symbolic name to download datasets."""
        dataset = ACS3
        year = 2011
        group_name = "B19001"
        name = f"{group_name}_001E"
        df = ced.download(dataset, year, ["NAME", name], state=states.NJ, county="*")
        self.assertGreaterEqual(len(df.index), 1)
        self.assertEqual(["STATE", "COUNTY", "NAME", "B19001_001E"], list(df.columns))


class IntersectingGeosTestCase(unittest.TestCase):
    """Test intersection geometry keywords."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.dataset = ACS5
        self.year = 2020

    def test_intersecting_geos_cbsa(self):
        """Test intersection with a CBSA."""
        geo_spec = ced._intersecting_geos_kws(
            self.dataset,
            self.year,
            containing_geo_kwargs=dict(
                # New York-Newark-Jersey City
                metropolitan_statistical_area_micropolitan_statistical_area="35620"
            ),
            state="*",
            county="*",
        )

        self.assertEqual(2, len(geo_spec))

        state_spec = geo_spec["state"]

        self.assertIsInstance(state_spec, list)
        self.assertEqual(4, len(state_spec))
        self.assertSetEqual({NY, NJ, CT, PA}, set(state_spec))

        self.assertEqual("*", geo_spec["county"])

    def test_intersecting_geos_place(self):
        """Test intersection with a place."""
        geo_spec = ced._intersecting_geos_kws(
            self.dataset,
            self.year,
            containing_geo_kwargs=dict(
                state=NJ,
                # Asbury Park city
                place="01960",
            ),
            state=NJ,
            tract="*",
        )

        self.assertEqual(2, len(geo_spec))

        self.assertEqual(NJ, geo_spec["state"])
        self.assertEqual("*", geo_spec["tract"])


class ContainedWithinTestCase(unittest.TestCase):
    """Test the contains within functionality."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.dataset = ACS5
        self.year = 2020

    def test_state_county_contained_within_cbsa(self):
        """Test state and county contained within a CBSA."""
        df = ced.contained_within(
            # New York-Newark-Jersey City
            metropolitan_statistical_area_micropolitan_statistical_area="35620"
        ).download(
            self.dataset, self.year, ["NAME", "B03002_001E"], state="*", county="*"
        )

        self.assertEqual((23, 5), df.shape)

        self.assertEqual(
            [
                "METROPOLITAN_STATISTICAL_AREA_MICROPOLITAN_STATISTICAL_AREA",
                "STATE",
                "COUNTY",
                "NAME",
                "B03002_001E",
            ],
            list(df.columns),
        )

    def test_tract_contained_within_place(self):
        """Test tracts contained within places."""
        gdf = ced.contained_within(
            state=NJ,
            # Asbury Park city
            place="01960",
        ).download(
            self.dataset,
            self.year,
            ["NAME", "B03002_001E"],
            state="*",
            tract="*",
            with_geometry=True,
        )

        self.assertIsInstance(gdf, gpd.GeoDataFrame)
        self.assertEqual((6, 7), gdf.shape)

        self.assertEqual(
            ["STATE", "PLACE", "COUNTY", "TRACT", "NAME", "B03002_001E", "geometry"],
            list(gdf.columns),
        )

    def test_zcta_contained_within_state(self):
        """Test zip code tabulation area in states."""
        gdf = ced.contained_within(
            state=NJ,
        ).download(
            self.dataset,
            self.year,
            ["NAME", "B03002_001E"],
            zip_code_tabulation_area="*",
            with_geometry=True,
        )

        self.assertIsInstance(gdf, gpd.GeoDataFrame)
        self.assertEqual((593, 5), gdf.shape)


if __name__ == "__main__":
    unittest.main()
