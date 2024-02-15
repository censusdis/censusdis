# Copyright (c) 2022-2023 Darren Erik Vengroff
"""
Tools for downloading and analyzing U.S. Census data.

Includes plotting maps and computing diversity and integration metrics.

Both Python and CLI interfaces are available.
"""
from .impl.exceptions import CensusApiException
from usingversion import getattr_with_version

__all__ = ("CensusApiException",)

# Generate a version number.
__getattr__ = getattr_with_version("impactchart", __file__, __name__)
