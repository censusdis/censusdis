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

    def _read_shapefile(self, base_name: str, base_url: str, crs):
        """Helper function to read a shapefile."""

        self._auto_fetch_file(base_name, base_url)

        path = self._shapefile_full_path(base_name)

        gdf = gpd.read_file(path)
        if crs is not None:
            gdf.to_crs(crs, inplace=True)
        return gdf

    def _shapefile_full_path(self, basename):
        """Helper function to construct the full path to a shapefile."""
        path = os.path.join(self._shapefile_root, basename, basename + ".shp")
        return path

    def _x_read_state_bounds_shapefile(
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
        base_name = f"cb_{self._year}_us_state_{resolution}"
        base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp"

        gdf = self._read_shapefile(base_name, base_url, crs)

        if fifty_states_only:
            if not include_dc:
                gdf = gdf[gdf.STATEFP.isin(censusdis.states.ALL_STATES)]
            else:
                gdf = gdf[gdf.STATEFP.isin(censusdis.states.ALL_STATES_AND_DC)]

        return gdf

    def _x_read_county_bounds_for_state_shapefile(self, state: str, resolution: str = "500k", crs=None):
        """
        Read a shapefile containing the bounds of all the counties in a given state.

        Parameters
        ----------
        resolution
        state
        crs

        Returns
        -------

        """
        # The census serves these files differently for different years. On or
        # before 2010, there is a single file per state per year. From 2011 on,
        # there is a single file for the country.

        if self._year <= 2010:
            basename = f"gz_{self._year}_{state}_140_00_{resolution}"
            base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}"

            return self._read_shapefile(basename, base_url, crs)
        else:
            # Just filter down to the state we want.
            gdf_us = self.read_county_bounds_shapefile(resolution, crs)
            return gdf_us[gdf_us["STATE"] == state]

    def _x_read_county_bounds_shapefile(self, resolution: str = "500k", crs=None, *, states=None):
        """
        Read a shapefile containing the bounds of all the counties in the
        United States.

        For 2010 and earlier, the US Census servers only have this data state-by-state,
        so the first time you run it may take a while to load and cache all the state-level
        data.

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

        if self._year <= 2010:
            if states is None:
                states = censusdis.states.ALL_STATES_AND_DC
            # Load them all and concatenate.
            gdf = pd.concat(
                [
                    self.read_county_bounds_for_state_shapefile(state, resolution, crs)
                    for state in states
                ]
            ).pipe(gpd.GeoDataFrame)
            return gdf
        else:
            basename = f"cb_{self._year}_us_county_{resolution}"
            base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp"

            gdf = self._read_shapefile(basename, base_url, crs)

            if states is not None:
                gdf = gdf[gdf['STATEFP'].isin(states)]

            return gdf

    def _through_2010_tiger(self, prefix, state, suffix):
        # Curiously, the server side puts the 2000 files under
        # the TIGER2010 directory early in the path and early
        # in the file name.
        path_year = self._year
        if path_year < 2010:
            path_year = 2010

        base_url = (
            f"https://www2.census.gov/geo/tiger/TIGER{path_year}/{suffix.upper()}/{self._year}"
        )
        name = f"{prefix}_{path_year}_{state}_{suffix}{str(self._year)[-2:]}"
        return base_url, name

    def _post_2010_tiger(self, prefix, state, suffix):
        base_url = (
            f"https://www2.census.gov/geo/tiger/TIGER{self._year}/{suffix.upper()}"
        )
        # Special case for whatever reason the US Census decided.
        if self._year == 2020 and suffix == 'tabblock':
            suffix = 'tabblock10'

        name = f"{prefix}_{self._year}_{state}_{suffix}"
        return base_url, name

    def _tiger(self, state, geography, crs):
        prefix, suffix = ("tl", geography)

        if self._year <= 2010:
            base_url, name = self._through_2010_tiger(prefix, state, suffix)
        else:
            base_url, name = self._post_2010_tiger(prefix, state, suffix)

        gdf = self._read_shapefile(name, base_url, crs)

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
            gdf["STATEFP"] = state

        return gdf

    # The summary level to use for each of the resolutions we
    # support.
    # See https://www2.census.gov/geo/tiger/GENZ2010/ReadMe.pdf
    _CB_SUMMARY_LEVEL_BY_GEOGRAPHY_THROUGH_2010 = {
        'state': "040",
        'county': "050",
        'cousub': '060',
        'tract': '140',
        'bg': '150'
    }

    def _through_2010_cb(self, state: str, geography: str, resolution: str):
        summary_level = self._CB_SUMMARY_LEVEL_BY_GEOGRAPHY_THROUGH_2010[geography]

        name = f"gz_{self._year}_{state}_{summary_level}_00_{resolution}"
        base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}"

        return base_url, name

    def _post_2010_cb(self, state: str, geography, resolution: str):
        name = f"cb_{self._year}_{state}_{geography}_{resolution}"
        base_url = f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp"

        return base_url, name

    def _cartographic_bound(self, state, geography, resolution, crs):
        if self._year <= 2010:
            base_url, name = self._through_2010_cb(state, geography, resolution)
        else:
            base_url, name = self._post_2010_cb(state, geography, resolution)

        gdf = self._read_shapefile(name, base_url, crs)

        # Some files on the server, like
        # https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_us_050_00_500k.zip
        # leave the 'FP' suffix of column names.
        gdf.rename(
            {
                'STATE': 'STATEFP',
                'COUNTY': 'COUNTYFP',
            },
            axis='columns',
            inplace=True
        )

        return gdf

    def read_shapefile(
        self,
        state: str,
        geography: str,
        crs=None
    ):
        return self._tiger(state, geography, crs)

    def read_cb_shapefile(
        self,
        state: str,
        geography: str,
        resolution: str = "500k",
        crs=None
    ):
        return self._cartographic_bound(state, geography, resolution, crs)

    def _x_read_cousub_shapefile(self, state, crs=None):
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

        gdf = self._tiger(crs, prefix, state, suffix)

        # There are some filler areas around coastal regions that
        # are entirely water and have no land area. Filter these out.
        gdf = gpd.GeoDataFrame(gdf[~((gdf.FUNCSTAT == "F") & (gdf.ALAND == 0))])

        return gdf

    def _x_read_tract_shapefile(self, state: str, crs=None):
        """
        Read a shapefile containing the bounds of all the census tracts in a
        given state.

        The original source of the files is
        https://www.census.gov/geographies/mapping-files/2020/geo/carto-boundary-file.html
        or similar for 2011 and later. The full url to download will look something like
        https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_34_tract10.zip
        up to 2010 and
        https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_34_tract_500k.zip for 2011 and
        later.

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

        return self._tiger(crs, prefix, state, suffix)

    def _x_read_block_group_shapefile(self, state, crs=None):
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

        return self._tiger(crs, prefix, state, suffix)

    def _x_read_block_shapefile(self, state, crs=None):
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
        prefix, suffix = ("tl", "tabblock")

        return self._tiger(crs, prefix, state, suffix)

    def _x_read_cousub_shapefiles(self, states, crs=None):
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
        name: str,
        base_url: str
    ):
        if not self._auto_fetch:
            return

        self._fetch_file(name, base_url)

    def _url_for_file(self, name: str) -> str:
        if name.startswith("cb_"):
            return f"https://www2.census.gov/geo/tiger/GENZ{self._year}/shp/{name}.zip"

        if name.startswith("tl_"):
            suffix = name.split("_")[-1]

            if self._year <= 2010:
                return (
                    f"https://www2.census.gov/geo/tiger/TIGER{self._year}/{suffix.upper()[:-2]}/{self._year}/{name}.zip"
                )
            else:
                return (
                    f"https://www2.census.gov/geo/tiger/TIGER{self._year}/{suffix.upper()}/{name}.zip"
                )

        # This will not work, but it's the main download page where we
        # can start to look for what we want.
        return "https://www.census.gov/cgi-bin/geo/shapefiles/index.php"

    def _fetch_file(
        self,
        name: str,
        base_url: str,
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
        response = requests.get(zip_url)

        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Unzip the file and extract all contents.
        with ZipFile(zip_path) as zf:
            zf.extractall(dir_path)

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
