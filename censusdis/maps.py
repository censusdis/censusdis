# Copyright (c) 2022 Darren Erik Vengroff
"""
Utilities for loading and rendering maps.

This module relies on shapefiles from the US Census,
which it downloads as needed and caches locally.
"""

import os
import shutil
from logging import getLogger
from typing import Optional, Union
from zipfile import BadZipFile, ZipFile

import geopandas as gpd
import requests
import shapely.affinity
from shapely.geometry import MultiPolygon, Point, Polygon
from shapely.geometry.base import BaseGeometry

from censusdis.impl.exceptions import CensusApiException
from censusdis.states import STATE_AK, STATE_HI, TERRITORY_PR

logger = getLogger(__name__)


class MapException(CensusApiException):
    """An exception generated from `censusdis.maps` code."""


class ShapeReader:
    """
    A class for reading shapefiles into GeoPandas GeoDataFrames.

    See the demo notebooks for more details. The shapefiles need
    to already have been downloaded to the local machine. We may
    add a lazy option in the future that will fetch them if they
    don't exist.

    Parameters
    ----------
    shapefile_root
        The location in the filesystem where shapefiles are stored.
    year
        The year we want shapefiles for,
    auto_fetch
        If `True` then fetch remote shape files as needed.
    """

    def __init__(
        self,
        shapefile_root: Optional[str] = None,
        year: int = 2020,
        auto_fetch: bool = True,
    ):
        if shapefile_root is None:
            shapefile_root = os.path.join(
                os.environ["HOME"], ".censusdis", "data", "shapefiles"
            )
            os.makedirs(shapefile_root, exist_ok=True)

        self._shapefile_root = shapefile_root
        self._year = year
        self._auto_fetch = auto_fetch

    @property
    def shapefile_root(self) -> str:
        """The path at which shapefiles are cached locally."""
        return self._shapefile_root

    def _read_shapefile(
        self, base_name: str, base_url: str, crs, timeout: int
    ) -> gpd.GeoDataFrame:
        """Helper function to read a shapefile."""

        self._auto_fetch_file(base_name, base_url, timeout=timeout)

        path = self._shapefile_full_path(base_name)

        gdf = gpd.read_file(path)
        if crs is not None:
            gdf.to_crs(crs, inplace=True)
        return gdf

    def _shapefile_full_path(self, basename):
        """Helper function to construct the full path to a shapefile."""
        path = os.path.join(self._shapefile_root, basename, basename + ".shp")
        return path

    def _through_2010_tiger(self, prefix, shapefile_scope: str, suffix):
        # Curiously, the server side puts the 2000 files under
        # the TIGER2010 directory early in the path and early
        # in the file name.
        path_year = self._year
        path_year = max(path_year, 2010)

        base_url = f"https://www2.census.gov/geo/tiger/TIGER{path_year}/{suffix.upper()}/{self._year}"
        name = f"{prefix}_{path_year}_{shapefile_scope}_{suffix}{str(self._year)[-2:]}"
        return base_url, name

    def _post_2010_tiger(self, prefix, shapefile_scope: str, suffix):
        base_url = (
            f"https://www2.census.gov/geo/tiger/TIGER{self._year}/{suffix.upper()}"
        )
        # Special case for whatever reason the US Census decided.
        if self._year == 2020 and suffix in ["puma", "tabblock"]:
            suffix = f"{suffix}10"

        name = f"{prefix}_{self._year}_{shapefile_scope}_{suffix}"
        return base_url, name

    def _tiger(self, shapefile_scope: str, geography, crs, timeout: int):
        prefix, suffix = ("tl", geography)

        if self._year <= 2010:
            base_url, name = self._through_2010_tiger(prefix, shapefile_scope, suffix)
        else:
            base_url, name = self._post_2010_tiger(prefix, shapefile_scope, suffix)

        gdf = self._read_shapefile(name, base_url, crs, timeout=timeout)

        # Pull off the extra two digits of year that get tacked
        # on for the older data.
        if self._year <= 2010:

            def mapper(col: str) -> str:
                col_suffix = str(self._year)[-2:]
                if col.endswith(col_suffix):
                    return col[:-2]
                return col

            gdf.rename(mapper, axis="columns", inplace=True)

        if "STATEFP" not in gdf.columns:
            gdf["STATEFP"] = shapefile_scope

        return gdf

    # The summary level to use for each of the resolutions we
    # support.
    # See https://www2.census.gov/geo/tiger/GENZ2010/ReadMe.pdf
    _CB_SUMMARY_LEVEL_BY_GEOGRAPHY_THROUGH_2010 = {
        "state": "040",
        "county": "050",
        "cousub": "060",
        "tract": "140",
        "bg": "150",
    }

    def _through_2010_cb(
        self, cartographic_scope: str, geography: str, resolution: str
    ):
        if geography not in self._CB_SUMMARY_LEVEL_BY_GEOGRAPHY_THROUGH_2010:
            raise MapException(
                "Don't know how to interpret geography '%s' for pre-2010 maps.",
                geography,
            )

        summary_level = self._CB_SUMMARY_LEVEL_BY_GEOGRAPHY_THROUGH_2010[geography]

        name = f"gz_{self._year}_{cartographic_scope}_{summary_level}_00_{resolution}"
        base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}"

        return base_url, name

    def _post_2010_cb(self, cartographic_scope: str, geography, resolution: str):
        # May need to revise when 2020 PUMA is published.
        if geography == "puma" and 2010 <= self._year < 2020:
            geography = "puma10"

        name = f"cb_{self._year}_{cartographic_scope}_{geography}_{resolution}"
        base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp"

        return base_url, name

    def _cartographic_bound(
        self, shapefile_scope, geography, resolution, crs, *, timeout: int
    ) -> gpd.GeoDataFrame:
        if self._year <= 2010:
            base_url, name = self._through_2010_cb(
                shapefile_scope, geography, resolution
            )
        else:
            base_url, name = self._post_2010_cb(shapefile_scope, geography, resolution)

        gdf = self._read_shapefile(name, base_url, crs, timeout=timeout)

        # Some files on the server, like
        # https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_us_050_00_500k.zip
        # leave the 'FP' suffix of column names.
        gdf.rename(
            {
                "STATE": "STATEFP",
                "COUNTY": "COUNTYFP",
            },
            axis="columns",
            inplace=True,
        )

        return gdf

    def read_shapefile(
        self, shapefile_scope: str, geography: str, crs=None, *, timeout: int = 30
    ):
        """
        Read the geometries of geographies.

        This method reads maps suitable
        for use with geometric joins and queries of various types. If you are
        only interested in plotting maps, the
        :py:meth:`~ShapeReader.read_cb_shapefile` method may be more suitable.

        The files are read from the US Census servers and cached locally.
        They are in most cases the same files you can download manually from
        https://www.census.gov/cgi-bin/geo/shapefiles/index.php.

        Individual files the API may download follow a naming convention
        that has evolved a bit over time. So for example a 2010 block group file
        for New Jersey would be found at
        https://www2.census.gov/geo/tiger/TIGER2010/BG/2010/tl_2010_34_bg10.zip
        whereas a similar file for 2020 would be at
        https://www2.census.gov/geo/tiger/TIGER2020/BG/tl_2020_34_bg.zip.

        This method knows many of the subtle changes that have occurred over the years,
        so you should mostly not have to worry about them. It is unlikely it knows
        them all, so please submit an
        issue at https://github.com/vengroff/censusdis/issues if you find
        otherwise.

        Once read, the files are cached locally so that when we reuse the same
        files we do not have to go back to the server.

        Parameters
        ----------
        shapefile_scope
            The geography that is covered by the entire shapefile. In some
            cases, this is a state, e.g. `STATE_NJ`. For cases where files
            are available for the entire country, the string `"us"` is typically
            used. In some rare cases, like for the Alaska Native Regional Corporations
            (``"anrc"``) geography, other strings like ``"02"`` are used.
            See the dowload links at
            https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
            if you need to debug issues with a given geography.
        geography
            The geography we want to download bounds for. Supported
            geometries are `"state'`, `"county"`, `"cousub"` (county subdivision),
            `"tract"`, and `"bg"` (block group). Other geometries as defined
            by the US Census may work, but have not been thoroughly tested.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.
        timeout
            Time out limit (in seconds) for the remote call.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the requested
            geometries.
        """
        return self._tiger(shapefile_scope, geography, crs, timeout=timeout)

    def read_cb_shapefile(
        self,
        shapefile_scope: str,
        geography: str,
        resolution: str = "500k",
        crs=None,
        *,
        timeout: int = 30,
    ) -> gpd.GeoDataFrame:
        """
        Read the cartographic boundaries of a given geography.

        These are smaller
        files suited for plotting maps, as compared to those returned by
        :py:meth:`~ShapeReader.read_shapefile`, which returns higher
        resolution geometries.

        The files are read from the US Census servers and cached locally.
        They are in most cases the same files you can download manually from
        https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
        or similar URLs for other years.

        Individual files the API may download follow a naming convention
        that has evolved a bit over time. So for example a 2010 census tract
        cartographic bounds file
        for New Jersey at 500,000:1 resolution would be found at
        https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_34_140_00_500k.zip
        whereas a similar file for 2020 would be at
        https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_34_tract_500k.zip

        This method knows many of the subtle changes that have occurred over the years,
        so you should mostly not have to worry about them. It is unlikely it knows
        them all, so please submit an
        issue at https://github.com/vengroff/censusdis/issues if you find
        otherwise.

        Once read, the files are cached locally so that when we reuse the same
        files we do not have to go back to the server.

        Parameters
        ----------
        shapefile_scope
            The geography that is covered by the entire shapefile. In some
            cases, this is a state, e.g. `STATE_NJ`. For cases where files
            are available for the entire country, the string `"us"` is typically
            used. In some rare cases, like for the Alaska Native Regional Corporations
            (``"anrc"``) geography, other strings like ``"02"`` are used.
            See the dowload links at
            https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
            if you need to debug issues with a given geography.
        geography
            The geography we want to download bounds for. Supported
            geometries are `"state'`, `"county"`, `"cousub"` (county subdivision),
            `"tract"`, and `"bg"` (block group)
        resolution
            What resolution shapes should we use. Permitted options are
            `"500k"`, `"5m"`, and `"20m"` for 1:500,000, 1:5,000,000, and
            1:20,000,000 resolution respectively. Availability varies, but for
            most geographies `"500k"` is available even if others are not.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.
        timeout
            Time out limit (in seconds) for the remote call.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the requested
            geometries.
        """
        return self._cartographic_bound(
            shapefile_scope, geography, resolution, crs, timeout=timeout
        )

    def _auto_fetch_file(self, name: str, base_url: str, *, timeout: int):
        if not self._auto_fetch:
            return

        self._fetch_file(name, base_url, timeout=timeout)

    def _url_for_file(self, name: str) -> str:
        if name.startswith("cb_"):
            return f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp/{name}.zip"

        if name.startswith("tl_"):
            suffix = name.split("_")[-1]

            if self._year <= 2010:
                return (
                    f"https://www2.census.gov/geo/tiger/TIGER{self._year}/"
                    f"{suffix.upper()[:-2]}/{self._year}/{name}.zip"
                )

            return (
                f"https://www2.census.gov/geo/tiger/TIGER{self._year}/"
                f"{suffix.upper()}/{name}.zip"
            )

        # This will not work, but it's the main download page where we
        # can start to look for what we want.
        return "https://www.census.gov/cgi-bin/geo/shapefiles/index.php"

    def _fetch_file(
        self,
        name: str,
        base_url: str,
        *,
        timeout: int,
    ) -> None:
        dir_path = os.path.join(self._shapefile_root, name)

        if os.path.isdir(dir_path):
            # Does it have the .shp file? If not maybe something
            # random went wrong in the previous attempt, or someone
            # deleted some stuff by mistake. So delete it and
            # reload.
            shp_path = os.path.join(dir_path, f"{name}.shp")
            if os.path.isfile(shp_path):
                # Looks like the shapefile is there.
                return

            # No shapefile so remove the whole directory and
            # hope for the best when we recreate it.
            shutil.rmtree(dir_path)

        # Make the directory
        os.mkdir(dir_path)

        # We will put the zip file in the dir we just created.
        zip_path = os.path.join(dir_path, f"{name}.zip")

        # Construct the URL to get the zip file.
        # url = self._url_for_file(name)
        zip_url = f"{base_url}/{name}.zip"

        # Fetch the zip file and write it.
        response = requests.get(zip_url, timeout=timeout)

        with open(zip_path, "wb") as file:
            file.write(response.content)

        # Unzip the file and extract all contents.
        try:
            with ZipFile(zip_path) as zip_file:
                zip_file.extractall(dir_path)
        except BadZipFile as exc:
            raise MapException(f"Bad zip file retrieved from {zip_url}") from exc
        finally:
            # We don't need the zipfile anymore.
            os.remove(zip_path)


