# Copyright (c) 2022 Darren Erik Vengroff

import pandas as pd

import geopandas as gpd
import os
import requests
import shutil
from zipfile import ZipFile

from shapely import affinity
from shapely.geometry import MultiPolygon, Polygon

import censusdis.states

from censusdis.states import STATE_AK, STATE_HI


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
            shapefile_root: str,
            year: int = 2020,
            auto_fetch: bool = True,
    ):

        self._shapefile_root = shapefile_root
        self._year = year
        self._auto_fetch = auto_fetch

    def _read_shapefile(self, basename, crs):
        """Helper function to read a shapefile."""

        self._auto_fetch_file(basename)

        path = self._shapefile_full_path(basename)

        gdf = gpd.read_file(path)
        if crs is not None:
            gdf.to_crs(crs, inplace=True)
        return gdf

    def _shapefile_full_path(self, basename):
        """Helper function to construct the full path to a shapefile."""
        path = os.path.join(self._shapefile_root, basename, basename + ".shp")
        return path

    def read_shapefile(self, basename, crs=None):
        """
        Read a shapefile from the filesystem.

        This is a fallback for reading file types that do not have
        specific helper methods like
        :py:meth:`~ShapeReader.read_state_bounds_shapefile`,
        :py:meth:`~ShapeReader.read_tract_shapefile`,
        :py:meth:`~ShapeReader.read_block_group_shapefile`,
        :py:meth:`~ShapeReader.read_block_shapefile`,
        and so on. Normally it is preferred to use one of those
        methods.

        Parameters
        ----------
        basename
            The base name of the file. This is determined by the
            Census Bureau, who manages the files.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.
        Returns
        -------
            A `gpd.GeoDataFrame` containing the contents of the shapefile.
        """
        return self._read_shapefile(basename, crs)

    def _read_state_shapefile(self, state, prefix, suffix, crs):
        """Helper function to read a single state shapefile."""
        basename = "_".join([prefix, str(self._year), state, suffix])

        return self._read_shapefile(basename, crs)

    def read_state_bounds_shapefile(
        self,
        fifty_states_only: bool = True,
        include_dc: bool = True,
        resolution: str = "500k",
        crs=None,
    ):
        """
        Read the bounds of all the states. This is useful for plotting
        the entire country and also for clipping other polygons to state
        boundaries using, for example, the
        :py:meth:`~ShapeReader.clip_to_state` method.

        The original source for these files is
        https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
        and similar for other years.

        Parameters
        ----------
        fifty_states_only
            If `True`, drop the portion of the map that covers territories
            outside the fifty states. This is useful since the default
            Census maps include these and we aren't always interested in
            plotting them on maps.
        include_dc
            If `True` include the geometry for the District of Columbia
            as well as the states.
        resolution:
            What resolution shapes should we use. Permitted options are
            '500k', '5m', and '20m' for 1:500,000, 1:5,000,000, and
            1:20,000,000 resolution respectively.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the outlines of the states.
        """
        basename = f"cb_{self._year}_us_state_{resolution}"
        gdf = self._read_shapefile(basename, crs)

        if fifty_states_only:
            if not include_dc:
                gdf = gdf[gdf.STATEFP.isin(censusdis.states.ALL_STATES)]
            else:
                gdf = gdf[gdf.STATEFP.isin(censusdis.states.ALL_STATES_AND_DC)]

        return gdf

    def read_county_bounds_shapefile(self, resolution: str = "500k", crs=None):
        """
        Read a shapefile containing the bounds of all the counties in the
        United States.

        The resolution is 1:500,000.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
        or similar for other years.

        Parameters
        ----------
        resolution:
            What resolution shapes should we use. Permitted options are
            '500k', '5m', and '20m' for 1:500,000, 1:5,000,000, and
            1:20,000,000 resolution respectively.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the counties.
        """
        basename = f"cb_{self._year}_us_county_{resolution}"
        return self._read_shapefile(basename, crs)

    def read_cousub_500k_shapefile(self, state, crs=None):
        """
        Read a shapefile containing the bounds of all the county subdivistions in a
        given state.

        The resolution is 1:500,000.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html
        or similar for other years.

        Parameters
        ----------
        state
            The state, e.g. `STATE_NJ`.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the county subdivisions
            in the state.
        """

        prefix, suffix = ("cb", "cousub_500k")

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf["STATEFP"] = state
        return gdf

    def read_block_group_shapefile(self, state, crs=None):
        """
        Read a shapefile containing the bounds of all the block groups in a
        given state.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/2020/geo/carto-boundary-file.html
        or similar for other years.

        Parameters
        ----------
        state
            The state, e.g. `STATE_NJ`.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the block groups
            in the state.
        """
        prefix, suffix = ("tl", "bg")

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf["STATEFP"] = state
        return gdf

    def read_tract_shapefile(self, state, crs=None):
        """
        Read a shapefile containing the bounds of all the census tracts in a
        given state.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/2020/geo/carto-boundary-file.html
        or similar for other years.

        Parameters
        ----------
        state
            The state, e.g. `STATE_NJ`.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the census tracts
            in the state.
        """
        prefix, suffix = ("tl", "tract")

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf["STATEFP"] = state
        return gdf

    def read_block_shapefile(self, state, crs=None):
        """
        Read a shapefile containing the bounds of all the blocks in a
        given state.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/2020/geo/carto-boundary-file.html
        or similar for other years.

        Parameters
        ----------
        state
            The state, e.g. `STATE_NJ`.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the blocks
            in the state.
        """
        yy = self._year % 100
        yy = 10 * (yy // 10)

        prefix, suffix = ("tl", "tabblock{:02d}".format(yy))

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        return gdf

    def read_cousub_shapefile(self, state, crs=None):
        """
        Read a shapefile containing the bounds of all the county subdivisions in a
        given state.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/2020/geo/carto-boundary-file.html
        or similar for other years.

        Parameters
        ----------
        state
            The state, e.g. `STATE_NJ`.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the county subdivisions
            in the state.
        """
        prefix, suffix = ("tl", "cousub")

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf["STATEFP"] = state

        # There are some filler areas around coastal regions that
        # are entirely water and have no land area. Filter these out.
        gdf = gpd.GeoDataFrame(gdf[~((gdf.FUNCSTAT == "F") & (gdf.ALAND == 0))])

        # gdf.rename({'GEOID': 'COUSUB_GEOID'}, axis=1, inplace=True)

        return gdf

    def read_cousub_shapefiles(self, states, crs=None):
        """
        This is like :py:meth:`~ShapeReader.read_cousub_shapefile` but
        it reads from several states and puts the results all into one
        large `GeoDataFrame`.

        Parameters
        ----------
        states
            The states, e.g. `[STATE_NY, STATE_NJ, STATE_CT]`.
        crs
            The crs to make the file to. If `None`, use the default
            crs of the shapefile. Setting this is useful if we plan
            to merge the resulting `GeoDataFrame` with another so we
            can make sure they use the same crs.

        Returns
        -------
            A `gpd.GeoDataFrame` containing the boundaries of the county subdivisions
            in all the specified states.
        """
        gdf = pd.concat(
            [self.read_cousub_shapefile(state, crs) for state in states]
        ).pipe(gpd.GeoDataFrame)

        return gdf

    def _auto_fetch_file(
        self,
        name: str
    ):
        if not self._auto_fetch:
            return

        self._fetch_file(name)

    def _fetch_file(
        self,
        name: str,
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
        url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp/{name}.zip"

        # Fetch the zip file and write it.
        response = requests.get(url)

        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # Unzip the file and extract all contents.
        with ZipFile(zip_path) as zf:
            zf.extractall(dir_path)

        # We don't need the zipfile any more.
        # os.remove(zip_path)


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


def _wrap_poly(poly):
    """
    A helper function for moving a polygon.

    Used in shifting AK and HI geometries.
    """
    x, _ = poly.exterior.coords.xy
    if x[0] > 0:
        poly = affinity.translate(poly, xoff=-360.0, yoff=0.0)
    return poly


def _wrap_polys(polys):
    """
    A helper function for moving polygons.

    Used in shifting AK and HI geometries.
    """
    # Just in case it's not a MultiPolygon
    if type(polys) == Polygon:
        return _wrap_poly(polys)
    wrapped_polys = [_wrap_poly(p) for p in polys.geoms]
    return MultiPolygon(wrapped_polys)


def _relocate_ak_hi_group(group):
    """
    A helper function that relocates a group of geometries.

    They are relocated if they belong to AK or HI, otherwise
    they are left alone.
    """
    if group.name == STATE_AK:
        # Deal with the Aleutian islands wrapping at -180/180 longitude.
        group.geometry = group.geometry.apply(_wrap_polys)
        ak_scale_x = 0.25
        ak_scale_y = 0.4
        ak_x = 33
        ak_y = -34
        ak_origin = (-149.9003, 61.2181)  # Anchorage
        group.geometry = group.geometry.scale(
            xfact=ak_scale_x, yfact=ak_scale_y, origin=ak_origin
        )
        group.geometry = group.geometry.translate(xoff=ak_x, yoff=ak_y)
    elif group.name == STATE_HI:
        hi_x = 50
        hi_y = 6
        group.geometry = group.geometry.translate(xoff=hi_x, yoff=hi_y)

    return group


def relocate_ak_hi(gdf):
    """
    Relocate any geometry that is in Alaska or Hawaii for plotting
    purposes.
    Parameters
    ----------
    gdf
        the geo data frame to relocate.
    Returns
    -------
        a geo data frame with any geometry in AK or HI moved for plotting.
    """
    gdf = gdf.groupby(gdf["STATEFP"]).apply(_relocate_ak_hi_group)

    return gdf


def plot_us(gdf: gpd.GeoDataFrame, *args, **kwargs):
    """
    Plot a map of the US by relocating any geometries in the
    GeoDataFrame where the STATEFP column is for AK or HI.

    Parameters
    ----------
    gdf
        The geometries to be plotted.
    args
        Args to pass to the plot
    kwargs
        Kwarge to pass to the plot.
    Returns
    -------
        ax of the plot.
    """
    gdf_relocated = relocate_ak_hi(gdf)
    ax = gdf_relocated.plot(*args, **kwargs)
    return ax


def plot_us_boundary(gdf: gpd.GeoDataFrame, *args, **kwargs):
    """
    Plot a map of the US by relocating any geometries in the
    GeoDataFrame where the STATEFP column is for AK or HI.
    Plot only the boundary of the geometry passed in.

    Parameters
    ----------
    gdf
        The geometries to be plotted.
    args
        Args to pass to the plot
    kwargs
        Kwarge to pass to the plot.
    Returns
    -------
        ax of the plot.
    """
    gdf_relocated = relocate_ak_hi(gdf)
    ax = gdf_relocated.boundary.plot(*args, **kwargs)
    return ax
