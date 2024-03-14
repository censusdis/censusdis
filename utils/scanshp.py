# Copyright (c) 2023 Darren Erik Vengroff
"""
Scan the U.S. Census servers for shapefiles.

The purpose of this script is to help the development
team identify shapefiles that exist on the U.S. Census
servers, and therefore might be useful to support in
`censusdis.us_census_shapefile._GEO_QUERY_FROM_DATA_QUERY_INNER_GEO`
but are not found there.

A useful resource for tracking down the names is
https://www2.census.gov/geo/tiger/GENZ2020/2020_file_name_def.pdf?#
"""

from typing import Iterable, Union, Optional, Tuple
import requests
import re
from logging import getLogger

from logargparser import LoggingArgumentParser

from censusdis.impl.us_census_shapefiles import (
    _geo_query_from_data_query_inner_geo_items,
)


logger = getLogger(__name__)


def scan_cb(
    year: int,
    *,
    verify: Union[bool, str] = True,
    cert: Optional[Union[str, Tuple[str, str]]] = None,
):
    """Scan CB files for a given year."""
    if year < 2014:
        dir_url = f"https://www2.census.gov/geo/tiger/GENZ{year}"
    else:
        dir_url = f"https://www2.census.gov/geo/tiger/GENZ{year}/shp"

    response = requests.get(dir_url, verify=verify, cert=cert)

    if response.status_code != 200:
        logger.warning(
            f"Skipping {year}; status code {response.status_code} from {dir_url}."
        )
        return

    text = response.text

    pattern = re.compile(
        rf'href="(cb_{year}_(us|[0-9][0-9])_([a-z0-9]+)_([a-z0-9]+)\.zip)"'
    )

    sample_us_files_by_name = {}
    sample_state_files_by_name = {}

    found_some = False

    for filename, geo, name, resolution in pattern.findall(text):
        found_some = True

        if geo == "us":
            if name not in sample_us_files_by_name:
                sample_us_files_by_name[name] = filename
                yield name, geo, resolution, filename
        else:
            if name not in sample_state_files_by_name:
                sample_state_files_by_name[name] = filename
                yield name, None, resolution, filename

    if not found_some:
        logger.warning(f"No matching links found for {year} in {dir_url}.")


def scan_cb_years(years: Iterable[int]):
    """Scan CB files for a range of years."""
    for year in years:
        for name, geo, resolution, filename in scan_cb(year):
            yield year, name, geo, resolution, filename


def main():
    """Parse args and run the main program."""
    parser = LoggingArgumentParser(logger)

    parser.add_argument(
        "--exists-ok",
        action="store_true",
        help="If set, then nothing will be printed for names that we know but in a different geo.",
    )

    args = parser.parse_args()

    years = range(2010, 2023)

    geo_maps_by_year = {
        year: [row for row in _geo_query_from_data_query_inner_geo_items(year)]
        for year in years
    }

    for year, name, geo, resolution, filename in scan_cb_years(years):
        if resolution == "500k":
            geo_map = geo_maps_by_year[year]
            found = False
            semi_found = False  # Matches on name but not geo.
            for _, row in geo_map:
                found = row[0] == geo and row[1] == name
                if not semi_found:
                    semi_found = row[0] != geo and row[1] == name
                    if semi_found:
                        semi_found_at_geo = row[0]
                if found:
                    break
            if not found:
                if semi_found:
                    if not args.exists_ok:
                        print(
                            f"{name} exists at {semi_found_at_geo} (not {geo}) for {year}."
                        )
                else:
                    print(f"{name} in {geo} unnamed for {year}.")


if __name__ == "__main__":
    main()