def clip_to_states(gdf, gdf_state_bounds):
    """
    Clip every geometry in a gdf to the state it
    belongs to, from the states in the state bounds.

    We clip to state bounds so that we don't plot areas
    outside the state. Typically, this clips areas that
    extend out into the water in coastal areas so we don't
    get strange artifacts in the water in plots.

    The way we tell what state an input geometry belongs to
    is by looking at the `STATEFP` column for that geometry's
    row in the input.

    Parameters
    ----------
    gdf
        The input geometries.
    gdf_state_bounds
        The state bounds.
    Returns
    -------
        The input geometries where each is clipped to the bounds
        of the state to which it belongs.
    """
    return (
        gdf.groupby(gdf.STATEFP)
        .apply(
            lambda s: gpd.clip(s, gdf_state_bounds[gdf_state_bounds.STATEFP == s.name])
        )
        .droplevel("STATEFP")
    )


def _wrap_poly(poly: Union[Polygon, Point]):
    """
    A helper function for moving a polygon.

    Used in shifting AK and HI geometries.
    """
    if isinstance(poly, Polygon):
        x_coord, _ = poly.exterior.coords.xy
    elif isinstance(poly, Point):
        x_coord = [poly.x]
    else:
        # Not sure how to parse it, so leave it
        # where it is.
        return poly

    if x_coord[0] > 0:
        poly = shapely.affinity.translate(poly, xoff=-360.0, yoff=0.0)
    return poly


