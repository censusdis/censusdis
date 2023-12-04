import unittest

from typing import Any

import sys
from pathlib import Path
from shutil import rmtree

import matplotlib.pyplot as plt

import skimage.io
from skimage.metrics import structural_similarity as ssim

from censusdis.cli.yamlspec import PlotSpec, DataSpec


class PlotSpecTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plot_spec_directory = Path(__file__).parent / "data" / "plotspecs"
        cls.data_spec_directory = Path(__file__).parent / "data" / "dataspecs"

        output_dir = Path(__file__).parent / "_test_artifacts" / sys.platform
        rmtree(output_dir, ignore_errors=True)
        output_dir.mkdir(exist_ok=True, parents=True)
        cls.output_dir = output_dir

        cls.expected_dir = Path(__file__).parent / "expected" / sys.platform

    def test_load_plotspec1(self):
        spec = PlotSpec.load_yaml(self.plot_spec_directory / "plotspec1.yaml")

        self.assertIsInstance(spec, PlotSpec)

        self.assertEqual("B25003I_002E", spec.variable)

        self.assertEqual(PlotSpec(variable="B25003I_002E"), spec)

    def test_load_plotspec2(self):
        spec = PlotSpec.load_yaml(self.plot_spec_directory / "plotspec2.yaml")

        self.assertIsInstance(spec, PlotSpec)

        self.assertEqual(
            PlotSpec(
                variable="B25003I_002E",
                boundary=False,
                with_background=False,
                projection="US",
                plot_kwargs={"figsize": [12, 8], "cmap": "Greens"},
            ),
            spec,
        )

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

    def test_plot(self):
        plot_spec = PlotSpec.load_yaml(self.plot_spec_directory / "plotspec2.yaml")
        data_spec: DataSpec = DataSpec.load_yaml(
            self.data_spec_directory / "dataspec2.yaml"
        )

        png_file_name = "plot_spec.png"
        expected_file = self.expected_dir / png_file_name
        output_file = self.output_dir / png_file_name

        gdf = data_spec.download()

        ax = plot_spec.plot(gdf)
        fig = ax.get_figure()

        fig.savefig(output_file)
        plt.close(fig)

        self.assert_structurally_similar(expected_file, output_file)


if __name__ == "__main__":
    unittest.main()
