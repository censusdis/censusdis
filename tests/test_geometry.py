# Copyright (c) 2023 Darren Erik Vengroff
import math
import unittest

import geopandas as gpd
from shapely import MultiPolygon, Point, Polygon

from censusdis.impl.geometry import drop_slivers, isoperimetric_quotient


class IsoperimetricQuotientTestCase(unittest.TestCase):
    """Test the isoperimetric quotient computation."""

    def test_square(self):
        """Test with a square."""
        square = Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0)))

        q = isoperimetric_quotient(square)

        self.assertAlmostEqual(math.pi / 4, q, places=10)

    def test_zero_area(self):
        """Test with a zero area polygon."""
        line = Polygon(((0, 0), (0, 1), (0, 0.5), (0, 0)))

        q = isoperimetric_quotient(line)

        self.assertAlmostEqual(0.0, q, places=10)

    def test_circle(self):
        """Test with a regular polygon that is close to a circle."""
        circle = Point(0, 0).buffer(1.0, quad_segs=64)

        q = isoperimetric_quotient(circle)

        self.assertAlmostEqual(1.0, q, places=3)

    def test_series(self):
        """Test with a `gpd.GeoSeries`"""
        geometry = gpd.GeoSeries(
            [
                # Square
                Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
                # Line
                Polygon(((0, 0), (0, 1), (0, 0.5), (0, 0))),
            ]
        )

        q = isoperimetric_quotient(geometry)

        self.assertAlmostEqual(math.pi / 4, q.iloc[0], places=10)
        self.assertAlmostEqual(0.0, q.iloc[1], places=10)

    def test_geo_data_frame(self):
        """Test with a `gpd.GeoDataFrame`"""
        gdf_geometry = gpd.GeoDataFrame(
            [[1.0, 1.1], [2.0, 2.2]],
            columns=["col1", "col2"],
            geometry=[
                # Square
                Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
                # Line
                Polygon(((0, 0), (0, 1), (0, 0.5), (0, 0))),
            ],
        )

        q = isoperimetric_quotient(gdf_geometry)

        self.assertAlmostEqual(math.pi / 4, q.iloc[0], places=10)
        self.assertAlmostEqual(0.0, q.iloc[1], places=10)


class DropSliversTestCase(unittest.TestCase):
    """Test functionality to drop slivers from geometries."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.geometry = gpd.GeoSeries(
            [
                # MultiPolygon with square and line. Line drops.
                MultiPolygon(
                    (
                        # Square; stay
                        Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
                        # Line; drop
                        Polygon(((0, 0), (0, 1), (0, 0.5), (0, 0))),
                    )
                ),
                # Line; drop
                Polygon(((0, 0), (0, 1), (0, 0.5), (0, 0))),
                # Triangle; stays
                Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
                # Two triangles; both stay.
                MultiPolygon(
                    (
                        Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
                        Polygon(((10, 10), (11, 10), (11, 11), (10, 11), (10, 10))),
                    )
                ),
            ]
        )

    def test_drop_slivers_from_polygon(self):
        """Test on a polygon."""
        p1 = self.geometry.iloc[2]

        self.assertIsInstance(p1, Polygon)

        # Not dropped with the default threshold.
        p2 = drop_slivers(p1)
        self.assertEqual(p1, p2)

        # With threshold 1.0, dropped.
        p3 = drop_slivers(p1, threshold=1.0)
        self.assertIsNone(p3)

        # With threshold 0,0, not dropped.
        p4 = drop_slivers(p1, threshold=0.0)
        self.assertEqual(p1, p4)

    def test_drop_slivers_from_zero_area_polygon(self):
        p1 = self.geometry.iloc[1]

        self.assertIsInstance(p1, Polygon)

        p2 = drop_slivers(p1)
        self.assertIsNone(p2)

        # With threshold 0.0, not dropped, since area is 0.0.
        p3 = drop_slivers(p1, threshold=0.0)
        self.assertEqual(p1, p3)

        # With a high threshold, dropped.
        p4 = drop_slivers(p1, threshold=1.0)
        self.assertIsNone(p4)

    def test_drop_slivers_from_multi_polygon(self):
        mp1 = self.geometry.iloc[0]

        self.assertIsInstance(mp1, MultiPolygon)

        # Default behavior will remove the line.
        mp2 = drop_slivers(mp1)
        self.assertEqual(mp1.geoms[0], mp2)

        # With threshold 0.0, all remain.
        mp3 = drop_slivers(mp1, threshold=0.0)
        self.assertEqual(mp1, mp3)

        # With threshold 1.0, none remain.
        mp4 = drop_slivers(mp1, threshold=1.0)
        self.assertIsNone(mp4)

    def test_drop_slivers_from_geo_series(self):
        remaining = drop_slivers(self.geometry)

        self.assertEqual(len(self.geometry), len(remaining))

        self.assertEqual(
            Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
            remaining.geometry.iloc[0],
            "The square should be left as a single polygon.",
        )

        self.assertIsNone(remaining.geometry.iloc[1], "Line is dropped.")

        # The others don't change.
        self.assertTrue(
            self.geometry.geometry.iloc[2].equals(remaining.geometry.iloc[2])
        )
        self.assertTrue(
            self.geometry.geometry.iloc[3].equals(remaining.geometry.iloc[3])
        )

    def test_drop_slivers_from_gdf(self):
        gdf_geo = gpd.GeoDataFrame(
            [
                ["Square and Line"],
                ["Line"],
                ["Triangle"],
                ["Two Triangles"],
            ],
            columns=["description"],
            geometry=self.geometry,
        )

        remaining = drop_slivers(gdf_geo)

        self.assertEqual(len(gdf_geo.index), len(remaining))

        self.assertTrue(remaining["description"].equals(gdf_geo["description"]))

        self.assertEqual(
            Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))),
            remaining.geometry.iloc[0],
            "The square should be left as a single polygon.",
        )

        self.assertIsNone(remaining.geometry.iloc[1], "Line is dropped.")

        # The others don't change.
        self.assertTrue(gdf_geo.geometry.iloc[2].equals(remaining.geometry.iloc[2]))
        self.assertTrue(gdf_geo.geometry.iloc[3].equals(remaining.geometry.iloc[3]))


if __name__ == "__main__":
    unittest.main()