def _wrap_polys(polys):
    """
    A helper function for moving polygons.

    Used in shifting AK and HI geometries.
    """
    # Just in case it's not a MultiPolygon
    if not isinstance(polys, MultiPolygon):
        return _wrap_poly(polys)
    wrapped_polys = [_wrap_poly(p) for p in polys.geoms]
    return MultiPolygon(wrapped_polys)


# Boxes that contain AK and HI after _wrap_polys has
# been applied to it. We use this to identify
# geometries that we want to relocate in relocate_ak_hi
# when we don't have a STATEFP or STATE column to help
# identify what is in AK or HI.

_AK_MIN_X = -188.0
_AK_MIN_Y = 51.0
_AK_MAX_X = -129.0
_AK_MAX_Y = 72.0

_AK_BOUNDS = Polygon(
    (
        (_AK_MIN_X, _AK_MIN_Y),
        (_AK_MAX_X, _AK_MIN_Y),
        (_AK_MAX_X, _AK_MAX_Y),
        (_AK_MIN_X, _AK_MAX_Y),
        (_AK_MIN_X, _AK_MIN_Y),
    )
)

_HI_MIN_X = -179.0
_HI_MIN_Y = 18.0
_HI_MAX_X = -154.0
_HI_MAX_Y = 29.0

