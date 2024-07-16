# Copyright (c) 2023 Darren Erik Vengroff
"""Test map plotting functionality."""
import sys
import tempfile
import unittest
from pathlib import Path
from shutil import rmtree
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import skimage.io
from pyproj.crs import CRS
from shapely.geometry import Polygon
from skimage.metrics import structural_similarity as ssim

import censusdis.maps as cmap
from censusdis.states import (
    ABBREVIATIONS_FROM_IDS,
    AK,
    AL,
    ALL_STATES_DC_AND_PR,
    CA,
    FL,
    HI,
    ME,
    ND,
    NJ,
    PR,
    TX,
    WA,
    WY,
)


class ShapeReaderTestCase(unittest.TestCase):
    """
    Test reading shapefiles.

    The complexity we have to test is that file locations on the
    server side have changed over the years.
    """

    def setUp(self) -> None:
        """Set up before each test."""
        root = Path(tempfile.TemporaryDirectory().name)

        self.reader09 = cmap.ShapeReader(root, 2009)
        self.reader20 = cmap.ShapeReader(root, 2020)

    def test_url_for_file_09(self):
        """Test the shapefile url for 2009."""
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
        """Test the shapefile url for 2020."""
        url = self.reader20._url_for_file("cb_something")
        self.assertEqual(
            "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_something.zip", url
        )

        url = self.reader20._url_for_file("tl_something")
        self.assertEqual(
            "https://www2.census.gov/geo/tiger/TIGER2020/SOMETHING/tl_something.zip",
            url,
        )

    def test_tiger_url(self):
        """Test TIGER URLs."""
        base_url, name = self.reader09.tiger_url("tl", NJ, "tract")

        self.assertEqual(
            "https://www2.census.gov/geo/tiger/TIGER2009/34_NEW_JERSEY", base_url
        )
        self.assertEqual("tl_2009_34_tract00", name)

        base_url, name = self.reader09.tiger_url("tl", AL, "tract")

        self.assertEqual(
            "https://www2.census.gov/geo/tiger/TIGER2009/01_ALABAMA", base_url
        )
        self.assertEqual("tl_2009_01_tract00", name)


class GdfCrsBoundsTestCase(unittest.TestCase):
    """Test loading our CRS bounds resource file."""

    def test_load_resource(self):
        """Make sure we can load the resource file."""
        gdf_crs_bounds = cmap._gdf_crs_bounds()
        self.assertEqual((123, 2), gdf_crs_bounds.shape)
        self.assertEqual(["epsg", "geometry"], list(gdf_crs_bounds.columns))


