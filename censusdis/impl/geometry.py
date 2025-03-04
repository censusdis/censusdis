# Copyright (c) 2023 Darren Erik Vengroff
"""Utilities for geometric operations."""

import math
from typing import Optional, TypeVar, Union

import geopandas as gpd
from shapely import MultiPolygon, Polygon


def isoperimetric_quotient(
    geo: Union[gpd.GeoDataFrame, gpd.GeoSeries, Polygon],
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
    length = geo.exterior.length

    q = 4 * math.pi * area / (length * length)

    return q


def drop_polygon_if_sliver(
    polygon: Polygon, threshold: float = 0.01
) -> Optional[Polygon]:
    """
    Drop a polygon if it is a sliver.

    Parameters
    ----------
    polygon
        The polygon to check.
    threshold
        Threshold of sliveryness (isoperimetric quotient).

    Returns
    -------
        `polygon` if not a sliver or `None` if a sliver.
    """
    if isoperimetric_quotient(polygon) < threshold:
        return None

    return polygon


def drop_slivers_multi_polygon(
    multi_polygon: Union[Polygon, MultiPolygon], threshold: float = 0.01
) -> Optional[Union[Polygon, MultiPolygon]]:
    """
    Drop all the sliver polygons from a multi-polygon.

    Parameters
    ----------
    multi_polygon
        A `MultiPolygon`.
    threshold
        The isopermimetric threshold below which polygons are considered
        slivers.

    Returns
    -------
        A shape (either a `Polygon` or `MultiPolygon` containing all non-sliver
        polygones. If there aren't any, `None` is returned.
    """
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
    """
    Drop all slivers from the geometries in a `GeoSeries`.

    Parameters
    ----------
    gs_geo
        The original `GeoSeries`.
    threshold
        The isoperimetric quotient threshold.

    Returns
    -------
        The series with all slivers removed.
    """
    return gs_geo.map(
        lambda s: (
            drop_slivers_multi_polygon(s, threshold)
            if isinstance(s, MultiPolygon)
            else drop_polygon_if_sliver(s, threshold) if isinstance(s, Polygon) else s
        )
    )


def drop_slivers_from_gdf(
    gdf_geo: gpd.GeoDataFrame, threshold: float = 0.01
) -> gpd.GeoDataFrame:
    """
    Drop all slivers from the geometries in a `GeoDataFrame`.

    Parameters
    ----------
    gdf_geo
        The original `GeoDataFrame`.
    threshold
        The isoperimetric quotient threshold.

    Returns
    -------
        The geo data frame with all slivers removed.
    """
    new_geometry = drop_slivers_from_geo_series(gdf_geo.geometry, threshold=threshold)

    gdf_result = gpd.GeoDataFrame(gdf_geo, geometry=new_geometry)

    return gdf_result


T = TypeVar("T", Polygon, MultiPolygon, gpd.GeoSeries, gpd.GeoDataFrame)


def drop_slivers(
    geo: T,
    threshold: float = 0.01,
) -> Union[None, T]:
    """
    Drop slivers from an arbitrary geometry or collection of geometries.

    Accepts `MultiPolygon`, `Polygon`, `gpd.GeoSeries` or `gpd.GeoDataFrame`

    Parameters
    ----------
    geo
        the geography.
    threshold
        the isoperimetric threshold.

    Returns
    -------
        The geometry with slivers dropped.
    """
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