_HI_BOUNDS = Polygon(
    (
        (_HI_MIN_X, _HI_MIN_Y),
        (_HI_MAX_X, _HI_MIN_Y),
        (_HI_MAX_X, _HI_MAX_Y),
        (_HI_MIN_X, _HI_MAX_Y),
        (_HI_MIN_X, _HI_MIN_Y),
    )
)

_PR_MIN_X = -68.0
_PR_MIN_Y = 17.0
_PR_MAX_X = -65.0
_PR_MAX_Y = 19.0

_PR_BOUNDS = Polygon(
    (
        (_PR_MIN_X, _PR_MIN_Y),
        (_PR_MAX_X, _PR_MIN_Y),
        (_PR_MAX_X, _PR_MAX_Y),
        (_PR_MIN_X, _PR_MAX_Y),
        (_PR_MIN_X, _PR_MIN_Y),
    )
)


def _relocate_ak(geo: BaseGeometry) -> BaseGeometry:
    """
    Relocate a geometry that is already known to be in the AK bounding box.

    Parameters
    ----------
    geo
        The geometry.
    Returns
    -------
        The relocated geometry.
    """
    ak_scale_x = 0.25
    ak_scale_y = 0.4
    ak_x = 33
    ak_y = -34
    ak_origin = (-149.9003, 61.2181)  # Anchorage
    geo = shapely.affinity.scale(
        geo, xfact=ak_scale_x, yfact=ak_scale_y, origin=ak_origin
    )
    geo = shapely.affinity.translate(geo, xoff=ak_x, yoff=ak_y)

    return geo


