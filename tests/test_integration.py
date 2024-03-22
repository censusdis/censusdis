# Copyright (c) 2023 Darren Erik Vengroff
"""
These are integration tests because they require access to the remote census API.

Most of the functionality can be unit tested elsewhere or with mocks, but
these tests actually call the census API itself to cover the bits of code
immediately around those calls.
"""
import os
import unittest

import geopandas as gpd
import numpy as np
import pandas as pd

import censusdis.data as ced
import censusdis.impl.exceptions
import censusdis.impl.varsource.censusapi
import utils.symbolic as sym
import censusdis.values as cev
from censusdis import states
import censusdis.counties.new_jersey
from censusdis.datasets import ACS3, ACS5
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

    def test_state_county_contained_within_cbsa_2(self):
        """Test state and county contained within a CBSA with syntax 2."""
        df = ced.download(
            self.dataset,
            self.year,
            ["NAME", "B03002_001E"],
            state="*",
            county="*",
            download_contained_within=dict(
                # New York-Newark-Jersey City
                metropolitan_statistical_area_micropolitan_statistical_area="35620"
            ),
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

    def test_contained_within_context(self):
        """Test contained within in a with statement context."""
        with ced.contained_within(
            # New York-Newark-Jersey City
            metropolitan_statistical_area_micropolitan_statistical_area="35620"
        ) as cw:
            df = cw.download(
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


if __name__ == "__main__":
    unittest.main()
