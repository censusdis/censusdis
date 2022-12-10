import os.path
import filecmp
import unittest
import tempfile

import geopandas as gpd
import matplotlib.pyplot as plt

import censusdis.maps as cmap
from censusdis.states import ALL_STATES_AND_DC


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

    @classmethod
    def setUpClass(cls) -> None:
        cls.shapefile_path = os.path.join(
            os.path.dirname(__file__),
            'data', 'shapefiles', 'cb_2020_us_state_20m'
        )
        cls.expected_dir = os.path.join(os.path.dirname(__file__), 'expected')

    def setUp(self) -> None:
        gdf = gpd.read_file(self.shapefile_path)
        self.gdf = gdf[gdf.STATEFP.isin(ALL_STATES_AND_DC)]

        plt.rcParams["figure.figsize"] = (8, 5)

    def test_plot_us(self):
        png_file_name = "plot_us.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_dir = tempfile.gettempdir()
        output_file = os.path.join(output_dir, png_file_name)

        ax = cmap.plot_us(self.gdf, color='green')
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}"
        )

    def test_plot_us_boundary(self):
        png_file_name = "plot_us_boundary.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_dir = tempfile.gettempdir()
        output_file = os.path.join(output_dir, png_file_name)

        ax = cmap.plot_us_boundary(self.gdf, edgecolor='blue', linewidth=0.5)
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}"
        )

    def test_plot_us_no_relocate(self):
        png_file_name = "plot_us_no_relocate.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_dir = tempfile.gettempdir()
        output_file = os.path.join(output_dir, png_file_name)

        ax = cmap.plot_us(self.gdf, do_relocate_ak_hi=False, color='purple')
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}"
        )

    def test_plot_us_boundary_no_relocate(self):
        png_file_name = "plot_us_boundary_no_relocate.png"
        expected_file = os.path.join(self.expected_dir, png_file_name)

        output_dir = tempfile.gettempdir()
        output_file = os.path.join(output_dir, png_file_name)

        ax = cmap.plot_us_boundary(self.gdf, do_relocate_ak_hi=False, edgecolor='red', linewidth=0.5)
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assertTrue(
            filecmp.cmp(expected_file, output_file, shallow=False),
            f"Expected newly generated file {output_file} to match {expected_file}"
        )


if __name__ == "__main__":
    unittest.main()
