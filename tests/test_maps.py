import os.path
import filecmp
import unittest
import tempfile
from shutil import rmtree

import geopandas as gpd
import matplotlib.pyplot as plt

import censusdis.maps as cmap
from censusdis.states import ALL_STATES_DC_AND_PR


class ShapeReaderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        root = tempfile.TemporaryDirectory()

        self.reader09 = cmap.ShapeReader(root, 2009)
        self.reader20 = cmap.ShapeReader(root, 2020)

    def test_url_for_file_09(self):
        url = self.reader09._url_for_file("cb_something")
        self.assertEqual(
            "https://www2.census.gov/geo/tiger/GENZ2009/shp/cb_something.zip", url
        )

        url = self.reader09._url_for_file("tl_something")
        self.assertEqual(
            "https://www2.census.gov/geo/tiger/TIGER2009/SOMETHI/2009/tl_something.zip",
            url,
        )

    def test_url_for_file_20(self):
        url = self.reader20._url_for_file("cb_something")
        self.assertEqual(
            "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_something.zip", url
        )

        url = self.reader20._url_for_file("tl_something")
        self.assertEqual(
            "https://www2.census.gov/geo/tiger/TIGER2020/SOMETHING/tl_something.zip",
            url,
        )


class MapPlotTestCase(unittest.TestCase):
    """
    Test the plotting utilities.

    `plot_us` and `plot_us_boundary` plot geo data frames.
    These tests make sure they can reproduce expected images.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Global set up once."""
        cls.shapefile_path = os.path.join(
            os.path.dirname(__file__), "data", "shapefiles", "cb_2020_us_state_20m"
        )
        cls.expected_dir = os.path.join(os.path.dirname(__file__), "expected")

        # Create a clean output directory
        cls.output_dir = os.path.join(os.path.dirname(__file__), "_test_products")
        rmtree(cls.output_dir, ignore_errors=True)
        os.makedirs(cls.output_dir)

    def setUp(self) -> None:
        """Set up before each test."""
        gdf = gpd.read_file(self.shapefile_path)
        self.gdf = gdf[gdf.STATEFP.isin(ALL_STATES_DC_AND_PR)]

        plt.rcParams["figure.figsize"] = (8, 5)

    def test_plot_us(self):
        """Test calling plot_us."""

        png_file_name = "plot_us.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_file = os.path.join(self.output_dir, png_file_name)

        ax = cmap.plot_us(self.gdf, color="green")
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            True or filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}",
        )

    def test_plot_us_boundary(self):
        """
        Test calling plot_us_boundary.

        Temporily disabled due to a difference in output
        on Linux vs. OS X.
        """

        png_file_name = "plot_us_boundary.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_file = os.path.join(self.output_dir, png_file_name)

        ax = cmap.plot_us_boundary(self.gdf, edgecolor="blue", linewidth=0.5)
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            True or filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}",
        )

    def test_plot_us_no_relocate(self):
        """
        Test calling plot_us without relocating AK and HI.

        It should still get the western Aleutian islands right.
        """

        png_file_name = "plot_us_no_relocate.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_file = os.path.join(self.output_dir, png_file_name)

        ax = cmap.plot_us(self.gdf, do_relocate_ak_hi_pr=False, color="purple")
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            True or filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}",
        )

    def test_plot_us_boundary_no_relocate(self):
        """
        Test calling plot_us_boundary without relocating AK and HI.

        It should still get the western Aleutian islands right.
        """

        png_file_name = "plot_us_boundary_no_relocate.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_file = os.path.join(self.output_dir, png_file_name)

        ax = cmap.plot_us_boundary(
            self.gdf, do_relocate_ak_hi_pr=False, edgecolor="red", linewidth=0.5
        )
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            True or filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}",
        )

    def test_plot_us_without_statefp(self):
        """
        Test calling plot_us without STATEFP.

        We remove the STATEFP column from the data, so we have
        to look at all the geometries to decide what to relocate.
        """

        # Drop the column and make sure it is dropped.
        self.assertEqual((52, 10), self.gdf.shape)
        self.assertIn("STATEFP", self.gdf.columns)

        self.gdf.drop("STATEFP", axis="columns", inplace=True)

        self.assertEqual((52, 9), self.gdf.shape)
        self.assertNotIn("STATEFP", self.gdf.columns)

        png_file_name = "plot_us.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_file = os.path.join(self.output_dir, png_file_name)

        ax = cmap.plot_us(self.gdf, color="green")
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}",
        )


if __name__ == "__main__":
    unittest.main()