class MapPlotTestCase(unittest.TestCase):
    """
    Test the plotting utilities.

    `plot_us` and `plot_us_boundary` plot geo data frames.
    These tests make sure they can reproduce expected images.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Global set up once."""
        cls.shapefile_path = (
            Path(__file__).parent / "data" / "shapefiles" / "cb_2020_us_state_20m"
        )
        cls.expected_dir = Path(__file__).parent / "expected" / sys.platform

        # Create a clean output directory
        output_dir = Path(__file__).parent / "_test_artifacts" / sys.platform
        rmtree(output_dir, ignore_errors=True)
        output_dir.mkdir(parents=True)
        cls.output_dir = output_dir

    def setUp(self) -> None:
        """Set up before each test."""
        gdf = gpd.read_file(self.shapefile_path)
        self.gdf = gdf[gdf.STATEFP.isin(ALL_STATES_DC_AND_PR)]

        plt.rcParams["figure.figsize"] = (8, 5)

    def test_closest_epsg(self):
        """Test finding the right epsg to plot each of several states."""
        # See https://wiki.spatialmanager.com/index.php/Coordinate_Systems_objects_list
        epsg_wa_s = 32149
        epsg_ca_4 = 26944
        epsg_nd_s = 32121
        epsg_tx_c = 32139
        epsg_me_e = 26983
        epsg_fl_w = 26959
        epsg_ak_9 = 26939
        epsg_hi_2 = 26962
        epsg_pr_usvi = 32161

        for state, expected_epsg in [
            (WA, epsg_wa_s),
            (CA, epsg_ca_4),
            (ND, epsg_nd_s),
            (TX, epsg_tx_c),
            (ME, epsg_me_e),
            (FL, epsg_fl_w),
            (AK, epsg_ak_9),
            (HI, epsg_hi_2),
            (PR, epsg_pr_usvi),
        ]:
            gdf_state = self.gdf[self.gdf["STATEFP"] == state]

            epsg = cmap._closest_epsg(gdf_state)

            self.assertEqual(expected_epsg, epsg)

    def assert_structurally_similar(
        self, file0, file1, threshold: float = 0.98, msg: Any = None
    ):
        """
        Assert that the images stored in two files are structurally similar.

        Parameters
        ----------
        file0
            An image file
        file1
            Another image file
        threshold
            Minimum structural similarity threshold.
        msg
            A message to log on test failure.

        Returns
        -------
            None
        """
        image0 = skimage.io.imread(file0)
        image1 = skimage.io.imread(file1)

        for ii in range(len(image0[0, 0, :])):
            similarity = ssim(image0[:, :, ii], image1[:, :, ii])

            self.assertGreater(similarity, threshold, msg=msg)

    @unittest.skipIf(
        sys.platform.startswith("win"),
        reason="GitHub Actions hosts don't have enough RAM to run this.",
    )
    def test_plot_map(self):
        """Plot some states around the country with background maps."""
        states = [WA, CA, ND, TX, ME, FL, AK, HI, PR]

        # Generate them all first. That way if they fail on a
        # new platform we have them all to visually examine before
        # copying them over to expected and checking them in.
        for state in states:
            gdf_state = self.gdf[self.gdf["STATEFP"] == state].boundary

            png_file_name = f"plot_{ABBREVIATIONS_FROM_IDS[state].lower()}.png"

            output_file = self.output_dir / png_file_name

            ax = cmap.plot_map(gdf_state, with_background=True)
            ax.axis("off")
            fig = ax.get_figure()
            fig.savefig(output_file)
            plt.close(fig)

        for state in states:
            png_file_name = f"plot_{ABBREVIATIONS_FROM_IDS[state].lower()}.png"
            expected_file = self.expected_dir / png_file_name
            output_file = self.output_dir / png_file_name

            self.assert_structurally_similar(
                expected_file,
                output_file,
                msg=f"Maps for {ABBREVIATIONS_FROM_IDS[state]} should be similar.",
            )

    def test_plot_map_with_labels(self):
        """Plot states with labels."""
        gdf_continental = self.gdf[
            self.gdf["STATEFP"].isin(ALL_STATES_DC_AND_PR)
            & ~self.gdf["STATEFP"].isin([AK, HI, PR])
        ]

        ax = cmap.plot_map(gdf_continental, geo_label="NAME", color="beige")

        ax.axis("off")

        png_file_name = "plot_us_continental_labeled.png"

        output_file = self.output_dir / png_file_name

        fig = ax.get_figure()
        fig.savefig(output_file)
        plt.close(fig)

        expected_file = self.expected_dir / png_file_name

        self.assert_structurally_similar(
            expected_file,
            output_file,
            msg="Labeled map should be similar.",
        )

    def test_plot_us(self):
        """Test calling plot_us."""
        png_file_name = "plot_us.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us(self.gdf, color="green")
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_with_labels(self):
        """Test calling plot_us."""
        png_file_name = "plot_us_labels.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us(
            self.gdf,
            geo_label=self.gdf["NAME"],
            color="green",
            geo_label_text_kwargs={"size": 6},
        )
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_boundary(self):
        """Test calling plot_us_boundary."""
        png_file_name = "plot_us_boundary.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us_boundary(self.gdf, edgecolor="blue", linewidth=0.5)
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_boundary_with_background(self):
        """Test calling plot_us_boundary."""
        png_file_name = "plot_us_boundary_with_background.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us_boundary(
            self.gdf[~self.gdf["STATEFP"].isin([AK, HI, PR])],
            do_relocate_ak_hi_pr=False,
            edgecolor="blue",
            linewidth=0.5,
            with_background=True,
        )

        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_boundary_with_background_no_relocate(self):
        """Test calling plot_us_boundary."""
        png_file_name = "plot_us_boundary_with_background_no_relocate.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us_boundary(
            self.gdf,
            do_relocate_ak_hi_pr=False,
            edgecolor="blue",
            linewidth=0.5,
            with_background=True,
            figsize=(20, 6),
            epsg=3847,
        )

        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_with_background_no_relocate(self):
        """Test calling plot_us_boundary."""
        png_file_name = "plot_us_with_background_no_relocate.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us(
            self.gdf,
            do_relocate_ak_hi_pr=False,
            color="darkgreen",
            linewidth=0.5,
            with_background=True,
            figsize=(20, 6),
            epsg=3847,
        )

        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_no_relocate(self):
        """
        Test calling plot_us without relocating AK and HI.

        It should still get the western Aleutian islands right.
        """
        png_file_name = "plot_us_no_relocate.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us(self.gdf, do_relocate_ak_hi_pr=False, color="purple")
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

    def test_plot_us_boundary_no_relocate(self):
        """
        Test calling plot_us_boundary without relocating AK and HI.

        It should still get the western Aleutian islands right.
        """
        png_file_name = "plot_us_boundary_no_relocate.png"
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us_boundary(
            self.gdf, do_relocate_ak_hi_pr=False, edgecolor="red", linewidth=0.5
        )
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)

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
        expected_file = self.expected_dir / png_file_name

        output_file = self.output_dir / png_file_name

        ax = cmap.plot_us(self.gdf, color="green")
        ax.axis("off")
        fig = ax.get_figure()
        fig.savefig(output_file)

        self.assert_structurally_similar(expected_file, output_file)


