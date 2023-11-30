import unittest
from pathlib import Path

import censusdis.dataspec as cds
from censusdis.datasets import ACS5
from censusdis.states import NJ, NY


class VariableTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.variables = ["X01001_001E", "X01001_002E", "X01001_003E"]

    def test_variable_spec(self):
        spec = cds.VariableList(self.variables)

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables, variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_one(self):
        spec = cds.VariableList(self.variables[0])

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables[:1], variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_sum_denominator(self):
        spec = cds.VariableList(self.variables, denominator=True)

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables, variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_sum_denominator_var(self):
        spec = cds.VariableList(self.variables, denominator=self.variables[-1])

        variables_to_download = spec.variables_to_download()

        self.assertEqual(self.variables, variables_to_download)
        self.assertEqual([], spec.groups_to_download())

    def test_variable_spec_sum_denominator_other(self):
        spec = cds.VariableList(self.variables, denominator="X02001_001E")

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
        spec = cds.CensusGroup(self.group[0])

        self.assertEqual([], spec.variables_to_download())
        self.assertEqual([(self.group[0], False)], spec.groups_to_download())

    def test_groups(self):
        spec = cds.CensusGroup(self.group)

        self.assertEqual([], spec.variables_to_download())
        self.assertEqual(
            [(self.group[0], False), (self.group[1], False)], spec.groups_to_download()
        )

    def test_groups_leaves_only(self):
        for leaves_only in False, True:
            spec = cds.CensusGroup(self.group, leaves_only=leaves_only)

            self.assertEqual([], spec.variables_to_download())
            self.assertEqual(
                [(self.group[0], leaves_only), (self.group[1], leaves_only)],
                spec.groups_to_download(),
            )

    def test_groups_with_denominator(self):
        denominator = "X02001_001E"

        spec = cds.CensusGroup(self.group, denominator=denominator)

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
        variable_list = cds.VariableList(self.variables1)
        group = cds.CensusGroup(self.group1)

        spec = cds.VariableSpecCollection([variable_list, group])

        self.assertEqual(len(self.variables1), len(spec.variables_to_download()))
        self.assertSetEqual(set(self.variables1), set(spec.variables_to_download()))
        self.assertEqual([(self.group1, False)], spec.groups_to_download())

    def test_collection_multiple_vars(self):
        variable_list1 = cds.VariableList(self.variables1)
        variable_list2 = cds.VariableList(self.variables2)

        spec = cds.VariableSpecCollection([variable_list1, variable_list2])

        self.assertEqual(
            len(self.variables1) + len(self.variables2),
            len(spec.variables_to_download()),
        )
        self.assertSetEqual(
            set(self.variables1 + self.variables2), set(spec.variables_to_download())
        )
        self.assertEqual([], spec.groups_to_download())

    def test_collection_multiple_vars_overlap(self):
        variable_list1 = cds.VariableList(self.variables1)
        variable_list2 = cds.VariableList(self.variables2)
        variable_list_overlap = cds.VariableList(self.variables_overlap)

        spec = cds.VariableSpecCollection(
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
        census_group1 = cds.CensusGroup(self.group1)
        census_group2 = cds.CensusGroup(
            self.group2, denominator=self.group2_denominator
        )
        census_group3 = cds.CensusGroup(self.group3, leaves_only=True)
        census_group_overlap = cds.CensusGroup([self.group1, self.group2])

        spec = cds.VariableSpecCollection(
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
        spec = cds.VariableList(["NAME", self.variable_total_pop])

        df = spec.download(dataset=self.dataset, vintage=self.vintage, state=[NJ, NY])

        self.assertEqual((2, 3), df.shape)
        self.assertSetEqual({"STATE", "NAME", self.variable_total_pop}, set(df.columns))
        self.assertEqual("New Jersey", df[df["STATE"] == NJ]["NAME"].iloc[0])
        self.assertEqual("New York", df[df["STATE"] == NY]["NAME"].iloc[0])

    def test_variables_denominator(self):
        # Try both an explicit denominator and an implicit one.
        for denominator in True, self.variable_total_pop:
            spec = cds.VariableList(
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
        spec = cds.CensusGroup(self.group, denominator=self.variable_total_pop)

        df = spec.download(dataset=self.dataset, vintage=self.vintage, state=NJ)

        self.assertEqual((1, 43), df.shape)

        print(df.shape)


class YamlTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = Path(__file__).parent / "data" / "dataspecs"

    def test_load_variables(self):
        spec = cds.VariableSpec.load_yaml(self.directory / "variable_list.yaml")

        self.assertIsInstance(spec, cds.VariableList)

        self.assertEqual(
            cds.VariableList(["B03002_002E", "B03002_012E"], denominator="B03002_001E"),
            spec,
        )

    def test_load_group(self):
        spec = cds.VariableSpec.load_yaml(self.directory / "group.yaml")

        self.assertIsInstance(spec, cds.CensusGroup)

        self.assertEqual(
            cds.CensusGroup("B03002", leaves_only=True, denominator="B03002_001E"), spec
        )

    def test_load_spec_collection(self):
        spec = cds.VariableSpec.load_yaml(self.directory / "collection.yaml")

        self.assertIsInstance(spec, cds.VariableSpecCollection)

        expected = cds.VariableSpecCollection(
            [
                cds.VariableList(["B03002_002E", "B03002_012E"], denominator="B03002_001E"),
                cds.CensusGroup("B03002", leaves_only=True, denominator="B03002_001E")
            ]
        )

        self.assertEqual(expected, spec)


if __name__ == "__main__":
    unittest.main()
