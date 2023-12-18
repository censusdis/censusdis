# Copyright (c) 2023 Darren Erik Vengroff
"""These are integration tests that test the code behind with_geometry=True."""
import tempfile
import unittest
from pathlib import Path

from typing import Dict, Iterable, Optional, List

import geopandas
import geopandas as gpd
import pandas as pd

import censusdis.counties.new_jersey
import censusdis.counties.puerto_rico
import censusdis.data
import censusdis.impl
from censusdis import data as ced, states, maps as cem
from censusdis.datasets import DECENNIAL_PUBLIC_LAW_94_171, ACS5
from censusdis.states import NJ


class _GeometryTypeRecorder:
    def __init__(self):
        self._recorded: Dict[int, float] = {}

    def record(self, year: int, gdf: gpd.GeoDataFrame):
        geo_rows = len(gdf[~gdf["geometry"].isnull()].index)
        rows = len(gdf.index)

        self._recorded[year] = geo_rows / rows

    def full(self) -> List[int]:
        return [year for year, fill in self._recorded.items() if fill == 1.0]

    def empty(self) -> List[int]:
        return [year for year, fill in self._recorded.items() if fill == 0.0]

    def partial(self) -> List[int]:
        return [year for year, fill in self._recorded.items() if 0.0 < fill < 1.0]

    def geo_fraction(self, year: int) -> float:
        return self._recorded[year]

    def __repr__(self):
        """
        Construct a representation.

        Helpful for debugging.
        """
        return ", ".join(
            [
                f"[{','.join([str(y) for y in self.full()])}]",
                f"[{','.join([str(y) for y in self.empty()])}]",
                f"[{','.join([str(y) for y in self.partial()])}]",
            ]
        )