class GeographicCentroidsTestCase(unittest.TestCase):
    """Test computing geographic centroids."""

    def setUp(self) -> None:
        """Set up before each test."""
        # Geometry of Wyoming.

        geometry_wy = Polygon(
            [
                [-111.05, 41.0],
                [-104.05, 41.0],
                [-104.05, 45.0],
                [-111.05, 45.0],
                [-111.05, 41.0],
            ]
        )

        self.gdf_wy = gpd.GeoDataFrame(
            [WY],
            columns=["STATE"],
            geometry=[geometry_wy],
            crs=CRS(4269),  # This is what Census shapefiles are delivered with.
        )

    def test_geographic_centroids(self):
        """We should get a slightly different centroid under the projection to 3857."""
        centroid_geo = cmap.geographic_centroids(self.gdf_wy).iloc[0]

        centroid_4269 = self.gdf_wy.centroid.iloc[0]

        # In the x direction the projection should be symmetric about the
        # centroid, but in the y it should not. This is because the projection
        # stretches the y non-linearly.
        self.assertAlmostEqual(centroid_4269.x, centroid_geo.x, places=10)
        self.assertGreater(centroid_geo.y - centroid_4269.y, 0.03)


class MostlyContains(unittest.TestCase):
    """Test for mostly contains."""

    def setUp(self) -> None:
        """Set up before each test."""
        self.gdf_big = gpd.GeoDataFrame(
            [["BIG"]],
            columns=["NAME"],
            geometry=[
                Polygon(
                    [[0.0, 0.0], [12.00, 0.0], [12.00, 20.75], [0.0, 20.75], [0.0, 0.0]]
                )
            ],
            crs=4269,
        )

        self.gdf_small = gpd.GeoDataFrame(
            [["A"], ["B"], ["C"], ["D"], ["E"]],
            columns=["NAME"],
            geometry=[
                Polygon(
                    [
                        [10, 10],
                        [10, 11],
                        [11, 11],
                        [11, 10],
                        [10, 10],
                    ]
                ),
                Polygon(
                    [
                        [20, 10],
                        [20, 11],
                        [21, 11],
                        [21, 10],
                        [20, 10],
                    ]
                ),
                Polygon(
                    [
                        [10, 20],
                        [10, 21],
                        [11, 21],
                        [11, 20],
                        [10, 20],
                    ]
                ),
                Polygon(
                    [
                        [20, 20],
                        [20, 21],
                        [21, 21],
                        [21, 20],
                        [20, 20],
                    ]
                ),
                Polygon(
                    [
                        [15, 15],
                        [15, 16],
                        [16, 16],
                        [16, 15],
                        [15, 15],
                    ]
                ),
            ],
            crs=4269,
        )

    def test_mostly_contains(self):
        """Test the mostly contains utility."""
        # At the default 80% threshold only one is contained.
        gdf_contained = cmap.sjoin_mostly_contains(self.gdf_big, self.gdf_small)

        # At 50%, a second is contained.
        gdf_contained_05 = cmap.sjoin_mostly_contains(
            self.gdf_big, self.gdf_small, area_threshold=0.5
        )

        self.assertEqual((1, 4), gdf_contained.shape)
        self.assertEqual((2, 4), gdf_contained_05.shape)

        gdf_expected = gpd.GeoDataFrame(
            [["A", 0, "BIG"]],
            columns=["NAME_small", "index_large", "NAME_large"],
            index=[0],
            geometry=[
                Polygon(
                    [
                        [10, 10],
                        [10, 11],
                        [11, 11],
                        [11, 10],
                        [10, 10],
                    ]
                ),
            ],
            crs=4269,
        )

        gdf_expected_05 = gpd.GeoDataFrame(
            [["A", 0, "BIG"], ["C", 0, "BIG"]],
            columns=["NAME_small", "index_large", "NAME_large"],
            index=[0, 2],
            geometry=[
                Polygon(
                    [
                        [10, 10],
                        [10, 11],
                        [11, 11],
                        [11, 10],
                        [10, 10],
                    ]
                ),
                Polygon(
                    [
                        [10, 20],
                        [10, 21],
                        [11, 21],
                        [11, 20],
                        [10, 20],
                    ]
                ),
            ],
            crs=4269,
        )

        self.assertTrue(gdf_expected.equals(gdf_contained))
        self.assertTrue(gdf_expected_05.equals(gdf_contained_05))


if __name__ == "__main__":
    unittest.main()