def _relocate_hi(geo: BaseGeometry) -> BaseGeometry:
    """
    Relocate a geometry that is already known to be in the HI bounding box.

    Parameters
    ----------
    geo
        The geometry.
    Returns
    -------
        The relocated geometry.
    """
    hi_x = 50
    hi_y = 6

    geo = shapely.affinity.translate(geo, xoff=hi_x, yoff=hi_y)

    return geo


def _relocate_pr(geo: BaseGeometry) -> BaseGeometry:
    """
    Relocate a geometry that is already known to be in the PR bounding box.

    Parameters
    ----------
    geo
        The geometry.
    Returns
    -------
        The relocated geometry.
    """
    pr_x = -7
    pr_y = 8

    geo = shapely.affinity.translate(geo, xoff=pr_x, yoff=pr_y)

    return geo


def _relocate_parts_in_ak_hi_pr(geo: BaseGeometry) -> BaseGeometry:
    """
    Relocate any sub-geometries that happen to fall in the AK or HI or PR bounding boxes.

    If the geometry is a simple polygon, check if it intersects the
    bounding boxes of AK or HI and relocate if so. If it is a
    `MultiPolygon` then recurse in and relocate some
    contained geometries as appropriate. This way it can work on small
    polygons completely contained in the bounding box, or on larger
    multi-polygons like regions that may have some polygons in the bounding
    box and others outside it.

    Parameters
    ----------
    geo
        The geography.

    Returns
    -------
        The geography, possibly with some parts relocated.
    """
    if isinstance(geo, MultiPolygon):
        relocated_geos = [_relocate_parts_in_ak_hi_pr(g) for g in geo.geoms]
        return MultiPolygon(relocated_geos)

    # It is an individual polygon. So see if it is
    # in a box that should be relocated.

    if geo.intersects(_AK_BOUNDS):
        geo = _relocate_ak(geo)
    elif geo.intersects(_HI_BOUNDS):
        geo = _relocate_hi(geo)
    elif geo.intersects(_PR_BOUNDS):
        geo = _relocate_pr(geo)

    return geo


def _wrap_and_relocate_geos(geo: BaseGeometry):
    geo = _wrap_polys(geo)
    return _relocate_parts_in_ak_hi_pr(geo)


def _relocate_ak_hi_pr_group(group):
    """
    A helper function that relocates a group of geometries.

    They are relocated if they belong to AK, HI or PR, otherwise
    they are left alone.
    """
    if group.name == STATE_AK:
        # Deal with the Aleutian islands wrapping at -180/180 longitude.
        group.geometry = group.geometry.apply(_wrap_polys)
        # Relocate
        group.geometry = group.geometry.apply(_relocate_ak)
    elif group.name == STATE_HI:
        group.geometry = group.geometry.apply(_relocate_hi)
    elif group.name == TERRITORY_PR:
        group.geometry = group.geometry.apply(_relocate_pr)

    return group


