
import pandas as pd

import geopandas as gpd
import os

from shapely import affinity
from shapely.geometry import MultiPolygon, Polygon

from .states import STATE_AK, STATE_HI


class ShapeReader:

    def __init__(self, shapefile_root, year=2020):
        self._shapefile_root = shapefile_root
        self._year = year

    @staticmethod
    def _read_shapefile(path, crs):
        gdf = gpd.read_file(path)
        if crs is not None:
            gdf.to_crs(crs, inplace=True)
        return gdf

    def _shapefile_name(self, basename):
        path = os.path.join(self._shapefile_root, basename, basename + '.shp')
        return path

    def read_shapefile(self, basename, crs=None):
        path = self._shapefile_name(basename)
        return self._read_shapefile(path, crs)

    def _read_state_shapefile(self, state, prefix, suffix, crs):
        basename = '_'.join([prefix, str(self._year), state, suffix])

        path = self._shapefile_name(basename)
        return self._read_shapefile(path, crs)

    def read_state_bounds_shapefile(self, fifty_states_only=True, include_dc=True, twenty_m=False, crs=None):
        suffix = '_us_state_20m' if twenty_m else '_us_state_500k'

        path = self._shapefile_name('cb_' + str(self._year) + suffix)
        gdf = self._read_shapefile(path, crs)

        if fifty_states_only:
            if not include_dc:
                gdf = gdf[gdf.STATEFP.isin(somaccr2021.states.ALL_STATES)]
            else:
                gdf = gdf[gdf.STATEFP.isin(somaccr2021.states.ALL_STATES) | (gdf.STATEFP == somaccr2021.states.STATE_DC)]

        return gdf

    def read_county_bounds_shapefile(self, crs=None):
        path = self._shapefile_name('cb_' + str(self._year) + '_us_county_500k')
        return self._read_shapefile(path, crs)

    def read_cousub_500k_shapefile(self, state, crs=None):
        # Original downloads from
        # https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2019.html
        prefix, suffix = ('cb', 'cousub_500k')

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf['STATEFP'] = state
        return gdf

    def read_school_district_shapefile(self, state, district_type: str="unified", crs=None):
        prefix = 'cb'

        suffixes = {
            'unified': 'unsd_500k',
            'elementary': 'elsd_500k',
            'secondary': 'scsd_500k',
        }

        suffix = suffixes.get(district_type, None)

        if suffix is None:
            raise ValueError(f"Unknown district type '{district_type}'. " +
                             "Valid values are 'elementary', 'secondary' and 'unified'.")

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf['STATEFP'] = state
        return gdf

    def read_bg_shapefile(self, state, crs=None):
        # Original downloads from
        # https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2019&layergroup=Block+Groups
        prefix, suffix = ('tl', 'bg')

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf['STATEFP'] = state
        return gdf

    def read_tract_shapefile(self, state, crs=None):
        # Original downloads from
        # https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2020&layergroup=Census+Tracts
        prefix, suffix = ('tl', 'tract')

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf['STATEFP'] = state
        return gdf

    def read_block_shapefile(self, state, crs=None):
        # Original downloads from
        # https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2019&layergroup=Blocks+%282010%29

        yy = self._year % 100
        yy = 10 * (yy // 10)

        prefix, suffix = ('tl', 'tabblock{:02d}'.format(yy))

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        return gdf

    def read_cousub_shapefile(self, state, crs=None):
        # Original downloads from
        # https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2019&layergroup=Block+Groups
        prefix, suffix = ('tl', 'cousub')

        gdf = self._read_state_shapefile(state, prefix, suffix, crs)
        gdf['STATEFP'] = state

        # There are some filler areas around coastal regions that
        # are entirely water and have no land area. Filter these out.
        gdf = gpd.GeoDataFrame(gdf[~((gdf.FUNCSTAT == 'F') & (gdf.ALAND == 0))])

        #gdf.rename({'GEOID': 'COUSUB_GEOID'}, axis=1, inplace=True)

        return gdf

    def read_cousub_shapefiles(self, states, crs=None):
        gdf = pd.concat(
            [self.read_cousub_shapefile(state, crs) for state in states]
        ).pipe(gpd.GeoDataFrame)

        return gdf


def clip_to_states(gdf, gdf_state_bounds):
    """
    Clip every geometry in a gdf to the state it
    belongs to, from the states in the state bounds.

    We clip to state bounds so that we don't plot areas
    outside the state. Typically, this clips areas that
    extend out into the water in coastal areas so we don't
    get strange artifacts in the water in plots.
    """
    return gdf.groupby(gdf.STATEFP).apply(
        lambda s: gpd.clip(s, gdf_state_bounds[gdf_state_bounds.STATEFP == s.name])
    )


def _wrap_poly(poly):
    x, _ = poly.exterior.coords.xy
    if x[0] > 0:
        poly = affinity.translate(poly, xoff=-360.0, yoff=0.0)
    return poly


def _wrap_polys(polys):
    # Just in case it's not a MultiPolygon
    if type(polys) == Polygon:
        return _wrap_poly(polys)
    wrapped_polys = [_wrap_poly(p) for p in polys.geoms]
    return MultiPolygon(wrapped_polys)


def _relocate_ak_hi_group(group):
    if group.name == STATE_AK:
        # Deal with the Aleutian islands wrapping at -180/180 longitude.
        group.geometry = group.geometry.apply(_wrap_polys)
        ak_scale_x = 0.25
        ak_scale_y = 0.4
        ak_x = 33
        ak_y = -34
        ak_origin = (-149.9003, 61.2181) # Anchorage
        group.geometry = group.geometry.scale(xfact=ak_scale_x, yfact=ak_scale_y, origin=ak_origin)
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
    :param gdf: the geo data frame to relocate.
    :return: a geo data frame with any geometry in AK or HI moved for plotting.
    """
    gdf = gdf.groupby(gdf['STATEFP']).apply(_relocate_ak_hi_group)

    return gdf


def plot_us(gdf: gpd.GeoDataFrame, *args, **kwargs):
    """
    Plot a map of the US by relocating any geometries in the
    GeoDataFrame where the STATEFP column is for AK or HI.
    :param gdf:
    :param args: args for plot
    :param kwargs: kwargs for plot
    :return: ax of the plot
    """
    gdf_relocated = relocate_ak_hi(gdf)
    ax = gdf_relocated.plot(*args, **kwargs)
    return ax


def plot_us_boundary(gdf: gpd.GeoDataFrame, *args, **kwargs):
    """
    Plot a map of the US by relocating any geometries in the
    GeoDataFrame where the STATEFP column is for AK or HI.
    Plot only the boundary of the geometry passed in.
    :param gdf:
    :param args: args for plot
    :param kwargs: kwargs for plot
    :return: ax of the plot
    """
    gdf_relocated = relocate_ak_hi(gdf)
    ax = gdf_relocated.boundary.plot(*args, **kwargs)
    return ax

