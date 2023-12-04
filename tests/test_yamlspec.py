"""Tests for YAML specification for the CLI."""
import unittest
from pathlib import Path

import censusdis.states
from censusdis.cli.yamlspec import (
    CensusGroup,
    DataSpec,
    VariableSpec,
    VariableList,
    VariableSpecCollection,
)
from censusdis.datasets import ACS5
from censusdis.states import NJ, NY


class VariableTestCase(unittest.TestCase):
    """Test for VariableSpec."""
    def setUp(self) -> None:
        self.variables = ["X01001_001E", "X01001_002E", "X01001_003E"]

    def test_variable_spec(self):
        spec = VariableList(self.variables)

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables, variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_one(self):
        spec = VariableList(self.variables[0])

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables[:1], variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_sum_denominator(self):
        spec = VariableList(self.variables, denominator=True)

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables, variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_sum_denominator_var(self):
        spec = VariableList(self.variables, denominator=self.variables[-1])

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables, variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_sum_denominator_other(self):
        spec = VariableList(self.variables, denominator="X02001_001E")

        variables_to_download = spec.variables_to_download()

        self.assertEqual(len(self.variables) + 1, len(variables_to_download))

        for var in self.variables:
            self.assertIn(var, variables_to_download)

        self.assertIn("X02001_001E", variables_to_download)

        self.assertEqual([], spec.groups_to_download())


class GroupTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.group = ["X01001", "X01002"]

    def test_one_group(self):
        spec = CensusGroup(self.group[0])

        self.assertEqual([], spec.variables_to_download())
        self.assertEqual([(self.group[0], False)], spec.groups_to_download())

    def test_groups(self):
        spec = CensusGroup(self.group)

        self.assertEqual([], spec.variables_to_download())
        self.assertEqual(
            [(self.group[0], False), (self.group[1], False)], spec.groups_to_download()
        )

    def test_groups_leaves_only(self):
        for leaves_only in False, True:
            spec = CensusGroup(self.group, leaves_only=leaves_only)

            self.assertEqual([], spec.variables_to_download())
            self.assertEqual(
                [(self.group[0], leaves_only), (self.group[1], leaves_only)],
                spec.groups_to_download(),
            )

    def test_groups_with_denominator(self):
        denominator = "X02001_001E"

        spec = CensusGroup(self.group, denominator=denominator)

        self.assertEqual([denominator], spec.variables_to_download())
        self.assertEqual(
            [(self.group[0], False), (self.group[1], False)], spec.groups_to_download()
        )


class VariableSpecCollectionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.variables1 = ["X01001_001E", "X01001_002E", "X01001_003E"]
        self.group1 = "X01001"
        self.variables2 = ["Y01001_001E", "Y01001_002E", "Y01001_003E"]
        self.group2 = "Y01001"
        self.variables_overlap = ["X01001_001E", "Y01001_002E", "Z01001_003E"]
        self.group2_denominator = "X02001_001E"
        self.group3 = "Q01001"

    def test_collection(self):
        variable_list = VariableList(self.variables1)
        group = CensusGroup(self.group1)

        spec = VariableSpecCollection([variable_list, group])

        self.assertEqual(len(self.variables1), len(spec.variables_to_download()))
        self.assertSetEqual(set(self.variables1), set(spec.variables_to_download()))
        self.assertEqual([(self.group1, False)], spec.groups_to_download())

    def test_collection_multiple_vars(self):
        variable_list1 = VariableList(self.variables1)
        variable_list2 = VariableList(self.variables2)

        spec = VariableSpecCollection([variable_list1, variable_list2])

        self.assertEqual(
            len(self.variables1) + len(self.variables2),
            len(spec.variables_to_download()),
        )
        self.assertSetEqual(
            set(self.variables1 + self.variables2), set(spec.variables_to_download())
        )
        self.assertEqual([], spec.groups_to_download())

    def test_collection_multiple_vars_overlap(self):
        variable_list1 = VariableList(self.variables1)
        variable_list2 = VariableList(self.variables2)
        variable_list_overlap = VariableList(self.variables_overlap)

        spec = VariableSpecCollection(
            [variable_list1, variable_list_overlap, variable_list2]
        )

        self.assertEqual(
            len(self.variables1) + len(self.variables2) + 1,
            len(spec.variables_to_download()),
        )
        self.assertSetEqual(
            set(self.variables1 + self.variables2 + self.variables_overlap),
            set(spec.variables_to_download()),
        )
        self.assertEqual([], spec.groups_to_download())

    def test_collection_multiple_groups(self):
        census_group1 = CensusGroup(self.group1)
        census_group2 = CensusGroup(self.group2, denominator=self.group2_denominator)
        census_group3 = CensusGroup(self.group3, leaves_only=True)
        census_group_overlap = CensusGroup([self.group1, self.group2])

        spec = VariableSpecCollection(
            [census_group1, census_group2, census_group3, census_group_overlap]
        )

        self.assertEqual([self.group2_denominator], spec.variables_to_download())
        self.assertEqual(3, len(spec.groups_to_download()))
        self.assertSetEqual(
            set([(self.group1, False), (self.group2, False), (self.group3, True)]),
            set(spec.groups_to_download()),
        )


class DownloadTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dataset = ACS5
        self.vintage = 2020
        self.group = "B03002"
        self.variable_total_pop = "B03002_001E"
        self.variable_hispanic_latino_pop = "B03002_012E"
        self.variable_not_hispanic_latino_pop = "B03002_002E"

    def test_one_variable_spec(self):
        spec = VariableList(["NAME", self.variable_total_pop])

        df = spec.download(dataset=self.dataset, vintage=self.vintage, state=[NJ, NY])

        self.assertEqual((2, 3), df.shape)
        self.assertSetEqual({"STATE", "NAME", self.variable_total_pop}, set(df.columns))
        self.assertEqual("New Jersey", df[df["STATE"] == NJ]["NAME"].iloc[0])
        self.assertEqual("New York", df[df["STATE"] == NY]["NAME"].iloc[0])

    def test_variables_denominator(self):
        # Try both an explicit denominator and an implicit one.
        for denominator in True, self.variable_total_pop:
            spec = VariableList(
                [
                    self.variable_hispanic_latino_pop,
                    self.variable_not_hispanic_latino_pop,
                ],
                denominator=denominator,
            )

            df = spec.download(dataset=self.dataset, vintage=self.vintage, state=NJ)

            self.assertEqual(
                (1, 6 if denominator == self.variable_total_pop else 5), df.shape
            )

            self.assertAlmostEqual(
                1.0,
                df[
                    [
                        f"frac_{self.variable_hispanic_latino_pop}",
                        f"frac_{self.variable_not_hispanic_latino_pop}",
                    ]
                ]
                .sum(axis="columns")
                .iloc[0],
                places=10,
            )

    def test_group_denominator(self):
        spec = CensusGroup(self.group, denominator=self.variable_total_pop)

        df = spec.download(dataset=self.dataset, vintage=self.vintage, state=NJ)

        self.assertEqual((1, 43), df.shape)

        print(df.shape)


class YamlTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(__file__).parent / "data" / "dataspecs"

    def test_load_variables(self):
        spec = VariableSpec.load_yaml(self.directory / "variable_list.yaml")

        self.assertIsInstance(spec, VariableList)

        self.assertEqual(
            VariableList(["B03002_002E", "B03002_012E"], denominator="B03002_001E"),
            spec,
        )

    def test_load_group(self):
        spec = VariableSpec.load_yaml(self.directory / "group.yaml")

        self.assertIsInstance(spec, CensusGroup)

        self.assertEqual(
            CensusGroup("B03002", leaves_only=True, denominator="B03002_001E"), spec
        )

    def test_load_spec_collection(self):
        spec = VariableSpec.load_yaml(self.directory / "collection.yaml")

        self.assertIsInstance(spec, VariableSpecCollection)

        expected = VariableSpecCollection(
            [
                VariableList(["B03002_002E", "B03002_012E"], denominator="B03002_001E"),
                CensusGroup("B03002", leaves_only=True, denominator="B03002_001E"),
            ]
        )

        self.assertEqual(expected, spec)


class DataSpecTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(__file__).parent / "data" / "dataspecs"

    def test_load_yaml1(self):
        dataspec = DataSpec.load_yaml(self.directory / "dataspec1.yaml")

        self.assertIsInstance(dataspec, DataSpec)

        self.assertEqual(ACS5, dataspec.dataset)
        self.assertEqual(2020, dataspec.vintage)
        self.assertFalse(dataspec.with_geometry)

        self.assertIsInstance(dataspec.variable_spec, CensusGroup)

    def test_load_yaml2(self):
        dataspec = DataSpec.load_yaml(self.directory / "dataspec2.yaml")

        self.assertIsInstance(dataspec, DataSpec)

        self.assertEqual(ACS5, dataspec.dataset)
        self.assertEqual(2021, dataspec.vintage)
        self.assertTrue(dataspec.with_geometry)

        self.assertIsInstance(dataspec.variable_spec, VariableSpecCollection)

    def test_state_geo(self):
        """Test mapping state names."""
        dataspec = DataSpec.load_yaml(self.directory / "dataspec3.yaml")

        self.assertIsInstance(dataspec, DataSpec)

        # This one had a single state.
        self.assertEqual("34", dataspec.geography["state"])

    def test_state_geo_download(self):
        dataspec = DataSpec.load_yaml(self.directory / "dataspec4.yaml")

        self.assertIsInstance(dataspec, DataSpec)

        # This one had a list.
        self.assertEqual(["36", "34", "09", "06"], dataspec.geography["state"])

        # Download it and make sure we got the names of the four states we expected.
        df = dataspec.download()

        self.assertEqual((4, 3), df.shape)
        self.assertSetEqual({"STATE", "NAME", "B25003_001E"}, set(df.columns))
        for state in dataspec.geography["state"]:
            self.assertEqual(
                df[df["STATE"] == state]["NAME"].iloc[0],
                censusdis.states.NAMES_FROM_IDS[state],
            )

    def test_download_from_yaml_dataspec(self):
        dataspec = DataSpec.load_yaml(self.directory / "dataspec2.yaml")

        self.assertIsInstance(dataspec, DataSpec)

        gdf_data = dataspec.download()

        # 50 states + DC + PR = 52
        # Columns and frac_ columns add up to 39.
        self.assertEqual((52, 39), gdf_data.shape)

        frac_variables = set(
            variable for variable in gdf_data.columns if variable.startswith("frac")
        )

        self.assertEqual(18, len(frac_variables))

        # The raw version of each is in there.
        for variable in frac_variables:
            self.assertIn("_".join(variable.split("_")[-2:]), gdf_data.columns)

        # The fractions of this group should add up to 1.0.
        group = "B03002"

        group_frac_variables = [
            variable
            for variable in frac_variables
            if variable.startswith(f"frac_pop_{group}")
        ]

        sum_of_group_fracs = gdf_data[group_frac_variables].sum(axis="columns")

        sum_of_group_fracs.apply(lambda s: self.assertAlmostEqual(1.0, s, places=10))


if __name__ == "__main__":
    unittest.main()
