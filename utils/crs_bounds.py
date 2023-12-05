# Copyright (c) 2023 Darren Erik Vengroff
"""
An internal utility to generate the bounds of regional CRS's.

This is not a user-facing file and is not included in the
distribution of censusdis. It is, instead, the code that is
used to generate censusdis/resources/crs_bounds.geojson, which
is then checked in.

It's not worth making running this code and generating a new
crs_bounds.geojson file part of the build process because we
expect the output to rarely, if ever at all, change.

If you do need to run it,

```
python utils/crs_bounds.py -o /tmp/crs_bounds.geojson -p /tmp/crs_bounds.png
```

is a good way to invoke it. Examine the plot it generates to see that
it looks right (covers the US with rectangles), and then copy
`crs_bounds.geojson` to censusdis/resources and check it in.
"""

import itertools
from argparse import ArgumentParser, BooleanOptionalAction
from typing import Generator, Iterable, Tuple

import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from shapely import Polygon


def epsg_bounds_rect(
    epsgs: Iterable[int],
    verbose: bool = False,
) -> Generator[Tuple[int, Polygon], None, None]:
    """
    Generae the bounds rectangles for EPSGs.

    Parameters
    ----------
    epsgs
        The EPSGs
    verbose
        Print verbose messages

    Returns
    -------
        A generator of bounds.
    """
    for epsg in epsgs:
        try:
            crs = pyproj.CRS(epsg)
            area_of_use = crs.area_of_use

            east = (
                area_of_use.east if area_of_use.east < 0 else area_of_use.east - 360.0
            )
            west = (
                area_of_use.west if area_of_use.west < 0 else area_of_use.west - 360.0
            )

            yield epsg, Polygon(
                [
                    (east, area_of_use.north),
                    (east, area_of_use.south),
                    (west, area_of_use.south),
                    (west, area_of_use.north),
                    (east, area_of_use.north),
                ]
            )
        except pyproj.exceptions.CRSError:
            if verbose:
                print(f"Skipping epsg {epsg}")


def main():
    """Generate CRS bounds."""
    parser = ArgumentParser()

    parser.add_argument("-v", "--verbose", action=BooleanOptionalAction)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-p", "--plot", help="Output file to save a plot.")

    args = parser.parse_args()

    # These are the EPSG's that cover zones across the United State.
    # See https://wiki.spatialmanager.com/index.php/Coordinate_Systems_objects_list
    # for details.

    state_zone_epsgs = itertools.chain(
        range(26929, 26999),
        range(32100, 32162),
    )

    gdf_zones = gpd.GeoDataFrame(
        [
            {"epsg": epsg, "geometry": geometry}
            for epsg, geometry in epsg_bounds_rect(
                state_zone_epsgs, verbose=args.verbose
            )
        ],
        crs=pyproj.CRS(4326),
    )

    gdf_zones.to_file(args.output)

    if args.plot is not None:
        gdf_zones.boundary.plot(figsize=(12, 6))

        plt.savefig(args.plot)


if __name__ == "__main__":
    main()
