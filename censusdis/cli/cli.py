# Copyright (c) 2023 Darren Erik Vengroff
"""Main module for the command line interface to censusdis."""
from typing import Optional
import argparse
import logging
import sys
from logging import getLogger

import geopandas as gpd
import matplotlib.pyplot as plt

from logargparser import LoggingArgumentParser

from censusdis.cli.yamlspec import DataSpec, PlotSpec

logger = getLogger(__name__)


def main():
    """Entry point for the CLI interface to censusdis."""
    parser = LoggingArgumentParser(logger, prog="censusdis")

    subparsers = parser.add_subparsers(
        parser_class=argparse.ArgumentParser,
        required=True,
        title="command",
        description="Choose one of the following commands.",
    )
    download_parser = subparsers.add_parser(
        "download", help="Download data from the U.S. Census API."
    )

    download_parser.add_argument(
        "--api-key",
        type=str,
        help="Optional API key. Alternatively, store your key in "
        "~/.censusdis/api_key.txt. It you don't have a key, you "
        "may get throttled or blocked. Get one from "
        "https://api.census.gov/data/key_signup.html",
    )
    download_parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output file to store the data in. Format will be determined from the "
        "file extansion. .csv or .geojson (the latter if your spec has with_geometry: true.",
    )
    download_parser.add_argument("dataspec", type=str, help="A dataspec YAML file.")

    download_parser.set_defaults(func=download)

    plot_parser = subparsers.add_parser("plot", help="Plot data on a map.")

    data_group = plot_parser.add_mutually_exclusive_group(required=True)
    data_group.add_argument(
        "--dataspec",
        type=str,
        help="A data specification YAML file. "
        "If provided, data is downloaded from the U.S. Census API as in the download command.",
    )
    data_group.add_argument(
        "-i",
        "--input-data-file",
        type=str,
        help="Local file to load data from. This is normally a .geojson file "
        "that was previously downloaded with the download command.",
    )

    plot_parser.add_argument(
        "--api-key",
        type=str,
        help="Optional API key. Ignored if data is loaded from a local file "
        "with -i/--input-data-file. Alternatively, store your key in "
        "~/.censusdis/api_key.txt. It you don't have a key, you "
        "may get throttled or blocked. Get one from "
        "https://api.census.gov/data/key_signup.html",
    )

    plot_parser.add_argument(
        "plotspec", type=str, help="A plot specification YAML file."
    )
    plot_parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output file to store the plotted map in. Format will be determined from the "
        "file extansion. .png or .jpeg typically.",
    )

    plot_parser.set_defaults(func=plot)

    args = parser.parse_args()

    args.func(args)


def _read_dataspec(dataspec_file: str) -> DataSpec:
    logger.info(f"Loading data spec from {dataspec_file}.")
    dataspec = DataSpec.load_yaml(dataspec_file)
    logger.info("Loaded.")

    if not isinstance(dataspec, DataSpec):
        logging.critical(
            f"{dataspec_file} does not contain YAML for a data spec. It should start with the tag '!DataSpec'"
        )
        sys.exit(1)

    return dataspec


def _download_data(dataspec: DataSpec, needs_geometry: bool, api_key: Optional[str]):
    if needs_geometry and not dataspec.with_geometry:
        logger.critical(
            "Data specification does not have `with_geometry: true`, but geometry is needed to save "
            "in .geojson format or to plot."
        )
        sys.exit(2)

    logger.info("Downloading data from the U.S. Census API.")
    df_or_gdf = dataspec.download(api_key=api_key)
    logger.info("Download complete.")

    return df_or_gdf


def download(args):
    """Execute the download command from the CLI."""
    logger.debug("Download command selected.")

    dataspec_file = args.dataspec
    output = args.output
    needs_geometry = output.endswith(".geojson")

    dataspec = _read_dataspec(dataspec_file)

    df_or_gdf = _download_data(dataspec, needs_geometry, args.api_key)

    logger.info(f"Writing data to {output}.")

    if output.endswith(".csv"):
        if dataspec.with_geometry:
            logger.warning(
                "Data with geometry being written to a csv file. You might prefer .geojson."
            )
        df_or_gdf.to_csv(output, index=False)
    elif output.endswith(".geojson"):
        df_or_gdf.to_file(output, driver="GeoJson")
    else:
        logger.warning(
            f"Unrecognized file type {output}. This might or might not work."
        )
        df_or_gdf.to_file(output)
    logger.info("Writing complete.")


def plot(args):
    """Execute the plot command from the CLI."""
    logger.debug("Plot command selected.")

    logger.info(f"Loading plot spec from {args.plotspec}.")

    plotspecs = PlotSpec.load_yaml(args.plotspec)

    logger.info("Loaded.")

    if args.input_data_file is not None:
        # Load from a local file.
        logger.info(f"Loading data from local file {args.input_data_file}.")
        gdf = gpd.read_file(args.input_data_file)
    else:
        # Load from a dataspec.
        dataspec_file = args.dataspec
        dataspec = _read_dataspec(dataspec_file)
        gdf = _download_data(dataspec, True, args.api_key)

    if isinstance(plotspecs, PlotSpec):
        plotspecs = [plotspecs]

    ax = None

    for plotspec in plotspecs:
        ax = plotspec.plot(gdf, ax=ax)

    fig = ax.get_figure()

    output_file = args.output

    logger.info(f"Saving plot to {output_file}.")
    fig.savefig(output_file)
    plt.close(fig)


if __name__ == "__main__":
    main()
