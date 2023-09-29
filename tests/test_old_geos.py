import unittest
import censusdis.data as ced


class OlderGeometryTestCase(unittest.TestCase):
    """
    Tests for issues with older dates and geometry.

    As described in https://github.com/vengroff/censusdis/issues/158.
    """

    def test_geo_tract_across_years(self):
        """
        Test that we can load tract-level data with geometry.

        The key thing we are testing is that we can do this
        across a wide range of years, even though the Census
        data changed between 2013 and 2014. They changed both
        the directory structure and the name of some columns, e.g.
        'TRACT' vs. 'TRACTCE'.
        """

        # TODO include all the years back to 2009? or so.
        for year in [2010] + list(range(2014, 2022)):
            print()
            print(f"Year: {year}")
            gdf_tract = ced.download(
                "acs/acs5",
                year,
                ["NAME"],
                state="01",
                county="*",
                tract="*",
                with_geometry=True,
            )

            self.assertEqual(
                ["STATE", "COUNTY", "TRACT", "NAME", "geometry"],
                list(gdf_tract.columns),
            )


if __name__ == "__main__":
    unittest.main()