class DownloadWithGeometryTestCase(unittest.TestCase):
    """
    Test downloading with geometry at many different geo levels.

    This is similar to `DownloadTestCase` but adds geometry to
    make sure the mappings to shapefiles and merges happen correctly.

    Most of the tests loop over several years in order to catch any
    year-dependent effects in `_GEO_QUERY_FROM_DATA_QUERY_INNER_GEO`.
    But we don't do every year for every test to avoid things getting
    too slow.

    If there is a case we don't cover that breaks, the right thing to
    do is add the year and details to the corresponding test here so
    that we track the fix going forward.
    """

    PATH_PREFIX = "test_integration_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        censusdis.impl.us_census_shapefiles.set_shapefile_path(
            Path(tempfile.mkdtemp(prefix=cls.PATH_PREFIX))
        )

    def setUp(self) -> None:
        """Set up before each test."""
        self._name = "B19001_001E"
        self.recorder = _GeometryTypeRecorder()

    def assert_recorded(
        self,
        full: Iterable[int],
        empty: Optional[Iterable[int]] = None,
        partial: Optional[Iterable[int]] = None,
    ):
        """Assert that we recorded full, empty, and partial years."""
        if empty is None:
            empty = set()
        if partial is None:
            partial = set()

        equal = (
            (set(full) == set(self.recorder.full()))
            and (set(empty) == set(self.recorder.empty()))
            and (set(partial) == set(self.recorder.partial()))
        )

        if not equal:
            msg = (
                ",".join([repr(list(full)), repr(list(empty)), repr(list(partial))])
                + " != "
                + repr(self.recorder)
            )
            raise self.failureException(msg)

    def test_path(self):
        """Are we using the right cache path for shapefiles."""
        path = censusdis.impl.us_census_shapefiles.get_shapefile_path()

        filename = path.name
        self.assertTrue(filename.startswith(self.PATH_PREFIX))

    def test_download_with_geometry_region(self):
        """Download at the region level with geometry."""
        for year in 2013, 2014, 2020, 2022:
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                region="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((4, 4), gdf.shape)

            self.assertEqual(
                ["REGION", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
            )

        self.assert_recorded([2013, 2014, 2020, 2022])

    def test_download_with_geometry_division(self):
        """Download at the region level with geometry."""
        for year in 2013, 2014, 2020, 2022:
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                division="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((9, 4), gdf.shape)

            self.assertEqual(
                ["DIVISION", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
            )

            self.assertTrue((~gdf["geometry"].isnull()).any())

        self.assert_recorded([2013, 2014, 2020, 2022])

    def test_download_with_geometry_zcta(self):
        """Download at the zip code tabulation area level with geometry."""
        for year, num_zcta in (2020, 33_120), (2022, 33_774):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                zip_code_tabulation_area="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((num_zcta, 4), gdf.shape)

            self.assertEqual(
                ["ZIP_CODE_TABULATION_AREA", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

        self.assert_recorded([2022], [], [2020])

    def test_download_with_geometry_state(self):
        """Download at the state level with geometry."""
        for year in range(2009, 2023):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((52, 4), gdf.shape)

            self.assertEqual(
                ["STATE", "NAME", "B19001_001E", "geometry"], list(gdf.columns)
            )

        self.assert_recorded(range(2010, 2023), [2009])

    def test_download_with_geometry_state_zcta(self):
        """
        Download at the state and zip code tabulation area level with geometry.

        Before 2020, the data model nested zcta inside of state.
        """
        for year, num_zcta in (2011, 595), (2019, 595):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=NJ,
                zip_code_tabulation_area="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((num_zcta, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "ZIP_CODE_TABULATION_AREA",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

        self.assert_recorded([2019], [2011])

    def test_download_with_geometry_multi_state(self):
        """
        Download at the tract level for multiple states with geometry.

        The point of this test is that tract-level shapefiles exist
        only on a per-state basis, so inside the call we have to
        recognize this and download and concatenate several shapefiles
        before merging with our data.
        """
        for year, num_tracts in (2010, 1348), (2020, 1614):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=["01", "02"],  # Two specific states.
                tract="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((num_tracts, 6), gdf.shape)

            self.assertEqual(
                ["STATE", "COUNTY", "TRACT", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

            self.assertGreater(self.recorder.geo_fraction(year), 0.999)

        self.assert_recorded([], [], [2010, 2020])

    def test_download_with_geometry_county(self):
        """Download at the county level with geometry."""
        for year in range(2009, 2023):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((21, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "COUNTY", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

        # Note that the pre-2010 TIGER landscape is still a little
        # of a mess. We should be able to fix this by getting the
        # tiger code for 2009 to find
        # https://www2.census.gov/geo/tiger/TIGER2009/tl_2009_us_county.zip
        self.assert_recorded(range(2010, 2023), [2009])

    def test_download_with_geometry_county_subdivision(self):
        """Download at the county subdivision level with geometry."""
        for year in 2009, 2010, 2011, 2015, 2019, 2020, 2022:
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county=censusdis.counties.new_jersey.HUDSON,
                county_subdivision="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((12, 6), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "COUNTY",
                    "COUNTY_SUBDIVISION",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

        self.assert_recorded([2010, 2011, 2015, 2019, 2020, 2022], [2009])

    def test_download_with_geometry_tract(self):
        """Download at the tract level with geometry."""
        for year, num_tracts in (
            (2009, 64),
            (2010, 70),
            (2015, 70),
            (2020, 74),
            (2022, 74),
        ):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county="001",
                tract="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((num_tracts, 6), gdf.shape)

            self.assertEqual(
                ["STATE", "COUNTY", "TRACT", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

            self.assertGreater(self.recorder.geo_fraction(year), 0.98)

        self.assert_recorded([2009], [], [2010, 2015, 2020, 2022])

    def test_download_with_geometry_block_group(self):
        """Download at the county level with geometry."""
        # No block group maps before 2013.
        for year, num_bg in (2013, 184), (2020, 194), (2022, 194):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                county="001",
                block_group="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.recorder.record(year, gdf)

            self.assertEqual((num_bg, 7), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "COUNTY",
                    "TRACT",
                    "BLOCK_GROUP",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

            self.assertGreater(self.recorder.geo_fraction(year), 0.99)

        self.assert_recorded([], [], [2013, 2020, 2022])

    def test_download_with_geometry_place(self):
        """Download at the PLACE level with geometry."""
        for year, num_place in (2010, 545), (2015, 545), (2020, 701), (2022, 700):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                place="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_place, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "PLACE", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_consolidated_city(self):
        """Download at the consolidated city level with geometry."""
        for year in range(2010, 2023, 2):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.IN,
                consolidated_city="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((1, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "CONSOLIDATED_CITY", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_congressional_district(self):
        """Download at the congressional district level with geometry."""
        for year, num_districts in (
            (2009, 13),
            (2010, 13),
            (2011, 13),
            (2012, 12),
            (2020, 12),
            (2022, 12),
        ):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                congressional_district="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_districts, 5), gdf.shape)

            self.assertEqual(
                ["STATE", "CONGRESSIONAL_DISTRICT", "NAME", "B19001_001E", "geometry"],
                list(gdf.columns),
            )

    def test_download_with_geometry_state_legislative_district_upper(self):
        """Download at the slate legislative district upper chamber level with geometry."""
        for year, num_districts in (2009, 62), (2010, 62), (2020, 63), (2022, 63):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NY,
                state_legislative_district_upper_chamber="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_districts, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "STATE_LEGISLATIVE_DISTRICT_UPPER_CHAMBER",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_state_legislative_district_lower(self):
        """Download at the slate legislative district lower chamber level with geometry."""
        for year in 2009, 2010, 2020, 2022:
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NY,
                state_legislative_district_lower_chamber="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((150, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "STATE_LEGISLATIVE_DISTRICT_LOWER_CHAMBER",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_voting_district(self):
        """Download at the voting district level with geometry."""
        gdf = ced.download(
            DECENNIAL_PUBLIC_LAW_94_171,
            2020,
            ["NAME", "P1_001N"],
            with_geometry=True,
            state=states.NJ,
            county=censusdis.counties.new_jersey.HUDSON,
            voting_district="*",
        )

        self.assertIsInstance(gdf, geopandas.GeoDataFrame)

        self.assertEqual((452, 6), gdf.shape)

        self.assertEqual(
            [
                "STATE",
                "COUNTY",
                "VOTING_DISTRICT",
                "NAME",
                "P1_001N",
                "geometry",
            ],
            list(gdf.columns),
        )

    def test_download_with_geometry_school_district_unified(self):
        """Download at the school district unified level with geometry."""
        for year, num_districts in (2010, 234), (2015, 340), (2020, 343):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                school_district_unified="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_districts, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "SCHOOL_DISTRICT_UNIFIED",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_school_district_elementary(self):
        """Download at the school district elementary level with geometry."""
        for year, num_districts in (2010, 283), (2015, 175), (2020, 172):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                school_district_elementary="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_districts, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "SCHOOL_DISTRICT_ELEMENTARY",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_school_district_secondary(self):
        """Download at the school district secondary level with geometry."""
        for year, num_districts in (2009, 48), (2010, 48), (2015, 48), (2020, 47):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                school_district_secondary="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_districts, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "SCHOOL_DISTRICT_SECONDARY",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_aiannh_homeland(self):
        """Download at the aiannh homeland level with geometry."""
        for year, num_areas in (2009, 656), (2010, 813), (2015, 693), (2020, 704):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                american_indian_area_alaska_native_area_hawaiian_home_land="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_areas, 4), gdf.shape)

            self.assertEqual(
                [
                    "AMERICAN_INDIAN_AREA_ALASKA_NATIVE_AREA_HAWAIIAN_HOME_LAND",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_anrc(self):
        """Download at the alaskan native regional_corporation level with geometry."""
        for year in 2009, 2010, 2011, 2016, 2020, 2021:
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.AK,
                alaska_native_regional_corporation="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((12, 5), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "ALASKA_NATIVE_REGIONAL_CORPORATION",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_necta(self):
        """Download at the necta level with geometry."""
        for year, num_necta in (
            (2009, 43),
            (2010, 43),
            (2015, 38),
            (2020, 40),
            (2021, 40),
        ):
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                new_england_city_and_town_area="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((num_necta, 4), gdf.shape)

            self.assertEqual(
                [
                    "NEW_ENGLAND_CITY_AND_TOWN_AREA",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_subbario(self):
        """Download at the subbarrio level with geometry."""
        for year in 2013, 2020, 2021:
            gdf = ced.download(
                ACS5,
                year,
                ["NAME", self._name],
                with_geometry=True,
                state=states.PR,
                county=censusdis.counties.puerto_rico.SAN_JUAN,
                county_subdivision=["34070", "74017"],
                subminor_civil_division="*",
            )

            self.assertIsInstance(gdf, geopandas.GeoDataFrame)

            self.assertEqual((4, 7), gdf.shape)

            self.assertEqual(
                [
                    "STATE",
                    "COUNTY",
                    "COUNTY_SUBDIVISION",
                    "SUBMINOR_CIVIL_DIVISION",
                    "NAME",
                    "B19001_001E",
                    "geometry",
                ],
                list(gdf.columns),
            )

    def test_download_with_geometry_not_available(self):
        """Download at a geography level that has no geometry available."""
        with self.assertRaises(
            censusdis.impl.exceptions.CensusApiException
        ) as assertion:
            ced.download(
                ACS5,
                2020,
                ["NAME", self._name],
                with_geometry=True,
                state=states.NJ,
                combined_statistical_area_or_part="*",
            )

        self.assertTrue(
            str(assertion.exception).startswith(
                "The with_geometry=True flag is only allowed if"
            )
        )

        # But it is OK without geometry.

        df = ced.download(
            ACS5,
            2020,
            ["NAME", self._name],
            with_geometry=False,
            state=states.NJ,
            combined_statistical_area_or_part="*",
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertNotIsInstance(df, gpd.GeoDataFrame)

        self.assertEqual((2, 4), df.shape)


class ShapefileTestCase(unittest.TestCase):
    """Test shapefile functionality."""

    PATH_PREFIX = "test_integration_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        cls.shapefile_path = tempfile.mkdtemp(prefix=cls.PATH_PREFIX)

    def setUp(self) -> None:
        """Set up before each test."""
        self._year = 2019
        self.reader = cem.ShapeReader(self.shapefile_path, self._year)

    def test_county_shapefile(self):
        """Test reading a county level shapefile for the whole country."""
        gdf_counties = self.reader.read_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3233, 18), gdf_counties.shape)

    def test_county_cb_shapefile(self):
        """Test reading a county level cb shapefile for the whole country."""
        gdf_counties = self.reader.read_cb_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3233, 10), gdf_counties.shape)

    def test_puma_shapefile(self):
        """Test reading a puma level shapefile for the whole country."""
        gdf_puma = self.reader.read_cb_shapefile("us", "puma")

        self.assertIsInstance(gdf_puma, gpd.GeoDataFrame)

        self.assertEqual((2380, 9), gdf_puma.shape)

    def test_2010_shapefile(self):
        """Test special behavior in 2010."""
        # Override the normal setup for 2010.
        self._year = 2010
        self.reader = cem.ShapeReader(self.shapefile_path, self._year)

        gdf_counties = self.reader.read_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3221, 18), gdf_counties.shape)

    def test_2010_cb_shapefile(self):
        """Test special behavior in 2010."""
        # Override the normal setup for 2010.
        self._year = 2010
        self.reader = cem.ShapeReader(self.shapefile_path, self._year)

        gdf_counties = self.reader.read_cb_shapefile("us", "county")

        self.assertIsInstance(gdf_counties, gpd.GeoDataFrame)

        self.assertEqual((3221, 7), gdf_counties.shape)


class AddInferredGeographyTestCase(unittest.TestCase):
    """Test our ability to add inferred geometry."""

    PATH_PREFIX = "test_integration_shapefiles_"

    @classmethod
    def setUpClass(cls) -> None:
        """Set up our shapefile path once at class load time."""
        cls.shapefile_path = tempfile.mkdtemp(prefix=cls.PATH_PREFIX)

    def setUp(self) -> None:
        """Set up before each test."""
        self._year0 = 2020
        self.reader0 = cem.ShapeReader(self.shapefile_path, self._year0)

    def test_state(self):
        """Test that we can infer state geometries."""
        df_state = pd.DataFrame(
            [[states.NJ, 0.5, 0.6], [states.CA, 0.1, 0.2]],
            columns=["STATE", "metric1", "metric2"],
        )

        gdf_inferred = censusdis.data.add_inferred_geography(df_state, self._year0)

        self._assert_data_unchanged_in_inference(df_state, gdf_inferred)

        # Now get the state shapefile directly and see if we
        # inferred the right geometries.

        gdf_state = self.reader0.read_cb_shapefile("us", "state")

        for state in df_state["STATE"]:
            self.assertTrue(
                gdf_state[gdf_state.STATEFP == state].geometry.iloc[0],
                gdf_inferred[gdf_inferred.STATE == state].geometry.iloc[0],
            )

    def test_county(self):
        """Test that we can infer a county geometries."""
        df_county = pd.DataFrame(
            [[states.NJ, "011", 0.5, 0.6], [states.NJ, "013", 0.1, 0.2]],
            columns=["STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred = censusdis.data.add_inferred_geography(df_county, self._year0)

        self._assert_data_unchanged_in_inference(df_county, gdf_inferred)

        # Now get the county shapefile directly and see if we
        # inferred the right geometries.

        gdf_county = self.reader0.read_cb_shapefile("us", "county")

        for row in df_county[["STATE", "COUNTY"]].itertuples():
            state, county = row.STATE, row.COUNTY
            self.assertEqual(
                gdf_county[
                    (gdf_county.STATEFP == state) & (gdf_county.COUNTYFP == county)
                ].geometry.iloc[0],
                gdf_inferred[
                    (gdf_inferred.STATE == state) & (gdf_inferred.COUNTY == county)
                ].geometry.iloc[0],
            )

    def test_tract(self):
        """Test that we can infer census tract geometries."""
        df_tract = pd.DataFrame(
            [
                [states.NJ, "013", "019000", 0.1, 0.2],
                [states.NJ, "013", "019100", 0.3, 0.4],
                [states.NJ, "013", "019200", 0.5, 0.6],
                [states.NY, "061", "021600", 1.0, 1.1],
                [states.NY, "061", "021800", 1.2, 1.3],
            ],
            columns=["STATE", "COUNTY", "TRACT", "metric1", "metric2"],
        )

        gdf_inferred = censusdis.data.add_inferred_geography(df_tract, self._year0)

        self._assert_data_unchanged_in_inference(df_tract, gdf_inferred)

        # Now get the county shapefiles directly and see if we
        # inferred the right geometries.

        gdf_tract_nj = self.reader0.read_cb_shapefile(states.NJ, "tract")
        gdf_tract_ny = self.reader0.read_cb_shapefile(states.NY, "tract")

        gdf_tract = gpd.GeoDataFrame(pd.concat([gdf_tract_nj, gdf_tract_ny]))

        for row in df_tract[["STATE", "COUNTY", "TRACT"]].itertuples():
            state, county, tract = row.STATE, row.COUNTY, row.TRACT
            self.assertEqual(
                gdf_tract[
                    (gdf_tract.STATEFP == state)
                    & (gdf_tract.COUNTYFP == county)
                    & (gdf_tract.TRACTCE == tract)
                ].geometry.iloc[0],
                gdf_inferred[
                    (gdf_inferred.STATE == state)
                    & (gdf_inferred.COUNTY == county)
                    & (gdf_inferred.TRACT == tract)
                ].geometry.iloc[0],
            )

    def _assert_data_unchanged_in_inference(self, df, gdf_inferred):
        """
        Assert that when we added a geometry column nothing else changed.

        Parameters
        ----------
        df
            The original df.
        gdf_inferred
            The gdf with inferred geometry.
        """
        # We should have the name number of rows and one new column
        # for geometry.
        old_shape = df.shape
        new_shape = gdf_inferred.shape

        self.assertEqual(old_shape[0], new_shape[0])
        self.assertEqual(old_shape[1] + 1, new_shape[1])

        self.assertTrue(all(col in gdf_inferred.columns for col in df.columns))
        self.assertIn("geometry", gdf_inferred.columns)

        # Make sure all the data we had stayed where it was.
        self.assertTrue((gdf_inferred[df.columns] == df).all().all())

    def test_multi_year(self):
        """Test inferring geometry in a multi-year df."""
        df_county_multi_year = pd.DataFrame(
            [
                [2019, states.NJ, "011", 0.5, 0.6],
                [2019, states.NJ, "013", 0.1, 0.2],
                [2020, states.NJ, "011", 1.5, 1.6],
                [2020, states.NJ, "013", 1.1, 1.2],
                [2021, states.NJ, "011", 2.5, 2.6],
                [2021, states.NJ, "013", 2.5, 2.5],
            ],
            columns=["YEAR", "STATE", "COUNTY", "metric1", "metric2"],
        )

        df_county_by_year = {
            year: df_for_year
            for year, df_for_year in df_county_multi_year.groupby("YEAR")
        }

        gdf_inferred_geometry_multi_year = censusdis.data.add_inferred_geography(
            df_county_multi_year
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_multi_year
        )

        gdf_inferred_geometry_by_year = {
            year: censusdis.data.add_inferred_geography(df_for_year)
            for year, df_for_year in df_county_by_year.items()
        }

        gdf_inferred_geometry_by_year_all = gpd.GeoDataFrame(
            pd.concat(gdf_inferred_geometry_by_year.values()).reset_index(drop=True)
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_by_year_all
        )

        self.assertTrue(
            gdf_inferred_geometry_multi_year.equals(gdf_inferred_geometry_by_year_all)
        )

    def test_multi_year_missing_map_year(self):
        """Test inferring geometry when there are no maps for one year."""
        df_county_multi_year = pd.DataFrame(
            [
                # There are no maps for 1999.
                [1999, states.NJ, "011", 0.4, 0.5],
                [1999, states.NJ, "013", 0.0, 0.1],
                [2019, states.NJ, "011", 0.5, 0.6],
                [2019, states.NJ, "013", 0.1, 0.2],
                [2020, states.NJ, "011", 1.5, 1.6],
                [2020, states.NJ, "013", 1.1, 1.2],
                [2021, states.NJ, "011", 2.5, 2.6],
                [2021, states.NJ, "013", 2.5, 2.5],
            ],
            columns=["YEAR", "STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred_geometry_multi_year = censusdis.data.add_inferred_geography(
            df_county_multi_year
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_multi_year
        )

        # Make sure there is no geometry for 1999, but there is geometry
        # for other years.
        self.assertTrue(
            gdf_inferred_geometry_multi_year[
                gdf_inferred_geometry_multi_year["YEAR"] == 1999
            ]["geometry"]
            .isnull()
            .all()
        )

        self.assertFalse(
            gdf_inferred_geometry_multi_year[
                gdf_inferred_geometry_multi_year["YEAR"] != 1999
            ]["geometry"]
            .isnull()
            .any()
        )

    def test_multi_year_no_maps(self):
        """Test inferring geometry when there are no maps for any year."""
        df_county_multi_year = pd.DataFrame(
            [
                # There are no maps for these years.
                [1999, states.NJ, "011", 0.4, 0.5],
                [1999, states.NJ, "013", 0.0, 0.1],
                [1998, states.NJ, "011", 0.5, 0.6],
                [1998, states.NJ, "013", 0.1, 0.2],
            ],
            columns=["YEAR", "STATE", "COUNTY", "metric1", "metric2"],
        )

        gdf_inferred_geometry_multi_year = censusdis.data.add_inferred_geography(
            df_county_multi_year
        )

        self._assert_data_unchanged_in_inference(
            df_county_multi_year, gdf_inferred_geometry_multi_year
        )

        # Make sure there is no geometry.
        self.assertTrue(gdf_inferred_geometry_multi_year["geometry"].isnull().all())


class RemoveWaterTestCase(unittest.TestCase):
    """Test removing water."""

    def test_remove_water_nyc(self):
        """Test census tracts in NYC."""
        nyc_counties = [
            "061",
            "081",
        ]  # "005", "047", "085"]

        # We use EPSG 3857 since we will be computing areas.

        gdf_tracts = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NY,
            county=nyc_counties,
            tract="*",
            with_geometry=True,
            remove_water=False,
        ).to_crs(epsg=3857)

        gdf_tracts_no_water = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NY,
            county=nyc_counties,
            tract="*",
            with_geometry=True,
            remove_water=True,
        ).to_crs(epsg=3857)

        # We should not lose any tracts.
        self.assertEqual(gdf_tracts.shape, gdf_tracts_no_water.shape)

        # The names should be the same.
        self.assertTrue(gdf_tracts.NAME.equals(gdf_tracts_no_water.NAME))

        # Some of the areas of the tracts without water should be smaller than or
        # equal to those of the original.
        self.assertTrue(
            (gdf_tracts_no_water.geometry.area < gdf_tracts.geometry.area).any()
        )

        # But there are some rare cases when they get distorted to be a little bigger.
        # Lat's make sure it's not a lot bigger.
        self.assertFalse(
            (gdf_tracts_no_water.geometry.area / gdf_tracts.geometry.area >= 1.01).any()
        )

    def test_remove_water_nj(self):
        """Test in which we don't have explicit counties to fetch water and join on."""
        df_nj = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NJ,
            with_geometry=True,
            remove_water=False,
        ).to_crs(epsg=3857)

        df_nj_remove_water = ced.download(
            ACS5,
            2020,
            "NAME",
            state=states.NJ,
            with_geometry=True,
            remove_water=True,
        ).to_crs(epsg=3857)

        # All we have is the state boundary.
        self.assertEqual(1, len(df_nj.index))
        self.assertEqual(1, len(df_nj_remove_water.index))

        # Geometry should be a little different.
        self.assertNotEqual(
            df_nj["geometry"].iloc[0], df_nj_remove_water["geometry"].iloc[0]
        )


if __name__ == "__main__":
    unittest.main()
