# Copyright (c) 2023 Darren Erik Vengroff
"""
Utilities for geometric operations.
"""

import math
from typing import Optional, TypeVar, Union
import geopandas as gpd
from shapely import Polygon, MultiPolygon


def isoperimetric_quotient(
    geo: Union[gpd.GeoDataFrame, gpd.GeoSeries, Polygon]
) -> float:
    """
    Compute the isoperimetric quotient of a shape or collection of shapes.

    The isoperimetric quotient is a measure of the compactness of a polygom.
    It is defines as the ratio of the area of the shape to the area of a
    circle with the same perimeter. It ranges from zero, when the polygon
    has zero area, to 1.0 when the polygon approximates a circle. It is not
    possible for a shape that is not a circle to have more area than a circle
    with the same permimeter.

    For more info, see https://en.wikipedia.org/wiki/Compactness_measure_of_a_shape
    and https://en.wikipedia.org/wiki/Isoperimetric_inequality.

    This is also equivalent to the Polsby–Popper test. See
    https://en.wikipedia.org/wiki/Polsby%E2%80%93Popper_test.

    Parameters
    ----------
    geo:
        The geography or a series or dataframe of them.

    Returns
    -------
        The isoperimetric_quotient (Polsby–Popper test) value or values
        between 0 and 1.
    """
    area = geo.area
    length = geo.length

    q = 4 * math.pi * area / (length * length)

    return q


def drop_polygon_if_sliver(
    polygon: Polygon, threshold: float = 0.01
) -> Optional[Polygon]:
    if isoperimetric_quotient(polygon) < threshold:
        return None

    return polygon


def drop_slivers_multi_polygon(
    multi_polygon: Union[Polygon, MultiPolygon], threshold: float = 0.01
) -> Optional[MultiPolygon]:
    remaining_polygons = [
        poly
        for poly in multi_polygon.geoms
        if isoperimetric_quotient(poly) >= threshold
    ]

    if len(remaining_polygons) == 0:
        return None
    elif len(remaining_polygons) == 1:
        return remaining_polygons[0]
    else:
        return MultiPolygon(remaining_polygons)


def drop_slivers_from_geo_series(
    gs_geo: gpd.GeoSeries, threshold: float = 0.01
) -> gpd.GeoSeries:
    return gs_geo.map(
        lambda s: drop_slivers_multi_polygon(s, threshold)
        if isinstance(s, MultiPolygon)
        else drop_polygon_if_sliver(s, threshold)
        if isinstance(s, Polygon)
        else s
    )


def drop_slivers_from_gdf(
    gdf_geo: gpd.GeoDataFrame, threshold: float = 0.01
) -> gpd.GeoDataFrame:
    new_geometry = drop_slivers_from_geo_series(gdf_geo.geometry, threshold=threshold)

    gdf_result = gpd.GeoDataFrame(gdf_geo, geometry=new_geometry)

    return gdf_result


T = TypeVar("T", Polygon, MultiPolygon, gpd.GeoSeries, gpd.GeoDataFrame)


def drop_slivers(
    geo: T,
    threshold: float = 0.01,
) -> Union[None, T]:
    if isinstance(geo, MultiPolygon):
        return drop_slivers_multi_polygon(geo, threshold=threshold)
    elif isinstance(geo, Polygon):
        return drop_slivers_multi_polygon(MultiPolygon((geo,)), threshold=threshold)
    if isinstance(geo, gpd.GeoSeries):
        return drop_slivers_from_geo_series(geo, threshold=threshold)
    if isinstance(geo, gpd.GeoDataFrame):
        return drop_slivers_from_gdf(geo, threshold=threshold)

    raise ValueError(
        f"Unable to drop slivers from a {type(geo)}. "
        "Must be a GeoDataFrame, GeoSeries, and MultiPolygones only."
    )
