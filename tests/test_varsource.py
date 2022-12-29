import unittest

from censusdis.impl.varsource.censusapi import CensusApiVariableSource


class CensusApiVariableSourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._variable_source = CensusApiVariableSource()
        self._dataset = "acs/acs5"
        self._year = 2020
        self._group_name = "B01001"
        self._name = f"{self._group_name}_001E"

    def test_url(self):
        url = self._variable_source.url(self._dataset, self._year, self._name)

        self.assertEqual(
            "https://api.census.gov/data/2020/acs/acs5/variables/B01001_001E.json", url
        )

    def test_group_url(self):
        url = self._variable_source.group_url(self._dataset, self._year)

        self.assertEqual(
            "https://api.census.gov/data/2020/acs/acs5/variables.json", url
        )

        url = self._variable_source.group_url(
            self._dataset, self._year, self._group_name
        )

        self.assertEqual(
            "https://api.census.gov/data/2020/acs/acs5/groups/B01001.json", url
        )


if __name__ == "__main__":
    unittest.main()