def relocate_ak_hi_pr(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Relocate any geometry that is in Alaska or Hawaii for plotting purposes.

    We first try an optimization. If there is a `STATEFP`
    column then we relocate rows where that column has a value of
    `STATE_AK`, `STATE_HI` or `TERRITORY_PR`. If there is not a
    `STATEFP` column we check for a `STATE` column and do the same. If neither
    column exists then we dig down into the geometries themselves
    and relocate those that intersect bounding rectangles of the
    two states.

    Note: the expectation is that the crs or the incoming geo data frame
    is EPSG:4269 or something that closely approximates it, in units of
    degrees of latitude and longitude. If this is not the case, results
    are unpredictable.

    Parameters
    ----------
    gdf
        the geo data frame to relocate.
    Returns
    -------
        a geo data frame with any geometry in AK or HI moved for plotting.
    """
    if "STATEFP" in gdf.columns or "STATE" in gdf.columns:
        # There is a column idenfyig the state of each geometry
        # so use that to decide what to relocate.
        if "STATEFP" in gdf.columns:
            state_group_column = "STATEFP"
        else:
            state_group_column = "STATE"

        gdf = gdf.groupby(gdf[state_group_column], group_keys=False).apply(
            _relocate_ak_hi_pr_group
        )
    else:
        # There is no column indicating the state of each geometry. This
        # is often because the geometries span states. So we can't easily
        # relocate the two states, but we least wrap the Aleutian
        # islands if present and then relocate any geometries that are
        # in the bounding boxes of AK and HI.
        gdf = gdf.copy()
        gdf.geometry = gdf.geometry.map(_wrap_and_relocate_geos)

    return gdf


def plot_us(
    gdf: gpd.GeoDataFrame,
    *args,
    do_relocate_ak_hi_pr: bool = True,
    epsg: int = 9311,
    **kwargs,
):
    """
    Plot a map of the US with AK and HI relocated.

    This function will move and scale AK and
    HI so that they are plotted at the lower left of the other 48 states,
    just below CA, AZ, and NM.

    It also moves the Aleutian islands that are west of -180° longitude
    so that they are plotted next to the rest of AK. Otherwise, they
    tend to be plotted at longitudes just less than +180°, which
    creates visual discontinuities.

    Note: the expectation is that the crs or the incoming geo data frame
    is EPSG:4269 or something that closely approximates it, in units of
    degrees of latitude and longitude. If this is not the case, results
    are unpredictable.

    Parameters
    ----------
    gdf
        The geometries to be plotted.
    do_relocate_ak_hi_pr
        If `True` try to relocate AK, HI, and PR. Otherwise, still wrap
        the Aleutian islands west of -180° longitude if present.
    args
        Args to pass to the plot.
    epsg:
        The EPSG CRS to project to before plotting. Default is 9311, which
        is equal area. See https://epsg.io/9311.
    kwargs
        Keyword args to pass to the plot.

    Returns
    -------
        ax of the plot.
    """
    if gdf.crs != 4269:
        logger.warning(
            "Expected map to have crs epsg:4269, but got %s instead.", gdf.crs
        )

    if do_relocate_ak_hi_pr:
        gdf = relocate_ak_hi_pr(gdf)
    else:
        # At least wrap the Aleutian islands.
        gdf.geometry = gdf.geometry.map(_wrap_polys)

    gdf = gdf.to_crs(epsg=epsg)

    return gdf.plot(*args, **kwargs)


def plot_us_boundary(
    gdf: gpd.GeoDataFrame,
    *args,
    do_relocate_ak_hi_pr: bool = True,
    epsg: int = 9311,
    **kwargs,
):
    """
    Plot a map of boundaries the US with AK and HI relocated.

    This function is very much like :py:func:`~plot_us` except
    that it plots only the boundaries of geometries.

    Note: the expectation is that the crs or the incoming geo data frame
    is EPSG:4269 or something that closely approximates it, in units of
    degrees of latitude and longitude. If this is not the case, results
    are unpredictable.

    Parameters
    ----------
    gdf
        The geometries to be plotted.
    args
        Args to pass to the plot.
    do_relocate_ak_hi_pr
        If `True` try to relocate AK, HI, and PR. Otherwise, still wrap
        the Aleutian islands west of -180° longitude if present.
    epsg:
        The EPSG CRS to project to before plotting. Default is 9311, which
        is equal area. See https://epsg.io/9311.
    kwargs
        Keyword args to pass to the plot.

    Returns
    -------
        ax of the plot.
    """
    if gdf.crs != 4269:
        logger.warning(
            "Expected map to have crs epsg:4269, but got %d instead.", gdf.crs
        )

    if do_relocate_ak_hi_pr:
        gdf = relocate_ak_hi_pr(gdf)
    else:
        # At least wrap the Aleutian islands.
        gdf = gdf.copy()
        gdf.geometry = gdf.geometry.map(_wrap_polys)

    gdf = gdf.to_crs(epsg=epsg)

    return gdf.boundary.plot(*args, **kwargs)


def geographic_centroids(gdf: gpd.GeoDataFrame) -> gpd.GeoSeries:
    """
    Compute the centroid of a geography.

    We do this by projecting to epsg 3857 (https://epsg.io/3857),
    computing the centroid, and then projecting back. This gives
    a reasonable answer for most geometries and avoids warnings from
    `GeoPandas`.

    Parameters
    ----------
    gdf
        A geo data frame in any crs.
    Returns
    -------
        A geo data series of the centroids of all the geometries in
        `gdf`.
    """
    crs = gdf.crs

    projected_centroids = gdf.geometry.to_crs(epsg=3857).geometry.centroid
    centroids = projected_centroids.to_crs(crs)

    return centroids


def sjoin_mostly_contains(
    gdf_large_geos: gpd.GeoDataFrame,
    gdf_small_geos: gpd.GeoDataFrame,
    large_suffix: str = "large",
    small_suffix: str = "small",
    area_threshold: float = 0.8,
    area_epsg: int = 3857,
):
    """
    Spatial join based on fraction of contained area.

    This function is designed to implement the common case
    where we have a number of small geo areas like census
    tracts or block groups in a large area like a CBSA. The
    reason to use this instead of `gpd.GeoDataFrame.sjoin`
    directly is that the smaller geos may not all be
    strictly contained in the bounds of the larger geos.
    And small geos outside the bounds of the larger one
    may intersect along the boundary. So instead, this method
    looks for small geos whose area is at least 80%
    (or another chosen number) within the larger area,

    Parameters
    ----------
    gdf_large_geos
        A geo data frame of one or more large geo areas like CBSAs.
    gdf_small_geos
        A geo data frame of smaller areas like census tracts.
    large_suffix
        Suffix to add to column names from the large side when
        the same name appears in both.
    small_suffix
        Suffix to add to column names from the small side when
        the same name appears in both.
    area_threshold
        The fraction of each smaller area that must be covered by
        one of the large areas to be joined with it.
    area_epsg
        The CRS to use project to before doing area calculations.
        Defaults to 3857. (https://epsg.io/3857),

    Returns
    -------
        Geo data frame of the spatially joined results.
    """
    if gdf_large_geos.crs != gdf_small_geos.crs:
        raise ValueError(
            "Can only join geometries of the same crs. "
            f"Got {gdf_large_geos.crs} and {gdf_small_geos.crs}"
        )

    # Keep the original geos around in EPSG 3857 so
    # we can check intersection areas.
    gdf_large_geos["_original_large_geos_{area_epsg}"] = gdf_large_geos.geometry.to_crs(
        epsg=area_epsg
    )
    gdf_small_geos["_original_small_geos_{area_epsg}"] = gdf_small_geos.geometry.to_crs(
        epsg=area_epsg
    )

    # Do an intersection join.
    gdf_intersection = gdf_small_geos.sjoin(
        gdf_large_geos,
        how="inner",
        predicate="intersects",
        lsuffix=small_suffix,
        rsuffix=large_suffix,
    )

    # Filter down to only those where the area of the intersection
    # exceeds the threshold.
    gdf_results = gdf_intersection[
        gdf_intersection["_original_small_geos_{area_epsg}"]
        .intersection(gdf_intersection["_original_large_geos_{area_epsg}"])
        .area
        >= area_threshold * gdf_intersection["_original_small_geos_{area_epsg}"].area
    ]

    gdf_results = gdf_results.drop(
        ["_original_small_geos_{area_epsg}", "_original_large_geos_{area_epsg}"],
        axis="columns",
    ).copy()

    gdf_results = gdf_results[
        [col for col in gdf_results.columns if col != "geometry"] + ["geometry"]
    ]

    return gdf_results
