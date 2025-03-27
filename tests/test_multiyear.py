"""Tests for `censusdis.multiyear`."""

import unittest

import pandas as pd
import numpy as np

from censusdis.multiyear import (
    download_multiyear,
    pct_change_multiyear,
    graph_multiyear,
)
from censusdis.states import NY
from censusdis.counties.new_york import NASSAU
from censusdis.datasets import ACS1, ACS5

import pytest


class TestDownloadMultiyear:
    """Tests for the function download_multiyear."""

    def test_group_default(self, group_default):
        """Test `group` parameter."""
        df = download_multiyear(
            dataset=ACS5,
            vintages=[2009, 2023],
            group="B05012",
            state=NY,
            school_district_unified="12510",
        )

        pd.testing.assert_frame_equal(df, group_default)

    def test_group_rename(self, group_rename):
        """Test setting rename_vars=False."""
        df = download_multiyear(
            dataset=ACS5,
            vintages=[2009, 2023],
            group="B05012",
            state=NY,
            school_district_unified="12510",
            rename_vars=False,
        )

        pd.testing.assert_frame_equal(df, group_rename)

    def test_group_drop(self, group_drop):
        """Test setting drop_cols=False."""
        df = download_multiyear(
            dataset=ACS5,
            vintages=[2009, 2023],
            group="B05012",
            state=NY,
            school_district_unified="12510",
            drop_cols=False,
        )

        pd.testing.assert_frame_equal(df, group_drop)

    def test_download_variables(self, download_variables):
        """Test `download_variables` parameter."""
        df = download_multiyear(
            dataset=ACS1,
            vintages=[2005, 2006],
            download_variables="B05006_036E",
            state=NY,
            county=NASSAU,
        )

        pd.testing.assert_frame_equal(df, download_variables)


def test_pct_change_multiyear(group_default, pct_change):
    """Test pct_change_multiyear function."""
    pd.testing.assert_frame_equal(pct_change_multiyear(group_default), pct_change)


def TestGraphMultiyear(group_default):
    """Test graph_multiyear function executes and returns None."""
    assert graph_multiyear(group_default) is None


@pytest.fixture
def group_default():
    """Correct output for running the following code.

    download_multiyear(
        dataset=ACS5,
        vintages=[2009, 2023],
        group="B05012",
        state=NY,
        school_district_unified="12510",
    )
    """
    return pd.DataFrame(
        {
            "Total": {0: 44953, 1: 47891},
            "Native": {0: 31623, 1: 32414},
            "Foreign-born": {0: 13330, 1: 15477},
            "Year": {0: 2009, 1: 2023},
        }
    )


@pytest.fixture
def group_rename():
    """Correct output for running the following code.

    download_multiyear(
        dataset=ACS5,
        vintages=[2009, 2023],
        group="B05012",
        state=NY,
        school_district_unified="12510",
        rename_vars=False
    )
    """
    return pd.DataFrame(
        {
            "B05012_001E": {0: 44953, 1: 47891},
            "B05012_002E": {0: 31623, 1: 32414},
            "B05012_003E": {0: 13330, 1: 15477},
            "Year": {0: 2009, 1: 2023},
        }
    )


@pytest.fixture
def group_drop():
    """Correct output for running the following code.

    download_multiyear(
        dataset=ACS5,
        vintages=[2009, 2023],
        group="B05012",
        state=NY,
        school_district_unified="12510",
        drop_cols=False
    )
    """
    return pd.DataFrame(
        {
            "STATE": {0: "36", 1: "36"},
            "SCHOOL_DISTRICT_UNIFIED": {0: "12510", 1: "12510"},
            "Total": {0: 44953, 1: 47891},
            "Native": {0: 31623, 1: 32414},
            "Foreign-born": {0: 13330, 1: 15477},
            "GEO_ID": {0: "9700000US3612510", 1: "9700000US3612510"},
            "NAME": {
                0: "Great Neck Union Free School District, New York",
                1: "Great Neck Union Free School District, New York",
            },
            "Year": {0: 2009, 1: 2023},
        }
    )


@pytest.fixture
def download_variables():
    """Correct output for running the following code.

    download_multiyear(
        dataset=ACS1,
        vintages=[2005, 2006],
        download_variables="B05006_036E",
        state=NY,
        county=NASSAU,
    )
    """
    return pd.DataFrame({"China": {0: 11069, 1: 10495}, "Year": {0: 2005, 1: 2006}})


@pytest.fixture
def pct_change():
    """Correct output for running pct_change_multiyear on group_default."""
    return pd.DataFrame(
        {
            "Total": {0: np.nan, 1: 6.5},
            "Native": {0: np.nan, 1: 2.5},
            "Foreign-born": {0: np.nan, 1: 16.1},
            "Year": {0: 2009, 1: 2023},
        }
    )


if __name__ == "__main__":
    unittest.main()
