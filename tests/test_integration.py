"""
These are integration tests because they require access to the remote census API.

Most of the functionality can be unit tested elsewhere or with mocks, but
these tests actually call the census API itself to cover the bits of code
immediately around those calls.
"""

import unittest

import geopandas

from censusdis import data as ced
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

    def setUp(self) -> None:
        self._variable_source = ced.CensusApiVariableSource()
        self._dataset = "acs/acs5"
        self._year = 2020
        self._group_name = "B19001"
        self._name = f"{self._group_name}_001E"

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
        variables = [
            f'B01001_{ii:03d}E' for ii in range(1, 50)
        ] + [
            f'B01001A_{ii:03d}E' for ii in range(1, 32)
        ] + [
            f'B01001B_{ii:03d}E' for ii in range(1, 32)
        ] + [
            f'B01001I_{ii:03d}E' for ii in range(1, 32)
        ]

        self.assertGreater(len(variables), ced._MAX_FIELDS_PER_DOWNLOAD)

        df = ced.download_detail(
            self._dataset, self._year, ["NAME"] + variables, state=STATE_NJ, county="*"
        )

        # One column per variable plus state, county, and name.
        self.assertEqual((21, 3 + len(variables)), df.shape)

        columns = set(df.columns)
        for variable in ["STATE", "COUNTY", "NAME"] + variables:
            self.assertIn(variable, columns)

    def test_download_with_geometry(self):
        """Download just a couple of variables."""

        gdf = ced.download_detail(
            self._dataset, self._year, ["NAME", self._name],
            with_geometry=True,
            state=STATE_NJ, county="*"
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((21, 5), gdf.shape)

        self.assertEqual(["STATE", "COUNTY", "NAME", "B19001_001E", 'geometry'], list(gdf.columns))
