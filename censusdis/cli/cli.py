import argparse
import logging
import sys
from logging import getLogger
from logargparser import LoggingArgumentParser

from censusdis.dataspec import DataSpec

logger = getLogger(__name__)


def main():
    parser = LoggingArgumentParser(logger)

    subparsers = parser.add_subparsers(parser_class=argparse.ArgumentParser)
    download_parser = subparsers.add_parser("download", help="Download data from the U.S. Census API.")

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

    args = parser.parse_args()

    logger.info(f"Loading data spec from {args.dataspec}.")

    dataspec = DataSpec.load_yaml(args.dataspec)

    logger.info("Loaded.")

    if not isinstance(dataspec, DataSpec):
        logging.critical(
            f"{args.dataspec} does not contain YAML for a data spec. It should start with the tag '!DataSpec'"
        )
        sys.exit(1)

    output = args.output

    if output.endswith('.geojson') and not dataspec.with_geometry:
        logger.critical(
            f"Specification {args.dataspec} does no have `with_geometry: true`, so .geojson output to {output} is not possible."
        )
        sys.exit(2)

    logger.info("Downloading data for the U.S. Census API.")

    df_or_gdf = dataspec.download(api_key=args.api_key)

    logger.info("Download complete.")

    logger.info(f"Writing data to {output}.")

    if output.endswith('.csv'):
        if dataspec.with_geometry:
            logger.warning("Data with geometry being written to a csv file. You might prefer .geojson.")
        df_or_gdf.to_csv(output, index=False)
    elif output.endswith('.geojson'):
        df_or_gdf.to_file(output, driver="GeoJson")
    else:
        logger.warning(f"Unrecognized file type {output}. This might or might not work.")
        df_or_gdf.to_file(output)

    logger.info("Writing complete.")


if __name__ == "__main__":
    main()
