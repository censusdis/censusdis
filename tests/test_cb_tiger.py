# Copyright (c) 2023 Darren Erik Vengroff
"""Tests for fetching geometry and getting TIGER or CB files as available."""

import unittest
from typing import Union

from shapely import MultiPolygon, Polygon

import censusdis.data as ced


def _shape_size(shape: Union[Polygon, MultiPolygon]) -> int:
    """How many points in a Polygon or MultiPolygon."""
    if isinstance(shape, Polygon):
        return len(shape.exterior.coords) + sum(
            len(hole.coords) for hole in shape.interiors
        )
    elif isinstance(shape, MultiPolygon):
        return sum(_shape_size(poly) for poly in shape.geoms)
    else:
        return 0


class TigerTestCase(unittest.TestCase):
    """Test falling back on TIGER maps, which are much bigger and higher resolution."""

    def test_single_years(self):
        """Test for a single year."""
        for year in range(2010, 2022):
            gdf = ced.download(
                "acs/acs5",
                year,
                ["NAME"],
                state="01",
                county="*",
                tract="*",
                with_geometry=True,
            )

            gdf["geometry_size"] = gdf.geometry.map(_shape_size)

            total_size = gdf["geometry_size"].sum()

            # Old tiger files from before CB files started in 2013 are much
            # bigger. But there was a CB in 2010.
            if year < 2013 and year != 2010:
                # TIGER
                self.assertGreater(total_size, 1_000_000)
                self.assertLess(total_size, 1_050_000)
            else:
                # CB 500k
                self.assertGreater(total_size, 120_000)
                self.assertLess(total_size, 160_000)


if __name__ == "__main__":
    unittest.main()
