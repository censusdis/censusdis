# Copyright (c) 2022 Darren Erik Vengroff

"""
This module contains abbreviated names for commonly used data sets.

These are typically used as the first argument to :py:func:`censudis.data.download`.

There are a lot more data sets available than there are symbolic names here.
But you can always use raw strings. For example, even for `ACS5` you can use
`"acs/acs5"` instead.
"""

# Many more can be added here. We should do a pass of all the demo
# notebooks and put in names for all the data sets we us.

ACS5 = "acs/acs5"

DECENNIAL_PUBLIC_LAW_94_171 = "dec/pl"


DATASET_REFERENCE_URLS = {
    ACS5: "https://www.census.gov/data/developers/data-sets/acs-5year.html",
    DECENNIAL_PUBLIC_LAW_94_171: "https://www.census.gov/programs-surveys/decennial-census/data/datasets.html",
}
"""A set of useful documentation links for data sets."""
