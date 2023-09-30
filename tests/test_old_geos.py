import unittest
import itertools
import censusdis.data as ced
from censusdis.maps import MapException


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
        # These are the years for which the shape files exist.
        for year in itertools.chain(range(2010, 2011), range(2013, 2022)):
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

    def test_geo_tract_missing_year(self):
        """
        The years 2011 and 2012 are not currently supported.

        This is due
        to differences in the format of the shapefile directories.
        In the case of 2011 they are missing entirely. More exploration
        is needed to determine if 2012 shapefiles can be reliably
        located.
        """
        for missing_year in range(2011, 2013):
            with self.assertRaises(MapException):
                gdf_tract = ced.download(
                    "acs/acs5",
                    missing_year,
                    ["NAME"],
                    state="01",
                    county="*",
                    tract="*",
                    with_geometry=True,
                )


if __name__ == "__main__":
    unittest.main()
